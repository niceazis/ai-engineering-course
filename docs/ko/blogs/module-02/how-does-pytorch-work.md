# PyTorch는 어떻게 동작하는가? — 원문 기반 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-pytorch-work  
> Amit Shekhar / Outcome School · 2026-07-09  
> 원문의 Tensor → computation graph → autograd → Celsius/Fahrenheit 학습 → GPU 흐름을 따라 독립적으로 설명합니다.

## PyTorch의 역할

PyTorch는 machine learning model을 만들고 학습할 때 필요한 tensor 연산, 자동 미분, neural network 구성, GPU 실행 등을 제공하는 open-source framework입니다.

원문이 강조하는 핵심은 “모델이 틀린 정도를 계산한 뒤 parameter를 어느 방향으로 얼마나 바꿀지 자동으로 계산한다”는 점입니다.

## Tensor

Tensor는 숫자를 담는 다차원 자료구조입니다.

- scalar: 숫자 하나
- vector: 숫자 한 줄
- matrix: 행과 열
- 더 높은 차원의 배열

예:

```python
torch.tensor([1.0, 2.0, 3.0])
```

model의 입력, weight, intermediate activation 대부분이 tensor로 표현됩니다.

## 원문이 제시하는 학습 문제

Celsius를 Fahrenheit로 바꾸는 규칙을 model이 examples만 보고 학습한다고 가정합니다.

주어진 두 예:

```text
0°C   -> 32°F
100°C -> 212°F
```

실제 관계는 `F = 1.8*C + 32`이지만 model은 이를 모른다고 가정합니다.

학습해야 할 parameter:

```text
prediction = weight * celsius + bias
```

## Computation Graph

PyTorch는 forward 연산이 실행되는 동안 어떤 연산이 어떤 tensor에서 만들어졌는지 기록합니다.

원문의 간단한 예는:

```text
a=2, b=3, c=4
result = a*b + c = 10
```

입니다.

개념적인 graph:

```text
a ---      multiply -> 6 ---b ---/                  add -> 10
c ---------------------/
```

이 경로가 있어야 뒤에서 각 parameter가 결과에 미친 영향을 역으로 계산할 수 있습니다.

## Autograd

`requires_grad=True`인 tensor가 graph에 참여하면 PyTorch는 derivative 계산에 필요한 정보를 추적합니다.

예를 들어 `y=x*x`에서 x=3이면 derivative는 2x=6입니다. 원문은 automatic differentiation이 이 값을 계산해 주는 간단한 예를 사용합니다.

이 자동 미분이 backpropagation 구현의 핵심입니다.

## 원문의 전체 학습 예제

초기 parameter:

```text
weight = 0
bias = 0
learning rate = 0.0001
```

training loop의 구조:

```text
1. prediction 계산
2. 실제 Fahrenheit와의 squared error 계산
3. 자동 미분으로 gradient 계산
4. gradient 반대 방향으로 weight와 bias 수정
5. gradient 초기화
6. 반복
```

원문은 이 과정을 많은 step 반복하면:

```text
weight -> 약 1.8
bias   -> 약 32
```

에 접근한다고 설명합니다.

## gradient를 매 step 초기화하는 이유

PyTorch gradient는 기본적으로 누적됩니다. 일반적인 training loop에서는 이전 step의 gradient가 섞이지 않도록 update 뒤 gradient를 0으로 초기화해야 합니다.

optimizer를 사용할 때는 보통 `optimizer.zero_grad()`가 이 역할을 합니다.

## GPU를 사용하는 이유

deep learning은 큰 tensor에 같은 종류의 arithmetic operation을 대량으로 수행합니다. GPU는 이런 병렬 계산에 적합합니다.

원문은 CPU를 한 명의 빠른 작업자, GPU를 동시에 많은 작업을 처리하는 많은 작업자로 비유합니다.

PyTorch에서는 tensor와 model을 같은 device로 이동해 GPU 연산을 사용할 수 있습니다.

## 전체 관계

```text
Tensor
  ↓
Forward operations
  ↓
Computation Graph
  ↓
Loss
  ↓
Autograd / Backpropagation
  ↓
Gradients
  ↓
Optimizer
  ↓
Updated parameters
```

## 이해 확인

1. computation graph가 gradient 계산에 필요한 이유는 무엇인가요?
2. autograd와 backpropagation은 어떤 관계인가요?
3. gradient를 매 step 초기화해야 하는 이유는 무엇인가요?
4. tensor 연산이 GPU에 잘 맞는 이유는 무엇인가요?

## 연결 학습

- 원문: https://outcomeschool.com/blog/how-does-pytorch-work
- 이전: [RNN](recurrent-neural-network.md)
- 다음: [TensorFlow](how-does-the-machine-learning-library-tensorflow-work.md)
- [모듈 2](../../module-02.md)
