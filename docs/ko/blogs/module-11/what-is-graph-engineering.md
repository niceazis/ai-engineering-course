# Graph Engineering이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/what-is-graph-engineering  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 원문 본문 캐시를 직접 열지 못했습니다. Outcome School 공식 Module 11의 Node·Edge·State·Conditional Edge·Cycle·Parallel·Checkpoint·HITL 구조를 기준으로 독립적으로 설명합니다.

## 1. Graph Engineering의 핵심

복잡한 AI workflow를 하나의 거대한 prompt나 자유로운 loop로 두지 않고 **명시적인 node와 edge를 가진 graph**로 설계합니다.

    Graph = Nodes + Edges + State

## 2. Node

작은 실행 단위입니다.

예:

- retrieve
- classify
- generate
- validate
- tool call
- human review

Node는 가능한 한 한 책임만 갖게 합니다.

## 3. State

Node 사이에서 전달되는 structured data입니다.

    {
      goal,
      evidence,
      draft,
      errors,
      retries
    }

Conversation text만 state로 사용하면 분기/복구가 어렵습니다.

## 4. Edge

어떤 node 다음에 어디로 갈지 정의합니다.

Static:

    A → B

Conditional:

    Validate
      ├─ pass → Final
      └─ fail → Repair

## 5. Cycle

Graph도 loop를 포함할 수 있습니다.

    Generate
      → Test
        → Fail
          → Fix
          → Test

차이는 cycle 경로와 상태가 명시적이라는 점입니다.

## 6. Parallel Branch

독립 작업:

    Research A ─┐
    Research B ─┼→ Merge
    Research C ─┘

를 병렬 실행할 수 있습니다.

DAG scheduling으로 dependency를 명확히 합니다.

## 7. Checkpoint

각 node 뒤 state를 저장하면:

- crash recovery
- pause/resume
- human approval
- replay/debug

가 가능합니다.

Long-running agent에서 매우 중요합니다.

## 8. Human in the Loop

Graph에 human node를 넣을 수 있습니다.

    Draft
      → Human Approval
        ├─ approve → Publish
        └─ reject  → Revise

Human interaction이 exception이 아니라 first-class transition이 됩니다.

## 9. Error Edge

Tool error를 일반 success state와 분리합니다.

    Tool
      ├─ success → Parse
      ├─ retryable → Retry
      └─ fatal → Escalate

이 구조가 blind retry보다 안정적입니다.

## 10. Graph vs Loop Engineering

Loop:

- dynamic
- compact
- open-ended exploration에 좋음

Graph:

- explicit flow
- audit/recovery 쉬움
- known business process에 강함

실전에서는 graph node 내부에 bounded loop/agent를 넣을 수 있습니다.

## 11. Best Practice

- node를 작게
- state schema 명시
- edge condition deterministic하게
- checkpoint
- retry limit
- observability
- test each node and path

## 핵심 정리

- Graph Engineering은 AI workflow를 Node·Edge·State로 명시적으로 구조화합니다.
- Conditional edge, cycle, parallel branch, checkpoint, HITL을 first-class로 다룹니다.
- 복잡한 business workflow에서 free-form agent loop보다 audit/recovery가 쉽습니다.
- Graph와 Loop는 경쟁이 아니라 조합 가능합니다.
- 원문 본문 캐시 제한 때문에 구체 수치는 공식 outline에 없는 내용을 임의로 추가하지 않았습니다.

## 원문

- https://outcomeschool.com/blog/what-is-graph-engineering
