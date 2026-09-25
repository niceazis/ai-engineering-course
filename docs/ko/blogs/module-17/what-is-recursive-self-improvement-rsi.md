# Recursive Self-Improvement(RSI)이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/what-is-recursive-self-improvement-rsi  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문 URL은 현재 직접 열리지 않았습니다. Outcome School 공식 홈페이지의 2026-09-15 게시 설명과 공식 AI Engineering course/roadmap의 레슨 구조를 확인해 독립적으로 재구성했습니다. 현재 공개적으로 검증된 좁은 self-improvement 사례와 완전 자율적 RSI를 구분하며, 직접 확인하지 못한 원문 고유 수치는 사용하지 않습니다.

## 1. RSI란?

Recursive Self-Improvement는 AI system이 자신 또는 자신을 개선하는 process를 개선하고, 그 결과 더 강해진 system이 다음 improvement를 더 잘 수행하는 반복 loop입니다.

개념:

    System v1
      → improvement process
      → System v2

    System v2
      → better improvement process
      → System v3

    repeat

"Recursive"의 핵심은 **개선된 결과가 다음 개선 loop의 능력 자체를 높인다**는 점입니다.

## 2. 단순 Self-Reflection과의 차이

한 answer를 다시 고치는 것은 RSI라고 보기 어렵습니다.

예:

    draft
      → critique
      → revised answer

이 개선은 session 안에서 끝나고 다음 task의 system capability가 영구적으로 달라지지 않을 수 있습니다.

RSI에 가까우려면 accepted improvement가 future loop에 persistent하게 반영돼야 합니다.

## 3. 오늘날 AI가 개선되는 일반 방식

대부분의 AI improvement는 사람이 loop를 설계합니다.

    researchers
      → collect data
      → train
      → evaluate
      → inspect failures
      → change model/system
      → train again

AI가 code 작성이나 experiment를 돕더라도:

- 목표
- acceptance criteria
- deployment decision

은 사람이 통제하는 경우가 많습니다.

## 4. RSI Loop

교육적으로는 다음 단계로 볼 수 있습니다.

1. 현재 system 평가
2. 약점 발견
3. improvement hypothesis 생성
4. code/prompt/data/tool/workflow 수정
5. evaluation 실행
6. baseline과 비교
7. 더 좋은 version만 promote
8. 개선된 system이 다음 round 수행

이 loop가 자동화될수록 self-improvement autonomy가 커집니다.

## 5. 간단한 수치 예

가상의 coding agent:

    v1 pass rate = 60%

Agent가:

- better prompt
- new test strategy
- improved tool policy

를 제안하고 eval을 통과해:

    v2 = 68%

이 됩니다.

v2가 다시 improvement search를 더 잘해:

    v3 = 74%

가 된다면 recursive feedback의 직관을 보여 줍니다.

이 숫자는 학습용 예시이며 Outcome School 원문 수치로 확인된 것은 아닙니다.

## 6. 두 종류의 Improvement

### Object-Level Improvement

System 자체를 개선합니다.

예:

- prompt
- model code
- retrieval
- tool workflow
- training data

### Meta-Level Improvement

"어떻게 개선할지"의 process를 개선합니다.

예:

- better experiment selection
- better evaluator
- better search strategy
- better failure analysis

진정한 recursion은 meta-level까지 영향을 미칠 때 더 강해집니다.

## 7. 현재 현실에 가까운 형태

오늘날 실제로 가능한 좁은 형태:

- coding agent가 자기 code 수정
- automated prompt optimization
- model-generated synthetic data
- AI가 inference/training code 최적화
- agent skill/workflow mutation + eval
- automated experiment search

하지만 대부분:

- bounded environment
- fixed objective
- external verifier
- human oversight

안에서 동작합니다.

## 8. 완전한 RSI는 검증되지 않음

다음 형태:

> AI가 독립적으로 자기 architecture, training process, objectives까지 계속 재설계하며 open-ended하게 더 강한 successor를 만드는 system

은 현재 검증된 일반 기술로 볼 수 없습니다.

Outcome School 공식 소개도 "idea"와 현재 존재하는 부분적 형태를 구분하는 구조입니다.

## 9. Intelligence Explosion

RSI 논의에서 자주 나오는 가설:

    capability ↑
      → improvement ability ↑
      → 더 빠른 capability improvement
      → ...

이 positive feedback이 매우 빨라질 수 있다는 생각이 intelligence explosion입니다.

하지만 실제로는 bottleneck이 존재할 수 있습니다.

## 10. Bottleneck

- compute
- training data
- experiment time
- hardware fabrication
- environment feedback
- verifier quality
- objective misspecification
- scientific uncertainty

Improvement ability가 증가해도 물리적·정보적 bottleneck 때문에 속도가 무한히 증가하는 것은 아닙니다.

## 11. 어디서 잘 작동하는가

RSI-style loop는 success signal이 명확한 domain에서 강합니다.

예:

- code test pass
- runtime benchmark
- mathematical verifier
- benchmark score
- latency/cost metric

왜냐하면 candidate improvement를 자동으로 비교할 수 있기 때문입니다.

## 12. 어디서 실패하기 쉬운가

- subjective quality
- long-term social outcome
- sparse feedback
- easy-to-game metric
- unsafe experimentation

Verifier가 나쁜 proxy면 system은 실제 목표가 아니라 metric을 최적화합니다.

## 13. Human-in-the-Loop

강한 self-improvement loop일수록 다음 boundary가 중요합니다.

- objective approval
- evaluator design
- deployment gate
- rollback
- security review
- compute budget
- audit log

특히 system이 evaluator까지 수정할 수 있다면 "시험을 잘 보는 대신 시험지를 바꾸는" failure를 막아야 합니다.

## 14. RSI vs Normal Training

| 항목 | Normal Training | RSI-style Loop |
| --- | --- | --- |
| Improvement design | 주로 human | AI 참여 증가 |
| Evaluation | human-designed | 자동 evaluator 활용 |
| Persistence | checkpoint update | successor가 다음 loop 수행 |
| Meta-improvement | 제한적 | 핵심 가능성 |
| Autonomy | 낮음~중간 | 범위에 따라 높음 |

## 15. 가장 중요한 구분

다음 세 개를 혼동하지 않아야 합니다.

1. AI가 더 좋은 output을 만드는 것
2. AI가 AI 연구/개발을 돕는 것
3. AI가 자신을 개선하는 process까지 지속적으로 개선하는 RSI

현재는 1과 2가 널리 존재하지만 3의 완전 자율적 open-ended 형태는 검증되지 않았습니다.

## 핵심 정리

- RSI는 개선된 system이 다음 self-improvement loop를 더 잘 수행하는 recursive feedback 구조입니다.
- 단순 self-reflection이나 한 번의 fine-tuning과는 다릅니다.
- 오늘날에는 code, prompt, workflow, synthetic data 등 bounded self-improvement가 존재합니다.
- 완전 자율적 open-ended RSI는 현재 검증된 현실로 단정할 수 없습니다.
- 성공 여부는 objective와 verifier quality, persistent change, human oversight에 크게 좌우됩니다.

## 원문

- https://outcomeschool.com/blog/what-is-recursive-self-improvement-rsi
