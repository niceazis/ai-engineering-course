# 파인튜닝은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-fine-tuning-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-07-27 공개 원문을 직접 확인해 단계별 학습 흐름, 1-weight 수치 예제, Full Fine-tuning vs LoRA, 사용 기준을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Fine-tuning이란?

Fine-tuning은 이미 대규모 데이터로 학습된 **base model의 weight를 추가 데이터로 조금 더 학습해 특정 task나 style에 맞게 조정하는 과정**입니다.

처음부터 model을 새로 만드는 것이 아니라 이미 language, grammar, 일반 지식을 학습한 model에서 시작합니다.

원문의 비유는 “요리를 이미 잘하는 사람에게 Italian cuisine만 추가로 집중 훈련하는 것”입니다.

## 2. 왜 필요한가

Pretraining model은 broad capability는 강하지만 우리 조직의 구체적인 요구는 모를 수 있습니다.

예:

- 특정 고객지원 tone
- 의료/법률 response format
- 사내 전문용어
- 특정 structured output style
- 특정 task의 행동 패턴

Fine-tuning은 prompt 몇 줄로 안정적으로 고정하기 어려운 **행동 방식 자체**를 weight에 학습시키는 방법입니다.

중요한 기준:

> 새 사실을 읽게 하는 문제와 model의 행동을 바꾸는 문제를 구분해야 합니다.

사실 공급이 목적이라면 prompt/RAG가 더 간단할 수 있습니다.

## 3. Weight란 무엇인가

Model 내부에는 수백만~수천억 개의 숫자가 있고 이를 weight/parameter라고 합니다.

Training의 본질:

    prediction
      → loss
      → gradient
      → weight update

Fine-tuning도 pretraining과 기본 원리는 같습니다. 차이는 **이미 잘 학습된 weight에서 시작한다는 점**입니다.

## 4. Step 1 — Base Model 선택

선택 기준:

- task capability
- license
- context length
- tokenizer
- deployment hardware
- model size
- fine-tuning support

Model이 애초에 task에 필요한 기본 capability를 갖고 있지 않으면 작은 fine-tuning dataset만으로 새 능력을 만들기 어렵습니다.

## 5. Step 2 — Dataset 준비

일반적인 instruction tuning example:

    input:
      "고객이 환불을 요청했습니다..."

    target:
      "불편을 드려 죄송합니다. 주문번호를..."

좋은 dataset의 조건:

- 실제 production distribution과 비슷함
- target이 일관됨
- 잘못된 example 제거
- 중복/누수 방지
- train/validation/test 분리

원문도 “작고 깨끗한 data가 크고 지저분한 data보다 낫다”고 강조합니다.

## 6. Step 3 — Model Prediction

각 training example의 input을 model에 넣으면 token별 logits가 나옵니다.

Teacher forcing을 쓰는 language-model fine-tuning에서는 정답 response의 이전 token을 조건으로 다음 정답 token을 예측하게 합니다.

## 7. Step 4 — Loss 측정

Predicted probability와 target token의 차이를 cross-entropy loss로 계산합니다.

개념적으로:

    Loss = -log P(correct token)

정답 token에 높은 확률을 줄수록 loss가 작아집니다.

## 8. Step 5 — Backpropagation

Loss를 각 weight에 대해 미분해 gradient를 계산합니다.

    grad_w = dLoss / dw

Optimizer가 learning rate를 사용해 weight를 갱신합니다.

    w_new = w_old - lr * grad_w

실제 LLM에서는 수십억 weight가 동시에 업데이트됩니다.

## 9. 원문의 1-Weight 수치 예제

교육용 model:

    weight = 2.0
    input = 4
    target = 10

Prediction:

    4 × 2.0 = 8.0

Error:

    10 - 8 = 2

원문은 단순 update rule로:

    learning_rate = 0.05
    adjustment = 0.05 × 2 × 4 = 0.4

따라서:

    weight = 2.0 + 0.4 = 2.4

새 prediction:

    4 × 2.4 = 9.6

반복:

    8.00 → 9.60 → 9.92 → 9.98 → 10.00

실제 neural network는 단순 error×input 공식이 아니라 backpropagation으로 gradient를 계산하지만, “조금씩 loss가 줄어드는 방향으로 weight를 이동한다”는 직관을 보여 주는 예입니다.

## 10. Epoch

Dataset 전체를 한 번 학습하는 것을 epoch라고 합니다.

Too few epochs:

- underfitting

Too many epochs:

- overfitting
- training examples memorization
- base capability degradation

Validation loss와 task metric을 보면서 early stopping 여부를 결정해야 합니다.

## 11. Catastrophic Forgetting

특정 domain data만 계속 학습하면 base model의 기존 능력이 약해질 수 있습니다.

예:

    general model
      → sports-only fine-tuning
      → sports 성능 상승
      → math/history 일부 저하 가능

이를 catastrophic forgetting이라고 합니다.

Mitigation:

- replay/mixed data
- 낮은 learning rate
- PEFT
- regularization
- task-specific adapters

## 12. Full Fine-Tuning

모든 trainable weight를 업데이트합니다.

장점:

- 가장 큰 adaptation capacity
- architecture 전체가 task에 맞게 움직임

단점:

- optimizer state와 gradient 때문에 큰 memory 필요
- training cost 큼
- task별 full checkpoint 저장 필요
- forgetting 위험 큼

## 13. LoRA

원문은 LoRA를 실용적인 대안으로 소개합니다.

LoRA:

- base weight W는 freeze
- 작은 low-rank A/B matrix만 학습
- task-specific delta를 추가

즉 전체 model을 다시 저장하지 않고 작은 adapter만 저장할 수 있습니다.

## 14. Fine-Tuning vs RAG

### Fine-tuning에 적합

- style/tone
- output format
- task behavior
- domain-specific decision pattern

### RAG에 적합

- 최신 facts
- 자주 바뀌는 knowledge
- source citation
- 대규모 external documents

실전에서는 둘을 함께 쓸 수도 있습니다.

    fine-tuned behavior
      + RAG knowledge

## 15. Fine-Tuning 전에 먼저 확인할 것

1. Prompt만으로 해결되는가?
2. RAG로 facts만 공급하면 되는가?
3. Dataset quality가 충분한가?
4. Evaluation set이 있는가?
5. Base model의 license/deployment 조건은?
6. Full FT가 필요한가, LoRA로 충분한가?

## 16. 평가

Training loss만 보면 안 됩니다.

별도 holdout set에서:

- task accuracy
- format compliance
- safety
- factuality
- latency
- regression on general capability

를 확인해야 합니다.

## 핵심 정리

- Fine-tuning은 이미 학습된 base model을 specific task에 맞게 추가 학습하는 과정입니다.
- Input→prediction→loss→backprop→weight update를 반복합니다.
- 원문의 1-weight 예에서는 2.0→2.4로 update되어 prediction이 8.0→9.6으로 개선됩니다.
- Full fine-tuning은 모든 weight, LoRA는 작은 adapter만 업데이트합니다.
- 새 knowledge 공급만 목적이면 RAG가 더 적합할 수 있습니다.
- 가장 중요한 변수는 dataset quality와 independent evaluation입니다.

## 원문

- https://outcomeschool.com/blog/how-does-fine-tuning-work
