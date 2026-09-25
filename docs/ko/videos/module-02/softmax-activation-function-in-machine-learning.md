# Softmax Activation Function in Machine Learning — 한국어 상세 영상 학습 노트

> 원본 영상: https://www.youtube.com/watch?v=2Zx6x01WwWM  
> 제작: Outcome School · 공개일 2025-05-25  
> 공식 영상 설명에서 “다중 분류 모델의 raw score(logit)를 합이 1인 확률로 변환하는 함수”라는 주제를 확인했습니다. 자막 전문은 직접 검증하지 못했으므로 아래 내용은 확인된 주제와 Outcome School의 Cross-Entropy 공식 글을 바탕으로 독립적으로 해설합니다.

## Softmax가 하는 일

신경망의 마지막 layer가 다음 raw score를 냈다고 하겠습니다.

```text
cat=2
dog=3
rabbit=1
```

이 값은 probability가 아닙니다. Softmax는 각 score를 지수화하고 전체 합으로 나눕니다.

```text
p_i = exp(z_i) / sum(exp(z_j))
```

결과는 모두 0~1 사이이며 합이 1이 됩니다.

## Outcome School 공식 예제와 연결

Cross-Entropy 공식 글의 logits `[2,3,1]`을 사용하면:

```text
exp(2)=7.389
exp(3)=20.086
exp(1)=2.718
sum=30.193
```

따라서 약:

```text
cat    0.2447
dog    0.6652
rabbit 0.0900
```

가 됩니다.

## 왜 단순히 합으로 나누지 않나

지수함수는 score 차이를 양수의 상대적 weight로 바꿉니다. 큰 logit은 더 큰 probability를 받지만 모든 class의 probability가 0이 되거나 음수가 되는 문제는 없습니다.

또한 모든 class가 서로 경쟁합니다. 한 class probability가 커지면 다른 class가 차지할 몫은 줄어듭니다.

## Cross-Entropy와의 연결

정답이 dog이라면 Cross-Entropy는 softmax 결과에서 dog probability를 사용합니다.

```text
loss = -log(p_dog)
```

위 예에서는 약 0.4076입니다.

모델이 dog logit을 더 높여 `p_dog`를 1에 가깝게 만들면 loss는 0에 가까워집니다.

## Numerical Stability

실제 구현에서는 큰 logit 때문에 exponent가 overflow하지 않도록 모든 logit에서 최대값을 먼저 빼는 방식이 흔합니다.

```text
softmax(z)
= softmax(z - max(z))
```

확률 결과는 동일하지만 계산이 더 안정적입니다.

## Softmax를 쓰는 대표 위치

- single-label multi-class classification의 output
- Transformer attention score를 가중치로 변환하는 과정
- language model의 다음 token probability 계산

문제 형태에 따라 sigmoid처럼 각 class를 독립적으로 다루는 함수가 더 적절할 수도 있으므로 “분류면 항상 softmax”는 아닙니다.

## 이해 확인

1. Softmax output의 합이 1이 되는 이유는 무엇인가요?
2. logit과 probability는 어떻게 다른가요?
3. Cross-Entropy가 softmax와 자주 함께 쓰이는 이유는 무엇인가요?
4. 최대 logit을 빼는 계산이 확률을 바꾸지 않는 이유를 설명할 수 있나요?

## 연결 학습

- 원본 영상: https://www.youtube.com/watch?v=2Zx6x01WwWM
- 관련 블로그: [Cross-Entropy Loss](../../blogs/module-02/math-behind-cross-entropy-loss.md)
- [모듈 2](../../module-02.md)
