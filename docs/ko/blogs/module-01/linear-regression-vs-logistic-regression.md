# 선형 회귀 vs 로지스틱 회귀 — 원문 흐름을 따라가는 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/linear-regression-vs-logistic-regression  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: **원문의 핵심 비교 구조를 따라가며 한국어로 다시 설명한 상세 학습 노트**

---

## 이 글에서 반드시 이해해야 할 것

이 글의 핵심은 이름에 둘 다 “Regression”이 들어간다고 해서 같은 종류의 문제를 푸는 것이 아니라는 점입니다.

- Linear Regression: **숫자값 예측**
- Logistic Regression: **클래스 확률 예측**

---

## 1. 먼저 문제 유형부터 구분

### Regression

연속적인 값을 예측합니다.

예:

- 집값 5.3억
- 온도 27.4도
- 배송시간 18.2분

### Classification

범주를 예측합니다.

예:

- 스팸 / 정상
- 질병 있음 / 없음
- 구매 / 미구매

Linear Regression은 Regression 문제에, Logistic Regression은 Classification 문제에 사용됩니다.

---

## 2. Linear Regression

가장 단순한 식은 다음과 같습니다.

```text
ŷ = w*x + b
```

여러 feature라면:

```text
ŷ = w1*x1 + w2*x2 + ... + wn*xn + b
```

입력 feature의 가중합을 그대로 출력합니다.

예를 들어 면적만으로 집값을 예측한다고 하겠습니다.

```text
집값 = 0.08 * 면적 + 1.2
```

면적이 커질수록 예측 가격도 선형적으로 증가합니다.

---

## 3. Linear Regression의 학습 목표

모델이 실제값과 비슷한 값을 내도록 weight와 bias를 학습합니다.

대표적인 loss가 MSE입니다.

```text
MSE = 평균((y - ŷ)^2)
```

학습 과정은:

```text
예측 -> 실제값과 비교 -> MSE 계산 -> weight 수정
```

을 반복합니다.

---

## 4. 왜 Linear Regression으로 분류를 하면 안 되는가

이진 분류에서 정답을:

```text
0 = 정상
1 = 스팸
```

이라고 두면 Linear Regression으로도 숫자를 출력할 수는 있습니다.

하지만 출력 범위가 제한되지 않습니다.

```text
-0.3
0.7
1.4
```

같은 값이 나올 수 있습니다.

확률은 0~1 사이여야 하므로 그대로 쓰기 어렵습니다.

이 문제를 해결하는 것이 Logistic Regression입니다.

---

## 5. Logistic Regression의 첫 단계는 여전히 선형식이다

Logistic Regression도 먼저 다음 값을 계산합니다.

```text
z = w1*x1 + w2*x2 + ... + wn*xn + b
```

여기까지는 Linear Regression과 비슷합니다.

차이는 그다음입니다.

이 `z`를 Sigmoid 함수에 넣습니다.

```text
sigmoid(z) = 1 / (1 + e^(-z))
```

Sigmoid 출력은 항상 0과 1 사이입니다.

따라서 확률처럼 해석할 수 있습니다.

---

## 6. Sigmoid 직관

예를 들어:

```text
z = 0
```

이면:

```text
sigmoid(0) = 0.5
```

`z`가 매우 큰 양수이면 출력은 1에 가까워지고, 매우 큰 음수이면 0에 가까워집니다.

```text
z << 0  ->  p ≈ 0
z = 0   ->  p = 0.5
z >> 0  ->  p ≈ 1
```

---

## 7. 분류는 Threshold로 결정한다

모델이 다음과 같이 출력했다고 하겠습니다.

```text
p(y=1) = 0.82
```

기본 threshold를 0.5로 두면:

```text
0.82 >= 0.5 -> class 1
```

반대로:

```text
0.31 < 0.5 -> class 0
```

하지만 threshold가 반드시 0.5일 필요는 없습니다.

의료 선별처럼 놓치는 비용이 큰 문제에서는 0.3처럼 낮출 수 있습니다.

---

## 8. Logistic Regression의 Loss

Binary Classification에서는 Binary Cross-Entropy를 흔히 사용합니다.

핵심은:

- 정답이 1인데 확률을 0.99로 예측하면 loss가 작음
- 정답이 1인데 0.01로 예측하면 loss가 매우 큼

즉 단순히 맞고 틀림만 보는 것이 아니라 **확률의 자신감까지 평가**합니다.

---

## 9. Decision Boundary

Logistic Regression에서:

```text
p = 0.5
```

는:

```text
z = 0
```

과 같습니다.

따라서 기본적인 Logistic Regression은 feature space에서 선형 경계를 만듭니다.

2차원에서는 직선, 3차원에서는 평면에 해당합니다.

---

## 10. 예제로 비교

학생의 공부시간으로 점수를 예측한다면:

```text
공부시간 -> 예상 시험점수
```

출력이 숫자이므로 Linear Regression이 자연스럽습니다.

반면:

```text
공부시간 -> 합격/불합격
```

이면 Logistic Regression이 적합합니다.

---

## 11. 둘의 차이를 한 표로 정리

| 항목 | Linear Regression | Logistic Regression |
|---|---|---|
| 문제 | Regression | Classification |
| 출력 | 연속값 | 0~1 확률 |
| 핵심 함수 | 선형식 | 선형식 + Sigmoid |
| 대표 Loss | MSE | Binary Cross-Entropy |
| 예 | 집값 | 스팸 여부 |

---

## 12. Regularization

두 모델 모두 overfitting을 줄이기 위해 regularization을 적용할 수 있습니다.

### L1

```text
Penalty = Σ|w|
```

일부 weight를 0으로 만들 수 있습니다.

### L2

```text
Penalty = Σw²
```

weight 전체를 부드럽게 줄이는 효과가 있습니다.

---

## 13. Logistic Regression이 단순하지만 여전히 중요한 이유

현대에는 복잡한 모델이 많지만 Logistic Regression은 여전히 매우 유용합니다.

- 빠름
- 해석하기 쉬움
- baseline으로 좋음
- 확률 출력 가능
- feature 효과 분석 가능

특히 tabular data에서는 강력한 기준선 모델입니다.

---

## 14. 실패하기 쉬운 조건

### 비선형 관계

기본 Linear/Logistic Regression은 복잡한 비선형 패턴을 직접 표현하지 못합니다.

### Feature Scale

정규화가 필요한 경우가 있습니다.

### Multicollinearity

feature끼리 지나치게 강하게 상관되면 coefficient 해석이 불안정할 수 있습니다.

### Class Imbalance

Logistic Regression에서도 threshold와 class weight 등을 고려해야 합니다.

---

## 15. 한 장 요약

```text
Linear Regression
X -> 선형식 -> 연속값

Logistic Regression
X -> 선형식 z -> Sigmoid -> 확률 -> Threshold -> Class
```

가장 중요한 문장:

> **Linear Regression은 연속값을 예측하고, Logistic Regression은 선형 점수를 확률로 바꿔 분류합니다.**

---

## 다음 학습

- 원문: https://outcomeschool.com/blog/linear-regression-vs-logistic-regression
- 다음 레슨: https://outcomeschool.com/blog/feature-engineering
- 모듈 1 요약: [머신러닝 기초](../../module-01.md)
