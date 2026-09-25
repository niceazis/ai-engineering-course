# AI Orchestration이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/ai-orchestration  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 sequential/parallel/conditional/loop/orchestrator-worker pattern을 독립적으로 정리했습니다.

## 1. Orchestration의 정의

AI Orchestration은 여러:

- LLM
- tool
- data source
- step
- agent

를 **정해진 control flow와 정책으로 조율해 하나의 application을 만드는 것**입니다.

Agent와 달리 orchestration은 control flow가 code/graph에 명시적일 수 있습니다.

## 2. Agent vs Orchestration

Agent:

    model이 next action을 동적으로 결정

Orchestration:

    application/runtime이 flow를 명시

실전에서는 둘을 섞습니다.

    deterministic outer workflow
      → bounded agent step

가 안정적입니다.

## 3. Sequential Pattern

    A → B → C

예:

    extract
      → summarize
      → format

Dependency가 명확할 때 사용합니다.

## 4. Parallel Pattern

    A ─┐
    B ─┼→ aggregate
    C ─┘

독립 조사/분석을 동시에 실행해 latency를 줄입니다.

## 5. Conditional Pattern

    classify
      ├─ billing → workflow A
      └─ technical → workflow B

Routing decision은 code rule 또는 model judgment가 할 수 있습니다.

## 6. Loop Pattern

    generate
      → validate
        ├─ pass → done
        └─ fail → repair → validate

Reflection/agent loop의 일반화입니다.

반드시 iteration limit이 필요합니다.

## 7. Orchestrator-Worker

Manager가 task를 분해해 여러 worker에 위임하고 결과를 모읍니다.

Large report, code migration, research에 유용합니다.

## 8. State 관리

Orchestrator는 각 step의:

    input
    output
    status
    retries
    errors
    artifact references

를 관리해야 합니다.

LLM conversation history만 state store로 사용하면 복구와 retry가 어렵습니다.

## 9. Reliability

Production orchestration에 필요한 것:

- idempotency
- checkpoint
- retry policy
- timeout
- fallback
- human approval
- observability

AI call도 distributed workflow의 하나의 unreliable activity로 취급하는 것이 좋습니다.

## 10. Cost Routing

모든 step에 최고 model을 쓸 필요가 없습니다.

    extraction → small model
    hard reasoning → large model
    validation → code/verifier

처럼 task별로 resource를 배치합니다.

## 11. 언제 Agent보다 Orchestration이 낫나

- process가 이미 알려짐
- compliance가 중요
- repeatability 필요
- destructive action
- audit trail

동적 탐색이 필요한 부분만 agent에 맡기는 것이 안전합니다.

## 핵심 정리

- Orchestration은 여러 AI/tool step의 control flow를 설계합니다.
- Sequential, Parallel, Conditional, Loop, Orchestrator-Worker가 대표 pattern입니다.
- Agent는 model-driven dynamic flow, orchestration은 code/graph-driven flow라는 차이가 있습니다.
- Production에서는 deterministic outer flow + bounded agent를 결합하는 방식이 강합니다.
- State, retry, checkpoint, observability가 model prompt만큼 중요합니다.

## 원문

- https://outcomeschool.com/blog/ai-orchestration
