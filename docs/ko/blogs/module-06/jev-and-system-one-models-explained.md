# Jev와 System One Model — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/jev-and-system-one-models-explained  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School의 2026-09-17 소개와 TypeSafe의 2026-09-15 공식 Jev 발표, 현재 TypeSafe System One 문서를 교차검증해 독립적으로 다시 쓴 한국어 상세 해설입니다. TypeSafe 문서가 현재 API·개념의 source of truth이므로, Outcome School의 표현과 현재 공식 용어가 다를 때는 현재 TypeSafe 용어를 우선합니다.

## 1. System One Model이란?

TypeSafe가 말하는 System One Model은 일반적인 chat LLM처럼 자유로운 문자열을 생성하는 대신, **소프트웨어가 즉시 사용할 수 있는 제한된 형태의 판단과 확률을 반환하도록 설계된 모델**입니다.

핵심 interface:

    unstructured / structured state
      → System One model
      → typed decision + probability/confidence

Jev는 TypeSafe가 공개한 첫 System One Model입니다.

## 2. System One vs System Two라는 이름

이 이름은 Daniel Kahneman의 *Thinking, Fast and Slow*에서 빌려온 비유입니다.

- System 1: 빠르고 직관적인 판단
- System 2: 느리고 숙고하는 추론

TypeSafe는 이 구분을 model interface에 적용합니다.

### Jev

- 빠른 판단
- 제한된 typed output
- 확률과 confidence
- 여러 질문을 한 request에서 병렬 판단

### Reasoning LLM

- 긴 chain of thought / reasoning
- 자유로운 text generation
- 복잡한 planning, math, code에 적합
- latency와 cost가 큼

이는 "작은 모델 vs 큰 모델" 구분이 아니라 **문제가 요구하는 출력 형태와 계산 방식의 구분**입니다.

## 3. 작은 판단에 일반 LLM을 쓰면 생기는 문제

예를 들어 customer-support request에서 다음 세 가지를 판단한다고 합시다.

1. 긴급한가?
2. 어떤 category인가?
3. human review가 필요한가?

일반 LLM은 보통 다음처럼 prompt를 작성합니다.

    JSON으로 답해라.
    urgency는 low|medium|high 중 하나.
    category는 billing|technical|account 중 하나.
    needs_review는 true|false.

하지만 여전히 다음 문제가 남습니다.

- JSON syntax 오류 가능
- 허용하지 않은 label 생성 가능
- explanation이 섞일 가능성
- confidence가 calibration되지 않을 수 있음
- 여러 독립 판단을 긴 autoregressive string으로 순차 생성

TypeSafe가 해결하려는 문제는 바로 이 "LLM을 억지로 함수처럼 쓰는 friction"입니다.

## 4. Jev의 기본 programming model

TypeSafe에서 application code는 다음을 명시합니다.

- **state**: 판단에 필요한 현재 정보
- **questions**: 어떤 판단이 필요한지
- **criteria / options**: 허용되는 답의 의미
- **code**: 결과를 어떻게 조합하고 행동할지

Model은 workflow 전체를 자유롭게 실행하지 않습니다.

Code가 control flow를 소유하고, Jev는 semantic judgment가 필요한 작은 지점에 들어갑니다.

## 5. 세 가지 핵심 Primitive

현재 TypeSafe의 핵심 primitive는 Choice, Noul, Score입니다.

### Choice

정해진 option 중 하나를 고릅니다.

예:

    ["billing", "technical", "account", "other"]

출력은 단일 label뿐 아니라 각 option에 대한 probability distribution과 confidence를 포함할 수 있습니다.

### Noul

Yes/No 판단입니다.

예:

    "이 ticket은 보안 사고인가?"

출력은 yes의 probability로 이해할 수 있습니다.

중요한 점은 0.5가 "중간 정도로 사고"라는 뜻이 아니라 **yes/no가 거의 비슷하게 가능하다는 불확실성**이라는 점입니다.

### Score

정의된 ordered scale에서 정도를 판단합니다.

예:

    0 = harmless
    1 = low risk
    2 = medium risk
    3 = high risk
    4 = critical

각 level의 probability distribution에서 기대 위치를 score로 계산할 수 있습니다.

## 6. Typed Output의 의미

일반 LLM output:

    "This seems like a billing issue, probably medium urgency."

Jev-style output:

    category = billing
    urgency_score = 0.63
    needs_review_probability = 0.18

실제 schema와 field는 API에 따라 달라질 수 있지만 중요한 차이는 **허용되는 output space가 사전에 정의되어 있다는 것**입니다.

Code는 자연어 parser를 다시 돌릴 필요 없이 결과를 바로 branch에 사용할 수 있습니다.

## 7. "Hallucination이 없다"는 표현의 정확한 의미

Outcome School과 TypeSafe 공식 발표는 Jev가 hallucination할 수 없다고 강하게 표현합니다.

이를 정확히 해석해야 합니다.

### 구조적 의미에서는 맞다

Schema가 허용한 option 밖의 문자열을 새로 생성하지 않으므로:

- 존재하지 않는 tool 이름 생성
- 허용하지 않은 enum label
- 깨진 JSON field
- 자유로운 fabricated text

같은 **string-generation hallucination / type violation**은 구조적으로 제거할 수 있습니다.

### 그러나 판단이 항상 옳다는 뜻은 아니다

Jev도 semantic judgment를 틀릴 수 있습니다.

예:

    실제 category = billing
    Jev choice = account

처럼 **허용된 type 안에서 잘못된 판단**은 가능합니다.

따라서 type safety ≠ truth guarantee입니다.

이 구분이 production automation에서 가장 중요합니다.

## 8. Calibration

Jev의 핵심 목표 중 하나는 probability를 "정직하게" 만드는 것입니다.

잘 calibration된 model이라면:

    confidence ≈ 0.9

인 판단을 많이 모았을 때 실제 accuracy도 약 90% 수준에 가까워지는 것이 목표입니다.

그렇게 되면 code가 threshold를 사용할 수 있습니다.

예:

    if p > 0.98:
        auto_approve()
    elif p > 0.80:
        queue_for_light_review()
    else:
        escalate_to_human()

Confidence는 단순 decoration이 아니라 **automation policy의 입력값**이 됩니다.

## 9. RLCD

TypeSafe는 training 방법을 **Reinforcement Learning for Calibrated Decisions(RLCD)**라고 부릅니다.

기존 RLHF/RLVR과 대비하면:

- RLHF: 사람이 선호하는 응답을 최적화
- RLVR: 자동 검증 가능한 정답/reward를 최적화
- RLCD: typed decision의 correctness와 calibrated probability를 최적화

즉 "그럴듯한 설명문"보다 **software가 신뢰 가능한 판단 분포**가 목적입니다.

## 10. Parallel Sampling

Autoregressive LLM은 output token을 하나씩 생성합니다.

    token1 → token2 → token3 → ...

System One model은 여러 independent question의 결과를 한 request에서 병렬로 계산하도록 설계됩니다.

예:

    state = ticket + account + history

    questions:
      - category?
      - urgency?
      - refund eligibility?
      - abuse?
      - human review?

각 질문은 서로의 answer를 기다리지 않고 동일 state에서 독립적으로 판단할 수 있습니다.

TypeSafe 문서는 **독립 질문을 한 번에 묻는 것**을 권장합니다.

## 11. 언제 질문을 분리해야 하는가

모든 판단을 한 거대한 Choice로 합치면 안 됩니다.

예:

    "긴급 billing ticket이고 refund 가능하며 fraud는 아님"

같은 composite label은 option 수가 폭발하고 재사용성이 떨어집니다.

더 좋은 decomposition:

    category: Choice
    urgency: Score
    refund_eligible: Noul
    fraud_suspected: Noul

Code가 이 결과를 조합합니다.

## 12. Speculative Fan-Out

어떤 branch가 선택될지 아직 모르더라도 독립적으로 계산 가능한 질문은 미리 같은 request에 넣을 수 있습니다.

예:

    route = Choice(...)
    billing_priority = Score(... assuming route=billing)
    technical_severity = Score(... assuming route=technical)

각 speculative question은 전제를 명시하고, code는 실제 route에 해당하는 answer만 사용합니다.

이는 latency를 줄이는 대신 불필요한 question token 비용이 생길 수 있으므로 측정해야 합니다.

## 13. Jev vs LLM

| 관점 | Jev / System One | 일반 LLM |
| --- | --- | --- |
| 주 출력 | typed decision | free-form string |
| 생성 방식 | 병렬 판단 중심 | autoregressive token generation |
| Confidence | calibrated probability가 핵심 | 별도 prompt 시 일관성 낮을 수 있음 |
| Type error | schema 밖 output 방지 | parser/validator 필요 |
| 강점 | routing, scoring, verification, automation | writing, coding, complex reasoning |
| 약점 | open-ended generation 불가 | latency, cost, hallucinated strings |
| Control flow | code가 소유 | model에 더 많이 위임 가능 |

## 14. Jev가 잘 맞는 작업

TypeSafe 공식 use-case map과 Outcome School 설명을 연결하면:

- routing
- classification
- triage
- relevance 판단
- candidate 선택
- risk scoring
- citation/claim verification
- extraction candidate 선택
- agent trace 평가
- guardrail
- real-time game/UX 판단

공통점은 **가능한 행동/값이 미리 정의되고, semantic common sense가 필요한 경우**입니다.

## 15. 잘 맞지 않는 작업

Jev만으로 해결하기 어려운 경우:

- 긴 보고서 작성
- 자유로운 code generation
- 창작 글
- 복잡한 수학 proof
- multi-step research
- open-ended 계획 수립

이때는 reasoning/generative LLM을 쓰고, Jev를 검증·routing·scoring layer로 결합하는 방식이 자연스럽습니다.

## 16. Confidence를 잘못 쓰는 사례

### 잘못된 해석

    confidence 0.55
    → "중간 강도의 위험"

Noul에서는 틀린 해석입니다.

0.55는 yes와 no가 거의 비슷해 **불확실함**을 의미합니다.

### 올바른 policy

    p_yes > 0.95 → 자동 action
    0.70~0.95   → 추가 증거 수집
    <0.70       → human/reasoning model

Threshold는 demo 값을 복사하지 말고 실제 domain data에서 calibration해야 합니다.

## 17. Workflow가 Prompt보다 강한 이유

TypeSafe의 workflow eval은 큰 policy paragraph 하나를 LLM에게 통째로 맡기는 것보다:

1. 규칙은 code
2. semantic judgment만 narrow question
3. 독립 질문을 parallel
4. 확률을 code에서 조합

하는 구조가 더 안정적일 수 있음을 보여 줍니다.

핵심 원칙:

> AI는 판단 primitive로 쓰고, deterministic logic은 code에 남긴다.

## 18. 실제 설계 예

Customer ticket:

    state = {
      message,
      account_status,
      billing_history,
      previous_tickets
    }

Jev questions:

    category = Choice(...)
    urgent = Noul(...)
    sentiment = Score(...)
    refund_request = Noul(...)

Code:

    if category == "billing" and refund_request.p > 0.95:
        run_refund_policy_check()
    elif urgent.p > 0.90:
        escalate()
    else:
        normal_queue()

LLM을 쓴다면 마지막 response text 작성만 맡길 수 있습니다.

## 핵심 정리

- Jev는 자유로운 텍스트 생성기가 아니라 **typed probabilistic decision model**입니다.
- 현재 핵심 primitive는 Choice, Noul, Score입니다.
- Output space가 고정되어 있어 schema/type hallucination은 구조적으로 제거할 수 있지만 semantic 판단 오류까지 사라지는 것은 아닙니다.
- RLCD는 calibrated decision을 목표로 합니다.
- 여러 독립 질문을 같은 state에서 병렬 처리해 latency를 낮춥니다.
- Code가 workflow와 policy를 소유하고 Jev는 semantic judgment만 담당하는 것이 핵심 설계 원칙입니다.
- 복잡한 reasoning/generation은 LLM, 빠른 routing/scoring/verification은 Jev가 더 자연스럽습니다.

## 원문 및 교차검증 자료

- Outcome School: https://outcomeschool.com/blog/jev-and-system-one-models-explained
- TypeSafe 공식 발표: https://typesafe.ai/blog/introducing-system-one-models-and-jev
- TypeSafe 현재 System One / Primitive 문서
