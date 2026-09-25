# Reinforcement Learning — 원문 흐름을 따라가는 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/reinforcement-learning  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 Agent–Environment–State–Action–Reward 구조와 Exploration/Exploitation 흐름을 상세하게 풀어쓴 한국어 학습 노트입니다.

## 핵심

강화학습(Reinforcement Learning, RL)은 **Agent가 Environment와 상호작용하면서 어떤 Action이 장기적으로 더 큰 Reward를 만드는지 학습하는 방법**입니다.

지도학습처럼 각 상황마다 “정답 action”이 주어지는 것이 아닙니다.

```text
State
  ↓
Agent가 Action 선택
  ↓
Environment 변화
  ↓
Reward + New State
  ↓
다음 Action
```

이 반복 경험을 통해 행동 전략을 개선합니다.

## 1. 머신러닝 안에서의 위치

원문은 머신러닝을 크게 다음 세 범주로 소개합니다.

- Supervised Learning
- Unsupervised Learning
- Reinforcement Learning

지도학습은 정답 label을 이용하고, 비지도학습은 label 없이 구조를 찾습니다.

강화학습의 학습 신호는 **행동 결과로 돌아오는 reward**입니다.

## 2. 다섯 핵심 구성 요소

### Agent

행동을 선택하는 주체입니다.

예:

- 게임 캐릭터
- 로봇
- 자율주행 의사결정 시스템
- 추천 정책

### Environment

Agent가 행동하는 세계입니다.

### State

현재 상황을 표현합니다.

게임이라면 캐릭터 위치, 체력, 주변 물체 등이 state가 될 수 있습니다.

### Action

Agent가 선택할 수 있는 행동입니다.

```text
left / right / jump
```

처럼 discrete할 수도 있고, 로봇 관절 제어처럼 continuous할 수도 있습니다.

### Reward

행동 결과가 얼마나 좋았는지를 나타내는 학습 신호입니다.

```text
목표 달성 -> +10
충돌      -> -5
시간 소모 -> -0.01
```

처럼 설계할 수 있습니다.

## 3. RL loop

한 step을 풀어쓰면:

```text
1. Agent가 현재 state s_t 관찰
2. action a_t 선택
3. Environment가 action 실행
4. reward r_t 반환
5. 다음 state s_(t+1)로 이동
6. 경험을 이용해 행동 전략 개선
7. 반복
```

핵심은 단일 reward 하나만 최대화하는 것이 아니라 **시간에 걸쳐 받을 누적 reward**를 최대화하는 것입니다.

당장 작은 보상을 포기해야 미래에 더 큰 보상을 받을 수 있는 문제도 있기 때문입니다.

## 4. 예: 미로

Agent가 미로에서 출구를 찾는다고 하겠습니다.

- State: 현재 위치
- Action: 상/하/좌/우
- Reward: 출구 +100, 벽 충돌 -5, 한 걸음 -1
- Environment: 미로

초기 Agent는 좋은 길을 모릅니다.

여러 경로를 시도하면서:

```text
이 방향 -> 막힘 -> 낮은 reward
저 방향 -> 출구에 가까움 -> 더 좋은 장기 reward
```

를 경험합니다.

충분한 경험이 쌓이면 어떤 state에서 어떤 action을 선택해야 유리한지 학습합니다.

## 5. Value-based

원문이 제시하는 첫 번째 접근은 Value-based입니다.

핵심 질문:

> 이 state 또는 state-action 조합은 미래 reward 관점에서 얼마나 가치가 있는가?

Q-learning을 예로 들면:

```text
Q(s, a)
= state s에서 action a를 선택했을 때 기대되는 장기 가치
```

Agent는 높은 Q-value를 가진 action을 선택하는 방향으로 학습할 수 있습니다.

## 6. Policy-based

Policy는 state를 action 선택으로 직접 연결하는 전략입니다.

```text
π(a | s)
```

는 state `s`에서 action `a`를 선택할 확률로 이해할 수 있습니다.

Policy-based 방법은 action probability 자체를 조정해 높은 reward를 만드는 행동을 더 자주 선택하도록 학습합니다.

## 7. Model-based

Model-based RL은 environment가 어떻게 변하는지에 대한 모델을 사용하거나 학습합니다.

개념적으로:

```text
현재 state + action
       ↓
예상 next state / reward
       ↓
미래를 계획
```

할 수 있습니다.

Value-based, Policy-based, Model-based는 서로 완전히 배타적인 분류라기보다 실제 알고리즘에서 조합될 수 있습니다.

## 8. Exploration vs Exploitation

원문이 강조하는 핵심 trade-off입니다.

### Exploration

아직 잘 모르는 action을 시도해 정보를 얻습니다.

### Exploitation

현재까지 가장 좋다고 알고 있는 action을 선택해 reward를 얻습니다.

항상 exploitation만 하면 초기에 우연히 발견한 행동에 갇힐 수 있습니다.

항상 exploration만 하면 좋은 행동을 알아도 계속 무작위로 움직여 reward를 충분히 얻지 못합니다.

따라서:

```text
새로운 가능성 탐색
        ↕
현재 최선 활용
```

사이의 균형이 필요합니다.

## 9. Reward 설계가 중요한 이유

Agent는 우리가 “의도한 목표”가 아니라 **실제로 정의한 reward**를 최적화합니다.

잘못 설계하면 예상하지 못한 shortcut을 찾을 수 있습니다.

예를 들어 게임에서 점수 획득만 reward로 두었는데 특정 위치에서 무한히 점수를 얻을 수 있다면, Agent는 게임의 본래 목적보다 그 행동을 반복할 수 있습니다.

그래서 reward design은 RL 시스템 설계의 핵심입니다.

## 10. 지도학습과의 차이

| 지도학습 | 강화학습 |
|---|---|
| 정답 label 제공 | reward 제공 |
| 각 sample 비교 가능 | 행동 결과가 지연될 수 있음 |
| 고정 dataset 학습 가능 | environment interaction 중요 |
| 예측 오류 최소화 | 장기 누적 reward 최대화 |

## 11. 반드시 기억할 문장

```text
Reinforcement Learning
= Agent가 Environment와 상호작용하면서
  State에서 Action을 선택하고
  Reward를 통해 더 좋은 행동 전략을 학습하는 과정
```

## 이해 확인

1. RL에서 label 대신 핵심 학습 신호가 되는 것은 무엇인가요?
2. exploration을 완전히 없애면 어떤 문제가 생길 수 있나요?
3. 당장 reward가 가장 큰 action이 항상 최적이 아닌 이유는 무엇인가요?

## 원문 및 연결 학습

- 원문: https://outcomeschool.com/blog/reinforcement-learning
- 이전: [Regularization](regularization-in-machine-learning.md)
- 다음: [Contrastive Learning](contrastive-learning.md)
- 모듈 1: [머신러닝 기초](../../module-01.md)
