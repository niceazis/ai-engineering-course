# Reflection Agent란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/reflection-agent  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 Generate→Reflect→Revise loop와 ReAct 비교, failure mode를 독립적으로 설명합니다.

## 1. Reflection의 핵심

Reflection Agent는 첫 결과를 바로 final로 내지 않고 **자기 결과를 비평하고 수정하는 loop**를 둡니다.

    Generate
      → Reflect/Critique
      → Revise
      → optional Reflect again
      → Final

## 2. 왜 필요한가

LLM의 첫 draft에는:

- 빠진 요구사항
- 논리 오류
- format 문제
- source mismatch
- code bug

가 있을 수 있습니다.

Second pass에 critique라는 좁은 objective를 주면 이런 오류를 찾을 가능성이 높아집니다.

## 3. 역할 분리

같은 model을 사용해도 prompt role을 분리할 수 있습니다.

### Generator

    최선의 draft를 생성

### Critic

    요구사항/근거/테스트 기준으로 문제점만 찾음

### Reviser

    critic feedback을 반영해 수정

독립 model을 사용하면 error correlation을 줄일 수 있지만 cost가 증가합니다.

## 4. Code 예

    draft = generate(task)
    critique = review(draft, rubric)
    final = revise(draft, critique)

Code task라면 review 대신 실제 test/tool을 넣는 것이 더 강합니다.

    code → unit tests → failures → repair

## 5. Reflection과 Verification

Self-critique만으로 correctness가 보장되지는 않습니다.

강한 hierarchy:

1. deterministic test
2. source/evidence check
3. second model judge
4. self-reflection

가능하면 외부 verifier를 우선합니다.

## 6. ReAct와 차이

ReAct:

    외부 world에서 무엇을 할지 반복

Reflection:

    이미 만든 결과의 품질을 반복 개선

둘을 결합할 수 있습니다.

    ReAct research
      → draft
      → reflection
      → missing evidence 발견
      → ReAct 추가 검색
      → final

## 7. 종료 조건

Reflection을 무한 반복하면 문장이 계속 바뀌면서 오히려 품질이 나빠질 수 있습니다.

종료 기준:

- max revisions
- rubric pass
- tests pass
- no critical issue
- improvement score threshold

## 8. Failure Mode

### Echo Critique

Critic이 실제 검증 없이 "좋다"고 동의.

대응: concrete rubric.

### New Bugs

Revision이 기존 맞는 부분을 깨뜨림.

대응: regression test.

### Style Churn

내용은 같고 표현만 계속 변경.

대응: semantic stop condition.

### Confirmation Bias

같은 model이 자기 오류를 못 봄.

대응: external tool/model.

## 9. 잘 맞는 Task

- code generation
- report/proposal
- source-grounded answer
- complex structured output
- high-quality writing

단순 factual query에는 추가 cost가 불필요할 수 있습니다.

## 핵심 정리

- Reflection Agent는 Generate→Critique→Revise loop입니다.
- 첫 draft 품질을 올리는 데 유용하지만 self-review 자체가 truth guarantee는 아닙니다.
- Code/test/source checker 같은 external verifier와 결합하면 훨씬 강합니다.
- max revision과 pass criteria가 필요합니다.
- ReAct가 행동 loop라면 Reflection은 quality-improvement loop입니다.

## 원문

- https://outcomeschool.com/blog/reflection-agent
