# Multi-Agent System이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/multi-agent-systems  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 role specialization, communication, coordination과 single-agent trade-off를 중심으로 독립적으로 설명합니다.

## 1. 정의

Multi-Agent System(MAS)은 하나의 큰 agent가 모든 일을 하는 대신 **서로 다른 역할을 가진 여러 agent가 협력**해 목표를 수행하는 구조입니다.

예:

    Manager
      ├─ Researcher
      ├─ Coder
      └─ Reviewer

## 2. 세 Pillar

### Specialization

각 agent가 좁은 role/tool/context를 가짐.

### Communication

결과와 요청을 message로 주고받음.

### Coordination

누가 언제 무엇을 할지 orchestrator/protocol이 제어.

여러 model을 단순히 동시에 부른다고 MAS가 되는 것은 아닙니다.

## 3. 왜 분리하나

장점:

- context 분리
- tool permission 분리
- model specialization
- parallel execution
- independent review

한 agent에 모든 tool/context를 넣을 때 생기는 confusion을 줄일 수 있습니다.

## 4. 대표 Role

- planner/manager
- researcher
- coder
- data analyst
- verifier/reviewer
- domain specialist

Role은 task에 따라 설계합니다.

## 5. Communication

Agent 간 message에는 최소:

    task
    relevant state
    expected output schema
    source/evidence
    status/error

가 필요합니다.

Raw conversation 전체를 매번 공유하면 context cost가 폭증합니다.

## 6. Coordination Pattern

### Centralized

Manager가 worker에게 task를 할당.

장점: 통제/observability.

### Peer-to-Peer

Agent끼리 직접 message.

유연하지만 loop/conflict 관리 어려움.

### Blackboard/Shared State

공유 store를 읽고 씀.

Large project에서 durable state에 유리합니다.

## 7. Parallelism

독립 subtask:

    Research market
    Analyze code
    Check policy

를 parallel worker에게 맡기면 wall-clock time을 줄일 수 있습니다.

Dependency가 있으면 DAG로 실행 순서를 관리합니다.

## 8. Consensus

여러 agent가 독립 answer를 만든 뒤:

- majority
- judge
- evidence aggregation

으로 결합할 수 있습니다.

그러나 같은 base model이면 error가 correlated될 수 있습니다.

## 9. Single vs Multi

Single agent가 더 나은 경우:

- task 짧음
- tool 수 적음
- state 공유가 중요
- latency/cost 민감

Multi-agent가 유리:

- clear specialization
- parallel work
- separate permissions
- independent verification

## 10. 실패 Mode

- message ping-pong
- duplicate work
- inconsistent state
- role overlap
- manager bottleneck
- cost explosion
- no clear owner of final decision

Agent 수가 많다고 capability가 자동 증가하지 않습니다.

## 11. 평가

Agent별:

- task success
- tool-call efficiency

System:

- end-to-end quality
- latency
- cost
- coordination overhead
- duplicate work rate

를 따로 측정합니다.

## 핵심 정리

- MAS는 specialization·communication·coordination이 있는 agent team입니다.
- Central manager, peer-to-peer, shared-state 같은 topology가 있습니다.
- Parallelism과 permission separation이 주요 장점입니다.
- Coordination overhead 때문에 작은 task에는 single agent가 더 낫습니다.
- Role boundary와 structured message contract가 성패를 좌우합니다.

## 원문

- https://outcomeschool.com/blog/multi-agent-systems
