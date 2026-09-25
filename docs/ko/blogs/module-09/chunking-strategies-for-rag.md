# RAG 문서를 어떻게 Chunking할까? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/chunking-strategies-for-rag  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 원문 본문 캐시를 직접 열지 못했습니다. Outcome School 공식 Module 9 목차가 제시하는 Fixed/Sentence/Recursive/Structure/Semantic/Contextual/Small-to-big/Agentic 전략을 기준으로 독립적으로 설명합니다.

## 1. Chunking이 필요한 이유

RAG에서 문서 전체를 하나의 embedding으로 만들면 여러 주제가 한 vector에 섞입니다.

반대로 너무 작게 자르면 답에 필요한 문맥이 여러 chunk로 분리됩니다.

Chunking의 목표:

> Retrieval 단위는 작게 유지하되, 답변에 필요한 의미 단위는 잃지 않는다.

## 2. Fixed-Size Chunking

예:

    500 tokens
    overlap 50 tokens

장점:

- 구현 단순
- 크기 예측 가능
- batching 쉬움

단점:

- 문장/문단 중간에서 잘림
- table/code 구조 파괴

Baseline으로 좋지만 항상 최종 해법은 아닙니다.

## 3. Sentence-Based

문장 경계를 지키면서 일정 수의 문장을 묶습니다.

장점:

- 문법적 단위 보존

단점:

- 문장 길이가 매우 다를 수 있음
- section hierarchy를 반영하지 못함

## 4. Recursive Chunking

큰 separator부터 작은 separator 순으로 자릅니다.

예:

    section
      → paragraph
        → sentence
          → token

목표 size를 넘을 때만 더 작은 단위로 분해합니다.

일반 text에서 좋은 default입니다.

## 5. Document-Structure Chunking

Markdown heading, HTML section, PDF heading, code function/class 같은 구조를 사용합니다.

예:

    H2 section 하나
      + heading metadata
      + body

Technical document에서 의미 보존이 좋습니다.

## 6. Semantic Chunking

인접 sentence embedding similarity가 급격히 떨어지는 지점을 topic boundary로 봅니다.

장점:

- 의미 기반 구간 생성

단점:

- ingestion cost 증가
- threshold tuning 필요
- 재현성/설명 가능성 낮아질 수 있음

## 7. Contextual Chunking

Chunk text만 embedding하지 않고 문서 전체에서의 맥락을 짧게 덧붙입니다.

예:

    "이 chunk는 2026 환불정책의 해외 주문 예외 조항이다."

    + original chunk

Standalone chunk가 retrieval에서 의미를 잃는 문제를 줄입니다.

## 8. Small-to-Big

검색은 작은 chunk로 정밀하게 하고, LLM에는 부모 section을 확장해 전달합니다.

    small child chunk
      → retrieve
      → parent ID
      → larger parent context
      → generation

Precision과 generation context를 분리하는 좋은 패턴입니다.

## 9. Agentic Chunking

LLM/agent가 문서 구조와 의미를 보고 split 위치를 결정합니다.

장점:

- irregular document에 적응

단점:

- ingestion latency/cost
- nondeterminism
- 대규모 corpus에서 운영 복잡

## 10. Overlap

Overlap은 chunk boundary에서 이어지는 문맥을 보존합니다.

Too little:

- boundary information loss

Too much:

- duplicate retrieval
- embedding/storage cost
- context repetition

Overlap 비율은 retrieval eval로 결정해야 합니다.

## 11. Chunk Size Trade-off

작은 chunk:

- precise matching
- context 부족

큰 chunk:

- context 풍부
- embedding signal 희석
- prompt token 증가

정답은 embedding model, document type, question type에 따라 다릅니다.

## 12. Metadata를 함께 저장

Chunk마다 다음을 보존하면 좋습니다.

    document_id
    section_title
    page
    parent_id
    timestamp/version
    access_scope

Reranking, source citation, parent expansion에 필요합니다.

## 13. 평가 방법

Chunking 전략을 바꿀 때 반드시 retrieval benchmark를 고정합니다.

측정:

- Recall@k
- answer-support rate
- duplicate rate
- retrieved token count
- final answer accuracy

"chunk size 500이 표준" 같은 단일 숫자를 복사하지 않는 것이 중요합니다.

## 핵심 정리

- Chunking은 RAG quality를 결정하는 핵심 preprocessing 단계입니다.
- Fixed-size는 baseline, recursive/structure-aware는 실용적 default, semantic/contextual은 더 정교한 대안입니다.
- Small-to-big은 작은 retrieval 단위와 큰 generation context를 동시에 얻습니다.
- overlap과 chunk size는 실제 query set으로 검증해야 합니다.
- 원문 고유 수치는 직접 확인하지 못했으므로 임의로 원문 값으로 표시하지 않았습니다.

## 원문

- https://outcomeschool.com/blog/chunking-strategies-for-rag
