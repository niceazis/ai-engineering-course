# Regularization — 매우 자세한 한국어 학습 노트

> 원문: https://outcomeschool.com/blog/regularization-in-machine-learning
> 원저자: Amit Shekhar / Outcome School
> 문서 성격: **원문 전체 번역본이 아닌 독립적인 한국어 상세 해설·학습 노트**

## 핵심 정의

Regularization은 training error만 줄이는 대신 model complexity를 제어해 unseen data의 일반화 성능을 높이기 위한 기법이다.

---

## 1. Overfitting

- Training 성능은 매우 좋지만 validation/test 성능이 낮은 상태다.
- noise나 우연한 패턴까지 학습한 경우가 많다.

## 2. 기본 Objective

- Objective = Data Loss + lambda*Penalty.
- lambda가 커질수록 복잡한 parameter를 더 강하게 억제한다.

## 3. L1 Regularization

- Penalty = sum(|w|).
- 일부 weight를 정확히 0으로 만들 수 있다.
- Lasso와 feature selection 효과로 연결된다.

## 4. L2 Regularization

- Penalty = sum(w^2).
- weight를 전체적으로 부드럽게 shrink한다.
- Ridge와 연결된다.

## 5. Elastic Net

- L1과 L2를 함께 사용한다.
- sparsity와 안정성의 절충을 목표로 한다.

## 6. Deep Learning 기법

- Weight decay, dropout, early stopping, data augmentation도 regularization 관점에서 볼 수 있다.
- AdamW의 decoupled weight decay는 단순 L2 penalty와 구현적으로 구분할 필요가 있다.

## 7. Bias-Variance

- 복잡한 모델은 variance가 커질 수 있다.
- regularization은 일반적으로 variance를 줄이는 대신 bias를 조금 늘릴 수 있다.

## 8. Tuning

- lambda는 validation/CV로 선택한다.
- 너무 강하면 underfitting이 발생한다.
- train-validation gap과 절대 성능을 함께 본다.

## 학습 체크리스트

- 핵심 개념을 한 문장으로 설명할 수 있는가?
- 대표 수식이나 기준을 직접 설명할 수 있는가?
- 실무 예시를 하나 들 수 있는가?
- 실패하거나 오해하기 쉬운 조건을 설명할 수 있는가?

## 원문

- https://outcomeschool.com/blog/regularization-in-machine-learning
