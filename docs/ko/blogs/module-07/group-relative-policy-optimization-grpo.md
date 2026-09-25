# Group Relative Policy Optimization(GRPO)이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/group-relative-policy-optimization-grpo  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-05-18 공개 원문을 직접 확인해 value model 제거, group baseline, 12+7 수치 예, clipping·KL objective, group-size 실무 기준을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. GRPO의 정의

GRPO는 같은 prompt에 여러 response를 생성한 뒤 **group 내부의 상대 reward를 advantage baseline으로 사용**하는 LLM reinforcement-learning algorithm입니다.

핵심 차이:

> PPO의 별도 value model/critic을 제거한다.

## 2. 왜 PPO가 비싼가

Classic PPO RLHF:

- policy
- reference
- reward model
- value model

을 함께 사용합니다.

Value model은 policy에 가까운 큰 network일 수 있어 GPU memory와 training complexity를 크게 늘립니다.

GRPO는 group reward statistics로 baseline을 만들기 때문에 critic이 필요 없습니다.

## 3. Reward Model과 Value Model의 차이

### Reward Model

완성된 response 전체를 평가:

    response → reward

### Value Model

생성 중 각 state/prefix에서 future expected reward를 예측:

    prefix_t → V(s_t)

PPO는 value model로 advantage를 추정합니다.

GRPO는 complete response들 사이 상대 비교를 사용합니다.

## 4. Group 생성

하나의 prompt x에서 G개 response를 sample합니다.

    y_1, y_2, ..., y_G

원문 예에서는 흔히 G=8을 설명하고 practical range로 8~64를 언급합니다.

각 response에 reward를 계산합니다.

## 5. Group Baseline

Rewards:

    r_1, r_2, ..., r_G

평균:

    mean_r = mean(r_i)

단순 advantage:

    A_i = r_i - mean_r

실전 GRPO는 표준편차로 normalize할 수 있습니다.

    A_i
      = (r_i - mean_r)
        / (std_r + eps)

## 6. 원문의 12+7 예

Question:

    12 + 7 = ?

4 answers:

    A1: 19   reward 1
    A2: 18   reward 0
    A3: 19   reward 1
    A4: 20   reward 0

Group mean:

    (1+0+1+0)/4
    = 0.5

Advantages:

    A1 = +0.5
    A2 = -0.5
    A3 = +0.5
    A4 = -0.5

좋은 answer sequence 전체의 token probability를 올리고 나쁜 answer를 내립니다.

## 7. Credit Assignment 방식

PPO:

    value model을 이용해 token/state별 advantage

GRPO:

    complete response group-relative advantage

따라서 math/code처럼 final result를 verifier로 평가할 수 있는 task에 특히 잘 맞습니다.

세밀한 step-level reward가 필요한 task에서는 trade-off가 있습니다.

## 8. Reward Source

가능한 reward:

- learned reward model
- exact answer checker
- unit tests
- code execution
- theorem/formal verifier
- format check
- multi-objective weighted reward

Reasoning RL에서 rule-based/verifiable reward가 강력한 이유입니다.

## 9. Policy Ratio와 Clipping

GRPO도 PPO와 유사하게 old/new policy ratio를 사용합니다.

    ratio
      = pi_theta(token|state)
        / pi_old(token|state)

Clipping 예:

    [0.8, 1.2]

큰 policy update를 제한합니다.

## 10. KL Penalty

Reference model에서 너무 멀어지지 않도록 KL penalty를 사용합니다.

전체 직관:

    objective
      ≈ clipped policy improvement
        × group advantage
        - beta * KL(policy || reference)

핵심 변화는 advantage source가 value model이 아니라 group statistics라는 점입니다.

## 11. Training Loop

1. Training prompt sample
2. Policy가 G개 response 생성
3. 각 response reward 계산
4. Group mean/std 계산
5. Relative advantage 계산
6. Old/current probability ratio
7. Clipped objective + KL penalty
8. Policy update
9. 다음 prompt

## 12. 장점

### Value Model 제거

Memory와 engineering complexity 감소.

### Verifiable Task에 적합

Math/code reward를 자동 계산 가능.

### Simple Baseline

Group 자체가 comparison baseline.

### Parallel Sampling

같은 prompt response들을 batch로 생성할 수 있습니다.

## 13. 한계

### Group Sampling Cost

한 prompt에 8~64 response를 만들어야 하므로 rollout compute가 큽니다.

### Uniform Reward Problem

모든 response가:

    [0,0,0,0]

또는:

    [1,1,1,1]

이면 std/advantage가 0에 가까워 learning signal이 없습니다.

Task difficulty curriculum이 필요할 수 있습니다.

### Reward Quality

Verifier가 잘못되면 model도 잘못된 behavior를 강화합니다.

### Sequence-Level Signal

어떤 token/step이 실제로 잘못됐는지 세밀한 credit assignment가 약할 수 있습니다.

## 14. Reward Hacking

KL/reference constraint가 약하면 verifier shortcut을 찾을 수 있습니다.

예:

- test parser exploit
- formatting loophole
- answer leakage

Verifier robustness가 RL model quality만큼 중요합니다.

## 15. PPO vs GRPO

| 항목 | PPO | GRPO |
| --- | --- | --- |
| Value model | 필요 | 불필요 |
| Baseline | learned critic | group mean/std |
| Memory | 높음 | 낮음 |
| Rollout | 필요 | group rollout 많이 필요 |
| Best fit | general RL | verifiable reasoning |
| Credit | state/token level 가능 | response-relative 중심 |

## 16. DPO와 차이

DPO:

- offline chosen/rejected pairs
- rollout 불필요

GRPO:

- current policy가 online으로 여러 response 생성
- reward function으로 score
- exploration 가능

새 reasoning strategy를 발견하는 online RL에는 GRPO가 더 적합할 수 있습니다.

## 핵심 정리

- GRPO는 같은 prompt의 response group reward를 baseline으로 사용합니다.
- PPO의 value model을 제거해 memory와 complexity를 줄입니다.
- 원문의 12+7 예에서는 reward [1,0,1,0], mean 0.5, advantage ±0.5입니다.
- Policy ratio clipping과 KL penalty를 함께 사용합니다.
- Group size 8~64가 실무 예로 언급되며, 큰 group은 안정적이지만 rollout 비용이 큽니다.
- Verifiable math/code reasoning에 특히 잘 맞지만 reward design과 group diversity가 중요합니다.

## 원문

- https://outcomeschool.com/blog/group-relative-policy-optimization-grpo
