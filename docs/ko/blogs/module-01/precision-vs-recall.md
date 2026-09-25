# Precision vs Recall — 원문 흐름을 따라가는 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/precision-vs-recall  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 spam filter 예제와 판단 흐름을 따라가며 한국어로 다시 설명한 상세 학습 노트입니다.

## 핵심 질문

Precision과 Recall은 둘 다 binary classifier의 성능을 측정하지만 질문이 다릅니다.

```text
Precision:
"Positive라고 판정한 것 중 실제 Positive는 얼마나 되는가?"

Recall:
"실제 Positive 전체 중 우리가 찾아낸 것은 얼마나 되는가?"
```

## 1. 문제: “정확하다”만으로는 부족하다

원문은 spam filter를 사용합니다.

모델의 질문은 단순합니다.

```text
이 이메일은 spam인가?
Yes / No
```

하지만 예측과 실제 상태를 조합하면 네 가지 결과가 생깁니다.

## 2. Confusion Matrix의 네 칸

| | 실제 Spam | 실제 Not Spam |
|---|---|---|
| Spam으로 판정 | True Positive | False Positive |
| Spam 아님으로 판정 | False Negative | True Negative |

### True Positive (TP)

실제로 spam이고 모델도 spam이라고 잡았습니다.

### False Positive (FP)

정상 메일인데 spam이라고 잘못 잡았습니다. **False alarm**입니다.

### False Negative (FN)

실제로 spam인데 놓쳤습니다. **Miss**입니다.

### True Negative (TN)

정상 메일을 정상으로 통과시켰습니다.

Precision과 Recall은 이 네 값 중 서로 다른 부분을 봅니다.

## 3. Precision

원문의 질문은:

> 모델이 spam이라고 표시한 것 중 실제 spam은 얼마나 되는가?

공식:

```text
Precision = TP / (TP + FP)
```

예를 들어 모델이 10개를 spam이라고 표시했고:

- 실제 spam: 8개
- 정상 메일을 잘못 표시: 2개

라면:

```text
Precision = 8 / (8 + 2)
          = 0.8
          = 80%
```

Precision이 높다는 것은 **모델이 positive라고 말할 때 그 말을 신뢰하기 쉽다**는 뜻입니다.

낮다면 FP가 많다는 뜻입니다.

spam filter에서는 중요한 정상 메일이 spam folder로 빠지는 문제가 커집니다.

## 4. Recall

Recall의 질문은 방향이 다릅니다.

> 실제 spam 전체 중 모델이 얼마나 잡았는가?

공식:

```text
Recall = TP / (TP + FN)
```

원문의 예에서 실제 spam이 20개이고:

- 잡은 spam: 8개
- 놓친 spam: 12개

라면:

```text
Recall = 8 / (8 + 12)
       = 0.4
       = 40%
```

Recall이 높다는 것은 **실제 positive를 거의 놓치지 않는다**는 뜻입니다.

낮다면 FN이 많습니다.

## 5. 분모를 보면 헷갈리지 않는다

Precision과 Recall을 외우기 어렵다면 분모가 “어떤 집합인가”를 보세요.

### Precision의 분모

```text
TP + FP
= 모델이 Positive라고 말한 전체
```

### Recall의 분모

```text
TP + FN
= 실제 Positive 전체
```

그래서:

```text
Precision -> 모델의 Positive 주장 품질
Recall    -> 실제 Positive 포착률
```

로 기억할 수 있습니다.

## 6. 왜 둘 사이에 trade-off가 생기나

분류 모델이 probability score를 낸다고 하겠습니다.

```text
spam probability >= threshold -> spam
```

threshold를 높이면 확신이 강한 것만 spam으로 판정합니다.

일반적으로:

```text
threshold ↑
positive 판정 ↓
FP 감소 가능
FN 증가 가능
Precision ↑ 경향
Recall ↓ 경향
```

반대로 threshold를 낮추면 더 많이 잡습니다.

```text
threshold ↓
positive 판정 ↑
FN 감소 가능
FP 증가 가능
Recall ↑ 경향
Precision ↓ 경향
```

항상 기계적으로 반대 방향으로 움직인다는 보장은 없지만, threshold를 조정할 때 흔히 나타나는 핵심 trade-off입니다.

## 7. 무엇을 더 중요하게 봐야 하나

정답은 **오류 비용**에 달려 있습니다.

### False Positive가 특히 비싼 문제

예: 정상 메일을 spam 처리해 중요한 업무 메일을 숨김.

이 경우 Precision을 중요하게 볼 이유가 큽니다.

### False Negative가 특히 비싼 문제

예: 위험 질환 screening에서 실제 환자를 놓침.

이 경우 Recall을 중요하게 볼 이유가 큽니다.

따라서 “Precision이 Recall보다 중요하다” 또는 그 반대라는 일반 정답은 없습니다.

## 8. Accuracy만 보면 왜 위험할 수 있나

10,000건 중 실제 사기가 10건뿐인 데이터가 있다고 하겠습니다.

모든 건을 정상이라고 예측하면:

```text
Accuracy = 9,990 / 10,000 = 99.9%
```

겉보기에는 매우 좋습니다.

하지만 사기 10건을 하나도 잡지 못했으므로 fraud class에 대한 Recall은 0입니다.

class imbalance가 심할수록 Accuracy 하나만 보는 것이 위험한 이유입니다.

## 9. F1 Score와 연결

Precision과 Recall을 하나의 수치로 균형 있게 보고 싶을 때 F1 Score를 사용할 수 있습니다.

```text
F1 = 2 * Precision * Recall / (Precision + Recall)
```

조화평균을 사용하므로 둘 중 하나가 매우 낮으면 F1도 낮아집니다.

다만 실제 비즈니스에서 FP와 FN 비용이 크게 다르다면 F1 하나로 의사결정을 끝내는 것도 적절하지 않을 수 있습니다.

## 10. 실무 판단 순서

1. Positive class가 무엇인지 명확히 정합니다.
2. FP가 발생했을 때의 비용을 적습니다.
3. FN이 발생했을 때의 비용을 적습니다.
4. Precision/Recall을 함께 측정합니다.
5. threshold별 두 지표의 변화를 봅니다.
6. 실제 운영 비용에 맞는 threshold를 선택합니다.

## 11. 반드시 기억할 문장

```text
Precision = 내가 잡았다고 한 것의 정확도
Recall    = 잡아야 할 것을 얼마나 잡았는가
```

## 이해 확인

1. 정상 메일을 spam으로 보내는 오류는 FP인가 FN인가?
2. 암 screening에서 환자를 놓치지 않는 것이 최우선이라면 어떤 지표를 특히 봐야 하는가?
3. threshold를 매우 낮추면 Recall과 FP는 일반적으로 어떤 방향으로 움직이는가?

## 원문 및 연결 학습

- 원문: https://outcomeschool.com/blog/precision-vs-recall
- 이전: [Feature Engineering](feature-engineering.md)
- 다음: [L1·L2 Loss](l1-and-l2-loss-functions.md)
- 모듈 1: [머신러닝 기초](../../module-01.md)
