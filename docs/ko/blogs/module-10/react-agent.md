# ReAct Agent란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/react-agent  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 Reasoning+Acting 구조와 trace, failure 대응을 독립적으로 정리했습니다.

## 1. ReAct의 뜻

ReAct:

    Reason + Act

문제를 내부적으로 판단하고 external tool/action을 실행한 뒤 observation을 받아 다음 행동을 정하는 pattern입니다.

    reasoning state
      → action
      → observation
      → next reasoning state

## 2. 일반 Agent와 관계

모든 agent가 ReAct 형식을 그대로 쓰는 것은 아닙니다.

ReAct는 **매 step에서 reasoning과 action을 교차**시키는 구체적인 orchestration pattern입니다.

Plan-and-Execute는 먼저 전체 plan을 만드는 점에서 다릅니다.

## 3. 예시

목표:

    "2026년 어떤 회사 CEO의 최근 발표를 확인해 요약"

Trace:

1. 최신 정보가 필요하다고 판단
2. web search
3. observation으로 기사 목록
4. 신뢰할 source 선택
5. page read
6. evidence 확인
7. final summary

Observation에 따라 next action이 달라집니다.

## 4. Tool Contract

ReAct에서 tool description이 중요합니다.

Model은:

- tool name
- description
- arguments
- returned observation

만 보고 다음 action을 정합니다.

Tool이 너무 많거나 설명이 겹치면 selection accuracy가 떨어집니다.

## 5. Prompt Template의 역할

고전 ReAct 논문은 Thought/Action/Observation 형식을 사용했습니다.

현대 function-calling model에서는 자유로운 문자열 parser 대신 native tool call을 사용해 같은 구조를 더 안정적으로 구현할 수 있습니다.

즉 ReAct의 본질은 label 문자열이 아니라 **interleaved reasoning-action loop**입니다.

## 6. Search Agent 예

    goal
      → search broad
      → observe
      → search specific
      → observe
      → read source
      → verify
      → final

첫 검색 결과가 충분하면 빨리 종료하고, 부족하면 반복합니다.

## 7. Failure: Hallucinated Tool

모델이 존재하지 않는 action을 말할 수 있습니다.

Native tool schema와 enum validation으로 방지합니다.

## 8. Failure: Observation Ignoring

Tool result가 "없음"인데 모델이 이전 가정을 계속 밀 수 있습니다.

대응:

- observation를 structured
- contradiction checker
- evidence-required completion rule

## 9. Failure: Loop

같은 query 반복.

대응:

    history of actions
    duplicate detector
    max_steps

## 10. ReAct vs Plan-and-Execute

ReAct:

- 다음 한 step만 정함
- 변화에 민첩
- 긴 task에서 local wandering 가능

Plan-and-Execute:

- upfront plan
- global structure 좋음
- plan이 틀리면 replanning 필요

Hybrid가 흔합니다.

## 핵심 정리

- ReAct는 reasoning과 external action을 번갈아 수행하는 agent pattern입니다.
- Tool observation이 다음 decision의 입력입니다.
- 현대 구현은 native function calling을 쓰는 편이 안정적입니다.
- Dynamic research/troubleshooting에 강하지만 loop와 tool misuse를 관리해야 합니다.
- Long structured task는 plan-execute와 혼합할 수 있습니다.

## 원문

- https://outcomeschool.com/blog/react-agent
