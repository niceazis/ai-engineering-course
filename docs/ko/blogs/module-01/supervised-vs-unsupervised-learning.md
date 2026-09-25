# 지도학습 vs 비지도학습 — 원문 흐름을 따라가는 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/supervised-vs-unsupervised-learning  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문 전체 직역본이 아니라, 원문의 설명 순서·데이터 예제·핵심 논리를 따라가면서 한국어로 다시 풀어쓴 상세 학습 노트입니다.

## 이 글의 핵심

머신러닝은 데이터에서 패턴을 학습하지만, **정답(label)이 함께 주어지는지**에 따라 학습 문제가 크게 달라집니다.

- 지도학습: 입력과 정답을 함께 보고 **입력 → 정답의 매핑**을 학습합니다.
- 비지도학습: 정답 없이 입력만 보고 **데이터 내부의 구조와 패턴**을 찾습니다.

## 1. 지도학습: 정답지를 보면서 배우기

지도학습은 문제와 정답을 함께 받는 학습에 가깝습니다.

```text
입력 X + 정답 y
      ↓
     모델
      ↓
    예측 ŷ
      ↓
정답 y와 비교
      ↓
오차를 줄이도록 weight 수정
```

학습이 끝나면 모델은 처음 보는 입력에도 정답을 예측해야 합니다.

대표 문제는 두 가지입니다.

### Classification

정해진 범주 중 하나를 예측합니다.

- 이메일 → spam / not spam
- 이미지 → 숫자 0~9
- 고객 → churn / stay

### Regression

연속적인 숫자를 예측합니다.

- 집값
- 온도
- 수요량

## 2. 원문의 집값 예제

원문은 다음처럼 **Area, Bedrooms, Location Score**를 입력으로 주고 **Price**를 label로 둡니다.

| Area (sq ft) | Bedrooms | Location Score | Price (₹ Lakhs) |
|---:|---:|---:|---:|
| 1200 | 2 | 7.5 | 85 |
| 1500 | 3 | 8.0 | 110 |
| 900 | 2 | 6.8 | 70 |
| 1800 | 3 | 8.5 | 130 |
| 1100 | 2 | 7.0 | 78 |

여기서 모델이 보는 것은:

```text
X = [Area, Bedrooms, Location Score]
y = Price
```

입니다.

학습 과정에서는 현재 모델이 예측한 가격과 실제 Price를 비교하고, 오차가 줄어들도록 parameter를 수정합니다.

학습이 충분히 되면 기존 표에 없던 새로운 집의 면적·침실 수·입지 점수를 넣어 가격을 예측할 수 있습니다.

핵심은 **Price가 학습 때 이미 알려진 정답**이라는 점입니다.

## 3. 비지도학습: 정답 없이 구조 찾기

비지도학습 데이터에는 label이 없습니다.

```text
입력 X만 존재
    ↓
데이터 구조 분석
    ↓
군집 / 압축 / 관계 발견
```

모델에게 “이 사용자는 활동적인 사용자다” 같은 정답을 미리 알려주지 않습니다.

대표 문제는 다음과 같습니다.

### Clustering

비슷한 데이터끼리 묶습니다. 대표적으로 K-Means가 있습니다.

### Dimensionality Reduction

많은 feature를 중요한 정보를 최대한 유지하면서 더 작은 차원으로 압축합니다. 대표적으로 PCA가 있습니다.

### Generative Modeling

데이터의 분포나 구조를 학습해 새로운 sample을 생성하는 계열입니다.

## 4. 원문의 피트니스 앱 사용자 예제

원문은 label이 없는 다음 feature들을 사용합니다.

- Daily Steps
- Active Minutes
- Weekly Workouts
- Avg Heart Rate
- Sleep Hours
- Water Intake
- App Engagement Score

예를 들어 한 사용자는 하루 12,500걸음, 75분 활동, 주 5회 운동을 하고 engagement score가 88입니다. 다른 사용자는 4,800걸음, 18분 활동, 주 1회 운동을 합니다.

중요한 점은 데이터에 처음부터 다음 열이 없다는 것입니다.

```text
Segment = Active / Moderate / Low
```

K-Means 같은 clustering 알고리즘은 feature 공간에서 서로 가까운 사용자들을 찾아 그룹을 만듭니다.

원문 예제에서는 결과를 해석해 다음과 같은 persona로 연결합니다.

- Active Lifestyle Enthusiasts
- Moderate Fitness Users
- Low Activity Busy Users

이 이름 자체를 K-Means가 인간처럼 이해해 붙이는 것은 아닙니다. 알고리즘은 cluster를 만들고, **그 cluster가 무엇을 의미하는지는 사람이 feature 특성을 보고 해석**하는 것이 일반적입니다.

## 5. 두 방식의 결정적 차이

| 기준 | 지도학습 | 비지도학습 |
|---|---|---|
| Label | 있음 | 없음 |
| 목표 | 알려진 target 예측 | 숨은 구조 발견 |
| 대표 문제 | Classification, Regression | Clustering, Dimensionality Reduction |
| 학습 신호 | 예측과 정답의 오차 | 데이터 자체의 구조 |
| 예 | 스팸 판별, 집값 예측 | 고객 세분화, 이상 패턴 탐색 |

가장 빠른 판단 질문은 이것입니다.

> **내가 예측하려는 정답 열(target)이 학습 데이터에 있는가?**

있고 그 값을 예측하려는 문제라면 지도학습일 가능성이 높습니다. 정답 없이 데이터가 어떤 그룹과 구조를 갖는지 알고 싶다면 비지도학습 문제에 가깝습니다.

## 6. 흔히 헷갈리는 부분

### “분류”와 “클러스터링”은 둘 다 그룹을 만드는 것 아닌가?

결과 모양은 비슷해 보여도 학습 조건이 다릅니다.

분류에서는:

```text
고양이 이미지 -> 고양이
자동차 이미지 -> 자동차
```

처럼 정답 클래스가 이미 있습니다.

클러스터링에서는:

```text
데이터 -> 비슷한 것끼리 그룹 A/B/C
```

처럼 그룹의 의미가 사전에 주어지지 않습니다.

### 비지도학습은 평가할 수 없는가?

평가가 더 어렵다는 뜻이지 불가능하다는 뜻은 아닙니다. 군집의 응집도·분리도 같은 내부 지표를 사용할 수도 있고, 실제 비즈니스 목적에서 cluster가 유용한지 외부적으로 검증할 수도 있습니다.

## 7. 실무에서 선택하는 방법

다음 순서로 판단하면 됩니다.

1. 해결하려는 문제를 먼저 정의합니다.
2. 예측해야 할 target이 있는지 확인합니다.
3. 신뢰할 수 있는 label을 충분히 확보할 수 있는지 봅니다.
4. label이 있다면 classification/regression을 검토합니다.
5. label이 없고 구조 탐색이 목적이면 clustering/dimensionality reduction 등을 검토합니다.
6. 마지막으로 처음 보는 데이터나 실제 업무에서 결과가 유용한지 검증합니다.

## 8. 반드시 기억할 문장

```text
Supervised Learning = 정답을 이용해 예측 규칙을 학습
Unsupervised Learning = 정답 없이 데이터 구조를 학습
```

원문의 표현을 학습 관점에서 정리하면 **지도학습은 predict, 비지도학습은 discover**에 더 가깝습니다.

## 이해 확인

1. 집값 데이터에서 Price가 빠진다면 같은 방식의 지도 회귀 학습을 바로 할 수 있을까요?
2. 고객 segment 이름이 전혀 없는데 자연스러운 사용자 그룹을 찾고 싶다면 어떤 방식이 적합할까요?
3. spam/not-spam label이 이미 수십만 건 있다면 clustering보다 classification이 자연스러운 이유는 무엇일까요?

## 원문 및 연결 학습

- 원문: https://outcomeschool.com/blog/supervised-vs-unsupervised-learning
- 이전: [머신러닝이란?](machine-learning.md)
- 다음: [선형 회귀 vs 로지스틱 회귀](linear-regression-vs-logistic-regression.md)
- 모듈 1: [머신러닝 기초](../../module-01.md)
