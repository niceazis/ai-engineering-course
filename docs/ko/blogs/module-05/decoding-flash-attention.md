# Flash Attention이란 무엇이며 왜 빠른가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/decoding-flash-attention  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-04-11 공개 원문을 직접 확인해 N×N 수치, HBM/SRAM 차이, tiling, online softmax, backward recomputation, FlashAttention 2/3 설명을 보존하면서 독립적으로 다시 쓴 한국어 해설입니다.

## 1. 가장 중요한 한 문장

FlashAttention은 attention의 수학을 바꾸지 않습니다.

    Attention(Q,K,V)
      = softmax(QK^T / sqrt(d_k)) V

결과를 근사하거나 sparse하게 만드는 것이 아니라 **같은 결과를 GPU에서 더 적은 memory traffic으로 계산하는 IO-aware algorithm**입니다.

## 2. Standard Attention의 병목

sequence length가 N이면 score matrix:

    S = QK^T

의 shape은:

    N × N

입니다.

원문의 수치:

- 4,000 tokens → 16 million entries
- 10,000 tokens → 100 million entries
- 100,000 tokens → 10 billion entries

N을 2배로 늘리면 matrix element는 4배가 됩니다.

## 3. Standard Attention의 Memory Traffic

원문의 단순화한 흐름:

1. S = QK^T 계산
2. S를 HBM에 write
3. S를 다시 read해 softmax
4. P = softmax(S)를 HBM에 write
5. P를 다시 read해 V와 곱함
6. 최종 O를 write

큰 N×N matrix가 여러 번 HBM과 compute unit 사이를 오갑니다.

핵심 병목은 단순 FLOPs보다 **memory movement**일 수 있습니다.

## 4. HBM vs SRAM

원문의 직관:

### HBM

- GPU의 큰 memory
- tens of GB 수준 용량
- SRAM보다 상대적으로 느림

### SRAM

- GPU chip 내부의 매우 빠른 on-chip memory
- 용량은 훨씬 작음
- 원문은 HBM read보다 대략 10~20배 빠른 접근이라는 교육용 설명을 사용

비유:

- HBM = 다른 층의 큰 도서관
- SRAM = 바로 앞 작은 책상

FlashAttention의 핵심은 책상 크기에 맞춰 일하고 도서관 왕복을 줄이는 것입니다.

## 5. 핵심 아이디어: N×N Matrix를 HBM에 만들지 않는다

원문의 질문:

> 왜 거대한 attention matrix를 HBM에 저장해야 하는가?

FlashAttention은 Q/K/V를 작은 block으로 나눠 SRAM 안에서 partial attention을 계산하고, full score/probability matrix를 HBM에 materialize하지 않습니다.

## 6. Tiling

원문 예는 256-token block을 사용합니다.

    Q → [Q1][Q2][Q3]...
    K → [K1][K2][K3]...
    V → [V1][V2][V3]...

각 Q block에 대해:

1. Q block을 SRAM으로 load
2. K/V block을 하나씩 SRAM으로 load
3. partial score 계산
4. partial softmax state 갱신
5. running output 갱신
6. 최종 output block만 HBM에 write

## 7. Softmax 문제

Softmax는 row 전체를 알아야 하는 것처럼 보입니다.

예:

    scores = [2, 4, 6]

stable softmax는 max=6을 사용해:

    exp(2-6), exp(4-6), exp(6-6)
    = exp(-4), exp(-2), exp(0)

를 계산합니다.

그런데 tiling에서는 row 전체가 한 번에 SRAM에 있지 않습니다.

해결이 Online Softmax입니다.

## 8. Online Softmax

유지하는 state:

- running max
- running sum
- running weighted output

새 block의 max가 더 크면 과거 state를 새 max 기준으로 rescale합니다.

## 9. 원문의 [2,4,6] 수치 예

첫 block:

    [2,4]

running max:

    m_old = 4

running sum:

    exp(2-4) + exp(4-4)
    = exp(-2) + 1
    ≈ 0.135 + 1
    = 1.135

다음 block:

    [6]

새 max:

    m_new = 6

과거 sum을 rescale:

    1.135 × exp(4-6)
    ≈ 1.135 × 0.135
    ≈ 0.153

새 항:

    exp(6-6) = 1

최종:

    0.153 + 1 = 1.153

전체 row를 한 번에 계산한 값:

    exp(-4)+exp(-2)+1
    ≈ 0.018+0.135+1
    = 1.153

동일합니다.

## 10. End-to-End 흐름

    for each Q block:
        init running max/sum/output
        for each K,V block:
            compute partial QK^T
            update max
            rescale old state
            add current V contribution
        write final output block

Full N×N matrix는 HBM에 저장되지 않습니다.

## 11. 4,000-token Data Movement 예

Standard attention:

    N = 4,000
    N^2 = 16M

원문은 S/P matrix의 큰 이동만 단순 계산해:

- write S: 16M
- read S: 16M
- write P: 16M
- read P: 16M

합계 약:

    64M entries

라고 설명합니다.

Q/K/V와 output의 작은 이동은 이 교육용 비교에서 생략합니다.

핵심은 FlashAttention이 N×N intermediate를 HBM에 쓰고 읽는 대규모 traffic을 제거한다는 것입니다.

## 12. Backward에서 Recomputation

Training backward에는 attention score가 다시 필요합니다.

FlashAttention은 forward에서 full matrix를 저장하지 않았으므로 backward 시 SRAM에서 score를 재계산합니다.

Forward에서 저장하는 것은 row별 running max/sum 같은 O(N) 규모 statistics입니다.

Trade-off:

    more recompute
    ↔ much less HBM traffic

현대 GPU는 compute 대비 memory bandwidth가 상대적으로 더 귀한 경우가 많아 이 trade-off가 유리합니다.

## 13. FlashAttention 2

원문은 세 가지 개선을 설명합니다.

### 1) Non-matmul 작업 감소

rescaling 같은 느린 scalar/vector 작업을 inner loop에서 줄이고 tensor core가 잘하는 matmul 비중을 늘립니다.

### 2) Sequence 방향 병렬화

FlashAttention 1은 batch×heads parallelism 중심이었지만 FA2는 Q block을 sequence dimension에서도 병렬화해 작은 batch·긴 sequence에서 GPU utilization을 높입니다.

### 3) Worker 내부 work partition 개선

thread 간 shared-memory read/write를 줄이는 방식으로 work split을 개선합니다.

원문은 FA2가 FA1 대비 대략 2배 빠른 수준이라고 설명합니다. 실제 속도는 GPU와 shape에 따라 달라집니다.

## 14. FlashAttention 3

FA3는 NVIDIA Hopper(H100/H200) 계열 hardware feature를 적극 활용합니다.

원문 핵심:

- Tensor Memory Accelerator(TMA)
- asynchronous copy
- data movement와 tensor-core compute overlap

즉 다음 K/V block을 가져오는 동안 현재 block 계산을 진행해 wait time을 줄입니다.

## 15. FlashAttention이 해결하지 않는 것

FlashAttention은 dense attention pair 자체를 제거하는 sparse algorithm이 아닙니다.

따라서:

- mathematical attention relation은 dense
- compute complexity의 큰 틀은 여전히 attention shape에 영향
- 하지만 memory footprint와 IO가 크게 개선

됩니다.

SWA/sparse attention과는 문제를 푸는 층위가 다릅니다.

## 16. 언제 효과가 큰가

- long sequence
- attention memory가 bottleneck인 training
- prefill-heavy workload
- GPU memory bandwidth가 병목인 경우

Framework에서는 PyTorch SDPA, xFormers, vendor kernels 등이 적절한 kernel을 자동 선택할 수도 있으므로 실제 implementation을 확인합니다.

## 핵심 정리

- FlashAttention은 attention 수학을 바꾸지 않는 exact IO-aware algorithm입니다.
- 거대한 N×N S/P matrix를 HBM에 materialize하지 않습니다.
- Tiling으로 SRAM 안에서 block별 계산합니다.
- Online softmax로 full row 없이도 정확한 softmax를 계산합니다.
- Backward는 저장 대신 recompute를 선택해 memory traffic을 줄입니다.
- FA2는 GPU utilization을 개선하고 FA3는 Hopper의 asynchronous memory movement를 활용합니다.

## 원문

- https://outcomeschool.com/blog/decoding-flash-attention
