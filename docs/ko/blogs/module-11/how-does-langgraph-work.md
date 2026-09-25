# LangGraph는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-langgraph-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 State·Node·Edge·Conditional Edge·Persistence·HITL의 핵심 구조를 독립적으로 설명합니다. 실제 API는 최신 LangGraph 공식 문서를 확인해야 합니다.

## 1. LangGraph의 목적

LLM agent workflow를 **stateful graph**로 표현합니다.

    State
      → Node
      → Edge
      → Node
      → ...

Free-form while loop보다 control flow와 checkpoint를 명시적으로 만들기 쉽습니다.

## 2. State

Graph 전체가 공유하는 structured object입니다.

예:

    {
      messages,
      current_task,
      tool_result,
      attempts
    }

각 node는 state 일부를 읽고 update를 반환합니다.

## 3. Node

실행 함수입니다.

예:

- call_model
- retrieve
- execute_tool
- validate
- human_review

Node를 작게 유지하면 test/debug가 쉬워집니다.

## 4. Edge

Normal edge:

    A → B

Conditional edge:

    validator
      ├─ "pass" → END
      └─ "fail" → repair

LLM의 decision을 router로 사용할 수도 있고 deterministic code를 사용할 수도 있습니다.

## 5. Cycle

Graph는 DAG에 한정되지 않습니다.

    model
      → tool
      → model

처럼 agent loop를 cycle로 표현할 수 있습니다.

Iteration limit은 별도로 두어야 합니다.

## 6. Tool 실행 주체

Model은 tool call을 **요청**합니다.

Tool node/runtime가 실제 function을 실행하고 result를 state/message에 추가합니다.

이 구분이 permission/safety의 핵심입니다.

## 7. Persistence

Checkpoint를 저장하면:

- pause/resume
- crash recovery
- long-running workflow
- conversation thread persistence

를 구현할 수 있습니다.

State를 durable store에 저장하는 것이 LLM memory의 한 형태가 됩니다.

## 8. Human-in-the-Loop

Critical node 전 graph를 interrupt하고 사람의 입력/승인을 기다릴 수 있습니다.

    generate action
      → interrupt
      → human approve/edit
      → resume

Financial/destructive workflow에서 중요합니다.

## 9. LangChain과의 관계

LangChain:

- components/integrations

LangGraph:

- stateful control flow/runtime

라고 이해하면 쉽습니다.

LangChain component를 LangGraph node 안에서 사용할 수 있습니다.

## 10. 언제 Graph가 유용한가

- 여러 branch
- retry/revision
- long-running state
- human approval
- deterministic+agent hybrid
- recoverability/audit 중요

한 번의 단순 prompt에는 과합니다.

## 11. Failure 관리

Error를 state로 명시하면:

    tool_error
      → retry node
      → fallback node
      → human

같은 path를 설계할 수 있습니다.

## 핵심 정리

- LangGraph는 agent workflow를 State·Node·Edge로 표현하는 stateful runtime입니다.
- Conditional edge와 cycle로 agent behavior를 명시적으로 통제할 수 있습니다.
- Checkpoint가 persistence, resume, HITL을 가능하게 합니다.
- Tool은 model이 아니라 runtime/node가 실행합니다.
- 복잡한 workflow에서 free-form loop보다 관찰·복구하기 쉽습니다.

## 원문

- https://outcomeschool.com/blog/how-does-langgraph-work
