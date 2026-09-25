# AI SubAgent란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/ai-subagents  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 parent-agent delegation과 context/tool isolation을 중심으로 독립적으로 설명합니다.

## 1. SubAgent의 정의

SubAgent는 parent agent가 큰 goal을 수행하는 동안 **특정 subtask를 맡기기 위해 생성/호출하는 좁은 agent**입니다.

    Parent Agent
      → delegate Task A → SubAgent A
      → delegate Task B → SubAgent B
      → collect results
      → final integration

## 2. Multi-Agent와 차이

Multi-agent system은 여러 agent가 지속적인 고정 role로 존재할 수 있습니다.

SubAgent pattern은 parent가 필요할 때 **bounded worker를 생성/호출**하고 결과를 돌려받는 delegation이 핵심입니다.

## 3. 필요한 이유

Parent context가 너무 커지는 문제를 줄입니다.

Research subagent는 research 자료만 보고, coding subagent는 repository/code tool만 보는 식으로 context와 permission을 분리할 수 있습니다.

## 4. Delegation Contract

좋은 task handoff:

    objective
    input/evidence
    allowed tools
    constraints
    expected output
    completion criteria

"알아서 조사해"처럼 모호하면 parent가 결과를 쓰기 어렵습니다.

## 5. Example

목표:

    신규 제품 launch report

Parent:

1. market research subagent
2. pricing analysis subagent
3. risk review subagent

각 worker가 structured result를 반환하고 parent가 최종 report를 합칩니다.

## 6. Context Isolation

SubAgent는 parent의 전체 history가 필요하지 않을 수 있습니다.

필요한 state만 전달하면:

- token cost 감소
- distraction 감소
- private data 노출 최소화

할 수 있습니다.

## 7. Tool Isolation

Coding worker:

    GitHub + shell

Research worker:

    web + files

처럼 최소 권한 principle을 적용합니다.

## 8. Parallel SubAgents

독립 subtask는 병렬로 실행합니다.

Dependency가 있으면:

    A → B → C

순서로 orchestrate합니다.

## 9. 결과 Integration

Parent는 worker output을 그대로 concatenate하면 안 됩니다.

검증:

- duplicate
- contradiction
- missing evidence
- format
- confidence

을 수행하고 필요하면 subagent에 revision을 요청합니다.

## 10. 위험

- delegation overhead
- worker hallucination
- inconsistent assumptions
- too many agents
- hidden cost explosion
- parent integration error

Subagent는 decomposition이 명확할 때만 가치가 큽니다.

## 핵심 정리

- SubAgent는 parent가 좁은 subtask를 위임하는 bounded worker입니다.
- Context와 tool permission을 분리하는 효과가 큽니다.
- Delegation contract와 structured return schema가 중요합니다.
- 독립 작업은 병렬화할 수 있습니다.
- Parent는 결과 통합과 검증 책임을 유지해야 합니다.

## 원문

- https://outcomeschool.com/blog/ai-subagents
