# Plan-and-Execute Agent란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/plan-and-execute-agent  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 planner/executor 구조, replanning과 ReAct 비교를 독립적으로 정리했습니다.

## 1. 정의

Plan-and-Execute Agent는 복잡한 목표를 받으면 먼저 **전체 작업 계획을 만든 뒤 각 step을 실행**하는 pattern입니다.

    Goal
      → Planner
      → [Step1, Step2, Step3, ...]
      → Executor
      → observations/results
      → optional Replan
      → Final

## 2. 왜 Planning이 필요한가

ReAct처럼 매 순간 다음 한 step만 고르면 local optimum에 빠질 수 있습니다.

예:

    "경쟁사 5개 조사 → 가격 비교 → 리스크 분석 → 보고서"

같은 task는 처음부터 필요한 subtask와 dependency를 구조화하면 누락을 줄일 수 있습니다.

## 3. Planner

Planner는 goal을 실행 가능한 step으로 분해합니다.

좋은 plan:

- step이 너무 크지 않음
- dependency가 명확
- tool로 실행 가능
- 완료 조건이 있음

나쁜 plan:

    "조사한다"
    "잘 분석한다"

처럼 검증 불가능한 모호한 step입니다.

## 4. Executor

Executor는 plan의 현재 step만 집중합니다.

예:

    Step 2: 공식 가격 페이지에서 세 제품 가격 수집

필요한 tool만 사용하고 structured result를 반환합니다.

Planner와 Executor를 같은 model로 구현할 수도 있고 서로 다른 model을 사용할 수도 있습니다.

## 5. Full Trace 예

목표:

    "서울 출장 비용 계획을 만들어라"

Plan:

1. 항공/철도 옵션 찾기
2. 호텔 후보 수집
3. 교통비 추정
4. 합계 계산
5. 예산 조건 검증

Execution 중 호텔이 매진이면 plan을 업데이트할 수 있습니다.

## 6. Replanning

실제 환경은 plan과 다를 수 있습니다.

    step result = failure / new information

이면:

    current plan
      + observation
      → planner
      → revised plan

Replanning이 없으면 처음 계획의 잘못을 끝까지 따라갈 수 있습니다.

## 7. ReAct와 비교

| 항목 | ReAct | Plan-and-Execute |
| --- | --- | --- |
| 계획 범위 | 다음 action | 전체/큰 단계 |
| 적응 | 즉각적 | replan 필요 |
| 장기 구조 | 약할 수 있음 | 강함 |
| overhead | 낮음 | planner call 추가 |
| 적합 | 탐색적 task | 구조적 multi-step task |

Hybrid:

    plan
      → 각 step 내부 ReAct
      → replan

이 실용적입니다.

## 8. Failure Mode

### Bad Initial Plan

대응: early validation, replan.

### Overplanning

작은 task를 지나치게 세분화하면 latency가 증가합니다.

### Stale Plan

환경이 바뀌었는데 plan을 고정.

### Completion Illusion

Step text만 완료 처리하고 실제 evidence가 없음.

대응: step별 acceptance criteria.

## 9. Plan State

문자열 checklist보다 structured state가 좋습니다.

    {
      "step": 3,
      "status": "running",
      "dependencies": [1,2],
      "evidence": [...]
    }

Resume/retry/observability가 쉬워집니다.

## 핵심 정리

- Plan-and-Execute는 먼저 전체 plan을 만들고 step별로 실행합니다.
- 긴 dependency task에서 ReAct보다 global structure가 좋습니다.
- 현실과 plan이 달라지므로 replanning이 핵심입니다.
- 각 step에는 실행 가능한 scope와 완료 기준이 필요합니다.
- 실전에서는 plan → step별 ReAct → replan hybrid가 유용합니다.

## 원문

- https://outcomeschool.com/blog/plan-and-execute-agent
