# Agentic RAG란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/agentic-rag  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-05-01 공개 원문을 직접 확인해 Standard RAG와의 차이, agent loop, 세 building block과 ReAct-style pattern을 보존하면서 독립적으로 다시 쓴 한국어 해설입니다.

## 1. Standard RAG의 한계

Standard RAG:

    query
      → retrieve once
      → top chunks
      → LLM answer

단순 fact lookup에는 좋지만 다음 질문에는 약합니다.

- 여러 source를 순차 조회해야 함
- 첫 검색 결과가 부족함
- query rewrite가 필요
- 검색 자체가 필요한지 먼저 판단해야 함
- multi-hop reasoning 필요

원문은 Standard RAG를 "책 한 권을 가져오는 librarian", Agentic RAG를 "필요하면 여러 서가를 다시 조사하는 researcher"로 비유합니다.

## 2. 정의

    Agentic RAG
      = RAG + retrieval을 제어하는 AI Agent

Agent는 매 step에서 다음을 결정합니다.

- retrieval이 필요한가?
- 어떤 tool/source를 사용할까?
- query를 어떻게 바꿀까?
- 결과가 충분한가?
- 다시 검색할까?
- 언제 답을 작성할까?

## 3. Agentic RAG Loop

일반적인 loop:

    observe question/state
      → plan
      → choose retrieval/tool
      → execute
      → inspect evidence
      → enough?
          no → reformulate/retrieve again
          yes → synthesize answer

Fixed pipeline이 아니라 condition-based loop입니다.

## 4. 세 Building Block

원문은 세 가지로 정리합니다.

### Agent — Brain

LLM이 plan, tool choice, evidence evaluation을 담당합니다.

### Tools — Hands

- vector search
- keyword search
- SQL
- web
- files/API

같은 외부 source입니다.

### Memory/State — Notebook

이전 검색 결과, unresolved subquestion, intermediate facts를 유지합니다.

## 5. Multi-Hop 예

질문:

    "올해 매출이 가장 크게 줄어든 제품은 무엇이고,
     그 제품 고객 불만의 가장 흔한 원인은?"

필요한 step:

1. SQL에서 제품별 매출 비교
2. 최악 제품 식별
3. support ticket 검색
4. 불만 theme 분석
5. evidence 연결
6. 답 작성

한 번의 vector retrieval로는 자연스럽게 풀기 어렵습니다.

## 6. Query Rewriting

검색 결과가 약하면 agent가:

    original query
      → more specific query
      → alternative keyword
      → source-specific query

로 바꿀 수 있습니다.

이를 무제한 허용하면 loop/cost가 폭증할 수 있어 max step과 stop condition이 필요합니다.

## 7. ReAct-Style RAG

원문이 설명하는 대표 pattern:

    think → act → observe → repeat

실무에서는 raw chain-of-thought 노출보다:

- tool choice
- search query
- evidence
- state transition

을 trace하는 것이 더 중요합니다.

## 8. Corrective/Self-RAG 방향

고급 pattern은 retrieved evidence 품질을 별도로 평가합니다.

    retrieve
      → grade relevance
        ├─ good → answer
        └─ poor → rewrite/retrieve

즉 retrieval 자체에 verification loop를 넣습니다.

## 9. Standard vs Agentic

| 항목 | Standard RAG | Agentic RAG |
| --- | --- | --- |
| Retrieval 횟수 | 보통 1 | 필요 시 여러 번 |
| Tool | 한 종류 중심 | 여러 source |
| Query rewrite | 고정 | 동적 |
| Evidence 평가 | 제한적 | 명시적 가능 |
| Multi-hop | 약함 | 강함 |
| Latency/cost | 낮음 | 높음 |
| 시스템 복잡도 | 낮음 | 높음 |

## 10. 언제 사용하나

원문 기준과 실무를 합치면:

- research
- legal/medical multi-source investigation
- enterprise data across SQL/vector/web
- ambiguous complex question
- retrieval quality가 latency보다 중요한 경우

FAQ처럼 단순한 query에는 Standard RAG가 더 낫습니다.

## 11. 실패 시나리오

- 같은 검색 반복
- 잘못된 source 선택
- search result hallucinated interpretation
- 너무 일찍 stop
- 끝없는 loop
- tool error propagation

따라서 max steps, budget, validators, citation/evidence checks가 필요합니다.

## 12. Evaluation

단순 answer accuracy 외에도:

- number of retrievals
- tool success rate
- evidence recall
- unnecessary-tool rate
- latency
- cost
- groundedness

를 측정해야 합니다.

## 핵심 정리

- Agentic RAG는 retrieval을 고정 pipeline이 아니라 agent decision loop로 바꿉니다.
- Agent는 retrieval 필요 여부, source, query rewrite, evidence 충분성, stop을 결정합니다.
- 원문은 Agent/Tools/State 세 building block과 ReAct-style loop를 설명합니다.
- Multi-hop·multi-source 문제에서 강하지만 비용과 failure mode가 크게 늘어납니다.
- 단순 query까지 agentic하게 만들지 말고 complexity routing을 두는 것이 실용적입니다.

## 원문

- https://outcomeschool.com/blog/agentic-rag
