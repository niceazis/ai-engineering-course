# 머신러닝 Regularization — 원문 흐름을 따라가는 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/regularization-in-machine-learning  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 Overfitting → L1/L2 Regularization 흐름을 따라가며 의미와 차이를 보강한 상세 학습 노트입니다.

## 핵심

Regularization은 모델이 training data에 지나치게 맞춰지는 **overfitting**을 줄이기 위해 모델 복잡도에 penalty를 주는 방법입니다.

대표적으로:

- L1 / Lasso
- L2 / Ridge

가 있습니다.

## 1. Overfitting이란?

원문은 overfitting을 **training data의 detail과 noise까지 너무 많이 학습해 새로운 데이터 성능이 나빠지는 현상**으로 설명합니다.

전형적인 모습:

```text
Training error   -> 매우 낮음
Validation error -> 높음
```

모델이 일반적인 규칙보다 training set에만 존재하는 우연한 패턴까지 기억한 것입니다.

## 2. 왜 큰 weight가 문제가 될 수 있나

선형 모델을 생각해 보겠습니다.

```text
ŷ = w1*x1 + w2*x2 + ... + wn*xn
```

특정 weight가 지나치게 크면 해당 feature의 작은 변화가 예측을 크게 흔들 수 있습니다.

Regularization은 원래 loss에 weight 크기에 대한 비용을 추가합니다.

```text
Total Loss
= Data Loss
+ Regularization Penalty
```

모델은 이제 두 목표를 동시에 만족해야 합니다.

1. 데이터에 잘 맞기
2. weight를 불필요하게 크게 만들지 않기

## 3. L1 Regularization / Lasso

원문의 L1 penalty는 weight 절댓값의 합입니다.

```text
Loss_total
= Loss_data + λ Σ|w_i|
```

여기서 `λ`는 regularization strength를 조절합니다.

### λ가 작으면

원래 loss를 맞추는 것이 더 중요합니다.

### λ가 크면

큰 weight에 더 강한 penalty가 생깁니다.

L1의 중요한 특성은 일부 weight를 정확히 0으로 만들기 쉽다는 것입니다.

그래서 sparse model과 feature selection 효과로 이어질 수 있습니다.

## 4. L2 Regularization / Ridge

L2는 weight 제곱합을 penalty로 사용합니다.

```text
Loss_total
= Loss_data + λ Σ(w_i²)
```

큰 weight는 제곱되어 더 강한 penalty를 받습니다.

L2는 보통 weight를 0 근처로 부드럽게 줄이는 경향이 있습니다.

```text
before: [4.8, 0.9, -3.7, 2.2]
after : [2.1, 0.7, -1.8, 1.4]
```

정확한 값은 데이터와 λ에 따라 달라지지만, 핵심은 특정 feature에 과도하게 의존하는 것을 줄이는 것입니다.

## 5. L1과 L2의 차이

| 항목 | L1 | L2 |
|---|---|---|
| Penalty | Σ|w| | Σw² |
| 별칭 | Lasso | Ridge |
| Weight 효과 | 일부를 0으로 만들기 쉬움 | 전체를 부드럽게 축소 |
| Sparse model | 유리 | 상대적으로 덜함 |
| 큰 weight 억제 | 함 | 강하게 함 |

## 6. λ가 너무 크면 Underfitting

Regularization은 많을수록 좋은 것이 아닙니다.

```text
λ 너무 작음 -> overfitting 억제 부족
λ 적절함   -> generalization 개선 가능
λ 너무 큼   -> 모델이 충분히 학습하지 못함
```

따라서 λ는 validation set이나 cross-validation을 이용해 선택해야 합니다.

## 7. Loss와 Regularization을 구분

이전 레슨의 L1/L2 Loss와 이름은 같지만 역할이 다릅니다.

### L1/L2 Loss

```text
실제값 y와 예측값 ŷ의 차이에 적용
```

### L1/L2 Regularization

```text
모델 parameter w에 적용
```

예를 들어 MSE + L2 Regularization이면:

```text
Total Loss
= MSE(y, ŷ)
+ λ Σw²
```

입니다.

## 8. “모든 feature weight를 균등하게 만든다”로 이해하면 안 된다

원문의 직관은 특정 feature에 과도한 weight를 주는 것을 억제한다는 것입니다.

하지만 좋은 모델의 weight가 반드시 모두 비슷해야 하는 것은 아닙니다. 실제로 중요한 feature는 더 큰 weight를 가질 수 있습니다.

Regularization의 정확한 목적은 **필요 이상으로 복잡하고 극단적인 parameter를 억제해 일반화를 개선하는 것**입니다.

## 9. 실무 체크리스트

1. Training 성능과 validation 성능의 gap을 봅니다.
2. 데이터 leakage나 train/validation split 문제를 먼저 확인합니다.
3. 모델 복잡도가 과한지 봅니다.
4. L1/L2 regularization을 적용합니다.
5. λ를 validation으로 튜닝합니다.
6. 새로운 데이터 성능이 실제로 좋아졌는지 확인합니다.

## 10. 반드시 기억할 문장

```text
Regularization
= training data에 맞는 것만 최적화하지 말고
  parameter 복잡도에도 비용을 부과해
  generalization을 개선하려는 방법
```

## 이해 확인

1. Training loss는 매우 낮지만 validation loss가 높다면 어떤 문제를 의심해야 하나요?
2. 일부 feature weight를 0으로 만들어 sparse model을 원한다면 L1과 L2 중 어느 쪽이 더 자연스러운가요?
3. λ가 지나치게 크면 왜 underfitting이 생길 수 있나요?

## 원문 및 연결 학습

- 원문: https://outcomeschool.com/blog/regularization-in-machine-learning
- 이전: [L1·L2 Loss](l1-and-l2-loss-functions.md)
- 다음: [Reinforcement Learning](reinforcement-learning.md)
- 모듈 1: [머신러닝 기초](../../module-01.md)
