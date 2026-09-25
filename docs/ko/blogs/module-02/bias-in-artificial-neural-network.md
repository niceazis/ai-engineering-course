# 인공신경망의 Bias란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/bias-in-artificial-neural-network  
> 원저자: Amit Shekhar / Outcome School · 2019-08-02  
> 원문의 설명 흐름을 따라 독립적으로 다시 쓴 한국어 학습 노트입니다.

## 핵심 아이디어

원문은 선형식 `y = mx`와 `y = mx + c`를 비교해 bias의 필요성을 설명합니다.

```text
bias 없음: y = m*x
bias 있음: y = m*x + c
```

`y=mx`는 입력이 0이면 출력도 반드시 0이므로 직선이 원점을 지나야 합니다. 실제 데이터가 원점을 지나지 않으면 `m`만 바꿔서는 최적의 직선을 만들 수 없습니다.

`c`를 추가하면 직선을 위아래로 이동할 수 있습니다. 원문에서 이 `c`가 bias입니다.

## 신경망의 일반형

한 뉴런은 보통 다음처럼 계산합니다.

```text
z = w1*x1 + w2*x2 + ... + wn*xn + b
a = activation(z)
```

여기서 `b`가 bias입니다. 입력이 모두 0이어도 `z=b`가 될 수 있으므로 뉴런의 활성화 기준점을 조정할 수 있습니다.

## 왜 중요한가

bias가 없다면 모델은 불필요한 구조적 제약을 받습니다. 예를 들어 실제 관계가 `y=2x+5`라면 `y=mx`로는 `x=0, y=5`를 맞출 수 없습니다. `b=5`를 허용하면 그 제약이 사라집니다.

bias는 사람이 고정하는 값이 아니라 weight와 함께 학습되는 parameter입니다.

```text
b_new = b_old - learning_rate * dL/db
```

분류에서도 `w1*x1 + w2*x2 + b = 0` 형태의 decision boundary를 이동시키는 역할을 합니다.

## 한 줄 정리

```text
Bias = 모델이 원점에 묶이지 않고 데이터에 맞는 기준점을 학습하게 하는 파라미터
```

## 이해 확인

1. `y=mx`가 원점을 반드시 지나는 이유는 무엇인가요?
2. bias가 바뀌면 직선이나 decision boundary는 어떻게 달라지나요?
3. bias도 gradient descent로 학습되는 이유는 무엇인가요?

## 연결 학습

- 원문: https://outcomeschool.com/blog/bias-in-artificial-neural-network
- 다음: [경사하강법](math-behind-gradient-descent.md)
- [모듈 2](../../module-02.md)
