# AI Agent는 어떻게 통신하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-ai-agents-communicate  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 direct/centralized/broadcast/shared-memory communication과 message contract를 독립적으로 정리했습니다.

## 1. Agent Communication이 필요한 이유

Multi-agent system에서는 각 agent가 가진:

- goal
- evidence
- tool result
- progress
- error

를 다른 agent에게 전달해야 합니다.

통신이 없으면 specialization의 이점을 합칠 수 없습니다.

## 2. Message의 기본 요소

좋은 agent message:

    sender
    receiver
    task / intent
    payload
    context/provenance
    expected response
    correlation/task id
    timestamp/status

Free-form chat만으로 전달하면 중요한 field가 누락될 수 있어 structured schema가 유리합니다.

## 3. Direct Communication

Agent A가 Agent B에 직접 보냅니다.

    A → B

장점:

- 빠르고 단순
- 작은 team에 적합

단점:

- agent 수가 커지면 connection 복잡도 증가
- 전체 workflow observability 어려움

## 4. Centralized Communication

모든 message가 coordinator/orchestrator를 통합니다.

    Worker A → Manager → Worker B

장점:

- routing/control
- permission
- logging
- global state

단점:

- manager bottleneck
- single point of failure

## 5. Broadcast

한 agent의 message를 여러 subscriber에 보냅니다.

예:

    "dataset refreshed"

를 analyst/researcher/reviewer가 모두 받음.

Event-driven agent system과 잘 맞지만 불필요한 message가 많아질 수 있습니다.

## 6. Shared Memory / Blackboard

Agent가 같은 shared store를 읽고 씁니다.

    Agent A → shared state
    Agent B ← shared state

장점:

- 비동기 collaboration
- large artifact 저장

단점:

- race condition
- stale state
- overwrite conflict

version/locking semantics가 필요합니다.

## 7. Synchronous vs Asynchronous

Synchronous:

    request → wait response

단순하지만 slow worker가 전체 latency를 묶습니다.

Async:

    enqueue task
      → worker processes
      → result event

long-running agent에 유리하지만 task tracking이 복잡합니다.

## 8. Message Format

JSON/schema를 사용하면:

- validation
- routing
- retry
- audit

가 쉬워집니다.

Natural-language payload 안에서도 critical state는 separate fields로 두는 것이 좋습니다.

## 9. Protocol

Communication protocol에는 다음을 정의해야 합니다.

- request/response semantics
- timeout
- retry
- idempotency
- error format
- cancellation
- authentication

"agent끼리 말하게 한다"보다 **distributed-system contract**가 핵심입니다.

## 10. Best Practice

- 최소 정보만 전달
- source/provenance 포함
- task ID 유지
- output schema 명시
- shared mutable state 최소화
- retries idempotent
- end-to-end trace 수집

## 핵심 정리

- Agent communication은 multi-agent 협력의 data/control plane입니다.
- Direct, centralized, broadcast, shared-memory 방식이 대표적입니다.
- Structured message contract와 task correlation이 중요합니다.
- Async communication은 scale에 유리하지만 state/retry가 복잡합니다.
- 실제 문제는 LLM 대화보다 distributed-system semantics에 가깝습니다.

## 원문

- https://outcomeschool.com/blog/how-ai-agents-communicate
