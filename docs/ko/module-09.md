# 모듈 9 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 9: 벡터 검색과 검색 증강 생성(RAG)

이 모듈에서는 LLM이 학습하지 않은 지식을 외부 데이터에서 찾아 활용하게 만드는 방법을 배웁니다. 벡터 저장·검색부터 다양한 검색 기법, 고급 RAG 형태까지 단계적으로 살펴봅니다.

모듈을 마치면 프로덕션 수준의 RAG 파이프라인을 구성하고 데이터 특성에 맞는 검색 기법을 선택할 수 있습니다.

**이 모듈의 레슨:**

1. [Vector Database는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-a-vector-database-work)
   ↳ [한국어 상세 학습 노트](blogs/module-09/how-does-a-vector-database-work.md)

2. [Approximate Nearest Neighbor(ANN) 검색은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-approximate-nearest-neighbor-ann-search-work)
   ↳ [한국어 상세 학습 노트](blogs/module-09/how-does-approximate-nearest-neighbor-ann-search-work.md)

3. [Semantic Search는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-semantic-search-work)
   ↳ [한국어 상세 학습 노트](blogs/module-09/how-does-semantic-search-work.md)

4. [Hybrid Search는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-hybrid-search-work)
   ↳ [한국어 상세 학습 노트](blogs/module-09/how-does-hybrid-search-work.md)

5. [Reranker는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-a-reranker-work)
   ↳ [한국어 상세 학습 노트](blogs/module-09/how-does-a-reranker-work.md)

6. [ColBERT란? Late Interaction Retrieval](https://outcomeschool.com/blog/decoding-colbert)
   ↳ [한국어 상세 학습 노트](blogs/module-09/decoding-colbert.md)

7. [RAG 문서를 어떻게 Chunking할까?](https://outcomeschool.com/blog/chunking-strategies-for-rag)
   ↳ [한국어 상세 학습 노트](blogs/module-09/chunking-strategies-for-rag.md)

8. [HyDE는 RAG에서 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-hyde-work)
   ↳ [한국어 상세 학습 노트](blogs/module-09/how-does-hyde-work.md)

9. [Embedding Cache는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-an-embedding-cache-work)
   ↳ [한국어 상세 학습 노트](blogs/module-09/how-does-an-embedding-cache-work.md)

10. [Semantic Caching은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-semantic-caching-work)
   ↳ [한국어 상세 학습 노트](blogs/module-09/how-does-semantic-caching-work.md)

11. [Agentic RAG란?](https://outcomeschool.com/blog/agentic-rag)
   ↳ [한국어 상세 학습 노트](blogs/module-09/agentic-rag.md)

12. [GraphRAG란? Knowledge Graph가 RAG를 개선하는 방법](https://outcomeschool.com/blog/graphrag)
   ↳ [한국어 상세 학습 노트](blogs/module-09/graphrag.md)

13. [Vectorless RAG란? Embedding과 Vector DB 없는 RAG](https://outcomeschool.com/blog/vectorless-rag)
   ↳ [한국어 상세 학습 노트](blogs/module-09/vectorless-rag.md)


---

### 9.1 Vector Database는 어떻게 동작하는가?

현대 AI 검색, 추천, 자체 문서 기반 질의응답의 핵심 구성 요소인 Vector Database를 배웁니다.

- Vector Database란?
- Embedding 복습
- 일반 DB의 한계
- Vector Database가 저장하는 것
- Similarity 측정
- Cosine Similarity
- Dot Product
- Euclidean Distance
- Nearest Neighbor 문제
- Brute Force가 느린 이유
- ANN과 Indexing
- HNSW
- IVF
- PQ
- 작은 코드 예제
- 실제 활용

시작하기: [Vector Database](https://outcomeschool.com/blog/how-does-a-vector-database-work)

→ [한국어 상세 학습 노트](blogs/module-09/how-does-a-vector-database-work.md)


### 9.2 Approximate Nearest Neighbor(ANN) 검색은 어떻게 동작하는가?

거대한 데이터 집합에서 “비슷한 것”을 매우 빠르게 찾는 ANN 검색을 배웁니다.

- Nearest Neighbor Search란?
- 데이터를 Vector로 바꾸는 방법
- “가까움”을 측정하는 방법
- 단순한 방식과 한계
- ANN Search란?
- 속도 vs 정확도 trade-off
- Tree(KD-Tree)
- Hashing(LSH)
- Clustering(IVF)
- Graph(HNSW)
- 간단한 코드 예제
- 실제 활용
- 적절한 방법 선택

시작하기: [ANN Search](https://outcomeschool.com/blog/how-does-approximate-nearest-neighbor-ann-search-work)

→ [한국어 상세 학습 노트](blogs/module-09/how-does-approximate-nearest-neighbor-ann-search-work.md)


### 9.3 Semantic Search는 어떻게 동작하는가?

키워드가 아니라 의미를 기준으로 검색하는 Semantic Search의 전체 흐름을 배웁니다.

- Keyword Search란?
- Keyword Search가 실패하는 경우
- Semantic Search란?
- Embedding이란?
- 비슷한 의미가 가까운 벡터로 표현되는 방식
- Cosine Similarity
- Vector Database
- 전체 Semantic Search 흐름
- 대규모 검색을 위한 ANN
- 실제 활용

시작하기: [Semantic Search](https://outcomeschool.com/blog/how-does-semantic-search-work)

→ [한국어 상세 학습 노트](blogs/module-09/how-does-semantic-search-work.md)


### 9.4 Hybrid Search는 어떻게 동작하는가?

Keyword Search와 Semantic Search를 결합해 각각의 약점을 보완하는 Hybrid Search를 배웁니다.

- Keyword Search
- Keyword Search만 사용할 때의 한계
- Semantic Search
- Semantic Search만 사용할 때의 한계
- Hybrid Search란?
- 두 검색을 함께 실행하는 방법
- 결과 리스트 결합
- Reciprocal Rank Fusion(RRF)
- Weighted Score Combination과 Normalization
- 실제 RAG에서의 활용

시작하기: [Hybrid Search](https://outcomeschool.com/blog/how-does-hybrid-search-work)

→ [한국어 상세 학습 노트](blogs/module-09/how-does-hybrid-search-work.md)


### 9.5 Reranker는 어떻게 동작하는가?

검색·RAG 파이프라인에서 1차 검색 결과를 더 정밀하게 재정렬하는 Reranker를 배웁니다.

- Reranker란?
- 검색/RAG 파이프라인에서의 위치
- Two-stage Retrieval
- 1차 검색이 빠르지만 정밀하지 않은 이유
- Bi-encoder vs Cross-encoder
- 문서를 단계별로 Scoring하는 방식
- 정확도 vs Latency/Cost trade-off
- ColBERT 같은 Late-interaction 모델
- 실제 Reranker 사례
- RAG에서 중요한 이유

시작하기: [Reranker](https://outcomeschool.com/blog/how-does-a-reranker-work)

→ [한국어 상세 학습 노트](blogs/module-09/how-does-a-reranker-work.md)


### 9.6 ColBERT란? Late Interaction Retrieval

느린 BERT Reranker의 세밀한 단어 단위 매칭을 유지하면서 수백만 Passage를 검색할 수 있게 하는 ColBERT의 Late Interaction 아이디어를 배웁니다.

- ColBERT 논문
- 필요한 기초 개념
- 큰 그림
- 기존 두 극단적 접근
- Late Interaction
- Query와 Document Encoding
- MaxSim
- 평균 대신 Max를 쓰는 이유
- Document Ranking
- Positive/Negative를 이용한 학습
- 작은 수치로 보는 Loss
- 대규모 빠른 검색
- 더 큰 Index 비용
- 결과
- 이후 발전
- 빠른 요약

시작하기: [ColBERT](https://outcomeschool.com/blog/decoding-colbert)

→ [한국어 상세 학습 노트](blogs/module-09/decoding-colbert.md)


### 9.7 RAG 문서를 어떻게 Chunking할까?

큰 문서를 적절한 작은 조각으로 나눠 필요한 내용을 정확히 검색하는 Chunking 전략을 배웁니다.

- RAG란?
- Chunk란?
- Chunking이 필요한 이유
- Retrieval 동작 방식
- 잘못된 Chunking의 문제
- Fixed-size Chunking
- Sentence-based Chunking
- Recursive Chunking
- Document Structure 기반 Chunking
- Semantic Chunking
- Contextual Chunking
- Small-to-big Chunking
- Agentic Chunking
- Chunk Overlap
- Chunk Size 선택
- 전략 비교
- 흔한 실수
- 결론

시작하기: [RAG Chunking 전략](https://outcomeschool.com/blog/chunking-strategies-for-rag)

→ [한국어 상세 학습 노트](blogs/module-09/chunking-strategies-for-rag.md)


### 9.8 HyDE는 RAG에서 어떻게 동작하는가?

질문 자체 대신 LLM이 만든 가상의 답변을 이용해 더 잘 검색하는 HyDE(Hypothetical Document Embeddings)를 배웁니다.

- RAG를 쉽게 이해하기
- RAG의 검색 문제
- 질문만으로 검색할 때의 약점
- HyDE란?
- 가상의 답변으로 검색하면 나아지는 이유
- 단계별 동작
- Worked Example
- 간단한 코드 예제
- 장점
- 단점
- 사용 시점
- 요약

시작하기: [HyDE](https://outcomeschool.com/blog/how-does-hyde-work)

→ [한국어 상세 학습 노트](blogs/module-09/how-does-hyde-work.md)


### 9.9 Embedding Cache는 어떻게 동작하는가?

동일한 텍스트의 Embedding을 반복 계산하지 않고 재사용해 비용과 시간을 줄이는 Embedding Cache를 배웁니다.

- Embedding이란?
- Embedding 생성 복습
- Embedding Cache란?
- 필요한 이유
- 핵심 아이디어
- Text + Model Hash로 만드는 Cache Key
- Cache Hit/Miss 흐름
- Eviction, LRU, TTL
- Memory vs Disk
- 장점
- 실제 RAG·Semantic Search 활용

시작하기: [Embedding Cache](https://outcomeschool.com/blog/how-does-an-embedding-cache-work)

→ [한국어 상세 학습 노트](blogs/module-09/how-does-an-embedding-cache-work.md)


### 9.10 Semantic Caching은 어떻게 동작하는가?

문자열이 정확히 같지 않아도 의미가 비슷한 요청에 과거 답변을 재사용하는 Semantic Caching을 배웁니다.

- Cache란?
- AI 앱에서 전통적 Cache의 문제
- Semantic Caching이란?
- Embedding
- Embedding Similarity
- 단계별 동작
- 수치 예제
- Similarity Threshold 설정
- 장점
- 주의할 점

시작하기: [Semantic Caching](https://outcomeschool.com/blog/how-does-semantic-caching-work)

→ [한국어 상세 학습 노트](blogs/module-09/how-does-semantic-caching-work.md)


### 9.11 Agentic RAG란?

Standard RAG가 부족한 이유와 Agent가 검색 과정을 계획·반복·검증하는 Agentic RAG를 배웁니다.

- 큰 그림
- RAG 복습
- AI Agent 복습
- Standard RAG의 한계
- Agentic RAG란?
- Agentic RAG Loop
- 세 가지 Building Block
- 실제 예제
- 대표 패턴
- Standard RAG vs Agentic RAG
- 사용 시점
- 한계
- 빠른 요약

시작하기: [Agentic RAG](https://outcomeschool.com/blog/agentic-rag)

→ [한국어 상세 학습 노트](blogs/module-09/agentic-rag.md)


영상 보기: [Agentic RAG Explained](https://www.youtube.com/watch?v=6nSegpuWJVw)

### 9.12 GraphRAG란?

[Vector Search](https://outcomeschool.com/blog/how-does-a-vector-database-work)와 Knowledge Graph를 결합해 검색 품질을 높이는 GraphRAG를 배웁니다.

→ [한국어 상세 학습 노트](blogs/module-09/how-does-a-vector-database-work.md)


- GraphRAG란?
- 일반 RAG가 충분하지 않은 이유
- 큰 그림
- Knowledge Graph 구축 방법
- 질문에 답하는 과정
- Local Search vs Global Search
- 사용 시점
- Trade-off
- 빠른 요약

시작하기: [GraphRAG](https://outcomeschool.com/blog/graphrag)

→ [한국어 상세 학습 노트](blogs/module-09/graphrag.md)


### 9.13 Vectorless RAG란?

문서를 Vector로 변환하거나 Vector Database를 사용하지 않고 자체 문서에서 답을 찾는 Vectorless RAG를 배웁니다.

- LLM이란?
- RAG란?
- 일반 Vector RAG의 동작
- Vector RAG의 문제
- Vectorless RAG란?
- 동작 방식
- 예제
- 다른 Vectorless 접근
- 장점
- 단점
- Vector RAG vs Vectorless RAG
- 선택 기준

시작하기: [Vectorless RAG](https://outcomeschool.com/blog/vectorless-rag)

→ [한국어 상세 학습 노트](blogs/module-09/vectorless-rag.md)


**모듈 9 영상 및 추가 자료:**

- [AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization](https://www.youtube.com/watch?v=lnfWvX66FUk) (영상)
- [Agentic RAG Explained](https://www.youtube.com/watch?v=6nSegpuWJVw) (영상)

---
