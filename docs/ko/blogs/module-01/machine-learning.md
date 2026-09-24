# 머신러닝이란? — 매우 자세한 한국어 학습 노트

> 원문: https://outcomeschool.com/blog/machine-learning  
> 원저자: Amit Shekhar / Outcome School  
> 원문 게시일: 2019-08-02  
> 문서 성격: **원문 전체 번역본이 아닌 독립적인 한국어 상세 해설·학습 노트**
>
> Outcome School의 이용약관은 별도 허가가 없는 한 사이트 자료의 지식재산권을 보유한다고 명시하고, 재게시·복제·재배포를 제한합니다. 따라서 이 문서는 원문의 문장과 구성을 그대로 옮기지 않고, 원문에서 다루는 개념을 한국어 학습용으로 다시 설명합니다. 자세한 원문은 위 링크에서 확인하세요.

---

## 0. 이 글에서 얻어야 할 것

이 문서를 다 읽고 나면 다음 질문에 스스로 답할 수 있어야 합니다.

1. 머신러닝이 일반적인 규칙 기반 프로그래밍과 무엇이 다른가?
2. "기계가 학습한다"는 말을 수학적으로 풀어쓰면 무슨 뜻인가?
3. 데이터, 입력 특성(feature), 정답(label/target), 가중치(weight), 예측값(prediction)은 서로 어떤 관계인가?
4. 모델이 처음에는 틀리다가 학습을 거치면서 점점 맞아지는 이유는 무엇인가?
5. 손실(loss)과 오차(error)는 왜 필요하고, 경사하강법(gradient descent)은 어떤 역할을 하는가?
6. 학습(training)과 추론(inference)은 어떻게 다른가?
7. 학습 데이터에서 잘 맞는 것과 처음 보는 데이터에 잘 맞는 것은 왜 다른 문제인가?
8. 머신러닝, 딥러닝, 생성형 AI, LLM은 어떤 포함 관계에 있는가?

---

## 1. 머신러닝을 가장 짧게 설명하면

머신러닝은 **데이터에서 규칙을 직접 찾아내도록 모델의 파라미터를 조정하는 방법**입니다.

일반적인 프로그램은 사람이 규칙을 코드로 씁니다.

```text
입력 + 사람이 만든 규칙 -> 출력
```

머신러닝에서는 사람이 모든 규칙을 직접 작성하지 않습니다.

```text
입력 + 정답 데이터
        ↓
      학습
        ↓
모델이 규칙을 나타내는 파라미터를 찾음
        ↓
새로운 입력 -> 예측
```

핵심 차이는 **규칙을 누가 만드는가**입니다.

- 전통적인 프로그래밍: 사람이 규칙을 명시한다.
- 머신러닝: 학습 알고리즘이 데이터에 잘 맞는 파라미터를 찾는다.

여기서 "규칙을 찾는다"는 말을 신비하게 받아들일 필요는 없습니다. 많은 경우 실제로는 **숫자로 된 파라미터를 반복해서 바꾸면서 예측 오차를 줄이는 과정**입니다.

---

## 2. "학습한다"는 말의 정확한 의미

머신러닝에서 학습은 의식이나 이해를 의미하지 않습니다.

가장 기본적인 형태로 보면 학습은 다음과 같습니다.

> **주어진 데이터에 대해 모델의 예측 오차가 작아지도록 파라미터 값을 조정하는 과정**

예를 들어 아주 단순한 선형 모델을 생각해 봅시다.

```text
ŷ = w1*x1 + w2*x2
```

- `x1`, `x2`: 입력값
- `w1`, `w2`: 모델이 학습해야 할 가중치
- `ŷ`: 모델의 예측값
- `y`: 실제 정답

모델이 학습한다는 것은 결국 `w1`, `w2` 같은 값을 찾아가는 것입니다.

예를 들어 실제 데이터의 숨은 관계가 다음이라고 해봅시다.

```text
y = 2*x1 + x2
```

모델이 최종적으로

```text
w1 ≈ 2
w2 ≈ 1
```

을 찾아내면 새로운 입력에도 적절한 값을 예측할 수 있습니다.

---

## 3. 데이터에서 패턴을 찾는다는 것은 무엇인가

다음과 같은 학습 데이터가 있다고 가정해 보겠습니다.

| x1 | x2 | y |
|---:|---:|---:|
| 1 | 1 | 3 |
| 2 | 1 | 5 |
| 1 | 3 | 5 |
| 3 | 2 | 8 |

이 데이터에는 다음 관계가 숨어 있습니다.

```text
y = 2*x1 + x2
```

사람은 표가 작으면 눈으로 규칙을 찾을 수도 있습니다.

하지만 현실의 머신러닝 문제는 보통 다음과 같습니다.

- 행이 수십만~수십억 개
- 입력 변수가 수백~수만 개
- 관계가 선형이 아님
- 노이즈가 있음
- 일부 값이 누락됨
- 같은 입력이라도 결과가 확률적으로 달라짐

이런 상황에서는 사람이 규칙을 직접 발견하기 어렵습니다.

머신러닝의 역할은 데이터를 통해 **예측에 유용한 통계적 구조를 자동으로 찾는 것**입니다.

---

## 4. Feature, Label, Model, Parameter

초반에 가장 중요한 용어 네 가지입니다.

### 4.1 Feature

**Feature(특성)**는 모델에 들어가는 입력 정보입니다.

예를 들어 집값 예측이라면:

- 면적
- 방 개수
- 위치
- 건축 연도
- 역까지 거리

등이 feature가 될 수 있습니다.

수학적으로는 흔히 다음처럼 씁니다.

```text
x1, x2, x3, ...
```

### 4.2 Label / Target

모델이 맞히려고 하는 정답입니다.

집값 예측에서는 실제 거래 가격이 target입니다.

```text
y = 실제 정답
```

### 4.3 Model

입력에서 출력을 계산하는 함수입니다.

아주 단순한 예:

```text
ŷ = w1*x1 + w2*x2 + b
```

조금 더 복잡해지면:

- Decision Tree
- Random Forest
- Gradient Boosting
- Neural Network
- Transformer

등이 됩니다.

### 4.4 Parameter

학습을 통해 조정되는 숫자입니다.

선형 모델에서는:

- `w1`, `w2`: weight
- `b`: bias

신경망에서는 수백만~수천억 개 이상의 weight가 있을 수 있습니다.

---

## 5. 예측값과 실제값

머신러닝에서는 실제 정답과 모델 예측을 구분하는 표기가 중요합니다.

- `y`: 실제값
- `ŷ` ("y-hat"): 예측값

예를 들어:

```text
실제 집값 y = 5억 원
모델 예측 ŷ = 4.6억 원
```

예측이 실제값과 다르면 오차가 존재합니다.

단순하게는:

```text
error = y - ŷ
```

이라고 생각할 수 있습니다.

하지만 실제 학습에서는 여러 샘플의 오차를 하나의 값으로 모으는 **loss function**을 사용합니다.

---

## 6. 왜 Loss Function이 필요한가

모델에게 "잘했다" 또는 "틀렸다"만 말해줘서는 어느 방향으로 얼마나 고쳐야 할지 알 수 없습니다.

그래서 숫자로 된 평가 기준이 필요합니다.

그게 **Loss Function(손실 함수)**입니다.

회귀 문제의 대표적인 예가 Mean Squared Error(MSE)입니다.

```text
MSE = 평균((실제값 - 예측값)^2)
```

예측이 실제값에 가까울수록 loss가 작아집니다.

학습의 목적을 매우 단순화하면 다음과 같습니다.

```text
좋은 parameter = loss를 작게 만드는 parameter
```

따라서 머신러닝의 학습 문제는 흔히 **최적화(optimization) 문제**로 볼 수 있습니다.

---

## 7. 처음부터 정답 가중치를 아는 것은 아니다

모델은 처음부터 좋은 파라미터를 알고 있지 않습니다.

단순한 모델을 다음과 같이 초기화했다고 해봅시다.

```text
w1 = 0
w2 = 0
```

그러면 모든 입력에 대해:

```text
ŷ = 0
```

에 가까운 결과가 나올 수 있습니다.

당연히 실제값과 차이가 큽니다.

학습 알고리즘은 다음 순서를 반복합니다.

1. 현재 weight로 예측
2. 실제 정답과 비교
3. loss 계산
4. loss를 줄이는 방향 계산
5. weight 조금 수정
6. 다시 예측
7. 충분히 좋아질 때까지 반복

이 반복 자체가 training의 핵심입니다.

---

## 8. Gradient Descent의 직관

경사하강법은 loss를 줄이는 방향으로 parameter를 이동시키는 대표적인 최적화 알고리즘입니다.

산을 내려가는 상황을 떠올리면 이해하기 쉽습니다.

- 현재 위치: 현재 parameter
- 높이: loss
- 목표: 가능한 낮은 지점
- 기울기: 어느 방향으로 움직이면 loss가 커지고 작아지는지 알려주는 정보

업데이트는 개념적으로 다음과 같습니다.

```text
새 weight = 기존 weight - learning_rate * gradient
```

### Learning Rate

`learning_rate`는 한 번에 얼마나 크게 이동할지를 결정합니다.

너무 크면:

- 최적점을 지나칠 수 있음
- 학습이 불안정해질 수 있음
- loss가 발산할 수 있음

너무 작으면:

- 학습이 지나치게 느림
- 좋은 값에 도달하기까지 오래 걸림

즉, 방향뿐 아니라 **이동 크기**도 중요합니다.

---

## 9. 아주 작은 Training Loop를 직접 이해하기

개념을 코드 형태로 표현하면 다음과 같습니다.

```python
for step in range(num_steps):
    prediction = model(X)
    loss = loss_function(prediction, y)

    gradient = compute_gradient(loss)
    weights = weights - learning_rate * gradient
```

실제 PyTorch에서는 자동미분(autograd)이 gradient 계산을 맡습니다.

```python
optimizer.zero_grad()
prediction = model(X)
loss = criterion(prediction, y)
loss.backward()
optimizer.step()
```

두 코드의 본질은 같습니다.

```text
예측 -> 평가 -> 미분 -> 수정 -> 반복
```

---

## 10. Training과 Inference의 차이

둘은 반드시 구분해야 합니다.

### Training

모델의 parameter를 바꾸는 과정입니다.

```text
학습 데이터 -> 예측 -> loss -> gradient -> weight update
```

일반적으로 계산량이 많습니다.

### Inference

학습이 끝난 parameter를 고정한 채 새로운 입력에 대한 결과를 계산하는 과정입니다.

```text
새 입력 -> 이미 학습된 모델 -> 예측
```

ChatGPT에 질문하고 답을 받을 때 대부분의 사용자 관점에서는 inference를 이용하는 것입니다.

---

## 11. "Weight가 모델의 지식이다"라는 표현 이해하기

단순한 선형 모델에서는 weight의 의미를 사람이 직접 이해할 수 있습니다.

예:

```text
집값 = 0.8 * 면적 + 0.3 * 역세권점수 + ...
```

하지만 큰 Neural Network에서는 특정 weight 하나를 보고 "이 숫자가 서울이라는 지식을 담고 있다"고 말할 수 없습니다.

지식과 패턴은 **많은 parameter에 분산된 형태**로 표현됩니다.

따라서:

> "모델의 지식은 weight에 저장된다"

는 표현은 큰 방향에서는 맞지만, 실제로는 **수많은 parameter 사이의 관계와 활성화 패턴에 분산되어 있다**고 이해하는 것이 더 정확합니다.

---

## 12. 처음 보는 데이터도 예측할 수 있는 이유

학습 데이터만 외워버린다면 머신러닝은 별 의미가 없습니다.

중요한 것은 **Generalization(일반화)**입니다.

예를 들어:

```text
Training Data
x1=1, x2=1 -> y=3
x1=2, x2=1 -> y=5
...
```

만 본 모델이 새로운 입력:

```text
x1=4, x2=3
```

에 대해 올바른 관계를 적용할 수 있어야 합니다.

숨은 패턴이:

```text
y = 2*x1 + x2
```

라면:

```text
y = 2*4 + 3 = 11
```

처럼 예측해야 합니다.

이 능력이 Generalization입니다.

---

## 13. Overfitting과 Underfitting

### Underfitting

모델이 너무 단순하거나 학습이 부족해 training data조차 제대로 설명하지 못하는 상태입니다.

증상:

- Training error 높음
- Validation error 높음

### Overfitting

Training data에는 매우 잘 맞지만 새로운 데이터에서는 성능이 떨어지는 상태입니다.

증상:

- Training error 매우 낮음
- Validation/Test error 높음

좋은 머신러닝은 단순히 training loss를 최소화하는 데서 끝나지 않습니다.

> **새로운 데이터에서도 잘 동작해야 합니다.**

그래서 dataset을 보통 다음과 같이 나눕니다.

- Training Set
- Validation Set
- Test Set

---

## 14. Train / Validation / Test Set

### Training Set

실제로 parameter를 학습하는 데이터입니다.

### Validation Set

모델 선택과 hyperparameter 조정에 사용합니다.

예:

- learning rate
- tree depth
- regularization strength
- neural network layer 수

### Test Set

마지막 성능 확인에 사용하는 데이터입니다.

중요한 원칙:

> Test Set을 반복적으로 보면서 모델을 튜닝하면 Test Set도 사실상 학습 과정에 들어간 셈이 됩니다.

따라서 마지막까지 독립적으로 유지하는 것이 좋습니다.

---

## 15. Parameter와 Hyperparameter의 차이

헷갈리기 쉬운 개념입니다.

### Parameter

학습 과정에서 데이터로부터 자동으로 조정됩니다.

예:

- Neural Network Weight
- Bias
- Linear Regression coefficient

### Hyperparameter

학습 방법을 제어하는 설정입니다.

예:

- Learning Rate
- Batch Size
- Number of Epochs
- Tree Depth
- Regularization coefficient

간단히:

```text
Parameter = 모델이 배움
Hyperparameter = 사람이/탐색 알고리즘이 정함
```

---

## 16. 머신러닝 문제의 대표적인 형태

### 16.1 Regression

연속적인 숫자를 예측합니다.

예:

- 집값
- 온도
- 매출
- 수요량

### 16.2 Classification

범주를 예측합니다.

예:

- 스팸 / 정상
- 불량 / 정상
- 고양이 / 개
- 이탈 고객 / 유지 고객

### 16.3 Ranking

항목의 순서를 정합니다.

예:

- 검색 결과
- 추천 피드
- 광고 후보

### 16.4 Clustering

정답 label 없이 유사한 항목끼리 그룹을 만듭니다.

### 16.5 Generation

새로운 데이터를 생성합니다.

예:

- 텍스트
- 이미지
- 음성
- 코드

현대 Generative AI와 LLM은 이 영역과 깊게 연결됩니다.

---

## 17. Supervised Learning과 Unsupervised Learning

### Supervised Learning

입력과 정답이 함께 있습니다.

```text
(X, y)
```

예:

```text
이메일 본문 -> spam/not spam
집 정보 -> 가격
이미지 -> 클래스
```

### Unsupervised Learning

명시적인 정답 label이 없습니다.

모델은 데이터 자체의 구조를 찾습니다.

예:

- Clustering
- Dimensionality Reduction
- Representation Learning의 일부

---

## 18. Reinforcement Learning은 무엇이 다른가

강화학습은 정답 label을 한 줄씩 직접 주는 방식과 다릅니다.

Agent가 Environment에서 행동하고 Reward를 받으며 장기적으로 좋은 행동 정책을 학습합니다.

```text
State -> Action -> Reward -> Next State
```

LLM 분야에서는 RLHF 같은 정렬 방법과 연결됩니다.

---

## 19. 모델을 선택할 때의 사고방식

모든 문제에 Deep Learning이 필요한 것은 아닙니다.

### 단순한 선형 관계

- Linear Regression
- Logistic Regression

### 구조화된 Tabular Data

많은 경우 다음 계열이 매우 강합니다.

- Decision Tree
- Random Forest
- Gradient Boosting
- XGBoost/LightGBM 계열

### 이미지, 음성, 자연어처럼 복잡한 비정형 데이터

Neural Network와 Deep Learning이 강점을 가집니다.

### 대규모 자연어 생성·이해

Transformer 기반 LLM이 대표적입니다.

핵심은:

> "가장 복잡한 모델"이 아니라 **문제와 데이터에 적합한 모델**을 선택하는 것입니다.

---

## 20. 실제 머신러닝 프로젝트의 전체 Workflow

현업에서는 대략 다음 순서로 진행됩니다.

### 1. 문제 정의

먼저 무엇을 예측하거나 최적화하려는지 명확하게 합니다.

나쁜 예:

```text
AI로 고객 데이터를 분석한다.
```

좋은 예:

```text
향후 30일 안에 이탈할 고객을 예측한다.
```

### 2. Metric 정의

성공을 숫자로 정의합니다.

예:

- Accuracy
- Precision
- Recall
- F1
- ROC-AUC
- MAE
- RMSE
- Latency
- Revenue Lift

### 3. 데이터 수집

필요한 feature와 label을 확보합니다.

### 4. 데이터 정제

- Missing Value
- Duplicate
- Outlier
- 잘못된 Label
- Data Leakage

등을 확인합니다.

### 5. Feature Engineering

문제에 도움이 되는 입력 표현을 만듭니다.

### 6. Baseline Model

처음부터 가장 복잡한 모델로 가지 않고 비교 기준을 만듭니다.

### 7. Training

parameter를 학습합니다.

### 8. Validation

새 데이터에서도 잘 동작하는지 확인합니다.

### 9. Error Analysis

어떤 데이터에서 실패하는지 분석합니다.

### 10. Deployment

API, Batch Job, On-device Model 등 실제 서비스 형태로 배포합니다.

### 11. Monitoring

프로덕션에서는 시간이 지나며 데이터 분포가 바뀔 수 있습니다.

관찰할 항목:

- Prediction Quality
- Data Drift
- Latency
- Failure Rate
- Cost

### 12. Retraining

새 데이터가 쌓이거나 환경이 바뀌면 다시 학습합니다.

---

## 21. Data Leakage는 왜 위험한가

머신러닝 초보자가 특히 조심해야 할 문제입니다.

Data Leakage는 **실제 예측 시점에는 알 수 없는 정보가 학습 입력에 들어가는 현상**입니다.

예를 들어 고객 이탈 예측에서:

```text
계약 해지 처리 완료 여부
```

를 feature로 넣는다면 예측 시점보다 미래의 정보를 사용하게 될 수 있습니다.

Offline 성능은 매우 좋아 보이지만 실제 서비스에서는 쓸 수 없습니다.

따라서 모델보다 먼저 **데이터 생성 시점과 정보 가용 시점**을 이해해야 합니다.

---

## 22. 좋은 모델은 Accuracy만 높은 모델이 아니다

모델 평가에는 업무 목적이 들어가야 합니다.

예를 들어 암 선별 검사라면 놓치는 것(False Negative)의 비용이 클 수 있습니다.

스팸 필터라면 정상 메일을 스팸으로 잘못 보내는 False Positive도 큰 문제입니다.

따라서 다음을 함께 고려해야 합니다.

- Precision
- Recall
- F1
- Calibration
- Latency
- Memory
- Inference Cost
- Explainability
- Robustness

---

## 23. 머신러닝에서 "Math"가 실제로 필요한 지점

머신러닝의 기본 구조를 이해하려면 다음 수학이 도움이 됩니다.

### Linear Algebra

- Vector
- Matrix
- Dot Product
- Matrix Multiplication

### Calculus

- Derivative
- Partial Derivative
- Gradient
- Chain Rule

### Probability & Statistics

- Probability Distribution
- Expectation
- Variance
- Conditional Probability
- Maximum Likelihood

처음부터 모든 수학을 완벽히 끝낼 필요는 없습니다.

개념을 공부하면서 필요한 수학을 함께 익히는 방식이 효과적입니다.

---

## 24. AI, ML, Deep Learning, Generative AI, LLM의 관계

큰 범위에서 작은 범위로 보면 다음과 같이 이해할 수 있습니다.

```text
Artificial Intelligence
└── Machine Learning
    └── Deep Learning
        └── Generative AI의 주요 현대 구현
            └── Large Language Models
```

다만 실제 연구·제품 분류에서는 경계가 완전히 깔끔하지 않을 수 있습니다.

### Artificial Intelligence

사람의 지능적 행동과 유사한 기능을 수행하는 시스템을 포괄하는 가장 넓은 개념입니다.

### Machine Learning

데이터로부터 패턴을 학습하는 AI 방법론입니다.

### Deep Learning

여러 층의 Neural Network를 사용하는 머신러닝 계열입니다.

### Generative AI

새로운 텍스트, 이미지, 음성, 영상, 코드 등을 생성하는 AI 시스템입니다.

### LLM

대규모 텍스트 데이터에서 학습된 대규모 언어 모델입니다. 현대 LLM은 대부분 Transformer 기반 Deep Learning 모델입니다.

---

## 25. 원문에서 특히 기억할 핵심 개념을 다시 정리

원문이 전달하려는 핵심을 학습 관점에서 압축하면 다음과 같습니다.

### 핵심 1: 규칙을 직접 코딩하지 않는다

데이터에서 예측에 유용한 parameter를 학습합니다.

### 핵심 2: 학습은 반복적인 최적화다

```text
Predict -> Measure Error -> Update -> Repeat
```

### 핵심 3: Weight는 모델 동작을 결정한다

단순 모델에서는 weight가 데이터 관계를 직접 표현합니다.

### 핵심 4: Gradient Descent는 더 좋은 Weight로 이동하는 방법이다

Loss가 작아지는 방향을 gradient로 계산하고 parameter를 반복적으로 조정합니다.

### 핵심 5: 목표는 Training Data 암기가 아니다

처음 보는 데이터에서도 잘 동작하는 Generalization이 중요합니다.

### 핵심 6: 학습 이후에는 Inference를 수행한다

실제 서비스에서는 학습된 parameter로 새 입력을 처리합니다.

---

## 26. 직접 손으로 확인해 볼 미니 실습

다음 관계를 가진 데이터를 생각해 보세요.

```text
y = 2*x1 + x2
```

예:

| x1 | x2 | y |
|---:|---:|---:|
| 1 | 1 | 3 |
| 2 | 1 | 5 |
| 2 | 3 | 7 |
| 4 | 2 | 10 |

질문:

1. `w1=0, w2=0`일 때 예측값은?
2. 실제값과 예측값 차이는 얼마나 큰가?
3. `w1=1, w2=1`로 바꾸면 좋아지는가?
4. `w1=2, w2=1`이면 모든 샘플을 정확히 맞히는가?
5. 새로운 입력 `x1=5, x2=4`의 예측값은?

정답:

```text
ŷ = 2*5 + 4 = 14
```

이 아주 작은 예제 안에 머신러닝의 핵심 구조가 들어 있습니다.

---

## 27. 더 현실적인 예제로 바꾸면

현실 문제에서는 관계를 사람이 정확히 알지 못합니다.

예를 들어 집값을 예측한다고 해봅시다.

```text
price = f(
  area,
  location,
  floor,
  age,
  subway_distance,
  school_quality,
  interest_rate,
  market_condition,
  ...
)
```

우리는 정확한 함수 `f`를 모릅니다.

그래서 데이터와 모델을 이용해 `f`를 근사합니다.

머신러닝은 본질적으로 이런 문제를 다룹니다.

> **알 수 없는 실제 관계를 데이터로부터 유용하게 근사하는 함수 찾기**

---

## 28. 초보자가 자주 하는 오해

### 오해 1: 머신러닝 모델은 스스로 의미를 이해한다

기본적으로 모델은 목적 함수에 따라 패턴을 학습합니다. 인간과 같은 의미 이해를 전제로 하면 안 됩니다.

### 오해 2: 데이터가 많으면 무조건 좋아진다

잘못된 데이터, 편향된 데이터, 누수된 데이터가 많아지면 문제도 커질 수 있습니다.

### 오해 3: Training Accuracy가 높으면 끝이다

새 데이터에서의 성능이 중요합니다.

### 오해 4: Deep Learning이 항상 전통 ML보다 좋다

문제와 데이터 크기, Latency, Explainability 요구사항에 따라 다릅니다.

### 오해 5: 모델만 좋으면 제품도 좋다

실제 제품에서는 데이터 파이프라인, Serving, Monitoring, Feedback Loop가 매우 중요합니다.

---

## 29. 다음에 공부하면 좋은 순서

이 글을 이해했다면 다음 순서가 자연스럽습니다.

1. Supervised vs Unsupervised Learning
2. Linear Regression
3. Logistic Regression
4. Loss Function
5. Gradient Descent
6. Backpropagation
7. Overfitting과 Regularization
8. Neural Network
9. Transformer
10. LLM

이 저장소의 Module 1과 Module 2가 이 흐름을 이어갑니다.

---

## 30. 한 장 요약

```text
[데이터]
   ↓
[Feature X, Target y]
   ↓
[Model]
   ↓
[Prediction ŷ]
   ↓
[Loss(y, ŷ)]
   ↓
[Gradient]
   ↓
[Parameter Update]
   ↓
반복
   ↓
[학습 완료]
   ↓
새로운 입력
   ↓
[Inference]
   ↓
예측
```

가장 중요한 문장 하나만 남기면:

> **머신러닝은 데이터에 숨어 있는 관계를 잘 근사하도록 모델의 파라미터를 최적화하고, 그 파라미터를 이용해 새로운 데이터에 대해 예측하는 방법이다.**

---

## 원문 및 추가 학습

- 원문: https://outcomeschool.com/blog/machine-learning
- 다음 레슨: [지도학습 vs 비지도학습](https://outcomeschool.com/blog/supervised-vs-unsupervised-learning)
- 관련 주제: [Gradient Descent](https://outcomeschool.com/blog/math-behind-gradient-descent)
- 코스 모듈: [모듈 1 — 머신러닝 기초](../../module-01.md)
