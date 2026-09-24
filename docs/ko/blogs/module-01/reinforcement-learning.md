# Reinforcement Learning — 매우 자세한 한국어 학습 노트

> 원문: https://outcomeschool.com/blog/reinforcement-learning
> 원저자: Amit Shekhar / Outcome School
> 문서 성격: **원문 전체 번역본이 아닌 독립적인 한국어 상세 해설·학습 노트**

## 핵심 정의

강화학습은 Agent가 Environment와 상호작용하며 장기 누적 Reward를 최대화하는 Policy를 학습하는 방법이다.

---

## 1. 구성 요소

- Agent: 행동 주체.
- Environment: 상호작용하는 세계.
- State: 현재 상황.
- Action: 선택 가능한 행동.
- Reward: 행동 결과의 scalar feedback.
- Policy: state에서 action을 고르는 규칙.

## 2. Episode와 Return

- Episode는 시작부터 종료까지의 interaction sequence다.
- Return은 미래 reward의 할인 합이다.
- discount factor gamma는 미래 보상의 중요도를 조절한다.

## 3. Value Function

- V(s)는 state의 장기 가치다.
- Q(s,a)는 특정 state-action의 장기 가치다.
- Bellman relation은 현재 가치와 미래 가치를 재귀적으로 연결한다.

## 4. Exploration vs Exploitation

- 현재 최선 행동만 고르면 더 좋은 전략을 놓칠 수 있다.
- 탐험을 통해 불확실한 action의 가치를 학습한다.

## 5. 주요 계열

- Q-Learning/DQN은 value 기반.
- Policy Gradient는 policy 자체를 최적화.
- Actor-Critic은 행동 선택과 가치 평가를 결합한다.
- PPO는 policy update가 과도하게 변하지 않도록 제한한다.

## 6. Reward Design

- 잘못된 reward는 Reward Hacking을 유발할 수 있다.
- Sparse reward는 학습 신호 부족 문제를 만든다.
- Reward shaping은 도움되지만 원래 목표 왜곡 가능성이 있다.

## 7. Model-Free vs Model-Based

- Model-free는 환경 dynamics를 명시적으로 학습하지 않고 policy/value를 학습한다.
- Model-based는 dynamics를 이용해 planning/simulation을 수행한다.

## 8. LLM과 연결

- RLHF에서 PPO 같은 RL 방법이 사용됐다.
- 최근에는 DPO처럼 RL이 아닌 preference optimization도 널리 사용된다.

## 학습 체크리스트

- 핵심 개념을 한 문장으로 설명할 수 있는가?
- 대표 수식이나 기준을 직접 설명할 수 있는가?
- 실무 예시를 하나 들 수 있는가?
- 실패하거나 오해하기 쉬운 조건을 설명할 수 있는가?

## 원문

- https://outcomeschool.com/blog/reinforcement-learning
