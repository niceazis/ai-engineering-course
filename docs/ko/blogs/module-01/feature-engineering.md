# Feature Engineering — 매우 자세한 한국어 학습 노트

> 원문: https://outcomeschool.com/blog/feature-engineering
> 원저자: Amit Shekhar / Outcome School
> 문서 성격: **원문 전체 번역본이 아닌 독립적인 한국어 상세 해설·학습 노트**

## 핵심 정의

Feature Engineering은 원시 데이터를 모델이 문제의 구조를 더 잘 학습할 수 있는 표현으로 바꾸는 과정이다.

---

## 1. 왜 중요한가

- 좋은 feature는 같은 알고리즘의 성능을 크게 바꿀 수 있다.
- 특히 tabular ML에서는 도메인 지식과 feature 설계가 핵심이다.

## 2. 시간 Feature

- timestamp에서 hour, weekday, weekend, month 등을 추출할 수 있다.
- 주기형 값은 sin/cos encoding으로 23시와 0시의 근접성을 표현할 수 있다.

## 3. Feature Crossing

- 두 feature의 상호작용을 새 feature로 만들 수 있다.
- 예: 거리×혼잡도, 사용자활동×가입기간.
- 선형 모델에서 interaction term은 특히 유용할 수 있다.

## 4. Bucketization

- 연속값을 구간으로 나눠 비선형 패턴을 단순하게 표현한다.
- 정보 손실과 경계값 문제를 함께 고려해야 한다.

## 5. Categorical Encoding

- One-hot은 순서 없는 범주를 독립 column으로 만든다.
- Ordinal encoding은 실제 순서가 있을 때만 쓴다.
- Target encoding은 leakage 방지가 핵심이다.

## 6. Scaling과 Missing

- Standardization, Min-Max Scaling은 거리·gradient 기반 모델에 중요하다.
- 결측값은 삭제·대체·별도 category 등으로 처리한다.
- 결측 여부 자체를 feature로 만들 수도 있다.

## 7. Feature Selection

- 노이즈 feature 제거는 overfitting과 latency를 줄일 수 있다.
- L1, mutual information, tree importance 등을 활용할 수 있다.

## 8. Data Leakage

- 예측 시점에 알 수 없는 미래 정보를 feature로 쓰면 안 된다.
- Scaler나 encoding 통계도 training data로만 fit해야 한다.
- training-serving skew를 반드시 점검한다.

## 9. 반복 Workflow

- 가설 → feature 생성 → validation → error analysis → 개선을 반복한다.
- feature 수를 늘리는 것이 목적이 아니라 일반화 성능을 높이는 것이 목적이다.

## 학습 체크리스트

- 핵심 개념을 한 문장으로 설명할 수 있는가?
- 대표 수식이나 기준을 직접 설명할 수 있는가?
- 실무 예시를 하나 들 수 있는가?
- 실패하거나 오해하기 쉬운 조건을 설명할 수 있는가?

## 원문

- https://outcomeschool.com/blog/feature-engineering
