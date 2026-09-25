# 경사하강법은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/math-behind-gradient-descent  
> 원저자: Amit Shekhar / Outcome School · 2026-04-17  
> 원문의 수치 예제·식·learning rate 비교·gradient descent 종류를 따라 독립적으로 다시 쓴 학습 노트입니다.

## 큰 그림

모델은 예측 오차를 나타내는 loss를 줄이도록 weight를 반복해서 수정합니다.

```text
prediction -> loss -> gradient -> weight update -> repeat
```

Gradient Descent는 현재 parameter 위치에서 loss의 기울기를 계산하고 반대 방향으로 이동합니다.

## Loss Function

원문 예제에서 실제 집값이 60, 예측이 50이면 오차는 10입니다. 제곱 오차는:

```text
(60 - 50)^2 = 100
```

여러 sample의 제곱 오차 평균이 MSE입니다.

## 핵심 업데이트 식

```text
w_new = w_old - alpha * f'(w_old)
```

- `f'(w)`: 현재 위치의 derivative/gradient
- `alpha`: learning rate

gradient가 양수면 빼서 왼쪽으로, 음수면 음수를 빼므로 오른쪽으로 이동합니다. 두 경우 모두 local downhill 방향입니다.

## 원문의 단계별 수치 예제

```text
f(w) = (w - 3)^2
f'(w) = 2(w - 3)
초기 w = 0
alpha = 0.1
```

| Step | w before | gradient | w after |
|---:|---:|---:|---:|
| 1 | 0 | -6 | 0.6 |
| 2 | 0.6 | -4.8 | 1.08 |
| 3 | 1.08 | -3.84 | 1.464 |
| 4 | 1.464 | -3.072 | 1.7712 |
| 5 | 1.7712 | -2.4576 | 약 2.0170 |

최솟값인 `w=3`에 가까워질수록 gradient의 크기도 작아집니다.

## 여러 parameter

실제 신경망에서는:

```text
gradient = [dL/dw1, dL/dw2, ...]
```

를 계산하고 각 weight를 따로 업데이트합니다.

```text
w1_new = w1_old - alpha * dL/dw1
w2_new = w2_old - alpha * dL/dw2
```

## Learning Rate 비교

원문은 같은 함수로 세 경우를 비교합니다.

### 너무 작음: alpha=0.01

```text
0 -> 0.06 -> 0.1188 -> ...
```

20 step 후에도 약 0.997로 매우 느립니다.

### 적절한 예: alpha=0.1

안정적으로 3에 접근합니다.

### 너무 큼: alpha=1.5

```text
0 -> 9 -> -9 -> ...
```

minimum을 크게 넘기며 발산합니다.

## Gradient Descent의 세 형태

| 방식 | 한 step에서 사용하는 데이터 | 특징 |
|---|---|---|
| Batch | 전체 dataset | 안정적이지만 비쌈 |
| Stochastic | sample 1개 | 빠르지만 noisy |
| Mini-batch | 일부 sample | 속도·안정성 절충 |

원문은 현대 deep learning에서 mini-batch 방식이 일반적이라고 설명합니다.

## Python의 본질

```python
w = 0.0
lr = 0.1
for step in range(50):
    gradient = 2 * (w - 3)
    w = w - lr * gradient
    loss = (w - 3) ** 2
```

50 step 후 `w`는 사실상 3, loss는 0에 가까워집니다.

## Backpropagation과 역할 구분

```text
Backpropagation = 각 parameter의 gradient를 계산
Gradient Descent = 계산된 gradient로 parameter를 업데이트
```

## 이해 확인

1. update 식에 마이너스가 붙는 이유는 무엇인가요?
2. learning rate가 너무 크면 왜 발산할 수 있나요?
3. mini-batch가 실무에서 많이 쓰이는 이유는 무엇인가요?

## 연결 학습

- 원문: https://outcomeschool.com/blog/math-behind-gradient-descent
- 이전: [Bias](bias-in-artificial-neural-network.md)
- 다음: [Backpropagation](math-behind-backpropagation.md)
- 관련 영상: https://www.youtube.com/watch?v=NFLlXE-6vno
- [모듈 2](../../module-02.md)
