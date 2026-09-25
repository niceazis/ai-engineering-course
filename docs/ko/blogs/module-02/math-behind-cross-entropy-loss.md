# Cross-Entropy Loss란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/math-behind-cross-entropy-loss  
> 원저자: Amit Shekhar / Outcome School · 2026-04-20  
> 원문의 probability distribution, negative log, binary/categorical CE, cat-dog-rabbit 수치 예제와 language model 연결을 따라 독립적으로 다시 쓴 학습 노트입니다.

## 큰 그림

분류 모델은 class마다 probability를 출력합니다. Cross-Entropy는 정답 class에 얼마나 높은 probability를 주었는지를 loss로 바꿉니다.

```text
CE = - sum(y_i * log(p_i))
```

one-hot label에서는 정답 class만 남아:

```text
CE = -log(p_correct)
```

이 됩니다.

## Logit → Softmax → Loss

원문 예:

```text
logits z = [2, 3, 1]
softmax  = [0.2447, 0.6652, 0.0900]
정답     = dog
loss     = -log(0.6652) ≈ 0.4076
```

Softmax는 raw score를 합이 1인 probability distribution으로 바꿉니다.

## 왜 negative log인가

정답 probability가 높을수록 loss는 작아지고, 낮을수록 빠르게 커집니다.

```text
p=0.9 -> 0.105
p=0.5 -> 0.693
p=0.1 -> 2.303
```

따라서 확신을 갖고 틀린 예측에 큰 penalty를 줍니다.

## Binary Cross-Entropy

```text
BCE = -[y*log(p) + (1-y)*log(1-p)]
```

원문 예에서 y=1, p=0.8이면:

```text
BCE = -log(0.8) ≈ 0.223
```

입니다.

## Categorical Cross-Entropy

예:

```text
y = [0,1,0,0]
p = [0.2,0.7,0.05,0.05]

CE = -log(0.7) ≈ 0.357
```

## 원문의 cat-dog-rabbit 수치 예제

정답은 dog:

```text
y = [0,1,0]
z = [2.0,3.0,1.0]
```

Softmax 계산:

```text
exp(2.0)=7.389
exp(3.0)=20.086
exp(1.0)=2.718
sum=30.193
```

확률:

```text
cat≈0.2447
dog≈0.6652
rabbit≈0.0900
```

Loss는 약 0.4076입니다.

logits가 [1.0,5.0,0.5]이면 dog probability는 약 0.9714, loss는 약 0.0290까지 내려갑니다.

반대로 [5.0,1.0,0.5]인데 정답이 dog이면 dog probability는 약 0.0178이고 loss는 약 4.029로 커집니다.

## Language Model과 연결

LLM도 각 위치에서 실제 다음 token에 부여한 probability로 loss를 계산합니다.

```text
loss_t = -log(p_actual_next_token)
Total Loss = 평균(loss_t)
```

"The cat sat on the mat" 같은 문장이라면 각 위치의 실제 다음 token에 대해 같은 계산을 반복합니다.

## 구현 주의

PyTorch의 CrossEntropyLoss처럼 많은 구현은 raw logits를 직접 받습니다. softmax와 log를 내부에서 안정적으로 결합하므로 이미 softmax를 적용한 probability를 다시 입력하지 않는 것이 중요합니다.

## 이해 확인

1. 정답 class probability가 1에 가까워지면 CE는 어떻게 되나요?
2. confident wrong prediction이 큰 loss를 받는 이유는 무엇인가요?
3. LLM에서 token마다 CE를 계산하는 이유는 무엇인가요?

## 연결 학습

- 원문: https://outcomeschool.com/blog/math-behind-cross-entropy-loss
- 이전: [Backpropagation](math-behind-backpropagation.md)
- 다음: [Dropout](dropout-in-neural-networks.md)
- 관련 영상: https://www.youtube.com/watch?v=2Zx6x01WwWM
- [모듈 2](../../module-02.md)
