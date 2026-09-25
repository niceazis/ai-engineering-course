# RLHF란? 인간 피드백을 이용한 강화학습 — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/reinforcement-learning-from-human-feedback-rlhf  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문을 직접 확인해 SFT→Preference→Reward Model→PPO, KL penalty 수치 예, reward hacking과 best practice를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. RLHF의 목적

RLHF(Reinforcement Learning from Human Feedback)는 인간이 선호하는 response를 reward signal로 바꿔 language model을 정렬하는 방법입니다.

문제:

    next-token likelihood가 높다
    ≠ human이 좋은 답이라고 생각한다

RLHF는 human preference를 optimization target에 넣습니다.

## 2. 전체 Pipeline

원문의 큰 흐름:

    pretrained base model
      → supervised fine-tuning
      → preference data
      → reward model
      → RL fine-tuning(PPO)
      → aligned model

각 단계가 다른 문제를 해결합니다.

## 3. Stage 1 — SFT

High-quality prompt/response demonstration을 모읍니다.

Model이:

- 질문에 답하는 format
- instruction following
- 기본 tone

을 imitation learning으로 익힙니다.

SFT를 생략하고 base model에 바로 RL을 걸면 exploration이 너무 넓고 reward hacking 가능성이 커집니다.

## 4. Stage 2 — Preference Collection

한 prompt에 여러 response를 생성하고 human이 ranking합니다.

예:

    Response A: chosen
    Response B: rejected

Human이 직접 절대 reward를 쓰는 것이 아니라 상대 preference를 제공합니다.

## 5. Reward Model

Reward Model:

    RM(prompt, response) → scalar

Pairwise loss는 chosen의 reward가 rejected보다 높아지게 합니다.

    P(chosen > rejected)
      = sigmoid(r_chosen - r_rejected)

Reward model은 human preference의 proxy입니다.

## 6. Stage 3 — RL Fine-Tuning

Policy model이 response를 생성합니다.

Reward model이 score를 줍니다.

PPO가 policy를 조금씩 update합니다.

반복:

    prompt
      → response
      → RM score
      → advantage
      → PPO update

## 7. 왜 PPO인가

RL update를 너무 크게 하면 language model이 쉽게 무너집니다.

PPO는 old policy와 new policy의 probability ratio를 clipping해 큰 update를 제한합니다.

그래서 대규모 language policy optimization에 널리 사용됐습니다.

## 8. KL Penalty

원문 objective:

    Objective
      = Reward(response)
      - beta * KL(LLM, SFT_model)

KL divergence는 current policy와 SFT/reference policy의 distribution 차이를 측정합니다.

Model이 reward를 올리더라도 reference에서 너무 멀어지면 penalty를 받습니다.

## 9. 원문의 KL 수치 예

가정:

    reward = 3.0
    KL = 4.0
    beta = 0.1

최종 objective:

    3.0 - 0.1 * 4.0
    = 2.6

만약 drift가 커져:

    KL = 20

이면:

    3.0 - 0.1 * 20
    = 1.0

Raw reward는 같아도 reference에서 지나치게 멀어지면 가치가 크게 떨어집니다.

원문은 beta의 illustrative range로 약 0.01~0.2를 제시합니다.

## 10. Per-Token KL

실제 구현에서는 whole response 끝에 KL 한 번만 계산하기보다 generation token마다 KL penalty를 reward shaping에 반영하는 경우가 많습니다.

개념:

    r_t'
      = r_t
      - beta * KL_t

Response 마지막에 RM reward가 들어가고 token-level KL이 cumulative return에 포함될 수 있습니다.

## 11. Reward Hacking

Policy가 Reward Model의 weakness를 찾아 높은 score를 받지만 실제 human preference에는 나쁜 response를 만들 수 있습니다.

예:

- 지나치게 장황하면 reward가 높게 측정
- 특정 phrase 반복
- scorer가 좋아하는 형식만 과도하게 사용

이를 reward hacking이라고 합니다.

## 12. Reward Model은 Ground Truth가 아니다

Reward Model은 finite preference dataset으로 학습된 approximation입니다.

따라서:

- annotator disagreement
- distribution shift
- bias
- calibration error

가 있습니다.

RM score가 높다고 실제 user value가 항상 높은 것은 아닙니다.

## 13. Preference Data Quality

좋은 preference dataset은 단순히 data 수가 많은 것이 아니라:

- difficult comparison 포함
- instruction distribution 다양
- label guideline 일관
- ambiguous sample 처리
- annotator quality 관리

가 필요합니다.

## 14. RLHF의 비용

여러 model을 동시에 사용합니다.

- policy
- reference
- reward model
- value/critic(PPO)

큰 LLM에서는 memory/compute가 매우 큽니다.

이 복잡성이 DPO, GRPO 같은 대안이 등장한 배경입니다.

## 15. Common Mistakes

원문 핵심:

### SFT 생략

초기 policy가 너무 불안정.

### 약한 Reward Model

Wrong reward를 최적화.

### KL 무시

Policy가 scorer에 맞춰 이상한 distribution으로 drift.

### RM을 Truth로 간주

Human preference proxy임을 잊음.

## 16. Best Practice

- SFT baseline을 먼저 강하게 만들기
- holdout preference eval
- RM accuracy와 calibration 별도 측정
- KL/reward curve 모니터링
- policy output human audit
- reward hacking test
- task별 regression suite

## 17. RLHF vs DPO

RLHF/PPO:

    preference data
      → reward model
      → online generation
      → PPO

DPO:

    preference pair
      → direct supervised-style objective

DPO가 단순하지만 online exploration/reward shaping이 필요한 경우 RL이 더 유연할 수 있습니다.

## 핵심 정리

- RLHF는 human preference를 learned reward로 바꿔 policy를 강화학습합니다.
- SFT, Reward Model, PPO 세 단계가 핵심입니다.
- KL penalty가 reference model에서 과도하게 drift하는 것을 막습니다.
- 원문 예에서 reward 3, KL 4, beta 0.1이면 objective 2.6입니다.
- Reward Model은 human preference proxy이지 ground truth가 아닙니다.
- RLHF의 높은 system complexity가 DPO/GRPO 같은 단순화 방법을 촉진했습니다.

## 원문

- https://outcomeschool.com/blog/reinforcement-learning-from-human-feedback-rlhf
