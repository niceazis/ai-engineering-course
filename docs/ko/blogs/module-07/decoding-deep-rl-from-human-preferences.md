# Deep RL from Human Preferences란? RLHF의 시작이 된 논문 — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/decoding-deep-rl-from-human-preferences  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 공개 사본과 공식 뉴스레터를 확인해 2017년 논문의 trajectory segment, pairwise comparison, Bradley–Terry reward model, backflip 결과와 RLHF로의 연결을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 논문이 해결한 문제

전통 Reinforcement Learning은 사람이 reward function을 직접 설계해야 합니다.

예:

    reward = +1 if goal achieved

그러나 다음은 정확한 reward formula를 쓰기 어렵습니다.

- 자연스러운 robot backflip
- 좋은 article summary
- 안전하고 helpful한 response
- aesthetically pleasing behavior

잘못 설계한 reward는 reward hacking을 만들 수 있습니다.

즉 agent가 우리가 원하는 목적이 아니라 **literal reward function의 loophole**을 최대화할 수 있습니다.

## 2. 핵심 아이디어

2017년 *Deep Reinforcement Learning from Human Preferences*는 reward를 직접 쓰지 않습니다.

대신 human에게:

    Clip A vs Clip B
    어느 행동이 더 좋은가?

만 묻습니다.

많은 pairwise preference로 **reward model을 학습**합니다.

그 뒤 RL agent가 이 learned reward를 최대화합니다.

## 3. Building Blocks

### Agent

행동하는 policy.

### Trajectory

시간에 따른 state/action sequence.

    tau = (s_1,a_1,s_2,a_2,...)

### Reward

행동 품질을 나타내는 scalar.

### Policy

State를 보고 action distribution을 결정.

## 4. Trajectory Segment

전체 episode 대신 1~2초 정도의 짧은 behavior clip을 human에게 보여 줍니다.

왜 single frame이 아닌가?

Backflip처럼 **시간적 움직임**을 봐야 preference를 판단할 수 있기 때문입니다.

## 5. Human Comparison

Human UI는 단순합니다.

    [Clip A]      [Clip B]

    A better
    B better
    equal
    cannot tell

절대 score를 7.3처럼 붙이게 하지 않고 상대 비교만 합니다.

Pairwise comparison은 사람이 일관되게 판단하기 더 쉽다는 장점이 있습니다.

## 6. Reward Model

Reward model r_phi(s,a)는 각 step에 scalar reward를 예측합니다.

Clip 전체 reward:

    R(tau)
      = Σ_t r_phi(s_t, a_t)

두 clip의 총 reward를 비교해 human preference probability를 계산합니다.

## 7. Bradley–Terry Preference Model

A가 B보다 선호될 확률:

    P(A > B)
      = exp(R_A)
        / [exp(R_A) + exp(R_B)]

이는 두 total reward에 softmax를 적용한 것과 같습니다.

Human이 A를 고른 training example에서는:

    Loss = -log P(A > B)

가 작아지도록 reward model을 update합니다.

## 8. 작은 숫자 예

가정:

    R_A = 3
    R_B = 1

그러면:

    P(A > B)
      = exp(3) / [exp(3)+exp(1)]
      ≈ 0.88

Human이 A를 선택했다면 reward model이 올바른 방향입니다.

Human이 B를 선택했다면 loss가 커지고 reward model이 수정됩니다.

## 9. Reward Model Training Loop

1. Current agent가 여러 trajectory 생성
2. 짧은 segment pair 선택
3. Human이 더 나은 clip 선택
4. Pairwise preference dataset에 추가
5. Reward model update
6. Learned reward를 사용해 policy update
7. 새 agent behavior 생성
8. 반복

즉 human feedback과 policy improvement가 같이 진행됩니다.

## 10. Policy Training

원 논문은 domain에 따라:

- Atari: A2C
- robotics: TRPO

같은 RL algorithm을 사용했습니다.

현대 LLM RLHF에서는 PPO가 널리 사용됐습니다.

중요한 것은 **RL algorithm 자체보다 learned reward가 human preference에서 온다는 것**입니다.

## 11. 왜 Human Feedback이 적어도 가능했나

Human은 모든 timestep에 reward를 주지 않습니다.

Agent가 많은 경험을 스스로 생성하고, human은 작은 일부 pair만 비교합니다.

Reward model이 human judgment를 generalize해 나머지 trajectory에 reward를 제공합니다.

원문은 일부 complex task가 환경 interaction의 1% 미만 human feedback으로 학습됐다고 설명합니다.

## 12. Backflip 결과

대표적인 simulated robot task에서 human은 대략 **900번의 비교**를 제공했습니다.

Hand-written reward 없이 human preference만으로 backflip behavior를 학습했습니다.

이 결과는 “reward function을 직접 쓰기 어려운 task도 preference comparison으로 학습할 수 있다”는 강력한 proof-of-concept였습니다.

## 13. Active Querying

어떤 clip pair를 human에게 물을지 선택하는 것도 중요합니다.

Reward model이 확신하는 pair보다 **둘 중 어느 것이 좋은지 불확실한 pair**가 더 많은 정보를 줄 수 있습니다.

이를 active learning 관점에서 볼 수 있습니다.

원 논문에서는 이 방식이 항상 큰 이득을 주지는 않았다는 점도 중요합니다.

## 14. RLHF로의 연결

Game/robot:

    clip A vs clip B

LLM:

    response A vs response B

으로 바뀌었을 뿐 recipe는 동일합니다.

    human preference
      → reward model
      → policy optimization

InstructGPT와 ChatGPT로 이어진 핵심 구조입니다.

## 15. Modern Variation

오늘날에는 다음 변형이 있습니다.

### RLHF + PPO

Human preference reward model + policy RL.

### DPO

Explicit reward model/PPO loop 없이 chosen/rejected pair에서 직접 policy optimization.

### RLAIF

Human 대신 AI feedback 일부 사용.

### RLVR

Math/code처럼 answer를 자동 검증할 수 있는 task에서 rule/verifier reward.

### GRPO

Group reward를 baseline으로 value model 없이 reasoning model RL.

## 16. Reward Hacking

Reward model은 human preference의 근사치입니다.

Policy가 reward model의 약점을 찾으면:

    high predicted reward
    ≠ actually preferred behavior

가 될 수 있습니다.

현대 RLHF에서 KL penalty/reference model이 중요한 이유입니다.

## 핵심 정리

- 2017년 논문은 hand-written reward 대신 human pairwise preference로 reward model을 학습했습니다.
- Human은 1~2초 trajectory segment 두 개 중 더 나은 것을 고릅니다.
- Reward model은 clip reward 총합을 만들고 Bradley–Terry/softmax probability로 preference를 학습합니다.
- Learned reward로 일반 RL policy를 최적화합니다.
- Robot backflip은 약 900 human comparisons로 학습된 대표 결과입니다.
- 이 구조가 이후 text response preference 기반 RLHF의 직접적인 전신입니다.

## 원문

- https://outcomeschool.com/blog/decoding-deep-rl-from-human-preferences
