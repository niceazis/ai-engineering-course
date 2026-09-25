# World Model은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-do-world-models-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-06-20 공개 원문을 직접 확인해 Environment·State·Action·Reward, next-state prediction, latent state, rollout, Dreamer-style agent, model error accumulation과 real-world use를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Environment, State, Action

### Environment

AI가 상호작용하는 세계.

예:

- robot의 room
- game map
- self-driving car의 road

### State

현재 environment의 snapshot.

예:

    player 위치
    enemy 위치
    health

### Action

AI가 state를 바꾸기 위해 선택하는 행동.

예:

    move left
    jump
    robot arm lift

기본 loop:

    current state
      → action
      → environment
      → next state

## 2. World Model의 정의

원문 정의의 핵심:

> Current state와 action을 보고 next state와 reward를 예측하는 approximate internal simulator.

형식:

    (state_t, action_t)
      → World Model
      → predicted state_t+1
      + predicted reward

완벽한 simulation이 아니라 planning에 충분한 approximation이 목표입니다.

## 3. 인간 비유

체스에서 실제 말을 움직이기 전에 머릿속으로:

    이 수를 두면?
      → 상대가 이렇게?
      → 그다음은?

을 상상합니다.

World Model은 AI에게 이런 internal imagination을 제공하려는 접근입니다.

## 4. 왜 필요한가

Model-free trial-and-error는 실제 environment에서 수많은 action을 직접 실행해야 합니다.

원문은 세 문제를 강조합니다.

- slow
- expensive
- risky

Robot이 random action을 millions of times 실제 hardware에서 시도하면 wear, battery, 사고 위험이 큽니다.

## 5. World Model 학습 데이터

Environment interaction을 기록합니다.

각 transition:

    state_t
    action_t
    state_t+1
    reward_t

를 training example로 사용합니다.

## 6. Next State Prediction

Training:

1. state/action input
2. World Model이 next state/reward prediction
3. 실제 recorded transition과 비교
4. prediction error로 update
5. 반복

목표는 단순 memorization이 아니라 environment dynamics를 generalize하는 것입니다.

## 7. Raw State의 문제

Camera frame처럼 raw state가 매우 크면 pixel 전체를 직접 predict하는 것은 비효율적일 수 있습니다.

그래서 compact latent state를 사용합니다.

    observation
      → encoder
      → latent state z_t

World Model은:

    (z_t, action_t)
      → z_t+1

을 예측합니다.

## 8. Latent State

Latent representation은:

- object location
- velocity
- scene structure
- task-relevant feature

같은 meaningful dynamics를 압축해 표현하려 합니다.

JEPA의 representation-space prediction과 연결되는 지점입니다.

## 9. Imagination Rollout

World Model이 next latent state를 예측할 수 있으면 prediction을 연결할 수 있습니다.

    z0
      + action A
      → z1
      + action B
      → z2
      + action C
      → z3

실제 environment를 건드리지 않고 여러 future를 상상합니다.

이를 rollout이라고 합니다.

## 10. Sample Efficiency

Real-world data를 조금 수집한 뒤 internal model 안에서 많은 imagined experience를 만들 수 있습니다.

따라서 실제 environment interaction을 덜 사용하고도 policy를 개선할 수 있습니다.

이것이 sample efficiency의 핵심입니다.

## 11. Error Accumulation

원문이 강조하는 중요한 한계입니다.

World Model prediction에는 작은 error가 있습니다.

Long rollout:

    error_1
      + error_2
      + error_3
      + ...

으로 누적되면 먼 future prediction은 unreliable해집니다.

그래서 practical system은:

- short rollout
- real environment refresh
- model update

를 반복합니다.

## 12. Dreamer-Style Agent

원문 흐름:

1. Real environment에서 experience 수집
2. World Model update
3. World Model 안에서 imagined rollout 생성
4. Imagined experience로 policy/value 개선
5. 실제 environment에 다시 적용
6. 새 experience 수집
7. 반복

이름 그대로 agent가 model 안에서 "dream"하며 연습합니다.

## 13. Planning

여러 candidate action sequence를 imagination에서 평가할 수 있습니다.

    plan A → predicted rewards
    plan B → predicted rewards
    plan C → predicted rewards

가장 좋은 expected outcome의 plan을 실제로 실행합니다.

## 14. Real-World Use

- robotics
- autonomous driving research
- game agents
- model-based reinforcement learning
- video/future prediction
- planning

에 활용됩니다.

## 15. World Model vs Simulator

Hand-coded simulator:

    사람이 physics/rule을 작성

Learned World Model:

    data에서 dynamics를 학습

실제 system에서는 둘을 함께 사용할 수도 있습니다.

## 16. JEPA와 연결

JEPA는 raw pixel보다 representation space에서 predictable semantics를 학습하려 합니다.

World Model도 compact latent state에서 future를 예측하면:

- compute 감소
- irrelevant detail 제거
- planning-friendly representation

을 얻을 수 있습니다.

## 핵심 정리

- World Model은 state+action에서 next state와 reward를 예측하는 learned internal simulator입니다.
- 실제 trial-and-error를 줄여 sample efficiency와 safety를 높일 수 있습니다.
- Raw observation 대신 latent state를 사용하면 compact dynamics를 모델링할 수 있습니다.
- Predicted state를 연결한 rollout으로 실제 행동 전에 future를 상상합니다.
- Long rollout에서는 model error가 누적되므로 real-world feedback으로 계속 교정해야 합니다.
- Dreamer 계열은 real experience와 imagined training을 반복합니다.

## 원문

- https://outcomeschool.com/blog/how-do-world-models-work
