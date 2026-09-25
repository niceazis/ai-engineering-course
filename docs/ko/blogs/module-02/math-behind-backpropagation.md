# 역전파는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/math-behind-backpropagation  
> 원저자: Amit Shekhar / Outcome School · 2026-04-06  
> 원문의 계산 순서와 수치 예제를 따라 독립적으로 다시 쓴 학습 노트입니다.

## 핵심

Backpropagation은 최종 오차가 각 parameter에 얼마나 민감한지 연쇄법칙으로 계산합니다.

## 원문의 초기값

```text
x=0.5, y=1.0
w1=0.3, b1=0.1
w2=0.7, b2=0.2
```

## Forward Pass

```text
z_h = 0.3*0.5 + 0.1 = 0.25
a_h = sigmoid(0.25) ≈ 0.5622

z_o = 0.7*0.5622 + 0.2 ≈ 0.5935
a_o = sigmoid(0.5935) ≈ 0.6442
```

원문은 squared error를 사용합니다.

```text
L = 0.5 * (1.0 - 0.6442)^2
  ≈ 0.0633
```

## Chain Rule

w2에 대한 gradient:

```text
dL/dw2
= dL/da_o * da_o/dz_o * dz_o/dw2
```

원문 수치:

```text
dL/da_o   = -0.3558
da_o/dz_o ≈ 0.2292
dz_o/dw2  = 0.5622

dL/dw2 ≈ -0.0459
```

w1은 hidden layer를 거치므로 더 긴 경로를 사용합니다.

```text
dL/dw1
= dL/da_o
* da_o/dz_o
* dz_o/da_h
* da_h/dz_h
* dz_h/dw1
```

추가 항:

```text
dz_o/da_h = 0.7
da_h/dz_h ≈ 0.2461
dz_h/dw1 = 0.5
```

bias도 같은 원리로 gradient를 계산하며 weight와 함께 학습됩니다.

## Parameter Update

gradient를 계산한 뒤 gradient descent를 적용합니다.

```text
parameter_new
= parameter_old
- learning_rate * gradient
```

역할을 구분하면:

```text
Backpropagation -> gradient 계산
Gradient Descent -> parameter update
```

원문의 Python 예제는 같은 초기값과 learning rate 0.5로 1000 epoch 반복하면서 loss를 줄이고 prediction을 1.0에 가깝게 만듭니다.

## 이해 확인

1. w1의 gradient 계산 경로가 w2보다 긴 이유는 무엇인가요?
2. activation function의 derivative가 필요한 이유는 무엇인가요?
3. Backpropagation과 Gradient Descent의 역할은 어떻게 다른가요?

## 연결 학습

- 원문: https://outcomeschool.com/blog/math-behind-backpropagation
- 이전: [Gradient Descent](math-behind-gradient-descent.md)
- 다음: [Cross-Entropy Loss](math-behind-cross-entropy-loss.md)
- [모듈 2](../../module-02.md)
