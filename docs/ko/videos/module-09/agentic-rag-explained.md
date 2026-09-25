# Agentic RAG Explained — 한국어 상세 영상 학습 노트

> 영상: https://www.youtube.com/watch?v=6nSegpuWJVw  
> 제공: Outcome School  
> 검증 범위: 영상 URL과 주제는 공식 과정 자료에서 확인했습니다. **영상 자막 전문은 직접 검증하지 못했습니다.** 아래 내용은 동일 주제의 Outcome School 공식 Agentic RAG 블로그를 직접 확인해 만든 상세 보조 노트입니다.

## 1. Naive RAG vs Agentic RAG

Standard RAG:

    retrieve once
      → generate once

Agentic RAG:

    plan
      → retrieve
      → inspect
      → query rewrite / another tool
      → retrieve again
      → stop when enough
      → answer

차이는 retrieval을 **고정 pipeline이 아니라 decision loop**로 바꾸는 것입니다.

## 2. 왜 Agent가 필요한가

복잡한 질문은 한 번의 검색으로 끝나지 않습니다.

예:

    "매출이 가장 크게 감소한 제품을 찾고,
     그 제품 고객 불만의 공통 원인을 설명해라."

필요한 작업:

1. SQL로 제품별 매출 비교
2. 대상 제품 선택
3. support ticket 검색
4. 불만 theme 분석
5. evidence 결합

한 vector query만으로 해결하기 어렵습니다.

## 3. 세 Building Block

### Agent

질문을 읽고 next action을 결정합니다.

### Tools

- vector DB
- SQL
- web
- files
- APIs

### State

이전 검색 결과와 아직 해결하지 못한 subquestion을 유지합니다.

## 4. Retrieval Quality Check

Agentic RAG의 중요한 추가 단계:

    retrieved chunks
      → relevant enough?

No:

    rewrite query / change source / retrieve again

Yes:

    synthesize answer

이 verification loop가 standard RAG와의 핵심 차이입니다.

## 5. ReAct Pattern

개념적으로:

    reason about next step
      → action
      → observation
      → repeat

Production observability에서는 hidden reasoning text보다:

- selected tool
- arguments
- retrieved evidence
- stop reason

을 기록하는 것이 더 중요합니다.

## 6. Cost와 Latency

Agentic RAG는 retrieval과 LLM call이 여러 번 일어날 수 있습니다.

따라서 반드시:

- max steps
- timeout
- token budget
- tool-call budget
- stop condition

을 둬야 합니다.

## 7. Complexity Routing

모든 질문을 Agentic RAG로 보내면 낭비입니다.

    simple FAQ
      → standard RAG

    multi-hop / multi-source
      → agentic RAG

처럼 router를 두는 것이 실용적입니다.

## 8. Evaluation

- task success
- evidence correctness
- average tool calls
- redundant search rate
- latency
- cost
- groundedness

Agentic system은 final answer만 평가하면 왜 실패했는지 알기 어렵습니다.

## 핵심 정리

- Agentic RAG는 retrieval을 agent-controlled loop로 만듭니다.
- 여러 source와 multi-hop 질문에서 강합니다.
- Retrieval 결과를 평가하고 query/tool을 바꿔 재시도할 수 있습니다.
- 대가로 latency·cost·failure mode가 증가합니다.
- 단순 질문은 Standard RAG, 복잡한 질문만 Agentic RAG로 route하는 것이 효율적입니다.
- 이 노트는 자막 직역이 아니라 공식 Agentic RAG 블로그로 교차검증한 학습 노트입니다.
