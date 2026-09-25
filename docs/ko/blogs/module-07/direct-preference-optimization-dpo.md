# Direct Preference Optimization(DPO)이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/direct-preference-optimization-dpo  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문을 직접 확인해 preference pair, reference model, beta, DPO loss와 PPO-RLHF 비교를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. DPO가 나온 이유

Classic RLHF:

    preference data
      → reward model
      → online policy generation
      → PPO
      → value model

Pipeline이 복잡하고 memory/engineering cost가 큽니다.

DPO는 질문합니다.

> Reward Model과 PPO를 따로 학습하지 않고 chosen/rejected preference pair에서 policy를 직접 학습할 수 없는가?

## 2. Preference Data

Dataset 한 item:

    prompt x
    chosen y_w
    rejected y_l

예:

    prompt:
      "건강한 아침 식사를 추천해줘."

    chosen:
      "오트밀, 계란, 과일..."

    rejected:
      "사탕과 탄산음료..."

Human 또는 preference source가 chosen이 더 좋다고 label합니다.

## 3. Reference Model

DPO는 일반적으로 frozen reference policy pi_ref를 둡니다.

보통 SFT checkpoint입니다.

현재 policy pi_theta가 chosen/rejected에 부여하는 probability를 reference와 비교합니다.

Reference는 policy가 preference data에 맞추면서도 base behavior에서 무제한 drift하지 않게 하는 anchor입니다.

## 4. 핵심 직관

우리가 원하는 것:

    pi_theta(chosen | x)
      ↑

    pi_theta(rejected | x)
      ↓

하지만 absolute probability만 보면 length/model scale 영향이 있습니다.

DPO는 reference 대비 얼마나 chosen을 더 선호하게 됐는지를 비교합니다.

## 5. 원문 DPO Loss

원문 표기:

    Loss =
      -log sigmoid(
        beta * (
          log_ratio_chosen
          - log_ratio_rejected
        )
      )

여기서:

    log_ratio_chosen
      = log pi_theta(chosen|x)
        - log pi_ref(chosen|x)

    log_ratio_rejected
      = log pi_theta(rejected|x)
        - log pi_ref(rejected|x)

## 6. Margin

차이:

    margin
      = log_ratio_chosen
        - log_ratio_rejected

가 클수록 current policy가 reference보다 chosen을 더 상대적으로 선호하게 됐다는 뜻입니다.

Loss는 margin을 positive로 키웁니다.

## 7. Beta

원문은 common example로:

    beta = 0.1

을 언급합니다.

Beta는 reference에 대한 regularization strength와 preference update scale을 조절합니다.

원문 설명 기준:

- beta가 작음 → 더 큰 변화 허용
- beta가 큼 → reference에 더 가까움

실제 library의 parameter semantics와 scaling은 구현 문서를 확인해야 합니다.

## 8. Training Step

1. Prompt/chosen/rejected batch load
2. Current policy의 sequence log-prob 계산
3. Reference policy log-prob 계산
4. chosen/rejected log-ratio 계산
5. DPO loss
6. Backprop으로 current policy update
7. Reference는 frozen

Online rollout이나 reward model inference가 필요하지 않습니다.

## 9. 왜 RL처럼 보이지 않는데 RLHF 대안인가

DPO는 KL-regularized RLHF objective의 optimal policy와 preference model 관계를 algebraically 정리해 **binary classification 형태의 loss로 policy를 직접 최적화**합니다.

그래서 explicit reward model이 없어도 preference를 policy에 반영할 수 있습니다.

## 10. DPO vs PPO-RLHF

| 항목 | PPO RLHF | DPO |
| --- | --- | --- |
| Reward Model | 필요 | 불필요 |
| Value Model | 필요 | 불필요 |
| Online rollout | 필요 | 보통 불필요 |
| Preference pair | RM 학습에 사용 | 직접 policy 학습 |
| Implementation | 복잡 | 상대적으로 단순 |
| Exploration | 가능 | offline data에 제한 |

## 11. DPO 장점

- 구현 단순
- GPU memory 절감
- training 안정성 좋음
- SFT pipeline과 유사한 batch training
- preference dataset만 있으면 시작 가능

## 12. 한계

### Offline Distribution

Dataset에 없는 새로운 behavior를 online exploration하기 어렵습니다.

### Preference Quality

Chosen/rejected가 noisy하면 그대로 학습됩니다.

### Reference Dependence

Reference checkpoint가 너무 약하거나 distribution이 다르면 결과가 나쁠 수 있습니다.

### Reward Shaping Flexibility

여러 online reward signal을 동적으로 조합하는 PPO보다 제한적일 수 있습니다.

## 13. Reward Hacking은 사라지는가

Explicit reward model이 없으므로 reward-model exploit은 줄지만, preference dataset의 bias/shortcut을 과도하게 학습할 수 있습니다.

즉 optimization target의 misspecification 문제 자체가 사라지는 것은 아닙니다.

## 14. 언제 DPO를 선택할까

- high-quality preference pairs가 있음
- PPO infrastructure를 피하고 싶음
- offline post-training이면 충분
- 안정적이고 간단한 preference alignment 필요

반대로 environment interaction과 online verifier feedback을 반복해야 하는 reasoning RL에는 PPO/GRPO 계열이 더 자연스러울 수 있습니다.

## 핵심 정리

- DPO는 chosen/rejected pair로 policy를 직접 학습합니다.
- Reward Model과 Value Model, PPO loop가 필요 없습니다.
- Current policy의 chosen/rejected probability를 frozen reference와 비교합니다.
- 원문 loss는 beta × (chosen log-ratio - rejected log-ratio)에 sigmoid를 적용합니다.
- Offline preference alignment에는 단순하고 강력하지만 online exploration capability는 제한적입니다.

## 원문

- https://outcomeschool.com/blog/direct-preference-optimization-dpo
