# Feature Engineering — 원문 흐름을 따라가는 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/feature-engineering  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: **원문 핵심 개념과 예시를 따라가며 한국어로 다시 설명한 상세 학습 노트**

---

## 이 글에서 반드시 이해해야 할 것

Feature Engineering은 “컬럼을 많이 만드는 기술”이 아닙니다.

핵심은:

> **원시 데이터를 모델이 문제의 구조를 더 잘 학습할 수 있는 표현으로 바꾸는 과정**

입니다.

---

## 1. Feature란 무엇인가

Feature는 모델에 들어가는 입력 변수입니다.

예를 들어 집값 예측이라면:

- 면적
- 방 개수
- 위치
- 연식
- 역까지 거리

가 feature가 될 수 있습니다.

같은 원시 데이터라도 어떻게 표현하느냐에 따라 모델이 학습하기 쉬워질 수도, 어려워질 수도 있습니다.

---

## 2. 왜 Feature Engineering이 중요한가

예를 들어 timestamp가 다음처럼 있다고 하겠습니다.

```text
2026-09-25 08:30:00
```

이 문자열 하나를 그대로 넣는 것보다 다음 정보를 분리하면 모델이 더 쉽게 패턴을 찾을 수 있습니다.

- hour = 8
- weekday = Friday
- is_weekend = 0
- month = 9

즉 사람이 문제 구조를 이해하고 **학습에 유용한 형태로 변환**합니다.

---

## 3. 숫자 Feature 변환

### Scaling

feature마다 단위가 크게 다를 수 있습니다.

예:

```text
나이: 20~80
연봉: 30,000,000~300,000,000
```

거리 기반 모델이나 gradient 기반 최적화에서는 이런 scale 차이가 영향을 줄 수 있습니다.

대표 방법:

- Standardization
- Min-Max Scaling

---

## 4. 범주형 Feature

예:

```text
색상 = red / green / blue
```

단순히:

```text
red=1, green=2, blue=3
```

으로 바꾸면 존재하지 않는 순서 관계가 생깁니다.

그래서 One-hot Encoding을 사용할 수 있습니다.

| color | red | green | blue |
|---|---:|---:|---:|
| red | 1 | 0 | 0 |
| green | 0 | 1 | 0 |

---

## 5. Feature Crossing

두 feature의 조합이 중요할 수 있습니다.

예:

```text
거리
혼잡도
```

를 따로 쓰는 것보다:

```text
거리 × 혼잡도
```

가 실제 이동 시간을 더 잘 설명할 수 있습니다.

선형 모델에서 이런 interaction feature는 특히 중요할 수 있습니다.

---

## 6. Bucketization

연속값을 구간으로 나누는 방법입니다.

예:

```text
나이
0~19
20~29
30~39
40~49
...
```

이렇게 하면 비선형 패턴을 단순한 구간 효과로 표현할 수 있습니다.

단점은 경계값에서 정보가 갑자기 끊길 수 있다는 것입니다.

---

## 7. 시간 Feature의 특수성

시간은 주기적입니다.

예를 들어 23시와 0시는 숫자로는 멀어 보이지만 실제 시간상으로는 매우 가깝습니다.

그래서 다음처럼 sin/cos encoding을 사용할 수 있습니다.

```text
sin(2π * hour / 24)
cos(2π * hour / 24)
```

이렇게 하면 23시와 0시가 벡터 공간에서도 가깝게 표현됩니다.

---

## 8. Missing Value

결측값 처리 방법은 다양합니다.

- 행 제거
- 평균/중앙값 대체
- 별도 category
- 모델 자체의 missing 처리 기능 사용

중요한 점은 결측 여부 자체가 정보일 수 있다는 것입니다.

예:

```text
소득 정보 미입력 여부
```

가 특정 사용자 행동과 연결될 수 있습니다.

그래서:

```text
income_missing = 1/0
```

같은 feature를 추가하기도 합니다.

---

## 9. Feature Selection

feature가 많다고 항상 좋은 것은 아닙니다.

불필요한 feature는:

- noise 증가
- overfitting
- training cost 증가
- inference latency 증가

를 만들 수 있습니다.

대표 방법:

- correlation 분석
- mutual information
- L1 regularization
- tree feature importance
- permutation importance

---

## 10. 가장 위험한 문제: Data Leakage

Feature Engineering에서 가장 중요한 주의점 중 하나입니다.

예측 시점에 알 수 없는 미래 정보를 feature로 사용하면 안 됩니다.

예:

고객 이탈 예측에서:

```text
계약해지 처리 완료 여부
```

를 feature로 쓰면 이미 결과를 알고 있는 셈입니다.

offline 성능은 매우 높게 나오지만 실제 서비스에서는 사용할 수 없습니다.

---

## 11. Training / Serving 일관성

학습 시와 실제 서비스 시 feature 계산 방식이 다르면 문제가 발생합니다.

예:

Training:

```text
평균값을 전체 데이터로 계산
```

Serving:

```text
최근 데이터만 사용
```

이처럼 계산 로직이 달라지면 **training-serving skew**가 생깁니다.

실무에서는 feature pipeline을 재사용 가능하게 만드는 것이 중요합니다.

---

## 12. 좋은 Feature Engineering의 반복 과정

```text
문제 이해
  ↓
가설 설정
  ↓
Feature 생성
  ↓
Validation
  ↓
Error Analysis
  ↓
Feature 수정
  ↓
반복
```

feature를 무작정 늘리는 것이 목적이 아닙니다.

목표는 **새로운 데이터에서의 일반화 성능 개선**입니다.

---

## 13. 현대 Deep Learning에서는 Feature Engineering이 사라졌는가?

완전히 그렇지는 않습니다.

Deep Learning은 raw input에서 representation을 스스로 학습하는 능력이 강합니다.

예:

- 이미지 pixel -> visual feature
- text token -> embedding

하지만 실무에서는 여전히:

- 입력 전처리
- normalization
- metadata 설계
- temporal feature
- retrieval feature
- prompt/context 구성

등의 형태로 feature engineering 사고방식이 중요합니다.

---

## 14. 한 장 요약

```text
Raw Data
   ↓
Cleaning
   ↓
Transform / Encode / Combine
   ↓
Useful Features
   ↓
Model
   ↓
Better Generalization
```

가장 중요한 문장:

> **Feature Engineering은 데이터를 더 많이 만드는 일이 아니라, 문제의 구조를 모델이 더 잘 학습하도록 입력 표현을 설계하는 일입니다.**

---

## 다음 학습

- 원문: https://outcomeschool.com/blog/feature-engineering
- 다음 레슨: https://outcomeschool.com/blog/precision-vs-recall
- 관련 영상: https://www.youtube.com/watch?v=QLlywrWuXag
- 모듈 1 요약: [머신러닝 기초](../../module-01.md)
