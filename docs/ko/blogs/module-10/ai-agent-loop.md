# AI Agent Loop란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/ai-agent-loop  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 Think-Act-Observe, parallel tool call, termination/failure를 중심으로 다시 쓴 상세 학습 노트입니다.

## 1. Agent를 Agent답게 만드는 것

Agent loop는 model을 반복 호출하는 runtime control flow입니다.

    Think/Decide
      → Act
      → Observe
      → Think/Decide
      → ...

LLM 자체는 stateless한 request-response model일 수 있습니다. Loop가 history와 tool result를 누적해 지속적인 task 수행을 만듭니다.

## 2. Think

현재 state를 보고 결정합니다.

- 목표가 끝났는가?
- 어떤 정보가 부족한가?
- 어떤 tool이 필요한가?
- 여러 action을 병렬 실행할 수 있는가?

Production에서는 raw hidden reasoning보다 action decision과 state transition을 기록하는 것이 중요합니다.

## 3. Act

LLM이 고른 tool call을 runtime이 실행합니다.

    web_search
    sql_query
    read_file
    send_email

Action에는 side effect가 있을 수 있으므로 permission boundary가 필요합니다.

## 4. Observe

Tool result를 normalized message로 state에 넣습니다.

좋은 observation은:

- 필요한 field만 포함
- source/provenance
- error 상태
- timestamp/version

를 명확히 합니다.

## 5. 한 Turn의 Parallel Action

서로 독립적인 두 source를 조사한다면 LLM이 한 turn에 두 tool call을 낼 수 있습니다.

Runtime:

    Promise.all / async gather

처럼 병렬 실행하고 두 observation을 한번에 feed back할 수 있습니다.

## 6. 종료 조건

Loop 종료는 최소 다음을 포함해야 합니다.

- goal achieved
- LLM final answer
- max steps
- timeout
- cost/token budget
- unrecoverable tool error
- user cancellation

Model의 "done" 판단 하나만 믿으면 runaway loop가 생길 수 있습니다.

## 7. 상태 Machine으로 보기

Agent loop를 명시적 state machine으로 모델링하면 안정적입니다.

    PLAN
      → TOOL
      → VALIDATE
      → PLAN
      → FINAL

각 transition에 validator를 둘 수 있습니다.

## 8. 흔한 실패

### Infinite Loop

같은 search 반복.

대응: duplicate-action detector, max steps.

### Tool Thrashing

서로 다른 tool을 의미 없이 오감.

대응: tool policy, task state.

### Context Explosion

모든 observation을 raw로 계속 append.

대응: compaction, structured state.

### Premature Stop

근거 부족인데 final answer.

대응: completion checklist, verifier.

## 9. Retry

Tool error가 transient인지 semantic인지 구분합니다.

    timeout → retry 가능
    permission denied → retry 무의미
    invalid argument → repair 후 retry

Blind retry는 side effect를 중복시킬 수 있습니다.

## 핵심 정리

- Agent Loop는 LLM 결정, tool 실행, observation feedback을 반복하는 runtime입니다.
- Think-Act-Observe가 기본 구조입니다.
- 독립 action은 한 turn에서 병렬 실행할 수 있습니다.
- 종료 조건은 model 판단 외에도 step/time/cost budget이 필요합니다.
- Loop 안정성은 duplicate detection, validation, compaction, retry policy에 달려 있습니다.

## 원문

- https://outcomeschool.com/blog/ai-agent-loop
