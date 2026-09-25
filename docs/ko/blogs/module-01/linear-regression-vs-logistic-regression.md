# 선형 회귀 vs 로지스틱 회귀 — 원문 흐름을 따라가는 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/linear-regression-vs-logistic-regression  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 핵심 식과 비교 흐름을 유지하면서 한국어로 다시 설명한 상세 학습 노트입니다.

## 먼저 구분해야 할 것: Regression vs Classification

두 알고리즘 이름을 비교하기 전에 **무엇을 예측하는 문제인지**부터 구분해야 합니다.

### Regression

연속적인 숫자를 예측합니다.

- 집값
- 온도
- 키와 몸무게
- 수요량

### Classification

정해진 범주를 예측합니다.

- spam / not spam
- disease / no disease
- red / blue / green

이 구분을 놓치면 “Logistic **Regression**인데 왜 classification에 쓰지?”라는 혼란이 생깁니다.

## 1. Linear Regression

Linear Regression은 입력 feature와 출력 사이의 선형 관계를 이용해 **연속값**을 예측합니다.

원문의 기본 식은:

```text
y = w1*x1 + w2*x2
```

입니다.

- `x1, x2`: 입력 feature
- `w1, w2`: 학습할 weight
- `y`: 예측할 연속값

입력이 하나라면 직선, 입력이 여러 개라면 더 높은 차원의 hyperplane을 데이터에 맞추는 것으로 이해할 수 있습니다.

### 예: 집값

```text
x1 = 집 크기
x2 = 입지 점수
y  = 집값
```

모델은 실제 집값과 예측 집값의 차이를 작게 만드는 weight를 찾습니다.

원문에서는 대표적인 학습 loss로 **Mean Squared Error(MSE)**를 연결합니다.

```text
MSE = 평균((실제값 - 예측값)^2)
```

오차를 제곱하므로 큰 오차에 더 큰 패널티가 주어집니다.

### 출력 범위

Linear Regression의 출력은 0~1에 제한되지 않습니다.

```text
... -10, -1, 0, 0.7, 5, 100 ...
```

필요한 연속값을 그대로 낼 수 있다는 것이 장점이지만, 이것이 binary classification에 그대로 쓰기 어려운 이유이기도 합니다.

## 2. Logistic Regression

이름에는 Regression이 들어가지만 주 용도는 **classification**입니다.

출발점은 Linear Regression과 매우 비슷합니다.

```text
z = w1*x1 + w2*x2
```

그러나 여기서 `z`를 최종 출력으로 사용하지 않습니다.

다음으로 sigmoid 함수를 통과시킵니다.

```text
σ(z) = 1 / (1 + e^(-z))
```

Sigmoid의 출력은 항상 0과 1 사이입니다.

```text
linear score z
      ↓
   sigmoid
      ↓
probability 0~1
```

예를 들어 출력이 0.87이라면 특정 class 1에 속할 확률을 0.87로 해석할 수 있습니다.

## 3. 확률을 class로 바꾸기

원문의 단순한 binary classification 예에서는 threshold 0.5를 사용합니다.

```text
p >= 0.5 -> Class 1
p <  0.5 -> Class 0
```

실무에서 threshold는 항상 0.5일 필요는 없습니다.

False Positive와 False Negative의 비용이 다르다면 threshold를 조정할 수 있습니다. 이 부분은 Precision/Recall과 직접 연결됩니다.

## 4. 왜 이름이 Logistic Regression인가?

핵심은 내부 계산의 첫 단계입니다.

```text
z = w1*x1 + w2*x2
```

먼저 입력의 **선형 결합**을 계산합니다.

그 다음:

```text
p = sigmoid(z)
```

로 확률로 변환합니다.

즉 구조를 단순화하면:

```text
Regression-like linear score
          ↓
Logistic/Sigmoid transformation
          ↓
Probability
          ↓
Class decision
```

입니다.

그래서 최종 작업은 classification이지만 Logistic Regression이라는 이름이 남아 있습니다.

## 5. Loss도 다르다

원문은 다음 차이를 강조합니다.

### Linear Regression

주로 MSE 같은 회귀 loss를 사용합니다.

```text
실제 연속값과 예측 연속값의 거리
```

### Logistic Regression

주로 Cross-Entropy 계열 loss를 사용합니다.

binary classification에서는 모델이 정답 class에 높은 확률을 주도록 학습합니다.

예를 들어 정답이 1인데:

```text
p(class=1) = 0.95
```

라면 좋은 예측이고,

```text
p(class=1) = 0.05
```

라면 큰 loss를 받습니다.

## 6. 같은 입력을 넣어도 출력의 의미가 다르다

예를 들어 `x1`, `x2`가 환자의 검사 수치라고 하겠습니다.

Linear Regression이라면:

```text
ŷ = 137.4
```

처럼 연속값 자체를 예측하는 문제에 적합합니다.

Logistic Regression이라면:

```text
z = 2.1
sigmoid(z) ≈ 0.891
```

처럼 class 1에 속할 확률을 만들고 이를 이용해 분류합니다.

## 7. 핵심 비교

| 항목 | Linear Regression | Logistic Regression |
|---|---|---|
| 문제 | Regression | Classification |
| 최종 출력 | 연속값 | 0~1 확률 → class |
| 기본 계산 | 선형 결합 | 선형 결합 |
| 추가 변환 | 없음 | Sigmoid |
| 대표 loss | MSE | Cross-Entropy |
| 출력 범위 | 제한 없음 | 0~1 |
| 예 | 집값, 온도 | 스팸, 질병 여부 |

## 8. 모델 선택 체크리스트

### Linear Regression을 먼저 검토할 상황

- target이 숫자이고 연속적입니다.
- 입력과 출력의 관계를 선형 모델로 설명해 볼 가치가 있습니다.
- baseline을 빠르게 만들고 싶습니다.

### Logistic Regression을 먼저 검토할 상황

- target이 binary class입니다.
- 확률 출력이 필요합니다.
- 해석 가능한 간단한 classification baseline이 필요합니다.

## 9. 중요한 연결: Decision Boundary

Logistic Regression은 확률을 만든 뒤 threshold를 적용합니다.

```text
w1*x1 + w2*x2 = 어떤 기준값
```

이 경계의 한쪽은 class 0, 다른 쪽은 class 1이 됩니다.

따라서 Logistic Regression도 입력 공간에서는 **선형 decision boundary**를 만드는 모델이라는 점을 기억하면 좋습니다.

## 10. 반드시 기억할 문장

```text
Linear Regression:
linear score 자체가 예측값

Logistic Regression:
linear score -> sigmoid -> probability -> class
```

두 모델은 시작 계산은 닮았지만 **문제 유형, 출력 의미, loss**가 다릅니다.

## 이해 확인

1. 집값을 0/1로 분류하지 않고 실제 금액으로 예측하려면 어느 쪽이 자연스러운가요?
2. Logistic Regression에서 sigmoid가 없다면 어떤 문제가 생길까요?
3. threshold를 0.5에서 0.2로 낮추면 일반적으로 positive 판정 수는 어떻게 변할까요?

## 원문 및 연결 학습

- 원문: https://outcomeschool.com/blog/linear-regression-vs-logistic-regression
- 이전: [지도학습 vs 비지도학습](supervised-vs-unsupervised-learning.md)
- 다음: [Feature Engineering](feature-engineering.md)
- 모듈 1: [머신러닝 기초](../../module-01.md)
