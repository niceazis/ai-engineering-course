# AI Engineering Explained — RAG 중심 한국어 상세 영상 학습 노트

> 영상: https://www.youtube.com/watch?v=lnfWvX66FUk  
> 제공: Outcome School / Amit Shekhar  
> 검증 범위: 영상 제목과 Outcome School 공식 소개/LinkedIn 게시물은 확인했습니다. **YouTube 자막 전문은 직접 검증하지 못했습니다.** 아래 내용은 영상의 RAG 파트 학습을 돕기 위해 Module 9의 Outcome School 공식 블로그와 함께 재구성한 상세 노트이며 자막의 문장별 번역이 아닙니다.

## 1. 영상이 놓는 AI Engineering의 큰 지도

영상은 AI Engineering을 다음 핵심 요소로 묶습니다.

    LLM
    RAG
    MCP
    Agent
    Fine-tuning
    Quantization

Module 9에서는 이 중 RAG를 중심으로 연결해서 봅니다.

## 2. 왜 RAG가 필요한가

LLM parameter 안의 지식만으로는 다음 문제가 있습니다.

- 최신 정보 부족
- 사내/private data 없음
- source citation 어려움
- 자주 변하는 사실을 fine-tuning하기 비효율적

RAG는 외부 evidence를 **inference 시점에 검색해 prompt에 주입**합니다.

## 3. 기본 RAG Pipeline

    documents
      → chunking
      → embeddings
      → vector DB

    user query
      → query embedding
      → retrieval
      → relevant chunks
      → LLM
      → grounded answer

핵심은 LLM을 재학습하지 않고 knowledge source를 바꿀 수 있다는 점입니다.

## 4. RAG와 Fine-Tuning의 역할 차이

RAG:

- facts
- latest policy
- private documents
- citation

Fine-tuning:

- behavior
- style
- task pattern
- output format

둘은 대체 관계가 아니라 결합 가능합니다.

    fine-tuned behavior
      + retrieved knowledge

## 5. Retrieval 품질이 전체 품질을 제한한다

LLM이 아무리 강해도 정답 evidence가 context에 없으면 grounded answer를 만들기 어렵습니다.

따라서 RAG는 generation보다 먼저 retrieval을 평가해야 합니다.

- Recall@k
- reranker precision
- source freshness
- chunk quality

가 중요합니다.

## 6. Module 9에서 확장되는 기술

Basic RAG 뒤에는 다음 최적화가 이어집니다.

- Hybrid Search: BM25 + vector
- Reranker: 후보 재정렬
- HyDE: hypothetical document로 검색
- GraphRAG: entity relation 활용
- Agentic RAG: 검색을 agent loop로 제어
- Vectorless RAG: SQL/BM25 등 다른 retrieval

즉 RAG는 하나의 고정 architecture가 아니라 retrieval design space입니다.

## 7. MCP/Agent와의 연결

Agent가 RAG를 tool로 사용하면:

    agent
      → decide retrieval needed?
      → choose vector/SQL/web
      → retrieve
      → inspect
      → repeat

가 됩니다.

Module 10의 Agent/MCP가 Module 9 retrieval 위에 orchestration layer를 추가한다고 이해하면 됩니다.

## 8. Production Checklist

- source document versioning
- access-control filter
- embedding model version
- chunking
- retrieval/reranking
- context budget
- citations
- stale-data handling
- latency/cost
- eval dataset

RAG를 “vector DB 하나 붙이기”로 축소하면 production failure를 놓치기 쉽습니다.

## 핵심 정리

- RAG는 외부 지식을 inference 시점에 검색해 LLM context에 넣습니다.
- Fine-tuning은 behavior, RAG는 knowledge를 바꾸는 데 더 자연스럽습니다.
- Retrieval recall이 end-to-end answer quality의 상한을 만듭니다.
- Module 9의 Hybrid/Reranker/Graph/Agentic RAG는 기본 RAG의 retrieval 한계를 확장합니다.
- 이 노트는 영상 자막 직역이 아니라 공식 영상 주제와 Outcome School 공식 RAG 자료를 연결한 학습 노트입니다.
