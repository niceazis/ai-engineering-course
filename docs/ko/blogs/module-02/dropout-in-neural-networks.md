# 신경망의 Dropout이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/dropout-in-neural-networks  
> 원저자: Amit Shekhar / Outcome School · 2026-06-05  
> 원문의 overfitting 비유, dropout rate, 4-neuron 수치 예제, inverted dropout, training/inference 차이를 따라 독립적으로 다시 쓴 학습 노트입니다.

## 핵심

Dropout은 training 중 일부 neuron을 무작위로 꺼서 특정 neuron이나 경로에 지나치게 의존하는 것을 줄이는 regularization 기법입니다.

```text
training: 일부 neuron을 random drop
inference: 모든 neuron 사용
```

## 원문의 Overfitting 비유

한 학생이 한 문제집만 반복해서 외워 연습 문제에서는 100점을 받지만, 실제 시험에서 조금 다른 문제가 나오면 풀지 못하는 상황을 생각합니다.

신경망도 training data를 지나치게 외우면:

```text
training 성능은 매우 높음
unseen data 성능은 낮음
```

이 될 수 있습니다.

## 왜 neuron을 일부러 끄나

일부 neuron이 너무 강해지면 network가 그 neuron들에 의존할 수 있습니다.

Dropout은 매 step마다 다른 neuron 조합을 활성화하므로 각 neuron이 더 독립적으로 유용한 representation을 학습하도록 압력을 줍니다.

## Dropout Rate

`p`는 neuron이 꺼질 확률입니다.

```text
p=0.5 -> 각 neuron이 50% 확률로 drop
p=0.2 -> 각 neuron이 20% 확률로 drop
```

매 training step에서 새로운 random mask가 적용됩니다.

## 원문의 4-neuron 예제

원래 layer output:

```text
[2.0, 4.0, 6.0, 8.0]
```

`p=0.5`이고 예를 들어 두 번째와 네 번째 neuron이 drop되면:

```text
[2.0, 0.0, 6.0, 0.0]
```

이 됩니다.

그대로 두면 평균 activation이 작아지므로 현대 구현은 보통 **inverted dropout**을 사용합니다.

keep probability가 0.5이므로 살아남은 activation을 `1/0.5=2`배 합니다.

```text
[4.0, 0.0, 12.0, 0.0]
```

이렇게 training 단계에서 scale을 맞춰 두면 inference에서 별도 보정이 필요 없습니다.

## Training vs Inference

### Training

- random mask 사용
- 일부 neuron 비활성
- surviving activation scaling
- step마다 다른 sub-network처럼 동작

### Inference

- dropout 비활성
- 모든 neuron 사용
- randomness 없음
- inverted dropout 덕분에 추가 scale 조정 없음

## PyTorch 예제

원문은 다음 구조를 보여줍니다.

```python
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(p=0.5),
    nn.Linear(256, 10)
)
```

실제 사용에서는 `model.train()`과 `model.eval()` 상태가 dropout 동작을 바꾸므로 중요합니다.

## 너무 큰 p의 위험

dropout도 많을수록 좋은 것이 아닙니다.

```text
p 너무 작음 -> regularization 효과 약함
p 적절함   -> generalization 개선 가능
p 너무 큼   -> 정보 손실이 커져 underfitting 가능
```

## 변형

architecture에 따라 activation dropout, spatial dropout, recurrent dropout, attention dropout 등 서로 다른 위치와 형태로 적용될 수 있습니다.

따라서 모든 network에 같은 `p=0.5`를 기계적으로 적용하는 것은 적절하지 않습니다.

## 이해 확인

1. dropout이 inference에서 꺼지는 이유는 무엇인가요?
2. inverted dropout이 surviving activation을 키우는 이유는 무엇인가요?
3. p가 지나치게 크면 왜 underfitting이 생길 수 있나요?

## 연결 학습

- 원문: https://outcomeschool.com/blog/dropout-in-neural-networks
- 이전: [Cross-Entropy Loss](math-behind-cross-entropy-loss.md)
- 다음: [BatchNorm vs LayerNorm](batch-normalization-vs-layer-normalization.md)
- [모듈 2](../../module-02.md)
