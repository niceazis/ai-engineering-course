# ColBERT란? Late Interaction Retrieval — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/decoding-colbert  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 Outcome School 원문 본문 캐시를 직접 열지 못했습니다. 공식 Module 9 레슨 구조와 ColBERT 논문의 공개 핵심 알고리즘을 교차검증해 작성하며, 원문 고유 수치는 확인되지 않은 것으로 취급합니다.

## 1. Retrieval의 두 극단

### Bi-Encoder

Query와 document를 각각 하나의 vector로 압축합니다.

    q → one vector
    d → one vector
    score = q·d

매우 빠르지만 token-level 세부 matching이 하나의 vector에 압축됩니다.

### Cross-Encoder

    [query + document]
      → Transformer
      → relevance score

Token끼리 직접 상호작용해 정확하지만 모든 query-document pair를 다시 계산해야 해 대규모 corpus 검색에는 비쌉니다.

ColBERT는 둘 사이를 노립니다.

## 2. Late Interaction

ColBERT는 query와 document를 **token-level embedding sequence**로 따로 encoding해 document side를 미리 저장합니다.

    Q = [q1, q2, ... qm]
    D = [d1, d2, ... dn]

Query가 들어온 뒤에만 token 간 similarity를 계산합니다.

"Interaction을 늦게 한다"는 의미가 Late Interaction입니다.

## 3. MaxSim

각 query token q_i에 대해 document token 중 가장 비슷한 하나를 찾습니다.

    MaxSim(q_i, D)
      = max_j q_i · d_j

Document score:

    score(Q,D)
      = Σ_i max_j(q_i · d_j)

즉 query의 각 중요한 token이 document 어디에서 가장 잘 match되는지를 따로 봅니다.

## 4. 왜 Average가 아니라 Max인가

Query token "database"가 document 전체와 평균 similarity를 내면 대부분 무관한 token 때문에 signal이 희석됩니다.

MaxSim은:

    "database"
      → document의 "database"나 강하게 관련된 token

만 잡아냅니다.

그 뒤 query token별 best match를 합칩니다.

## 5. 예시

Query:

    "neural search"

Document A:

    "semantic neural retrieval systems"

Document B:

    "database backup policy"

Query token "neural"은 A의 "neural"과 큰 score, "search"는 "retrieval"과 높은 semantic score를 가질 수 있습니다.

A의 MaxSim 합이 B보다 높아집니다.

## 6. Indexing

Document를 매 query마다 BERT에 넣지 않습니다.

Offline:

    documents
      → encoder
      → token embeddings
      → compressed/indexed storage

Online:

    query
      → query token embeddings
      → candidate token search
      → MaxSim ranking

이 precomputation이 scale의 핵심입니다.

## 7. Storage Trade-off

Single-vector retriever는 document당 vector 하나를 저장합니다.

ColBERT는 많은 token vector를 저장하므로 index가 훨씬 큽니다.

따라서:

    retrieval quality ↑
    ↔ index/storage cost ↑

의 trade-off가 있습니다.

후속 ColBERT 계열은 compression과 indexing을 개선해 이 문제를 줄였습니다.

## 8. Training

Positive document는 score를 높이고 negative document는 낮추도록 학습합니다.

단순 pairwise loss 예:

    L = -log
        exp(s_pos)
        / [exp(s_pos)+exp(s_neg)]

Hard negative mining이 retrieval model 품질에 중요합니다.

## 9. Reranker인가 Retriever인가

ColBERT는 두 방식 모두에 활용될 수 있습니다.

- 큰 corpus에 자체 index를 구성해 first-stage retrieval
- BM25/vector 후보를 late-interaction으로 rerank

어느 위치에 쓰는지는 latency/storage budget에 따라 다릅니다.

## 10. Bi-Encoder / ColBERT / Cross-Encoder

| 항목 | Bi-Encoder | ColBERT | Cross-Encoder |
| --- | --- | --- | --- |
| Document 표현 | 1 vector | token vectors | query마다 재계산 |
| Interaction | vector-level | late token-level | full early interaction |
| 속도 | 가장 빠름 | 중간 | 가장 느림 |
| Index size | 작음 | 큼 | 사전 index 없음 |
| 정밀도 | 중간 | 높음 | 매우 높음 |

## 핵심 정리

- ColBERT는 query/document를 따로 encode하면서 token-level matching을 query 시점까지 늦춥니다.
- 핵심 scoring은 query token마다 document token의 최대 similarity를 찾는 MaxSim입니다.
- Cross-encoder의 세밀함과 bi-encoder의 precomputation 장점을 절충합니다.
- 대가로 document당 여러 token vector를 저장해 index가 큽니다.
- 원문 본문을 직접 확인하지 못한 부분은 ColBERT 공개 논문 수준의 설명으로만 보완했습니다.

## 원문

- https://outcomeschool.com/blog/decoding-colbert
