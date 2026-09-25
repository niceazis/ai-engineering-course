# Grouped Query Attention(GQA)이란 무엇이며 LLM은 왜 사용하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/grouped-query-attention  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-04-22 공개 원문을 직접 확인해 MHA→MQA→GQA 순서, 8-head/1,000-token 수치, KV-cache 절감 예를 보존한 독립적 한국어 해설입니다.

## 1. 큰 그림

GQA의 목적은 **MHA에 가까운 품질을 유지하면서 KV Cache를 크게 줄이는 것**입니다.

핵심:

- Query head는 여러 개 유지
- 여러 Query head가 하나의 K/V head를 공유
- MHA와 MQA 사이의 절충

## 2. MHA 복습

8-head MHA라면:

    Head 1: Q1, K1, V1
    Head 2: Q2, K2, V2
    ...
    Head 8: Q8, K8, V8

각 head가 서로 다른 Q/K/V projection을 가지므로 표현력이 높습니다.

하지만 inference에서 head마다 과거 K/V를 모두 저장해야 합니다.

## 3. KV Cache 문제

원문 예:

    past tokens = 1,000
    heads = 8

MHA는 layer 하나에서:

    Keys   = 8 × 1,000 = 8,000 vectors
    Values = 8 × 1,000 = 8,000 vectors
    total  = 16,000 vectors

를 저장합니다.

이 값은 **Transformer layer마다** 필요합니다.

64 heads와 100,000 tokens 같은 long-context 모델에서는 KV cache가 매우 커집니다.

## 4. MQA: 모든 Head가 K/V 하나 공유

Multi-Query Attention:

    Head 1: Q1, K_shared, V_shared
    Head 2: Q2, K_shared, V_shared
    ...
    Head 8: Q8, K_shared, V_shared

8개의 K/V set이 1개로 줄어 KV cache를 8배까지 줄일 수 있습니다.

장점:

- memory 감소
- memory bandwidth 감소
- decode throughput 개선

Trade-off:

모든 Query head가 같은 K/V representation을 보므로 MHA보다 표현 다양성이 줄어 품질 저하가 발생할 수 있습니다.

## 5. GQA: 그룹별로 K/V 공유

8 Query heads를 2 group으로 나누는 원문 예:

    Group 1: H1 H2 H3 H4 → K1, V1 공유
    Group 2: H5 H6 H7 H8 → K2, V2 공유

이제 K/V set은 8개가 아니라 2개입니다.

KV Cache 감소:

    8 K/V heads → 2 K/V heads
    = 4× smaller

MQA의 1 set보다는 많아 representation capacity를 더 유지합니다.

## 6. GQA가 MHA와 MQA를 일반화한다

Query head 수를 8이라고 할 때:

### MHA

    KV heads = 8

각 Query head가 독립 K/V.

### GQA

    1 < KV heads < 8

여러 Query가 그룹별 K/V 공유.

### MQA

    KV heads = 1

모든 Query가 K/V 하나 공유.

따라서 GQA parameter 하나로 양 극단을 연결할 수 있습니다.

## 7. GQA 계산

Query head h가 어느 KV group g에 속하는지 정합니다.

각 head는:

    Attention(Q_h, K_g, V_g)

를 계산합니다.

Query projection은 head별로 달라 여전히 서로 다른 질문을 만들 수 있고, K/V memory만 공유합니다.

## 8. KV Cache Memory 공식과 연결

대략적인 KV cache element 수는:

    layers
    × sequence_length
    × kv_heads
    × head_dim
    × 2

마지막 2는 K와 V입니다.

따라서 query_heads가 아니라 **kv_heads를 줄이는 것**이 cache memory에 직접 효과를 줍니다.

## 9. 왜 Decode에서 특히 중요한가

Prefill에서는 긴 prompt의 matrix operation이 중요하지만, autoregressive decode는 token 한 개씩 생성하며 매 step 과거 K/V를 읽습니다.

GQA는:

- cache size 감소
- HBM read 감소
- 더 큰 batch/concurrency 가능

으로 이어질 수 있어 serving throughput에서 효과가 큽니다.

## 10. 품질-메모리 Trade-off

| 방식 | Query heads | KV heads | Memory | 표현 다양성 |
| --- | ---: | ---: | --- | --- |
| MHA | H | H | 가장 큼 | 가장 높음 |
| GQA | H | G | 중간 | 중간~높음 |
| MQA | H | 1 | 가장 작음 | 상대적으로 제한 |

G를 몇 개로 할지가 architecture 선택입니다.

## 11. Uptraining

원문은 기존 MHA checkpoint를 GQA로 변환하는 연구 방향을 소개합니다.

새 GQA model을 처음부터 완전 재학습하지 않고 기존 K/V heads를 group 단위로 합치고 추가 training으로 적응시키는 방식입니다.

이 접근은 이미 비싼 MHA checkpoint를 재사용하는 데 유리합니다.

## 12. 실제 사용

현대 decoder LLM 다수는 GQA/MQA 계열을 사용합니다.

이유는 long context와 high-concurrency serving에서 KV cache가 실제 GPU memory의 큰 부분을 차지하기 때문입니다.

정확한 head 수는 모델 configuration을 확인해야 합니다.

## 핵심 정리

- MHA는 Query head마다 별도 K/V를 저장합니다.
- MQA는 모든 Query가 하나의 K/V를 공유합니다.
- GQA는 Query head를 group으로 묶고 group별 K/V를 공유합니다.
- 원문 8-head/2-group 예에서는 K/V set이 8→2로 줄어 cache가 4배 작아집니다.
- GQA는 MHA 품질과 MQA memory efficiency 사이의 실용적 절충입니다.
- Decode serving에서 KV cache와 memory bandwidth 절감 효과가 특히 중요합니다.

## 원문

- https://outcomeschool.com/blog/grouped-query-attention
