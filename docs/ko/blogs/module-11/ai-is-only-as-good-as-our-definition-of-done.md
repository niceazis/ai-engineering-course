# AI의 품질은 Definition of Done의 품질을 넘을 수 없다 — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/ai-is-only-as-good-as-our-definition-of-done  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 원문 본문 캐시를 직접 열지 못했습니다. Outcome School 공식 Module 11의 핵심 문제의식—AI task의 완료 기준을 측정 가능하게 만드는 것—을 기반으로 독립적으로 설명합니다.

## 1. Definition of Done이란?

AI에게 "좋게 해줘"라고 시키는 것과:

    tests pass
    no lint errors
    required fields present
    sources attached

처럼 **기계적으로 판정 가능한 종료 조건**을 주는 것은 완전히 다릅니다.

Definition of Done(DoD)은 "이 task가 완료됐다고 판정하는 규칙"입니다.

## 2. 측정 가능한 Task

예: code bug fix.

좋은 DoD:

- reproduction test가 처음 fail
- fix 후 test pass
- 기존 regression suite pass
- public API unchanged

Agent가 스스로 loop를 돌며 확인할 수 있습니다.

## 3. 모호한 Task

    "보고서를 더 좋게 만들어라"

는 종료 기준이 없습니다.

더 좋은 DoD:

- executive summary 포함
- 수치마다 source
- 5개 required section
- 2,000자 이내
- factual checker pass

Subjective quality를 완전히 objective하게 만들 수는 없어도 평가 rubric을 명확히 할 수 있습니다.

## 4. 왜 AI가 Measure 가능한 영역에서 강한가

Agent loop:

    attempt
      → measure
      → fail reason
      → repair
      → measure again

Feedback signal이 명확할수록 improvement loop가 안정적입니다.

Verifier-based reasoning RL이 강한 이유와 같은 원리입니다.

## 5. DoD와 Prompt의 차이

Prompt:

    무엇을 하라

DoD:

    **언제 성공이라고 인정할 것인가**

Good instruction만 있고 verifier가 없으면 agent가 premature completion을 선언할 수 있습니다.

## 6. 계층적 DoD

큰 task는 여러 수준으로 나눕니다.

### Step-level

각 subtask의 acceptance criteria.

### Artifact-level

파일/보고서/코드 품질.

### End-to-End

사용자의 실제 goal이 달성됐는지.

## 7. Negative Criteria

성공 조건뿐 아니라 금지 조건도 정의합니다.

예:

- source 없는 주장 금지
- destructive action 금지
- TODO 남기지 않음
- secret commit 금지

## 8. Test Pyramid

가능한 verifier 우선순위:

1. deterministic tests
2. schema/rule checks
3. domain model/checker
4. LLM judge
5. human review

Exact checker가 가능한데 LLM judge를 쓰는 것은 불필요한 불확실성을 추가합니다.

## 9. Good DoD 작성법

- observable
- binary 또는 명확한 metric
- user goal과 직접 연결
- 쉽게 game하기 어렵게
- cost/time 내 실행 가능
- regression 포함

## 10. 실패 예

Metric 하나만 주면 AI가 metric을 game할 수 있습니다.

예:

    "test count를 늘려라"

→ 의미 없는 test 생성 가능.

따라서 DoD도 실제 목표를 proxy하는 품질이 중요합니다.

## 핵심 정리

- Definition of Done은 AI loop의 종료/성공 판정 규칙입니다.
- "좋게" 같은 모호한 목표보다 test/schema/rubric으로 관찰 가능하게 만들어야 합니다.
- Measure→repair loop가 가능할수록 agent reliability가 높아집니다.
- Deterministic verifier를 LLM judge보다 우선합니다.
- DoD 자체가 나쁜 proxy이면 agent가 그것을 최적화해도 실제 목표를 달성하지 못합니다.

## 원문

- https://outcomeschool.com/blog/ai-is-only-as-good-as-our-definition-of-done
