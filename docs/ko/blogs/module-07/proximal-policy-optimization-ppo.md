# Proximal Policy Optimization(PPO)이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/proximal-policy-optimization-ppo  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문을 직접 확인해 policy ratio, clipping, RLHF 구조와 장단점을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. PPO가 해결하는 문제

Reinforcement Learning에서 policy를 reward가 높아지는 방향으로 업데이트합니다.

문제는 update가 너무 크면 기존에 잘하던 behavior가 한 번에 무너질 수 있다는 것입니다.

PPO의 핵심 철학:

> 한 번에 큰 도약 대신 작은 안전한 update를 반복한다.

## 2. Policy란?

Policy:

    pi(a | s)

현재 state s에서 action a를 선택할 probability distribution입니다.

LLM에서는:

    state = prompt + generated prefix
    action = next token

으로 볼 수 있습니다.

## 3. Old Policy와 New Policy

Training data는 old policy로 sample합니다.

그 뒤 new parameter를 update하려고 할 때 같은 action의 probability가 얼마나 변했는지 ratio를 봅니다.

    r_t(theta)
      = pi_theta(a_t|s_t)
        / pi_old(a_t|s_t)

## 4. Ratio 해석

    ratio = 1.0

→ probability 변화 없음.

    ratio = 1.2

→ selected action이 20% 더 likely.

    ratio = 0.8

→ 20% 덜 likely.

PPO는 이 ratio가 너무 멀리 움직이지 않게 합니다.

## 5. Advantage

Advantage A_t는 action이 예상보다 얼마나 좋았는지 나타냅니다.

    A_t > 0
    → 더 likely하게

    A_t < 0
    → 덜 likely하게

LLM RLHF에서 reward model과 value model을 사용해 advantage를 추정합니다.

## 6. Naive Policy Gradient 문제

Objective:

    ratio * advantage

만 최대화하면 advantage가 positive일 때 ratio를 무한히 크게 만들려는 pressure가 생길 수 있습니다.

Large neural policy에서 unstable update를 만들 수 있습니다.

## 7. PPO Clipping

원문 핵심은 clipping입니다.

보통 epsilon=0.2 예를 사용하면 ratio 허용 범위:

    [0.8, 1.2]

Clipped objective:

    min(
      r_t A_t,
      clip(r_t, 1-eps, 1+eps) A_t
    )

큰 update에서 추가 이익을 제한합니다.

## 8. Positive Advantage 예

    A = +1
    ratio = 1.5
    eps = 0.2

Unclipped:

    1.5

Clipped:

    1.2

min:

    1.2

즉 좋은 action probability를 올리되 한 step에 50%까지 급격히 올리는 incentive는 잘립니다.

## 9. Negative Advantage 예

A가 음수일 때도 clipping이 지나친 probability 감소를 제한하는 방향으로 작동합니다.

핵심은 sign에 따라 min 구조가 trust-region 같은 효과를 낸다는 것입니다.

## 10. PPO Training Loop

1. Old policy로 trajectories 생성
2. Reward 계산
3. Return/advantage 추정
4. Policy ratio 계산
5. Clipped policy loss
6. Value loss
7. Entropy bonus 등을 결합
8. 몇 epoch update
9. Old policy를 갱신
10. 반복

## 11. LLM RLHF에서 필요한 Model

Classic PPO RLHF에서는 보통:

- policy model
- reference model
- reward model
- value/critic model

이 필요합니다.

Policy와 value가 큰 경우 memory overhead가 큽니다.

## 12. Reference KL과 PPO Clipping은 다른 역할

PPO clipping:

    current update vs old policy

를 제한합니다.

KL penalty:

    current policy vs fixed SFT/reference

drift를 제한합니다.

둘은 유사해 보여도 다른 기준입니다.

## 13. 장점

- vanilla policy gradient보다 안정적
- 구현이 TRPO보다 단순
- 큰 neural policy에서도 잘 작동
- RLHF에서 검증된 역사

## 14. 단점

- value model 필요
- on-policy sample generation 비용
- reward model exploitation 가능
- hyperparameter 민감
- 큰 LLM에서 memory/throughput 부담 큼

## 15. PPO vs GRPO

PPO:

    value model로 baseline/advantage 추정

GRPO:

    같은 prompt의 response group reward를 baseline으로 사용
    → value model 제거

Reasoning task에서 GRPO가 인기를 얻은 이유입니다.

## 핵심 정리

- PPO는 policy update를 작은 안전한 step으로 제한하는 RL algorithm입니다.
- 핵심은 old/new probability ratio와 clipping입니다.
- eps=0.2라면 ratio를 0.8~1.2 범위로 제한하는 직관을 사용합니다.
- Advantage가 좋은 action을 강화하고 나쁜 action을 약화시킵니다.
- LLM RLHF에서는 reward model, value model, reference model과 함께 사용됩니다.
- 안정적이지만 on-policy generation과 critic 때문에 비용이 큽니다.

## 원문

- https://outcomeschool.com/blog/proximal-policy-optimization-ppo
