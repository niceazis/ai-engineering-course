# Semantic Caching은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-semantic-caching-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문을 직접 확인해 embedding similarity, threshold 수치 예와 cache hit/miss 흐름을 보존한 독립적인 한국어 상세 해설입니다.

## 1. Exact Cache의 한계

일반 cache는 key가 정확히 같아야 hit가 납니다.

    "프랑스 수도는?"
    "프랑스의 수도가 어디야?"

문자열은 다르지만 사실상 같은 질문입니다.

Semantic Cache는 두 질문의 embedding similarity를 비교해 **의미가 충분히 같으면 과거 answer를 재사용**합니다.

## 2. 기본 흐름

    new question
      → embedding
      → cached-query embeddings와 similarity
      → best match
         ├─ score >= threshold → cached answer
         └─ score < threshold  → LLM call
                                → query/answer 저장

Embedding Cache가 vector 계산을 재사용한다면 Semantic Cache는 더 공격적으로 **최종 model answer**를 재사용합니다.

## 3. 원문의 France 예

Cached question:

    "What is the capital of France?"
    → answer: "Paris"

새 질문:

    "Tell me the capital city of France."

Similarity:

    0.93

Threshold:

    0.85

0.93 > 0.85이므로 cache hit가 되고 LLM을 다시 부르지 않습니다.

반대로:

    "How do I bake a chocolate cake?"

의 similarity가 0.05라면 miss입니다.

## 4. Threshold가 핵심인 이유

Threshold를 너무 높게 두면:

    0.99

거의 exact paraphrase만 hit되어 절감 효과가 작습니다.

너무 낮게 두면:

    0.50

"capital of France"와 "capital of Germany"처럼 semantic shape는 비슷하지만 답이 다른 질문이 잘못 match할 위험이 있습니다.

원문은 0.85~0.95를 흔한 시작 범위로 제시하지만, 실제 값은 domain dataset으로 calibration해야 합니다.

## 5. False Hit가 가장 위험하다

Semantic cache miss:

    비용/latency 손실

False hit:

    틀린 과거 answer를 즉시 반환

따라서 일반적으로 precision을 보수적으로 높이는 쪽이 안전합니다.

고위험 domain에서는 exact constraint를 추가할 수 있습니다.

예:

    similarity > 0.92
    AND same tenant
    AND same policy version
    AND same locale

## 6. Cache Entry

저장할 항목:

    query_text
    query_embedding
    answer
    model/version
    source/version
    timestamp
    metadata

Answer가 RAG에 기반했다면 source document version도 같이 보존하는 것이 좋습니다.

## 7. Staleness

"오늘 환율", "현재 정책", "재고" 같은 질문은 semantic similarity가 높아도 과거 answer를 재사용하면 안 됩니다.

대응:

- TTL
- freshness category
- source-version invalidation
- cache bypass rules

Semantic cache는 content freshness policy와 반드시 같이 설계해야 합니다.

## 8. Similarity Search 자체의 비용

Cache entry가 매우 많아지면 모든 cached query와 exact comparison할 수 없습니다.

Vector DB/ANN index를 사용해:

    new embedding
      → nearest cached queries
      → threshold test

로 확장합니다.

## 9. Multi-Tenant Safety

서로 다른 고객의 answer가 같은 semantic cache에 섞이면 data leak이 발생할 수 있습니다.

Key/filter에:

    tenant_id
    permission scope
    knowledge-base version

을 포함해야 합니다.

## 10. 언제 효과가 큰가

- FAQ/support
- 반복 질문
- expensive reasoning call
- 동일 policy에 대한 paraphrase가 많음

효과가 작은 경우:

- 대부분 query가 unique
- answer가 실시간 데이터에 의존
- personalized state가 큼

## 11. Evaluation

Offline labeled pairs로:

- true semantic equivalents
- hard negatives
- temporal variants

를 만들고 threshold를 평가합니다.

측정:

- hit rate
- false-hit rate
- cost saved
- latency saved
- answer correctness

## 핵심 정리

- Semantic Cache는 문자열이 아니라 query embedding 의미를 기준으로 과거 answer를 재사용합니다.
- 원문 예에서는 similarity 0.93, threshold 0.85면 hit입니다.
- Threshold가 낮으면 false hit가 급증할 수 있어 domain별 calibration이 필수입니다.
- Stale answer와 cross-tenant leak을 막기 위해 TTL/version/metadata filter가 필요합니다.
- 비용 절감보다 false-hit 위험을 먼저 관리해야 합니다.

## 원문

- https://outcomeschool.com/blog/how-does-semantic-caching-work
