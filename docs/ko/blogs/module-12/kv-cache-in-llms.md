# LLM의 KV Cache — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/kv-cache-in-llms  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 autoregressive repeated computation과 K/V만 cache하는 이유를 독립적으로 정리했습니다.

## 1. 반복 계산 문제

Prompt:

    I love AI

에서 새 token을 하나 만들고 다시 다음 token을 생성할 때 과거 token의 K/V는 변하지 않습니다.

Cache가 없으면 과거 K/V projection을 매 step 다시 계산합니다.

## 2. KV Cache

각 layer에서 이미 계산한:

    K_past
    V_past

를 저장합니다.

새 token에서는:

    Q_new
    K_new
    V_new

만 계산하고 K/V를 cache 뒤에 append합니다.

## 3. 왜 Q는 Cache하지 않는가

현재 decode step의 query는 **새 token 위치가 과거 K/V를 조회하는 데 사용**됩니다.

과거 query는 다음 step에서 다시 필요하지 않습니다.

반면 과거 K/V는 새 query가 계속 참조하므로 저장합니다.

## 4. 속도 효과

Without cache:

    step t
      → past 1..t의 K/V 재계산

With cache:

    step t
      → token t의 K/V만 계산
      → 과거 cache read

Projection 재계산을 크게 줄입니다.

## 5. Memory Cost

대략:

    bytes
      ≈ layers
        × tokens
        × kv_heads
        × head_dim
        × 2(K,V)
        × bytes_per_element

Batch/concurrency가 늘면 request마다 cache가 필요합니다.

## 6. Trade-off

KV Cache는 decode compute를 memory로 바꾸는 최적화입니다.

따라서 long-context serving에서는 cache memory가 병목이 됩니다.

이 문제를 GQA, quantization, eviction, PagedAttention이 해결합니다.

## 핵심 정리

- KV Cache는 과거 token의 Key/Value를 재사용합니다.
- Query는 현재 token마다 새로 필요하지만 과거 Query는 재사용하지 않습니다.
- Decode 속도는 크게 좋아지지만 memory는 context length와 batch에 따라 증가합니다.
- 현대 serving 최적화 대부분이 KV Cache 관리와 연결됩니다.

## 원문

- https://outcomeschool.com/blog/kv-cache-in-llms
