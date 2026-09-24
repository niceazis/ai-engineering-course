# 선형 회귀 vs 로지스틱 회귀 — 매우 자세한 한국어 학습 노트

> 원문: https://outcomeschool.com/blog/linear-regression-vs-logistic-regression
> 원저자: Amit Shekhar / Outcome School
> 문서 성격: **원문 전체 번역본이 아닌 독립적인 한국어 상세 해설·학습 노트**

## 핵심 정의

Linear Regression은 연속값을 예측하고, Logistic Regression은 선형 점수를 sigmoid로 확률화해 분류에 사용한다.

---

## 1. Regression과 Classification

- Regression은 집값·온도처럼 연속값을 예측한다.
- Classification은 spam/normal처럼 class를 예측한다.

## 2. Linear Regression

- 기본식은 y_hat = w1*x1 + ... + wn*xn + b 이다.
- 보통 MSE 같은 loss를 최소화한다.
- 출력 범위가 제한되지 않아 확률 예측에는 부적합하다.

## 3. Logistic Regression

- 먼저 z = w^T x + b를 계산한다.
- sigmoid(z) = 1/(1+exp(-z))로 0~1 확률을 만든다.
- Binary Cross-Entropy가 대표 loss다.

## 4. Decision Threshold

- 기본 0.5가 흔하지만 업무 비용에 따라 바꿀 수 있다.
- threshold를 낮추면 recall이 오르고 false positive가 늘 수 있다.
- threshold는 validation set에서 조정해야 한다.

## 5. Decision Boundary

- p=0.5는 z=0과 대응한다.
- 기본 Logistic Regression의 경계는 feature space에서 선형이다.
- 복잡한 비선형 패턴에는 feature transformation이나 다른 모델이 필요할 수 있다.

## 6. Regularization

- L1은 sparsity를 유도해 feature selection 효과를 낼 수 있다.
- L2는 weight를 전체적으로 작게 만든다.
- 둘 다 overfitting을 줄이는 데 사용된다.

## 7. Calibration

- 0.8이라는 출력이 실제 80% 빈도와 잘 맞는지 calibration을 확인할 수 있다.
- 위험 기반 의사결정에서는 확률 calibration이 중요하다.

## 8. 선택 기준

- target이 연속값이면 Linear Regression 후보.
- target이 binary/categorical이면 Logistic Regression 후보.
- 이름보다 출력 형태와 loss를 보고 구분한다.

## 학습 체크리스트

- 이 개념을 한 문장으로 설명할 수 있는가?
- 실제 서비스 예시를 하나 들 수 있는가?
- 실패하거나 오해하기 쉬운 조건을 설명할 수 있는가?
- 이전/다음 레슨과의 연결을 설명할 수 있는가?

## 원문

- https://outcomeschool.com/blog/linear-regression-vs-logistic-regression
