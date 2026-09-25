# GraphRAG란? Knowledge Graph가 RAG를 개선하는 방법 — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/graphrag  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-05-05 공개 원문을 직접 확인해 graph indexing, entity/relation extraction, community summary, Local/Global Search를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 일반 RAG가 약한 질문

Vector RAG는 query와 비슷한 chunk를 찾는 데 강합니다.

하지만:

    "Person A가 과거 프로젝트를 통해 Company X와 어떻게 연결되는가?"

처럼 여러 entity/relation을 따라가야 하는 질문은 한두 chunk의 similarity만으로 풀기 어렵습니다.

이런 질문은 multi-hop relation이 필요합니다.

## 2. GraphRAG

    GraphRAG
      = Knowledge Graph + RAG

문서에서:

- Entity → node
- Relation → edge

를 추출해 연결 구조를 만듭니다.

Query 때 관련 node와 edge를 따라 evidence를 모읍니다.

## 3. Indexing Phase

원문 흐름:

    Documents
      → Chunks
      → Entity + Relation extraction
      → Knowledge Graph
      → Community detection
      → Community summaries
      → Graph + embeddings + summaries 저장

초기 indexing이 일반 vector RAG보다 훨씬 무겁습니다.

## 4. 예시

Text:

    "Alice worked at Acme as an engineer.
     Acme was acquired by Globex in 2020.
     Bob was the CEO of Globex."

Graph:

    Alice --worked_at--> Acme
    Acme --acquired_by--> Globex
    Bob --CEO_of--> Globex

이제 Alice와 Globex의 관계를 edge traversal로 연결할 수 있습니다.

## 5. Entity Resolution

여러 chunk에 등장한 "Globex"가 같은 entity라면 하나의 node로 합쳐야 합니다.

실전 난점:

- 약어
- 동명이인
- company rename
- aliases

잘못 merge하면 graph 자체가 오류를 전파합니다.

## 6. Query Phase

1. Query에서 entity/intent 파악
2. embedding 또는 entity lookup으로 starting nodes 선택
3. graph neighborhood/traversal
4. 연결된 source chunks 수집
5. 필요 시 community summary
6. LLM context 구성
7. 답 생성

Graph는 evidence를 연결하는 retrieval structure입니다.

## 7. Local Search

원문 예:

    "Alice의 Acme에서 역할은?"

특정 entity 주변 작은 subgraph와 관련 chunks를 수집합니다.

특정 사람/회사/프로젝트에 대한 질문에 적합합니다.

## 8. Global Search

원문 예:

    "회사 문서 전체에서 주요 theme은?"

한 subgraph로 답할 수 없습니다.

GraphRAG는 indexing 시 만든 community summaries를 활용합니다.

원문 흐름:

    Map:
      각 community summary에서 partial answer + relevance score

    Reduce:
      high-score partial answers를 최종 답으로 합침

대규모 dataset을 context window에 통째로 넣지 않고 global question을 처리합니다.

## 9. Vector RAG와 함께 쓰기

GraphRAG가 vector search를 대체해야 하는 것은 아닙니다.

실전 hybrid:

    query
      ├─ vector chunks
      ├─ graph neighborhood
      └─ community summaries
          → rerank/context assemble

Simple factual query는 vector search가 더 싸고 빠릅니다.

## 10. Cost

Indexing 비용:

- LLM entity extraction
- relation extraction
- graph build
- community detection
- summary generation

Query도 traversal과 context assembly가 추가됩니다.

따라서 모든 knowledge base에 GraphRAG를 적용할 필요는 없습니다.

## 11. 잘 맞는 경우

- 조직/사람/프로젝트 관계
- 사건 연결
- research literature
- fraud/network
- 전체 corpus theme analysis

## 12. 덜 맞는 경우

- 단순 FAQ
- exact document lookup
- relation이 거의 없는 독립 chunk corpus
- document가 자주 바뀌어 graph reindex cost가 큰 경우

## 핵심 정리

- GraphRAG는 entity와 relation을 knowledge graph로 만들고 RAG retrieval에 사용합니다.
- 일반 vector similarity가 놓치는 multi-hop 연결을 명시적으로 추적할 수 있습니다.
- 원문은 indexing에서 community summaries까지 만들고 Local/Global Search를 구분합니다.
- Global Search는 community별 map → relevance → reduce 구조를 사용합니다.
- 강력하지만 indexing 비용과 entity-resolution complexity가 큽니다.

## 원문

- https://outcomeschool.com/blog/graphrag
