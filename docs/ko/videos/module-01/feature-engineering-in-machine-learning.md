# Feature Engineering in Machine Learning — 한국어 상세 영상 학습 노트

> 원본 영상: https://www.youtube.com/watch?v=QLlywrWuXag  
> 채널: Outcome School  
> 문서 성격: 영상 전체 자막의 번역본이 아니라, 영상에서 다루는 학습 주제를 원문 블로그와 교차 확인해 한국어로 상세하게 다시 설명한 학습 노트입니다.
>
> **검증 범위:** 현재 YouTube 자막 원문을 직접 가져오지는 못했습니다. 영상과 연결된 Outcome School의 공식 Feature Engineering 글을 기준으로 핵심 예제와 논리를 교차 확인했습니다. 따라서 자막 문장 단위 번역이 아니라 **공식 글과 영상 주제에 근거한 상세 영상 학습 노트**입니다.

## 영상에서 이해해야 할 핵심

Feature Engineering은 raw data를 그대로 모델에 넣는 대신 **문제를 더 잘 드러내는 feature로 표현을 바꾸는 작업**입니다.

```text
Raw Data
   ↓
Domain Knowledge
   ↓
Useful Features
   ↓
Model
```

같은 모델이라도 입력 표현이 좋아지면 더 단순하게 중요한 패턴을 학습할 수 있습니다.

## 1. 머신러닝 pipeline에서의 위치

```text
Data Gathering
    ↓
Data Cleaning
    ↓
Feature Engineering
    ↓
Model Definition
    ↓
Training / Testing / Prediction
```

Feature Engineering은 “모델을 어떤 알고리즘으로 만들까?”보다 앞에서 **모델에게 무엇을 보여줄까?**를 결정합니다.

## 2. Date-Time 예제

비행 상태를 예측한다고 하겠습니다.

| Date-Time | Status |
|---|---|
| 2018-02-14 20:40 | Delayed |
| 2018-02-15 10:30 | On Time |
| 2018-02-14 07:40 | On Time |
| 2018-02-15 18:10 | Delayed |
| 2018-02-14 10:20 | On Time |

전체 timestamp보다 실제 지연과 관련된 것이 시간대라면:

```text
2018-02-14 20:40 -> Hour = 20
2018-02-15 10:30 -> Hour = 10
```

처럼 `Hour_Of_Day`를 추출합니다.

이제 모델은 복잡한 날짜 문자열보다 지연과 직접 연결된 시간 feature를 볼 수 있습니다.

## 3. Crossed Feature

집값 예측에 latitude와 longitude가 있다고 하겠습니다.

각 값을 따로 보는 것보다 둘의 조합이 실제 위치를 나타냅니다.

```text
latitude + longitude
       ↓
location representation
```

이것이 여러 feature를 조합해 더 의미 있는 feature를 만드는 직관입니다.

## 4. Bucketization

Age가 연속 숫자지만 결과가 특정 연령 구간에 따라 달라진다면:

```text
11~20 -> bucket 1
21~40 -> bucket 2
41~70 -> bucket 3
```

처럼 구간 feature를 만들 수 있습니다.

장점은 모델이 “정확히 29세와 30세의 차이”보다 “같은 연령 그룹인지”를 쉽게 활용할 수 있다는 것입니다.

단점은 bucket 경계에서 정보가 갑자기 끊기고 원래의 연속 정보가 손실될 수 있다는 점입니다.

## 5. Feature 제거

관련 없는 column을 없애는 것도 Feature Engineering입니다.

불필요한 feature는:

- noise 증가
- overfitting 가능성 증가
- 계산량 증가
- 잘못된 상관관계 학습

으로 이어질 수 있습니다.

## 6. 반복 과정

```text
아이디어 생성
   ↓
Feature 생성
   ↓
Model 학습
   ↓
Validation 결과 확인
   ↓
다시 수정
```

Feature Engineering은 한 번의 변환이 아니라 실험 과정입니다.

## 7. One-hot Encoding과 연결

범주형 feature가:

```text
City = Seoul / Busan / Incheon
```

처럼 문자열이라면 많은 모델은 이를 직접 처리하기 어렵습니다.

단순히:

```text
Seoul=1, Busan=2, Incheon=3
```

으로 바꾸면 존재하지 않는 순서와 거리 의미가 생길 수 있습니다.

이 문제를 해결하는 대표 방법이 다음 영상의 **One-hot Encoding**입니다.

## 8. 실무에서 추가로 확인할 것

Feature를 만들 때는 성능만 보면 안 됩니다.

### Data Leakage

예측 시점 이후에만 알 수 있는 정보를 feature로 사용하면 validation 성능은 좋아 보여도 실제 서비스에서는 사용할 수 없습니다.

### Train–Serving Consistency

학습과 실제 inference에서 같은 feature transformation을 적용해야 합니다.

### Distribution Shift

운영 환경에서 feature 분포가 바뀌면 과거에 유용했던 feature가 더 이상 유효하지 않을 수 있습니다.

## 핵심 요약

```text
Feature Engineering
= raw data를
  문제의 구조를 더 잘 표현하는 입력으로 바꾸는 것
```

대표 패턴:

- Extract: Date-Time → Hour
- Combine: Latitude + Longitude
- Bucketize: Age → Age Range
- Encode: Category → Numeric representation
- Remove: 불필요한 feature 삭제

## 이해 확인

1. 비행 지연이 요일에도 영향을 받는다면 timestamp에서 무엇을 추가로 추출할 수 있을까요?
2. 도시 이름을 1,2,3으로 바꾸는 것이 왜 위험할 수 있을까요?
3. training 시점에만 존재하는 feature가 왜 leakage 문제가 될까요?

## 관련 자료

- 원본 영상: https://www.youtube.com/watch?v=QLlywrWuXag
- 공식 블로그: https://outcomeschool.com/blog/feature-engineering
- [Feature Engineering 상세 블로그 학습 노트](../../blogs/module-01/feature-engineering.md)
- 다음 영상: [One-hot Encoding](one-hot-encoding-in-machine-learning.md)
