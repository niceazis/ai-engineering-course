# Large Reasoning Model(LRM)이란 무엇이며 LLM과 어떻게 다른가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/large-reasoning-models  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-05-12 공개 원문을 직접 확인해 reasoning-token 규모, test-time compute, AIME 2024 수치, training trace 예, 선택 기준을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 핵심 정의

원문의 한 줄 정의:

> LRM = 답하기 전에 먼저 생각하도록 훈련된 Large Language Model

Standard LLM:

    question → direct answer

LRM:

    question
      → extended reasoning
      → final answer

Reasoning trace는 제품에 따라 사용자에게 숨겨지거나 일부 형태로 노출될 수 있습니다.

## 2. LLM과 LRM의 차이

원문 비교:

| 항목 | Standard LLM | LRM |
| --- | --- | --- |
| 답변 방식 | direct | think first |
| Tokens | 100~500 | 5,000~50,000 |
| Latency | 1~3초 | 10~120초 |
| Cost | 낮음 | 약 10~30배 |
| 강점 | chat, summary, draft | math, code, logic, planning |
| 약점 | hard multi-step | easy task에는 비쌈 |

이 숫자는 고정 규칙이 아니라 원문의 전형적 범위 예입니다.

## 3. Reasoning Token

LRM은 final answer 전에 내부적으로 더 많은 token을 사용해:

- 문제 분해
- intermediate calculation
- self-check
- alternative path 탐색

을 할 수 있습니다.

중요한 점은 “보이는 답변이 짧다 = 계산도 적다”가 아니라는 것입니다.

## 4. Test-Time Compute

전통 scaling은 training에 compute를 더 넣습니다.

LRM은 inference에서도 compute를 늘릴 수 있습니다.

    same model
    + more reasoning tokens / samples
    → potentially higher accuracy

이를 test-time compute scaling이라고 합니다.

## 5. 원문의 AIME 2024 예

원문이 인용한 published example:

- GPT-4o: 약 12%
- o1 single reasoning attempt: 약 74%
- o1, 64 attempts majority vote: 약 83%
- o1, 1,000 attempts reranking: 약 93%

핵심은 같은 reasoning model에서도 **answer-time compute를 더 쓰면 성능이 올라갈 수 있음**을 보여 주는 것입니다.

다만 task마다 scaling curve가 다르고 무한히 증가하지 않습니다.

## 6. 비용 Trade-off

Reasoning token이 늘면:

- latency 증가
- output compute 증가
- token cost 증가

원문은 reasoning token 2배가 대략 query output 비용도 2배 규모로 늘 수 있다고 설명합니다.

따라서 모든 request에 최고 reasoning effort를 쓰는 것은 비효율적입니다.

## 7. Training은 어떻게 달라지는가

Standard LM pretraining은 next-token prediction입니다.

예:

    Input:  The capital of France is
    Target: Paris

LRM은 그 위에 **좋은 reasoning process와 correct answer를 강화하는 post-training**을 사용합니다.

원문은 hard problem에 대해 여러 reasoning trace를 생성하고 final answer를 verifier로 평가하는 방식으로 설명합니다.

## 8. 원문의 16 Trace 계산 예

문제:

    pens: 2개에 5 rupees
    notebooks: 3개에 12 rupees
    6 pens + 9 notebooks의 총액?

정답 계산:

    pens:
    6 / 2 = 3 packs
    3 × 5 = 15

    notebooks:
    9 / 3 = 3 packs
    3 × 12 = 36

    total = 51

원문은 training에서 같은 문제에 16 reasoning traces를 만들고:

- 6개가 51 정답
- 10개가 48/54 같은 오답

이라고 가정합니다.

정답 group보다 좋은 trace를 reinforce하고 나쁜 trace를 penalize하는 식으로 reasoning behavior를 개선합니다.

## 9. Verifiable Reward

Math/code처럼 final answer를 자동 채점할 수 있는 task는 reinforcement signal을 만들기 쉽습니다.

예:

- exact math answer
- unit test pass/fail
- compiler
- formal checker

Human preference보다 objective verification에 가까운 reward를 사용할 수 있습니다.

## 10. LRM Prediction

Inference에서는:

    prompt
      → long hidden/internal reasoning
      → final answer

흐름이 됩니다.

제품이 raw trace를 숨길 수 있으므로 사용자에게는 reasoning summary나 final answer만 보일 수 있습니다.

## 11. “생각을 많이 하면 항상 맞다”는 오해

Test-time compute는 성능을 높일 수 있지만:

- 잘못된 초기 가정
- 없는 지식
- flawed verifier
- ambiguous task

는 thinking을 늘려도 해결되지 않을 수 있습니다.

또 overthinking으로 simple task를 불필요하게 복잡하게 만들 수 있습니다.

## 12. 언제 LRM을 쓰나

원문 기준:

- multi-step reasoning 필요
- wrong answer cost가 큼
- hard math/code/science
- planning
- deep analysis
- 30초 이상 latency 허용
- 높은 token cost 허용

## 13. 언제 일반 LLM이 낫나

- quick chat
- short summary
- draft email
- high-volume simple calls
- latency가 중요
- low cost가 중요

Easy task에서 reasoning model은 기회비용이 큽니다.

## 14. Popular Reasoning Models

원문은 당시의 대표 예로:

- OpenAI GPT-5.5 Thinking
- DeepSeek R1 / R1-Zero
- newer DeepSeek think/non-think modes

등을 언급합니다.

이 목록은 2026-05 시점의 원문이며 모델 라인업은 이후 바뀔 수 있습니다.

## 15. R1-Zero가 보여 준 점

원문은 DeepSeek R1-Zero를 rule-based verifiable reward로 reasoning behavior를 강화한 대표 사례로 설명합니다.

핵심은 사람이 모든 reasoning trace를 직접 써주지 않아도 **correct final outcome을 보상**해 유용한 reasoning strategy가 생길 수 있다는 것입니다.

## 16. AI Engineering 관점

Routing policy 예:

    if task_complexity < threshold:
        use standard LLM
    else:
        use reasoning model

더 발전하면:

- confidence
- business risk
- estimated difficulty
- latency SLO

를 함께 넣어 dynamic reasoning effort를 정할 수 있습니다.

## 핵심 정리

- LRM은 inference 전에 더 많은 reasoning compute를 사용하도록 post-trained된 모델입니다.
- 원문은 reasoning 5K~50K tokens, latency 10~120초, 비용 10~30배 예를 사용합니다.
- 핵심 개념은 test-time compute scaling입니다.
- AIME 예에서 single attempt보다 64/1,000 sample compute를 늘렸을 때 점수가 상승합니다.
- Hard/verifiable task에 강하지만 easy task에는 느리고 비쌉니다.
- Production에서는 LLM/LRM을 task 난이도에 따라 route하는 것이 중요합니다.

## 원문

- https://outcomeschool.com/blog/large-reasoning-models
