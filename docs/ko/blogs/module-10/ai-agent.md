# AI Agent란? 어떻게 동작하는가 — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/ai-agent  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-04-27 공개 원문을 직접 확인해 다섯 핵심 구성 요소, Research Agent와 loop 구조를 반영한 독립적인 한국어 학습 노트입니다.

## 1. AI Agent의 정의

원문의 핵심 식:

    AI Agent
      = LLM
      + Instructions
      + Tools
      + Memory
      + Loop

Plain LLM이 한 번 응답하고 멈춘다면 Agent는 목표가 끝날 때까지 **결정→행동→관찰**을 반복합니다.

## 2. Plain LLM, Chatbot, Agent

- Plain LLM: one request → one response
- Chatbot: 대화 history를 포함해 여러 turn
- Agent: tool을 사용하고 loop를 돌며 실제 상태를 바꿈

Agent의 본질은 UI가 아니라 **tool use + iterative runtime**입니다.

## 3. 다섯 Core Part

### LLM — Brain

현재 state를 읽고 다음 action 또는 final answer를 선택합니다.

### Instructions

역할, 규칙, tool policy, 완료 조건을 정의합니다.

### Tools — Hands

검색, 파일 읽기, API, DB, 코드 실행, 이메일 등 외부 action.

### Memory

- short-term: 현재 run의 message/tool trace
- long-term: run 사이에 유지할 user/project state

### Loop — Runtime

LLM 요청 → tool 실행 → observation 추가 → 다시 LLM을 반복합니다.

## 4. 중요한 구분: Model이 Tool을 직접 실행하지 않는다

Function-calling model은 보통:

    tool_name + arguments

를 구조화해서 제안합니다.

실제 실행은 host runtime이 수행합니다.

따라서 permission, timeout, retry, confirmation 같은 안전 제어는 runtime 책임입니다.

## 5. End-to-End

    goal
      → assemble context
      → LLM decision
         ├─ final → stop
         └─ tool call
              → runtime executes
              → observation
              → state update
              → LLM again

Loop가 없으면 tool-using chatbot 한 turn일 수 있지만 장기 task 수행 agent로 발전하기 어렵습니다.

## 6. 원문의 Flight 예

사용자 목표:

    내일 Delhi행 직항 중 8,000 rupees 이하
    가장 싼 3개를 찾아라

Agent는:

1. flight search tool
2. 결과 관찰
3. 직항/가격 filter
4. top 3 선택
5. final answer

을 반복할 수 있습니다.

원문은 현대 LLM이 한 turn에 여러 tool call을 출력하고 runtime이 병렬 실행할 수도 있다고 설명합니다.

## 7. Research Agent

원문 노트북 조사 예에서는:

- web search
- page reader
- calculator

를 사용해 후보를 조사하고 가격/spec/review를 비교합니다.

중요한 점은 workflow가 완전히 hard-code된 것이 아니라 **LLM이 현재 observation을 보고 다음 조사 행동을 정한다**는 것입니다.

## 8. Step Limit

Agent loop에는 반드시:

    max_steps
    timeout
    token/cost budget

같은 종료 장치가 필요합니다.

잘못된 tool result나 ambiguous goal 때문에 무한 loop에 빠질 수 있기 때문입니다.

## 9. Failure Mode

- wrong tool selection
- malformed arguments
- stale/incorrect observation
- repeated same action
- premature finish
- permission overreach
- context growth
- hallucinated completion

Agent quality는 model quality뿐 아니라 harness/runtime quality에 크게 좌우됩니다.

## 10. 언제 Agent를 쓰나

좋음:

- 여러 단계가 필요
- tool interaction
- 결과에 따라 다음 step이 바뀜

불필요:

- 한 번의 deterministic API call
- 단순 transformation
- fixed pipeline으로 충분

## 핵심 정리

- Agent는 LLM 하나가 아니라 LLM+Instructions+Tools+Memory+Loop인 시스템입니다.
- Model은 action을 결정하고 runtime이 실제 tool을 실행합니다.
- Tool observation이 다음 LLM call의 state가 됩니다.
- max steps·permission·validation이 production agent의 핵심입니다.
- 단순 workflow에는 agent를 쓰지 않는 것이 더 안정적일 수 있습니다.

## 원문

- https://outcomeschool.com/blog/ai-agent
