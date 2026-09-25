# Vectorless RAG란? Embedding과 Vector DB 없는 RAG — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/vectorless-rag  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 원문 URL은 웹 도구에서 직접 열리지 않았습니다. Outcome School 공식 Module 9 레슨 구조를 기준으로 embedding/vector DB 없이 후보를 찾는 대표 retrieval 접근을 독립적으로 설명하며 원문 고유 수치는 단정하지 않습니다.

## 1. Vector RAG 복습

일반 RAG:

    documents
      → chunks
      → embeddings
      → vector DB

    query
      → embedding
      → vector search
      → chunks
      → LLM

이 방식은 강력하지만 ingestion pipeline과 vector index 운영이 필요합니다.

## 2. Vectorless RAG의 정의

Vectorless RAG는 **embedding/vector database를 필수 구성 요소로 쓰지 않고 문서에서 관련 context를 찾는 RAG**를 넓게 부르는 표현입니다.

가능한 retrieval source:

- BM25 / full-text search
- SQL
- metadata/filter
- file tree
- LLM-based scan/routing
- hierarchical summaries
- grep/code search

## 3. 왜 선택하는가

다음에서는 vector DB가 과할 수 있습니다.

- 문서가 소수
- 정확한 keyword/ID가 중요
- source가 이미 SQL/search engine에 잘 index됨
- corpus가 자주 바뀜
- embedding 비용/운영을 피하고 싶음

## 4. BM25 기반

기존 search engine:

    query
      → BM25
      → top documents
      → LLM

장점:

- mature infra
- exact term 강함
- 설명 가능

약점:

- paraphrase/semantic mismatch

## 5. SQL/Structured Retrieval

질문이 structured data에 관한 것이라면:

    "지난달 서울 매출 top 5"

vector search보다 SQL이 정확합니다.

    natural language
      → query plan / SQL
      → database
      → rows
      → LLM explanation

RAG의 핵심은 vector가 아니라 **외부 evidence를 generation 전에 가져오는 것**입니다.

## 6. Hierarchical Retrieval

Document tree를 유지합니다.

    corpus
      → document summaries
      → section summaries
      → raw paragraphs

Model/keyword search가 상위 summary에서 relevant branch를 선택하고 아래로 내려갑니다.

Embedding 없이도 큰 corpus를 단계적으로 줄일 수 있습니다.

## 7. LLM-Based Filtering

작은 candidate set이라면 LLM이 각 title/summary를 읽고 relevant 여부를 판단할 수 있습니다.

장점:

- semantic flexibility

단점:

- corpus가 커지면 LLM call 폭증
- nondeterminism/cost

따라서 first-stage lexical/metadata filter와 결합하는 것이 좋습니다.

## 8. File/Code Search

Codebase나 local files에서는:

- path
- symbol
- grep
- AST index

가 embedding보다 더 정확한 경우가 많습니다.

예:

    exact function name
    config key
    error string

이런 query는 lexical retrieval가 강합니다.

## 9. Vector RAG vs Vectorless

| 항목 | Vector RAG | Vectorless |
| --- | --- | --- |
| Semantic paraphrase | 강함 | 방법에 따라 약함 |
| Exact term | 보완 필요 | lexical은 강함 |
| Ingestion | embedding/index | 기존 search 활용 가능 |
| 운영 | vector DB 필요 | search/DB 재사용 |
| 업데이트 | re-embedding 필요 가능 | 즉시 index 가능 |
| 비용 | embedding + vector infra | query 방식에 따라 |

## 10. Hybrid가 더 현실적

실전에서는 "vector냐 아니냐"를 종교처럼 선택할 필요가 없습니다.

    query
      → router
         ├─ exact ID → BM25/SQL
         ├─ semantic QA → vector
         └─ relational → graph/SQL

처럼 데이터와 질문 유형에 맞춰 retrieval tool을 선택하는 편이 효율적입니다.

## 11. Evaluation

Vectorless를 선택할 때도 같은 labeled retrieval set에서:

- Recall@k
- latency
- update freshness
- infra cost
- final answer correctness

를 비교해야 합니다.

## 핵심 정리

- Vectorless RAG는 embedding/vector DB를 필수로 하지 않는 retrieval-augmented generation입니다.
- BM25, SQL, metadata, hierarchy, file/code search가 대표 대안입니다.
- Exact query나 structured source에서는 vector보다 더 단순하고 정확할 수 있습니다.
- Semantic paraphrase에는 vector retrieval가 유리할 수 있어 hybrid routing이 현실적입니다.
- 원문 본문을 직접 확인하지 못한 내용은 일반 retrieval 원리로만 보완했습니다.

## 원문

- https://outcomeschool.com/blog/vectorless-rag
