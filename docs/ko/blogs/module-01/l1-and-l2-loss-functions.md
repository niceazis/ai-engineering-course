# L1 Loss vs L2 Loss — 매우 자세한 한국어 학습 노트

> 원문: https://outcomeschool.com/blog/l1-and-l2-loss-functions
> 원저자: Amit Shekhar / Outcome School
> 문서 성격: **원문 전체 번역본이 아닌 독립적인 한국어 상세 해설·학습 노트**

## 핵심 정의

L1은 절대오차, L2는 제곱오차를 사용하며 L2가 큰 오차와 outlier에 훨씬 민감하다.

---

## 1. L1

- L1 = |y-y_hat|.
- 여러 sample 평균은 MAE와 연결된다.
- 큰 오차에 선형적으로 penalty를 준다.

## 2. L2

- L2 = (y-y_hat)^2.
- 평균하면 MSE다.
- 큰 오차를 제곱해 훨씬 강하게 벌준다.

## 3. Outlier

- 오차 10이면 L1 penalty는 10, L2는 100이다.
- Outlier가 많으면 L2가 극단값에 강하게 끌릴 수 있다.

## 4. Gradient

- L2 gradient는 오차 크기에 비례해 커진다.
- L1은 대체로 sign 중심이라 큰 오차에서도 gradient 크기가 일정하다.
- L1은 0에서 미분 불가능하지만 subgradient로 다룰 수 있다.

## 5. 통계적 관점

- MSE 최소화는 조건부 평균과 연결된다.
- MAE 최소화는 조건부 중앙값과 연결된다.
- Gaussian noise에는 L2, Laplace-like noise에는 L1 해석이 자연스럽다.

## 6. Huber Loss

- 작은 오차에는 L2, 큰 오차에는 L1처럼 동작한다.
- smoothness와 outlier robustness를 절충한다.

## 7. MAE vs RMSE

- MAE는 해석이 쉽고 outlier에 덜 민감하다.
- RMSE는 큰 실패를 더 크게 반영하며 target과 같은 단위를 유지한다.

## 8. 주의

- L1/L2 Loss와 L1/L2 Regularization은 이름이 같지만 적용 대상이 다르다.
- Loss는 prediction error, regularization은 parameter penalty다.

## 학습 체크리스트

- 핵심 개념을 한 문장으로 설명할 수 있는가?
- 대표 수식이나 기준을 직접 설명할 수 있는가?
- 실무 예시를 하나 들 수 있는가?
- 실패하거나 오해하기 쉬운 조건을 설명할 수 있는가?

## 원문

- https://outcomeschool.com/blog/l1-and-l2-loss-functions
