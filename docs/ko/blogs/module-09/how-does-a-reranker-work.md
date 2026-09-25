# Reranker는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-a-reranker-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-05-05 공개 원문을 직접 확인해 1M→100→5 two-stage retrieval, bi-encoder/cross-encoder와 France 수치 예제를 보존한 독립적 한국어 상세 해설입니다.

## 1. 왜 Reranker가 필요한가

첫 번째 retriever는 수백만 문서에서 매우 빠르게 후보를 찾아야 합니다.

그래서 계산이 싼 embedding/BM25를 사용하지만 정밀도가 완벽하지 않습니다.

Reranker는 **작은 후보 집합에 더 비싼 모델을 적용해 순서를 다시 매깁니다.**

원문 예:

    corpus: 1,000,000 docs
      → fast retriever
      → 100 candidates
      → reranker
      → top 5

## 2. Bi-Encoder

Query와 document를 독립적으로 embedding합니다.

    q → encoder → v_q
    d → encoder → v_d

장점:

- document vector 사전 계산 가능
- ANN index 사용 가능
- 대규모 retrieval 빠름

단점:

- query와 document가 encoder 내부에서 직접 상호작용하지 않음

## 3. Cross-Encoder

Query와 document를 하나의 input으로 함께 넣습니다.

    [query ; document]
      → Transformer
      → relevance score

모든 token이 서로 attention할 수 있어 훨씬 정밀하지만 document마다 forward pass가 필요해 느립니다.

그래서 top 100 같은 작은 후보에만 적용합니다.

## 4. 원문의 France 예

질문:

    What is the capital of France?

Retriever 후보에 reranker가 다음 score를 준 예:

    Doc 1 → 0.34
    Doc 2 (Paris is the capital...) → 0.97
    Doc 3 → 0.55
    Doc 4 (Germany...) → 0.21

최종:

    Doc2 > Doc3 > Doc1 > Doc4

Top-2만 LLM context로 보낼 수 있습니다.

## 5. Two-Stage Retrieval

1차 단계는 recall 중심:

    relevant document를 놓치지 않기

2차 단계는 precision 중심:

    가장 좋은 document를 위로

이 역할 분리가 핵심입니다.

원문은 retrieve 100~200, rerank 후 top 5~10 같은 범위를 실용 예로 설명합니다.

## 6. Late Interaction

ColBERT는 bi-encoder와 cross-encoder의 중간 접근입니다.

Query/document token embedding을 따로 계산하되 MaxSim으로 token-level interaction을 query 시점에 수행합니다.

Cross-encoder보다 빠르고 single-vector bi-encoder보다 세밀한 matching을 노립니다.

## 7. Cost-Latency Trade-off

Rerank candidate 수 N을 늘리면:

- recall ceiling ↑
- reranker cost ↑
- latency ↑

첫 retriever가 정답을 candidate set에 넣지 못하면 reranker가 복구할 수 없습니다.

따라서 retriever recall과 reranker precision을 따로 측정해야 합니다.

## 8. RAG에서의 영향

Context window가 크다고 top 100을 모두 넣는 것은 좋지 않을 수 있습니다.

Reranking으로:

- irrelevant chunk 제거
- prompt token 감소
- lost-in-the-middle 완화
- answer evidence density 증가

를 기대할 수 있습니다.

## 9. Evaluation

Retriever:

    Recall@100

Reranker:

    nDCG@10
    MRR
    Precision@k

End-to-end:

    answer correctness
    citation support
    latency
    token cost

## 핵심 정리

- Reranker는 빠른 1차 retrieval 뒤의 정밀한 2차 ranking 단계입니다.
- Bi-encoder는 scalable, cross-encoder는 accurate but expensive입니다.
- 원문은 1M 문서→100 후보→top 5 구조와 France score 예를 사용합니다.
- Reranker는 candidate set 밖의 문서를 복구할 수 없으므로 first-stage recall이 중요합니다.
- RAG에서는 relevance density와 context cost를 동시에 개선할 수 있습니다.

## 원문

- https://outcomeschool.com/blog/how-does-a-reranker-work
