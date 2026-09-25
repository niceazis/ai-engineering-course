# Embedding Cache는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-an-embedding-cache-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-06-21 공개 원문을 직접 확인해 text+model hash key, hit/miss, 1,000-query 예, LRU/TTL과 memory/disk 비교를 보존하면서 독립적으로 다시 쓴 한국어 해설입니다.

## 1. 핵심 아이디어

Embedding 계산은 API 비용과 compute latency가 듭니다.

같은 text를 같은 embedding model에 여러 번 보낸다면 결과도 같으므로 다시 계산할 필요가 없습니다.

    text
      → cache lookup
         ├─ HIT  → saved vector
         └─ MISS → embedding model
                  → save
                  → vector

## 2. 원문의 반복 Query 예

인기 query가 하루 1,000번 들어온다고 합시다.

Cache 없음:

    embedding calls = 1,000

Cache 있음:

    first = compute 1
    remaining = reuse 999

즉 999번의 중복 계산을 제거합니다.

## 3. Re-Ingestion에서도 유용

Document chunk 5개 중 1개만 수정됐다고 합시다.

    chunk1 unchanged → reuse
    chunk2 unchanged → reuse
    chunk3 changed   → recompute
    chunk4 unchanged → reuse
    chunk5 unchanged → reuse

전체 corpus를 다시 embedding하지 않고 바뀐 chunk만 계산할 수 있습니다.

## 4. Cache Key

Raw text만 key로 쓰면 model version이 바뀌었을 때 잘못된 vector를 재사용할 수 있습니다.

원문 원칙:

    key = hash(text + model_name/version)

예:

    "return policy"
    + "text-embedding-v3"
      → hash
      → a3f9c1...b27

Embedding dimension/preprocessing config도 결과에 영향을 준다면 version key에 포함하는 편이 안전합니다.

## 5. Hit / Miss

### Cache Hit

Key 존재:

    return saved embedding

### Cache Miss

Key 없음:

    call embedding model
    → store vector
    → return vector

Miss 결과를 저장하므로 다음 동일 request는 hit가 됩니다.

## 6. LRU

Cache 공간이 찼을 때 가장 오래 사용하지 않은 item을 제거합니다.

원문 예:

    A last used 1 min
    B last used 2 min
    C last used 30 min → evict

Popular item을 유지하는 정책입니다.

## 7. TTL

Time To Live는 일정 시간이 지나면 item을 만료시킵니다.

예:

    TTL = 1 hour

Model/version/data freshness 때문에 오래된 cache를 자동 정리할 때 유용합니다.

LRU와 TTL을 함께 쓸 수 있습니다.

## 8. In-Memory vs Disk

### Redis/Memory

- 매우 빠름
- 용량 제한
- live query cache에 적합

### Disk/Persistent Store

- 느림
- 큰 용량
- restart 후 유지
- 대규모 ingestion artifact에 적합

실전은 L1 memory + L2 persistent cache 계층을 둘 수 있습니다.

## 9. Cache Invalidation

Embedding model을 바꾸면 기존 vector space와 호환되지 않을 수 있습니다.

따라서:

    model version change
      → new cache namespace/key

가 필요합니다.

Text normalization rule도 key의 일부로 일관되게 적용해야 합니다.

## 10. Embedding Cache vs Semantic Cache

Embedding Cache:

    같은 input text → 같은 vector 재사용

Semantic Cache:

    의미가 비슷한 query → 과거 answer 재사용

Embedding cache는 correctness risk가 상대적으로 작습니다. 동일 model/input이면 결과 자체가 재계산 결과와 같습니다.

## 핵심 정리

- Embedding Cache는 동일 text/model의 embedding을 한 번만 계산합니다.
- 원문 예에서 1,000번 반복 query는 1 compute + 999 reuse가 됩니다.
- Key에 text와 model/version을 함께 넣어 vector-space collision을 막습니다.
- LRU는 공간, TTL은 freshness를 관리합니다.
- Query path는 memory, ingestion은 persistent disk cache가 적합할 수 있습니다.
- Semantic Cache와 달리 answer를 재사용하는 것이 아니라 embedding 계산만 재사용합니다.

## 원문

- https://outcomeschool.com/blog/how-does-an-embedding-cache-work
