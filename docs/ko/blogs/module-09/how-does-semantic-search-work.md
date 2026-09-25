# Semantic Search는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-semantic-search-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인하고, 의미 기반 검색의 전체 pipeline을 독립적으로 다시 설명한 학습 노트입니다.

## 1. Keyword Search의 한계

Keyword search는 exact word overlap에 강합니다.

하지만:

    "비밀번호를 잊었어요"
    "로그인 자격 증명을 재설정하려면?"

처럼 의미는 같고 단어는 다른 문장을 놓칠 수 있습니다.

또 "bank"처럼 같은 단어가 서로 다른 의미를 가질 때 keyword match만으로는 문맥 구분이 어렵습니다.

## 2. Semantic Search

Semantic Search는 query와 document를 embedding으로 바꾸고 **vector similarity**로 검색합니다.

    query text
      → query embedding
      → vector search
      → semantically close documents

핵심은 문자열 일치가 아니라 representation 공간의 거리입니다.

## 3. Indexing Phase

1. 문서 수집
2. chunking
3. 각 chunk embedding
4. vector DB 저장
5. source/metadata 저장

이 단계는 문서가 바뀔 때 다시 수행합니다.

## 4. Query Phase

1. user query embedding
2. 같은 embedding space에서 ANN search
3. top-k 결과
4. 필요하면 metadata filter/reranker
5. 사용자에게 결과 또는 RAG context로 전달

## 5. Cosine Similarity

    cos(q,d)
      = q·d / (||q|| ||d||)

Normalized embedding에서는 dot product와 cosine ranking이 같아질 수 있습니다.

Metric은 embedding model 문서를 따라야 합니다.

## 6. Why Embeddings Work

Embedding model은 의미가 비슷한 sample을 가까이 두도록 학습됩니다.

따라서 paraphrase나 synonym은 keyword overlap이 낮아도 가까운 vector가 될 수 있습니다.

그러나 embedding은 완벽한 의미 이해가 아닙니다. Domain, language, length에 따라 품질이 달라집니다.

## 7. 대규모 Search

수백만 vector를 모두 brute-force로 비교하면 느립니다.

그래서 HNSW, IVF 등 ANN index를 사용합니다.

Semantic Search 품질은:

    embedding quality
      × chunk quality
      × ANN recall
      × metadata/filter
      × reranker

의 결합 결과입니다.

## 8. Search와 RAG의 차이

Semantic Search:

    query → relevant documents

RAG:

    query → relevant documents
          → LLM
          → generated answer

즉 Semantic Search는 RAG의 retrieval component가 될 수 있습니다.

## 9. Failure Cases

- 숫자/ID/제품코드 exact match
- 매우 희귀 전문용어
- 최신 entity
- negation/constraint
- 긴 문서에서 chunk boundary 문제

이 경우 keyword search와 결합하는 Hybrid Search가 유리합니다.

## 10. Evaluation

Offline:

- Recall@k
- MRR
- nDCG
- labeled query-document pairs

Online:

- click/acceptance
- RAG answer correctness
- latency

Embedding cosine 값 자체보다 실제 task metric을 봐야 합니다.

## 핵심 정리

- Semantic Search는 query/document embedding의 의미적 가까움을 이용합니다.
- Indexing과 query 두 단계로 나뉩니다.
- Vector DB와 ANN이 대규모 검색을 담당합니다.
- Keyword exact match가 강한 경우가 있어 Hybrid Search가 실용적입니다.
- RAG 품질을 높이려면 retrieval 자체를 독립적으로 평가해야 합니다.

## 원문

- https://outcomeschool.com/blog/how-does-semantic-search-work
