# 모듈 7 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 7: 학습, 파인튜닝, 정렬

이 모듈에서는 사전학습 모델을 우리 작업에 맞게 조정하는 방법, 더 작고 효율적으로 만드는 방법, 그리고 사람의 지시와 선호를 따르도록 정렬하는 방법을 배웁니다.

모듈을 마치면 언제 파인튜닝이 필요한지, LoRA가 비용을 어떻게 줄이는지, RLHF·PPO·DPO·GRPO가 모델을 어떻게 정렬하는지 이해할 수 있습니다.

**이 모듈의 레슨:**

1. [파인튜닝은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-fine-tuning-work)
2. [LoRA(Low-Rank Adaptation)란 무엇이며 LLM을 어떻게 파인튜닝하는가?](https://outcomeschool.com/blog/lora-low-rank-adaptation-of-llms)
3. [Prefix Tuning은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-prefix-tuning-work)
4. [Knowledge Distillation은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-knowledge-distillation-work)
5. [LLM의 Continual Learning이란? Catastrophic Forgetting 해결](https://outcomeschool.com/blog/continual-learning-in-llms)
6. [Deep RL from Human Preferences란? RLHF의 시작이 된 논문](https://outcomeschool.com/blog/decoding-deep-rl-from-human-preferences)
7. [InstructGPT란? GPT-3가 지시를 따르게 된 방법](https://outcomeschool.com/blog/decoding-instructgpt)
8. [RLHF란? 인간 피드백을 이용한 강화학습](https://outcomeschool.com/blog/reinforcement-learning-from-human-feedback-rlhf)
9. [Proximal Policy Optimization(PPO)이란?](https://outcomeschool.com/blog/proximal-policy-optimization-ppo)
10. [Direct Preference Optimization(DPO)이란?](https://outcomeschool.com/blog/direct-preference-optimization-dpo)
11. [Group Relative Policy Optimization(GRPO)이란?](https://outcomeschool.com/blog/group-relative-policy-optimization-grpo)

---

### 7.1 파인튜닝은 어떻게 동작하는가?

Fine-tuning이 무엇인지, 왜 필요한지, 단계별 동작과 간단한 수치 예제, Full Fine-tuning과 LoRA의 차이, 사용 시점을 배웁니다.

- Fine-tuning이란?
- 필요한 이유
- 단계별 동작
- 간단한 수치 예제
- Full Fine-tuning vs LoRA
- Fine-tuning을 사용할 때
- Fine-tuning 전 팁
- 요약

시작하기: [파인튜닝은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-fine-tuning-work)

### 7.2 LoRA란 무엇이며 LLM을 어떻게 파인튜닝하는가?

대규모 언어 모델을 저비용으로 적응시키는 LoRA(Low-Rank Adaptation)를 배웁니다.

- 큰 그림
- Full Fine-tuning이 비싼 이유
- LoRA의 핵심 아이디어
- 단계별 동작
- 작은 수치 예제
- Transformer에서 적용되는 위치
- LoRA를 원 모델에 Merge하는 방법
- 실제 사용 사례
- 빠른 요약

시작하기: [LoRA](https://outcomeschool.com/blog/lora-low-rank-adaptation-of-llms)

### 7.3 Prefix Tuning은 어떻게 동작하는가?

모델 자체의 파라미터를 크게 변경하지 않고 새로운 작업에 적응시키는 Prefix Tuning을 배웁니다.

- LLM이란?
- Full Fine-tuning이 비싼 이유
- Prefix Tuning이란?
- Prefix + Tuning
- 동작 방식
- Prefix는 실제 단어가 아님
- Prefix가 추가되는 위치
- Prefix 학습
- Prefix의 크기
- 간단한 코드 예제
- Prefix Tuning vs Full Fine-tuning
- Prefix Tuning vs Prompt Tuning
- 장점
- 한계
- 실제 활용

시작하기: [Prefix Tuning](https://outcomeschool.com/blog/how-does-prefix-tuning-work)

### 7.4 Knowledge Distillation은 어떻게 동작하는가?

큰 모델의 지식을 작은 모델로 전달해 모바일·엣지 장치나 저비용 환경에서도 강력한 모델을 사용할 수 있게 하는 Knowledge Distillation을 배웁니다.

- Knowledge Distillation이란?
- 필요한 이유
- Hard Label vs Soft Label
- Dark Knowledge
- Softmax의 Temperature
- Distillation Loss
- 단계별 학습 과정
- Distillation의 종류
- 실제 사례
- 정리

시작하기: [Knowledge Distillation](https://outcomeschool.com/blog/how-does-knowledge-distillation-work)

### 7.5 LLM의 Continual Learning이란?

새로운 지식을 계속 학습하면서 기존 지식을 잃는 Catastrophic Forgetting 문제와 이를 해결하는 Continual Learning 접근법을 배웁니다.

- Continual Learning이란?
- LLM에 필요한 이유
- Catastrophic Forgetting
- 주요 접근법
- 해결 과정의 어려움
- 실제 사용 사례

시작하기: [Continual Learning](https://outcomeschool.com/blog/continual-learning-in-llms)

### 7.6 Deep RL from Human Preferences란?

사람에게 두 행동 중 어느 쪽이 더 좋은지 선택하게 해 머신이 사람의 선호를 배우도록 한 2017년 논문을 살펴봅니다. 오늘날 RLHF로 이어진 핵심 아이디어입니다.

- 필요한 기초 개념
- 논문의 큰 그림
- Reward 문제
- Trajectory Segment
- 사람의 비교
- Reward Model과 Preference 수학
- Reward Model 학습
- 강화학습으로 Agent 학습
- 반복 루프와 핵심 아이디어
- Backflip 등 결과
- RLHF로 이어진 영향
- 오늘날의 형태
- 빠른 요약

시작하기: [Deep RL from Human Preferences](https://outcomeschool.com/blog/decoding-deep-rl-from-human-preferences)

### 7.7 InstructGPT란?

GPT-3가 사람의 지시를 실제로 따르도록 만든 InstructGPT와 ChatGPT로 이어진 학습 방법을 배웁니다.

- InstructGPT 논문이란?
- 필요한 기초 개념
- 큰 그림
- GPT-3만으로 부족했던 이유
- Helpful, Honest, Harmless
- 3단계 방법
- 1단계: Supervised Fine-Tuning
- 2단계: Reward Model
- 3단계: PPO를 이용한 Reinforcement Learning
- Alignment Tax
- 결과
- 오늘날의 Alignment
- 빠른 요약

시작하기: [InstructGPT](https://outcomeschool.com/blog/decoding-instructgpt)

### 7.8 RLHF란?

사람의 선호를 학습해 사전학습 LLM을 더 유용하고 정직하며 안전한 Assistant로 만드는 Reinforcement Learning from Human Feedback을 배웁니다.

- RLHF란?
- 필요한 이유
- 큰 그림
- 1단계: Supervised Fine-Tuning(SFT)
- 2단계: Reward Model 학습
- 3단계: PPO를 이용한 RL Fine-Tuning
- KL Penalty
- 전체 과정 연결
- Reward Hacking
- 흔한 실수
- Best Practice
- 빠른 요약

시작하기: [RLHF](https://outcomeschool.com/blog/reinforcement-learning-from-human-feedback-rlhf)

### 7.9 Proximal Policy Optimization(PPO)이란?

PPO의 동작 원리와 LLM RLHF 학습에서의 사용법을 배웁니다.

- Reinforcement Learning이란?
- Policy란?
- 단순 Policy Update의 문제
- PPO란?
- 핵심 아이디어: Clipping
- PPO Objective를 쉽게 이해하기
- 단계별 동작
- LLM RLHF의 PPO
- 장점
- 단점

시작하기: [PPO](https://outcomeschool.com/blog/proximal-policy-optimization-ppo)

### 7.10 Direct Preference Optimization(DPO)이란?

DPO의 단계별 동작과 RLHF(PPO)와의 차이를 배웁니다.

- RLHF와 필요한 이유
- RLHF의 문제
- DPO란?
- Preference Data란?
- DPO의 핵심 아이디어
- DPO Loss를 쉽게 이해하기
- 단계별 동작
- DPO vs RLHF(PPO)
- 장점
- 단점

시작하기: [DPO](https://outcomeschool.com/blog/direct-preference-optimization-dpo)

### 7.11 Group Relative Policy Optimization(GRPO)이란?

GRPO가 왜 필요한지, PPO와 어떤 차이가 있는지, 단계별 동작과 사용 시점을 배웁니다.

- GRPO란?
- 필요한 이유
- PPO의 문제
- GRPO 동작 방식
- 단계별 예제
- GRPO Objective
- 장점
- 실무에서 주의할 점
- 사용 시점
- 결론

시작하기: [GRPO](https://outcomeschool.com/blog/group-relative-policy-optimization-grpo)

---
