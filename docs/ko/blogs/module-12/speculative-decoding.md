# Speculative Decoding이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/speculative-decoding  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 draft-target 구조, rejection-sampling 기반 검증, 200-token/4-draft/50ms 수치 예와 2~3× speedup 조건을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 문제

Autoregressive decode는 token 하나마다 큰 target model 전체를 한 번 실행합니다.

    token1
      → full target pass
    token2
      → full target pass
    ...

Low batch에서는 GPU compute가 충분히 활용되지 않고 weight/memory movement가 bottleneck이 되기 쉽습니다.

## 2. 핵심 아이디어

작고 빠른 Draft Model이 여러 token을 미리 제안합니다.

    draft:
      t1 t2 t3 t4

큰 Target Model은 이 4개 위치를 한 번의 병렬 forward로 검증합니다.

Accepted prefix가 길수록 target forward 횟수가 줄어듭니다.

## 3. 왜 품질이 유지되는가

단순히 draft가 맞으면 채택하는 heuristic이 아닙니다.

Speculative sampling은 rejection-sampling 계열 acceptance rule을 사용해 **최종 sample distribution이 target model 단독 sampling과 동일하도록 설계**할 수 있습니다.

따라서 올바르게 구현하면 lossless acceleration입니다.

## 4. Round

1. Draft model이 k token proposal
2. Target model이 proposal sequence의 logits 병렬 계산
3. 왼쪽부터 accept/reject
4. rejection이 나오면 target distribution에서 보정 sample
5. accepted tokens를 output에 추가
6. 다음 round

## 5. 원문의 수치 예

Baseline:

    target token step = 50 ms
    output = 200 tokens

대략:

    200 × 50 ms
    = 10,000 ms
    = 10 sec

Speculative:

    draft 4 tokens × 5 ms = 20 ms
    target verification = 50 ms
    round cost = 70 ms

평균 4 tokens/round가 accept된다고 가정하면:

    200 / 4 = 50 rounds
    50 × 70 ms = 3,500 ms
    = 3.5 sec

원문 계산:

    10 sec → 3.5 sec
    speedup ≈ 2.86×

## 6. Acceptance Rate가 핵심

Draft가 target과 비슷할수록 proposal accept 비율이 높습니다.

Acceptance가 낮으면:

- draft compute 낭비
- target verification는 계속 필요
- speedup 감소

## 7. Draft Length

너무 짧음:

    amortization 이득 작음

너무 김:

    뒷부분 reject 가능성 증가

Optimal k는 workload/model pair마다 다릅니다.

## 8. Tokenizer 조건

Draft와 target은 token alignment가 맞아야 합니다.

원문은 동일 tokenizer를 중요한 조건으로 설명합니다.

## 9. Batch Size 영향

원문은 speculative decoding이 **낮은 batch에서 특히 유리**하다고 설명합니다.

High batch에서는 continuous batching으로 이미 GPU compute가 꽉 차 speculative verification의 추가 parallelism 이득이 줄 수 있습니다.

## 10. 변형

- N-gram speculation: 별도 draft model 없음
- Medusa: multiple decoding heads
- EAGLE: feature-level drafter
- MTP drafter: target 내부 auxiliary head

## 11. Trade-off

- second model memory
- scheduler complexity
- acceptance tuning
- very short response에서는 overhead
- high batch에서 이득 감소 가능

## 핵심 정리

- Speculative Decoding은 작은 model이 여러 token을 draft하고 큰 model이 한 번에 검증합니다.
- Rejection-sampling acceptance를 사용하면 target model과 동일한 output distribution을 유지할 수 있습니다.
- 원문 예는 200 tokens에서 10초→3.5초, 약 2.86× speedup입니다.
- 실제 원문은 대체로 2~3× 범위를 설명합니다.
- 성능은 acceptance rate, draft length, batch size에 크게 좌우됩니다.

## 원문

- https://outcomeschool.com/blog/speculative-decoding
