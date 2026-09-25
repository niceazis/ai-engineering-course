# Chain-of-Thought(CoT) Prompting은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-chain-of-thought-prompting-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-07-11 공개 원문을 직접 확인해 apple·train·30-student 수치 예제, Zero-shot/Few-shot CoT, 사용 시점과 한계를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. CoT의 핵심

Chain-of-Thought Prompting은 복잡한 문제에서 model이 최종 답을 바로 내지 않고 **중간 reasoning step을 순서대로 만들도록 유도하는 prompting 기법**입니다.

기본 prompt:

    정답만 말해라.

CoT prompt:

    문제를 작은 단계로 나눠 계산하고 마지막에 답을 제시해라.

핵심은 autoregressive model에게 intermediate state를 text context 안에 남기게 하는 것입니다.

## 2. 왜 바로 답하면 틀릴 수 있는가

원문 문제:

    사과 12개
    오전에 5개 판매
    저녁에 8개 구매
    지금 몇 개?

정답:

    12 - 5 = 7
    7 + 8 = 15

Final number만 즉시 출력하게 하면 model이 중간 상태를 explicit context에 남기지 않고 shortcut을 사용할 수 있습니다.

복잡한 multi-step 문제일수록 error probability가 커집니다.

## 3. CoT가 만드는 Scratchpad

Reasoning을 text로 적으면 다음 token은 이전 reasoning token을 다시 볼 수 있습니다.

    Step 1 result
       ↓
    Step 2 input
       ↓
    Step 2 result
       ↓
    Step 3 input

즉 generated text가 temporary working memory/scratchpad 역할을 합니다.

## 4. 원문의 Apple 예

질문:

    A shop has 12 apples.
    It sells 5 in the morning
    and buys 8 in the evening.
    How many now?

CoT:

    Start = 12
    Sell 5 → 12 - 5 = 7
    Buy 8 → 7 + 8 = 15
    Final = 15

각 단계가 다음 단계의 입력이 됩니다.

## 5. Zero-Shot CoT

Example을 주지 않고 reasoning instruction만 추가합니다.

원문 예:

    If a train travels 60 km in 1 hour,
    how far in 3 hours?
    Let's think step by step.

Model은:

    60 km/hour × 3 hours = 180 km

같은 chain을 스스로 구성합니다.

장점:

- prompt 짧음
- 빠르게 적용 가능

한계:

- reasoning format/quality 제어가 약함

## 6. Few-Shot CoT

먼저 solved example을 몇 개 보여 줍니다.

원문 흐름:

    Q: 4 pens + 3 pens?
    A: 4 + 3 = 7 ...

    Q: 10 candies - 6?
    A: 10 - 6 = 4 ...

    Q: 8 books + 5?
    A:

Model이 example의 decomposition style을 imitate합니다.

Few-shot은 unusual task나 원하는 reasoning format이 명확할 때 유용합니다.

## 7. Zero-Shot vs Few-Shot

| 항목 | Zero-shot CoT | Few-shot CoT |
| --- | --- | --- |
| Example | 없음 | 몇 개 |
| Prompt 길이 | 짧음 | 김 |
| Setup cost | 낮음 | 높음 |
| Reasoning format control | 낮음 | 높음 |
| 새로운 task | 불안정할 수 있음 | 더 안정적일 수 있음 |

## 8. 원문의 30-Student 예

문제:

    총 30명
    football = 12명
    남은 학생의 절반이 cricket
    cricket은 몇 명?

Chain:

    30 - 12 = 18
    18 / 2 = 9
    answer = 9

중간 18이라는 state가 명시되므로 다음 계산이 쉬워집니다.

## 9. CoT가 도움이 되는 이유

### Problem Decomposition

큰 문제를 작은 subproblem으로 바꿉니다.

### Intermediate State

계산 결과를 context에 저장합니다.

### Autoregressive Conditioning

앞 reasoning token이 뒤 reasoning의 조건이 됩니다.

### Error Localization

Reasoning을 확인할 수 있다면 어느 단계가 잘못됐는지 찾기 쉽습니다.

## 10. CoT가 Model을 "더 똑똑하게" 만드는가?

Weight나 knowledge를 추가하지 않습니다.

같은 model이 inference 때 더 많은 token/compute를 사용하도록 problem representation을 바꾸는 것입니다.

즉 일종의 test-time compute 증가입니다.

Reasoning model의 high-thinking mode와 연결되는 개념입니다.

## 11. 중요한 현재 실무 주의점

사용자에게 raw hidden chain-of-thought를 노출하는 것이 항상 필요한 것은 아닙니다.

Production에서는:

- 내부 reasoning은 model/runtime에 맡기고
- 사용자에게는 concise rationale, 계산식, 근거만 제공

하는 방식이 더 적합할 수 있습니다.

핵심은 "긴 reasoning text를 보여 주는 것"보다 **문제를 충분히 분해하고 검증하는 것**입니다.

## 12. CoT가 특히 유용한 Task

원문:

- math word problems
- logic puzzles
- multi-step QA
- decision making
- reading comprehension

공통점은 하나의 fact retrieval이 아니라 여러 dependency를 순서대로 처리해야 한다는 것입니다.

## 13. 간단한 Task에는 불필요

    프랑스 수도는?

처럼 single-fact 문제에 긴 CoT를 요구하면:

- token cost 증가
- latency 증가
- 불필요한 reasoning error surface 증가

가 생길 수 있습니다.

## 14. CoT의 한계

Reasoning text가 그럴듯하다고 correctness가 보장되지는 않습니다.

가능한 실패:

- 잘못된 첫 가정
- arithmetic error
- 중간 hallucination
- final answer가 reasoning과 불일치
- post-hoc explanation

따라서 important task는 external checker와 결합해야 합니다.

## 15. Self-Consistency와 연결

같은 문제에 여러 reasoning chain을 sample하고 final answer majority를 선택할 수 있습니다.

    chain 1 → 42
    chain 2 → 42
    chain 3 → 39
    chain 4 → 42

→ 42 선택

이 방식은 compute를 더 쓰지만 single-chain error를 줄일 수 있습니다.

## 핵심 정리

- CoT Prompting은 final answer 전에 intermediate reasoning을 생성하게 합니다.
- 원문의 apple 예는 12-5=7, 7+8=15로 chain을 보여 줍니다.
- Zero-shot은 instruction만, Few-shot은 solved reasoning example을 제공합니다.
- Intermediate reasoning이 autoregressive context의 scratchpad가 됩니다.
- Simple fact task에는 불필요하고 multi-step reasoning에 가장 유용합니다.
- Reasoning이 길다고 truth가 보장되는 것은 아니므로 중요한 계산은 verifier/tool과 결합해야 합니다.

## 원문

- https://outcomeschool.com/blog/how-does-chain-of-thought-prompting-work
