# InstructGPT란? GPT-3가 지시를 따르게 된 방법 — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/decoding-instructgpt  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 공식 2026-08 뉴스레터에서 확인한 3단계 RLHF 구조와 InstructGPT 원 논문의 공개 결과를 교차검증해 독립적으로 다시 쓴 한국어 상세 해설입니다. 현재 Outcome School 본문 URL은 웹 캐시에서 직접 열리지 않아 이 한계를 명시합니다.

## 1. GPT-3만으로 왜 부족했나

Pretraining objective는 다음 token prediction입니다.

    text prefix
      → predict next token

이 objective는 internet text의 통계적 pattern을 잘 배우게 하지만:

    "사용자의 지시를 정확히 따른다"
    "도움이 된다"
    "안전하다"
    "모르면 솔직히 말한다"

를 직접 최적화하지 않습니다.

즉:

    next-token prediction
    ≠ instruction following

이 gap이 alignment 문제입니다.

## 2. InstructGPT의 목표

InstructGPT는 GPT-3 기반 model을 사람의 instruction preference에 맞추는 것이 목표였습니다.

핵심 pipeline:

    Pretrained GPT-3
      → SFT
      → Reward Model
      → PPO RL
      → InstructGPT

Outcome School은 이 recipe가 이후 ChatGPT로 이어졌다는 점을 강조합니다.

## 3. Step 1 — Supervised Fine-Tuning

Human labeler가 prompt에 대해 좋은 demonstration response를 작성합니다.

예:

    Prompt:
      "이 문단을 두 문장으로 요약해 주세요."

    Human demonstration:
      "..."

Base model을 이 pair들에 supervised fine-tuning합니다.

이 결과 SFT model은 instruction-response format을 기본적으로 익힙니다.

## 4. 왜 SFT만으로 충분하지 않은가

좋은 response는 하나가 아닙니다.

두 response가 모두 문법적으로 맞아도:

- 더 helpful
- 더 honest
- 더 safe
- 더 concise

한 쪽이 사람에게 더 선호될 수 있습니다.

SFT의 single target token loss만으로 이런 상대 preference를 충분히 반영하기 어렵습니다.

## 5. Step 2 — Preference Data

같은 prompt에 model response를 여러 개 생성합니다.

Human labeler가 순위를 매깁니다.

예:

    A > C > B > D

이를 pairwise data로 바꿀 수 있습니다.

    chosen=A, rejected=B
    chosen=A, rejected=D
    chosen=C, rejected=B
    ...

이 preference dataset으로 Reward Model을 학습합니다.

## 6. Reward Model

Reward Model은:

    prompt + response
      → scalar reward

를 출력합니다.

좋은 response가 높은 score를 갖게 학습합니다.

Pairwise probability를 단순화하면:

    P(A preferred to B)
      = sigmoid(r_A - r_B)

Human이 A를 선호하면 이 probability가 커지도록 loss를 줄입니다.

## 7. Step 3 — PPO

이제 SFT model이 prompt에 response를 생성합니다.

Reward Model이 score를 줍니다.

PPO가 model을 update해 높은 reward response를 더 잘 생성하게 합니다.

    prompt
      → policy model
      → response
      → reward model
      → reward
      → PPO update

## 8. KL Penalty

Reward Model만 최대화하면 model이 scorer의 약점을 이용할 수 있습니다.

그래서 SFT/reference model에서 너무 멀어지지 않도록 KL penalty를 사용합니다.

개념:

    objective
      = reward
      - beta * KL(policy || reference)

이 제약이 language quality와 base behavior를 유지하는 leash 역할을 합니다.

## 9. Helpful, Honest, Harmless

Alignment를 설명할 때 흔히 HHH를 사용합니다.

### Helpful

사용자의 실제 목표를 돕습니다.

### Honest

모르는 것을 아는 척하지 않고 근거 없는 claim을 줄입니다.

### Harmless

유해한 행동을 줄입니다.

실제 annotation guideline은 이러한 value를 구체적인 ranking rule로 operationalize해야 합니다.

## 10. 결과에서 중요한 점

InstructGPT 연구의 유명한 결과는 **1.3B InstructGPT가 human preference 평가에서 175B GPT-3보다 선호될 수 있었다**는 점입니다.

의미:

> raw parameter count보다 alignment/post-training이 user-perceived usefulness에 큰 영향을 줄 수 있다.

이는 작은 model이 모든 benchmark에서 큰 model보다 낫다는 뜻은 아닙니다.

## 11. Alignment Tax

Post-training으로 preference를 최적화하면 일부 pretraining benchmark 성능이 떨어질 수 있습니다.

이를 alignment tax라고 부릅니다.

InstructGPT 연구에서는 pretraining data를 RLHF mixture에 섞어 일부 regression을 줄이는 접근을 사용했습니다.

핵심은 alignment도 multi-objective optimization이라는 점입니다.

## 12. 왜 Reward Model이 완전한 Truth가 아닌가

Reward Model은 human label의 근사 model입니다.

따라서:

- label bias
- scorer blind spot
- distribution shift

가 있습니다.

PPO policy가 reward model을 너무 강하게 최적화하면 reward hacking이 생길 수 있습니다.

## 13. 현대 Alignment로 이어진 변화

InstructGPT recipe 이후 다양한 변형이 생겼습니다.

- DPO: reward model + PPO 없이 preference pair로 직접 학습
- RLAIF: human 대신 AI feedback 활용
- Constitutional AI: 원칙 기반 critique/revision
- RLVR: code/math verifier reward
- GRPO: group-relative baseline으로 value model 제거

그래도 SFT→preference learning→policy improvement이라는 큰 흐름은 현대 post-training의 기본 언어가 됐습니다.

## 핵심 정리

- GPT-3 pretraining objective는 instruction following 자체를 최적화하지 않습니다.
- InstructGPT는 SFT → Reward Model → PPO라는 3단계 RLHF recipe를 사용했습니다.
- Human demonstration으로 기본 instruction behavior를 학습하고, ranking으로 preference reward를 학습합니다.
- PPO가 reward를 높이되 KL penalty로 SFT/reference model에서 너무 멀어지지 않게 합니다.
- 1.3B InstructGPT가 human preference에서 175B GPT-3보다 선호된 결과는 post-training의 중요성을 보여 줍니다.
- 이 recipe가 이후 ChatGPT 계열 alignment의 중요한 기반이 됐습니다.

## 원문

- https://outcomeschool.com/blog/decoding-instructgpt
