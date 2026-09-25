# DeepSeek-V4란 무엇이며 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/decoding-deepseek-v4  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-04-24 공개 Outcome School 원문을 직접 확인해 모델 크기, 1M context, CSA/HCA, 128-token local branch, mHC, Muon, FP4 QAT, training schedule, OPD와 reasoning modes를 보존하면서 독립적으로 다시 쓴 상세 해설입니다.

## 1. 큰 그림

원문이 제시하는 DeepSeek-V4의 목표는 **1M-token ultra-long context의 inference cost를 크게 낮추는 것**입니다.

원문 요약식:

    DeepSeek-V4
      = DeepSeek-V3 계열 기반
      + Hybrid Compressed Attention
      + mHC residual
      + Muon optimizer
      + On-Policy Distillation

1M context에서 원문 비교:

- V4-Pro per-token compute: V3.2의 27%
- V4-Pro KV cache: V3.2의 10%
- V4-Flash compute: V3.2의 10%
- V4-Flash KV cache: V3.2의 7%

## 2. 두 Model

| Model | Total Params | Active Params | Layers | Context | Pretraining |
| --- | ---: | ---: | ---: | ---: | ---: |
| V4-Flash | 284B | 13B | 43 | 1M | 32T |
| V4-Pro | 1.6T | 49B | 61 | 1M | 33T |

둘 다 MoE model입니다.

- Pro: 더 큰 capacity
- Flash: 더 작은 active compute와 serving cost

MoE이므로 total parameter와 token당 active parameter를 구분해야 합니다.

## 3. 1M Context의 문제

Standard attention은 N token에서 대략 N×N pair를 처리합니다.

    N = 1,000,000
    N^2 = 1,000,000,000,000

즉 1조 pair 규모입니다.

KV cache도 context length에 따라 증가합니다.

V4는 full dense attention을 그대로 확장하지 않고 CSA와 HCA를 interleave합니다.

## 4. CSA — Compressed Sparse Attention

CSA는 두 단계입니다.

### Step 1: Compress

원문의 교육용 예는 m=4입니다.

    [t1 t2 t3 t4] → C1
    [t5 t6 t7 t8] → C2

learned softmax weight로 연속 token을 하나의 compressed K/V entry로 합칩니다.

1M token에서 m=4라면 설명상 250K compressed entries가 됩니다.

### Step 2: Select

Lightning Indexer가 현재 query와 compressed entries를 빠르게 score하고 top-k만 선택합니다.

실제 heavy attention은 선택된 entry에만 수행합니다.

즉:

    compressed + sparse

입니다.

## 5. HCA — Heavily Compressed Attention

HCA는 CSA보다 더 강하게 K/V를 압축하지만, 압축된 entry에 대해서는 dense attention을 수행하는 쪽입니다.

핵심 trade-off:

- CSA: 덜 압축 + sparse selection
- HCA: 더 압축 + dense attention

두 종류를 layer 사이에 섞어 local/global 정보와 비용을 균형 잡습니다.

## 6. Sliding Window Branch

압축은 최근 token의 미세한 detail을 흐릴 수 있습니다.

그래서 CSA/HCA 모두 별도의 recent uncompressed branch를 유지합니다.

원문 수치:

    window = 128 tokens

즉 오래된 context는 compressed path로 처리하고 최근 128 token은 full detail로 유지합니다.

## 7. Attention Sink

원문은 CSA/HCA core attention softmax denominator에 **learnable sink logits**를 넣는다고 설명합니다.

효과:

- 모든 probability mass를 실제 context token에 강제로 배분하지 않음
- 아무 token도 중요하지 않을 때 attention을 sink에 보낼 수 있음

또 core attention 직전에 query와 compressed KV에 RMSNorm을 적용해 logit scale을 안정화합니다.

## 8. mHC — Manifold-Constrained Hyper-Connections

일반 residual stream은 한 개입니다.

Hyper-Connections는 residual stream을 여러 parallel stream으로 넓히고 learned A/B/C matrix로 layer마다 혼합합니다.

원문 DeepSeek-V4:

    n_hc = 4

문제는 unconstrained HC가 deep stack에서 signal amplification/collapse를 만들 수 있다는 것입니다.

## 9. Birkhoff Polytope Constraint

mHC는 residual mixing matrix를 doubly stochastic matrix의 공간인 Birkhoff polytope에 제한합니다.

Doubly stochastic:

- 각 row 합 = 1
- 각 column 합 = 1

원문 설명에서는 이 constraint가 spectral norm을 1 수준으로 제한해 residual flow가 폭발하는 것을 막는 핵심으로 제시됩니다.

## 10. Muon Optimizer

대부분 weight에 AdamW 대신 Muon을 사용합니다.

Muon 핵심:

- gradient matrix 전체 구조를 봄
- update 방향을 orthogonalize
- Newton-Schulz iteration 사용
- singular direction 하나가 과도하게 지배하지 않도록 조정

원문에서 AdamW를 계속 쓰는 부분:

- embedding
- prediction head
- RMSNorm
- mHC의 static parts

그 외 대부분은 Muon.

## 11. FP4 Quantization-Aware Training

FP4는 4-bit floating-point format입니다.

QAT는 training 중 low precision effect를 simulation해 model이 precision loss에 적응하도록 합니다.

원문 적용 위치:

1. MoE expert weights
2. CSA Lightning Indexer의 QK path

원문은 FP4(E2M1) scale을 FP8(E4M3) dynamic range로 absorb해 existing FP8 pipeline을 재사용하는 설계를 설명합니다.

Indexer 결과:

- top-k selector 약 2× speedup
- KV entry recall 99.7%

이라고 원문이 제시합니다.

## 12. Pretraining Data

원문:

- 32T+ tokens
- math
- code
- web
- long documents
- scientific papers
- multilingual data

Long-context model이므로 long-document curation을 강조합니다.

## 13. Sequence-Length Curriculum

처음부터 1M sequence로 training하지 않습니다.

원문 schedule:

    4K
      → 16K
      → 64K
      → 1M

Sparse attention도 단계적으로 켭니다.

- 첫 1T tokens: dense warm-up
- 64K 단계부터 sparse attention 도입
- 이후 유지

## 14. Training Instability 완화

### Anticipatory Routing

step t에서 MoE router를 약간 오래된 parameter theta_(t-delta)로 계산하고 backbone은 현재 theta_t를 사용합니다.

목적은 bad routing → outlier → worse routing feedback loop를 끊는 것입니다.

### SwiGLU Clamping

SwiGLU output을 일정 범위로 clamp해 extreme activation이 training을 destabilize하지 않게 합니다.

## 15. Post-Training Stage 1 — Specialist Training

도메인별 specialist를 만듭니다.

예:

- math
- coding
- agent use
- instruction following

각 specialist:

1. high-quality domain SFT
2. GRPO 기반 RL

로 능력을 강화합니다.

## 16. Stage 2 — On-Policy Distillation

여러 specialist를 최종 unified student 하나에 통합합니다.

일반 distillation과 차이:

- teacher가 미리 만든 fixed data만 따라하지 않음
- student가 자기 trajectory/output을 생성
- task에 맞는 specialist teacher가 full vocabulary distribution을 제공
- reverse KL로 student를 teacher distribution 쪽으로 이동

원문은 reverse KL을 mode-seeking 성질로 설명합니다.

Task별 teacher weight도 다르게 둡니다.

## 17. Reasoning Modes

원문 세 mode:

| Mode | 용도 | 동작 |
| --- | --- | --- |
| Non-think | 일상/빠른 답 | 별도 think block 없이 응답 |
| Think High | 복잡한 문제/계획 | 더 긴 reasoning |
| Think Max | 최대 reasoning | 매우 높은 reasoning effort |

핵심은 inference 시 task 난도에 따라 compute를 조절하는 것입니다.

## 18. 전체 Data Flow

원문의 architecture 흐름:

    Input
      → Embedding
      → Transformer blocks
           CSA / HCA
           mHC residual mixing
           DeepSeekMoE FFN
           mHC residual mixing
      → Prediction Head
      → MTP modules
      → Output

MTP(Multi-Token Prediction)는 training data efficiency를 높이고 inference에서는 speculative decoding drafter 역할로도 활용될 수 있습니다.

## 19. 이 아키텍처에서 연결해야 할 개념

- MoE → total vs active parameter
- CSA/HCA → long-context attention cost
- SWA → recent detail 유지
- Attention sink → 불필요한 attention mass 처리
- mHC → deep residual stability
- Muon → optimization geometry
- FP4 QAT → serving bandwidth/compute
- OPD → specialist knowledge consolidation
- MTP → multi-token objective/speculation

## 핵심 정리

- V4-Pro는 1.6T total / 49B active, V4-Flash는 284B / 13B로 원문에 제시됩니다.
- 두 모델 모두 native 1M context를 목표로 합니다.
- CSA는 compress+top-k sparse, HCA는 heavier compression+dense attention입니다.
- 최근 128 token은 별도 sliding-window branch로 uncompressed 유지합니다.
- mHC는 residual mixing을 doubly stochastic constraint로 안정화합니다.
- Muon, FP4 QAT, staged long-context pretraining, specialist+OPD가 전체 pipeline을 구성합니다.

## 원문

- https://outcomeschool.com/blog/decoding-deepseek-v4
