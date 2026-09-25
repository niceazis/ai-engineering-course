# Hybrid Search는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-hybrid-search-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 keyword+semantic 결합, RRF와 weighted fusion을 중심으로 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 두 Search의 강점

### Keyword Search

BM25 같은 lexical search는 다음에 강합니다.

- exact product ID
- 사람/회사 이름
- 희귀 약어
- 특정 오류 코드

### Semantic Search

Embedding search는 다음에 강합니다.

- paraphrase
- synonym
- 자연어 의미 유사성

둘 중 하나만 쓰면 반대쪽 장점을 잃습니다.

## 2. Hybrid Search

같은 query를 두 검색기에 동시에 보냅니다.

    query
      ├─ BM25 → ranking A
      └─ vector → ranking B
             ↓
           fusion
             ↓
          final ranking

## 3. Reciprocal Rank Fusion(RRF)

Score scale이 서로 다른 두 system을 간단히 합치는 방법입니다.

    RRF(d)
      = Σ 1 / (k + rank_i(d))

보통 k는 ranking 상단에 지나치게 민감하지 않도록 하는 상수입니다.

RRF는 raw BM25 score와 cosine score를 직접 normalize하지 않아도 됩니다.

## 4. 예시

Keyword ranking:

    1. D1
    2. D3
    3. D2

Semantic ranking:

    1. D2
    2. D1
    3. D4

D1과 D2는 두 list 모두 상위에 있어 fusion에서 높은 점수를 얻습니다.

## 5. Weighted Score Fusion

또 다른 방법:

    final
      = alpha * normalized_BM25
      + (1-alpha) * normalized_vector

문제는 BM25와 cosine의 score distribution이 다르므로 normalization이 필요하다는 것입니다.

Alpha는 labeled data에서 튜닝해야 합니다.

## 6. 왜 Hybrid가 RAG에 유용한가

RAG 질문에는 exact entity와 semantic intent가 함께 나옵니다.

예:

    "ERR_1042 오류가 결제 취소에서 왜 발생하나요?"

- ERR_1042 → lexical match 중요
- "결제 취소에서 왜 발생" → semantic intent 중요

Hybrid가 두 signal을 동시에 살립니다.

## 7. Candidate Pool

실전:

    BM25 top 50
    vector top 50
      → union
      → RRF
      → top 20
      → cross-encoder reranker
      → top 5

처럼 multi-stage pipeline을 구성할 수 있습니다.

## 8. Metadata Filter

Tenant, language, date 같은 filter를 retrieval 전 적용하면 irrelevant candidate를 줄일 수 있습니다.

Hybrid search engine에서 두 branch가 동일한 filter semantics를 쓰는지 확인해야 합니다.

## 9. 실패 패턴

- alpha를 감으로 고정
- vector/keyword score를 normalize 없이 합침
- candidate pool이 너무 작음
- exact ID가 tokenizer/analysis 과정에서 손실
- duplicate document를 fusion 후 제거하지 않음

## 10. Evaluation

Query를 유형별로 나눠 평가합니다.

- exact lookup
- semantic paraphrase
- mixed query
- long natural-language query

Hybrid가 전체 평균만 높이고 특정 critical query를 망가뜨리지 않는지 확인해야 합니다.

## 핵심 정리

- Hybrid Search는 lexical BM25와 semantic vector search를 결합합니다.
- RRF는 ranking position만으로 합쳐 score-scale 문제를 피합니다.
- Weighted fusion은 더 유연하지만 normalization과 alpha tuning이 필요합니다.
- RAG에서는 candidate generation 후 reranker를 추가하는 구조가 흔합니다.
- exact entity와 semantic intent가 함께 있는 enterprise search에 특히 유용합니다.

## 원문

- https://outcomeschool.com/blog/how-does-hybrid-search-work
