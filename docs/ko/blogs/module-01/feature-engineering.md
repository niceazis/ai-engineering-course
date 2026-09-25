# Feature Engineering — 원문 흐름을 따라가는 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/feature-engineering  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 실제 예제와 작업 순서를 유지하면서 한국어로 다시 풀어쓴 상세 학습 노트입니다.

## 핵심 정의

Feature Engineering은 **raw data를 모델이 문제의 핵심 관계를 더 쉽게 학습할 수 있는 feature로 바꾸는 과정**입니다.

원문이 “art”라고 표현하는 이유는 단순한 공식 하나가 아니라 **도메인 지식과 실험**이 필요하기 때문입니다.

같은 알고리즘을 사용하더라도 입력을 어떻게 표현하느냐에 따라 결과가 크게 달라질 수 있습니다.

## 1. 전체 머신러닝 workflow에서의 위치

원문의 흐름은 다음과 같습니다.

```text
1. Data Gathering
2. Data Cleaning
3. Feature Engineering
4. Model Definition
5. Train / Test / Predict
```

즉 Feature Engineering은 모델을 학습시키기 전에 **모델이 무엇을 보게 할지 결정하는 단계**입니다.

## 2. 예제 1: Flight Date-Time → Hour of Day

원문에는 비행기의 날짜·시간과 운항 상태가 있습니다.

| Date_Time_Combined | Status |
|---|---|
| 2018-02-14 20:40 | Delayed |
| 2018-02-15 10:30 | On Time |
| 2018-02-14 07:40 | On Time |
| 2018-02-15 18:10 | Delayed |
| 2018-02-14 10:20 | On Time |

raw feature는 날짜와 시간이 합쳐진 값입니다.

하지만 문제를 살펴보니 지연 여부와 더 직접적으로 관련된 것은 **날짜 전체가 아니라 시간대**일 수 있습니다.

그래서 새로운 feature를 만듭니다.

```text
Date_Time_Combined
        ↓
시간(hour) 추출
        ↓
Hour_Of_Day
```

결과는 다음처럼 단순해집니다.

| Hour_Of_Day | Status |
|---:|---|
| 20 | Delayed |
| 10 | On Time |
| 7 | On Time |
| 18 | Delayed |
| 10 | On Time |

이제 모델은 “18~20시대에 지연이 더 자주 발생하는가?” 같은 관계를 훨씬 직접적으로 학습할 수 있습니다.

핵심은 정보를 무작정 늘린 것이 아니라 **예측 대상과 관계가 있는 표현으로 바꿨다**는 것입니다.

## 3. 예제 2: Latitude + Longitude

집값을 예측한다고 하겠습니다.

raw data에:

```text
latitude
longitude
Price_Of_House
```

가 있습니다.

위도와 경도를 서로 완전히 독립적인 숫자로만 보면 실제 “지역”이라는 의미를 모델이 활용하기 어려울 수 있습니다.

원문은 두 column을 결합하는 crossed feature의 예를 듭니다.

```text
latitude + longitude
        ↓
location을 표현하는 결합 feature
```

현대 실무에서는 geohash, grid cell, 거리 기반 feature, 지역 embedding 등 더 다양한 표현을 사용할 수 있지만 핵심 원리는 같습니다.

> 여러 raw feature를 조합해 문제와 더 직접적으로 관련된 표현을 만든다.

## 4. 예제 3: Age → Age Range

나이가 다음 class와 연결된 데이터가 있다고 하겠습니다.

```text
11~20 -> X
21~40 -> Y
41~70 -> Z
```

나이 숫자를 그대로 넣는 대신 구간을 만듭니다.

```text
Age
 ↓
11~20 -> bucket 1
21~40 -> bucket 2
41~70 -> bucket 3
```

새로운 `Age_Range` feature를 만드는 것입니다.

이를 **bucketization**이라고 합니다.

연속값을 구간으로 바꾸면 작은 숫자 차이보다 특정 범위에 속하는지가 중요한 문제에서 유용할 수 있습니다.

다만 bucket 경계를 잘못 정하면 정보가 손실되므로 항상 validation으로 확인해야 합니다.

## 5. Feature를 제거하는 것도 Feature Engineering이다

Feature Engineering은 새 열을 만드는 작업만 의미하지 않습니다.

문제와 무관하거나 잡음만 늘리는 feature를 제거하는 것도 포함됩니다.

불필요한 feature는:

- 모델이 우연한 상관관계를 학습하게 만들 수 있고
- 차원을 늘리고
- 학습 비용을 증가시키며
- 일반화 성능을 떨어뜨릴 수 있습니다.

따라서 “feature가 많을수록 좋다”는 전제는 틀렸습니다.

## 6. 원문의 반복적인 Feature Engineering 과정

원문은 다음 루프를 제시합니다.

```text
Brainstorm features
       ↓
Create features
       ↓
Model에서 성능 확인
       ↓
결과 분석
       ↓
다시 brainstorm
```

중요한 것은 Feature Engineering이 한 번 하고 끝나는 전처리가 아니라 **실험 루프**라는 점입니다.

## 7. 좋은 feature의 조건

좋은 feature는 대체로 다음 조건을 만족합니다.

### Target과 관련이 있다

예측하려는 결과와 실제 관계가 있어야 합니다.

### 미래 정보를 누설하지 않는다

예측 시점에는 알 수 없는 정보를 feature에 넣으면 data leakage가 됩니다.

### 안정적으로 계산할 수 있다

학습 때는 존재했지만 서비스 시점에는 얻을 수 없는 feature라면 사용할 수 없습니다.

### 의미 있는 일반화를 돕는다

training set의 우연한 패턴만 설명하는 feature는 오히려 과적합을 키울 수 있습니다.

## 8. 전처리와 Feature Engineering의 관계

경계가 완전히 고정된 것은 아니지만 다음처럼 구분하면 이해하기 쉽습니다.

### Data Cleaning

- 누락값 처리
- 잘못된 값 수정
- 중복 제거

### Feature Transformation

- scaling
- log transform
- normalization

### Feature Encoding

- one-hot encoding
- ordinal encoding

### Feature Construction

- 날짜 → 요일/시간
- 가격과 수량 → 총액
- 위도+경도 → 지역 feature

### Feature Selection

- 불필요한 feature 제거
- 중요한 feature 선택

이 모두가 넓은 의미의 Feature Engineering workflow에 들어갈 수 있습니다.

## 9. 왜 Deep Learning 시대에도 중요한가

딥러닝은 raw data에서 representation을 자동으로 학습하는 능력이 강합니다.

하지만 실제 시스템에서는 여전히 다음이 중요합니다.

- 어떤 데이터를 수집할지
- target을 어떻게 정의할지
- 시간 정보를 어떻게 자를지
- leakage를 어떻게 막을지
- 범주형 데이터를 어떻게 표현할지
- train/serving에서 같은 변환을 보장할지

즉 자동 representation learning이 Feature Engineering을 완전히 없앤 것이 아니라, **사람이 직접 설계하는 feature의 종류와 위치를 바꿨다**고 보는 편이 정확합니다.

## 10. 반드시 기억할 문장

```text
좋은 모델을 만드는 일
= 알고리즘 선택만의 문제가 아니라
  문제를 잘 드러내는 입력 표현을 만드는 일
```

원문의 세 예제를 다시 연결하면:

```text
Date-Time -> Hour
Latitude + Longitude -> Location representation
Age -> Age Range
Unrelated feature -> Remove
```

모두 raw data를 모델이 학습하기 좋은 표현으로 바꾸는 같은 원리입니다.

## 이해 확인

1. 비행 지연이 요일에도 크게 영향을 받는다면 어떤 feature를 추가할 수 있을까요?
2. Age를 bucket으로 바꿀 때 생길 수 있는 정보 손실은 무엇일까요?
3. 모델 배포 후 얻을 수 없는 feature가 training 성능을 크게 높였다면 사용해도 될까요?

## 원문 및 연결 학습

- 원문: https://outcomeschool.com/blog/feature-engineering
- 원본 영상: https://www.youtube.com/watch?v=QLlywrWuXag
- 이전: [선형 회귀 vs 로지스틱 회귀](linear-regression-vs-logistic-regression.md)
- 다음: [Precision vs Recall](precision-vs-recall.md)
- 모듈 1: [머신러닝 기초](../../module-01.md)
