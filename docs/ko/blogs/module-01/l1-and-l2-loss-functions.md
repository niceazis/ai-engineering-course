# L1 Loss vs L2 Loss — 원문 흐름을 따라가는 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/l1-and-l2-loss-functions  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 핵심 정의와 outlier 비교를 기반으로 수치 예제를 보강한 상세 한국어 학습 노트입니다.

## 핵심

Loss Function은 모델의 예측이 실제값에서 얼마나 벗어났는지를 숫자로 만듭니다.

L1과 L2의 차이는 오차를 처리하는 방식입니다.

```text
L1: |오차|
L2: 오차²
```

이 한 차이가 outlier에 대한 민감도를 크게 바꿉니다.

## 1. L1 Loss

원문은 L1을 **Least Absolute Deviations(LAD)**로 소개합니다.

각 sample에서:

```text
error_i = y_i - ŷ_i
```

를 계산하고 절댓값을 사용합니다.

```text
L1 = Σ |y_i - ŷ_i|
```

평균을 사용하면 MAE(Mean Absolute Error) 형태가 됩니다.

### 예제

실제값:

```text
[10, 20, 30]
```

예측값:

```text
[12, 18, 25]
```

오차 절댓값:

```text
|10-12| = 2
|20-18| = 2
|30-25| = 5
```

합:

```text
L1 = 2 + 2 + 5 = 9
```

오차가 2배가 되면 penalty도 2배가 되는 **선형 증가**입니다.

## 2. L2 Loss

원문은 L2를 **Least Square Errors**로 설명합니다.

```text
L2 = Σ (y_i - ŷ_i)^2
```

평균을 사용하면 MSE가 됩니다.

같은 오차 `[2, 2, 5]`를 제곱하면:

```text
2² = 4
2² = 4
5² = 25
```

합:

```text
L2 = 4 + 4 + 25 = 33
```

큰 오차가 훨씬 강하게 반영됩니다.

## 3. Outlier가 생기면 차이가 커진다

정상적인 오차가 대부분 1~2인데 한 sample만 오차가 20이라고 하겠습니다.

L1에서 그 sample의 penalty:

```text
|20| = 20
```

L2에서는:

```text
20² = 400
```

따라서 L2는 큰 오차 하나가 전체 loss와 gradient를 강하게 지배할 수 있습니다.

원문이 outlier가 있는 데이터에서 L1을 고려하라고 설명하는 이유입니다.

## 4. L2를 자주 사용하는 이유

그렇다고 L1이 항상 더 좋은 것은 아닙니다.

L2는:

- 큰 오차를 강하게 줄이려는 압력이 있고
- 미분이 매끄러우며
- 많은 최적화 문제에서 다루기 편합니다.

오차가 Gaussian noise에 가깝다는 가정에서도 자연스럽게 연결됩니다.

반면 L1은 outlier에 상대적으로 robust하지만 0 지점에서 절댓값 함수가 미분 불가능합니다. 실제 최적화에서는 subgradient 등으로 처리할 수 있습니다.

## 5. “Outlier에 영향을 받지 않는다”는 표현은 정확히는 과하다

L1도 outlier의 영향을 받습니다.

오차 100은 오차 1보다 L1 loss를 100배 크게 만듭니다.

정확한 표현은:

> **L1은 L2보다 outlier의 영향을 덜 증폭한다.**

L2는 제곱 때문에 큰 오차를 훨씬 더 확대합니다.

## 6. L1 Loss와 L1 Regularization은 다르다

이름이 같아 자주 혼동합니다.

### L1 Loss

예측 오차에 절댓값을 적용합니다.

```text
Σ |y - ŷ|
```

### L1 Regularization

모델 weight의 절댓값을 penalty로 추가합니다.

```text
original_loss + λ Σ|w|
```

대상이 다릅니다.

- Loss: 예측 오류
- Regularization: weight 크기

다음 레슨에서 이 차이가 중요합니다.

## 7. 선택 기준

### L2를 우선 검토

- 큰 오차를 강하게 줄이고 싶음
- outlier가 심하지 않음
- 매끄러운 optimization이 유리함

### L1을 검토

- outlier가 존재함
- 큰 오차 몇 개가 학습을 지나치게 지배하는 것을 줄이고 싶음
- 절대 오차 자체가 업무 의미와 잘 맞음

실무에서는 loss 선택 전에 outlier가 **오류 데이터인지 실제 중요한 rare case인지**도 확인해야 합니다. 무조건 제거하는 것은 위험합니다.

## 8. 반드시 기억할 문장

```text
L1 = absolute error -> 큰 오차를 선형으로 벌점
L2 = squared error  -> 큰 오차를 제곱으로 강하게 벌점
```

## 이해 확인

1. 오차가 3과 30일 때 L1 penalty 비율과 L2 penalty 비율은 각각 얼마인가요?
2. outlier 하나가 gradient를 지나치게 지배한다면 어느 loss가 상대적으로 robust한가요?
3. L1 Loss와 L1 Regularization은 무엇에 절댓값을 적용하는지가 어떻게 다른가요?

## 원문 및 연결 학습

- 원문: https://outcomeschool.com/blog/l1-and-l2-loss-functions
- 이전: [Precision vs Recall](precision-vs-recall.md)
- 다음: [Regularization](regularization-in-machine-learning.md)
- 모듈 1: [머신러닝 기초](../../module-01.md)
