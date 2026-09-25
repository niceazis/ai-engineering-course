# Batch Normalization vs Layer Normalization — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/batch-normalization-vs-layer-normalization  
> 원저자: Amit Shekhar / Outcome School · 2026-05-15  
> 원문의 4×3 예제와 두 normalization 방향 비교를 따라 다시 쓴 학습 노트입니다.

## 왜 normalization이 필요한가

깊은 신경망에서 layer를 통과하는 값이 너무 크거나 작아지면 training이 느려지고 불안정해질 수 있습니다.

기본 normalization 식:

```text
x_hat = (x - mean) / sqrt(variance + epsilon)
output = gamma * x_hat + beta
```

BatchNorm과 LayerNorm의 핵심 차이는 mean과 variance를 **어느 축에서 계산하는가**입니다.

## 원문의 데이터

```text
Example 1: [10, 12, 14]
Example 2: [20, 22, 24]
Example 3: [30, 32, 34]
Example 4: [40, 42, 44]
```

batch size는 4, feature 수는 3입니다.

## Batch Normalization

같은 feature를 batch 전체에서 normalize합니다.

첫 feature:

```text
[10,20,30,40]
mean = 25
```

두 번째와 세 번째 feature도 각각 batch 방향으로 통계를 계산합니다.

```text
column-wise normalization
```

training에서는 현재 batch 통계를 사용하고, inference에서는 보통 training 중 누적한 running mean/variance를 사용합니다.

따라서 BatchNorm은 batch 구성과 크기의 영향을 받으며 training/inference 통계 사용 방식도 다릅니다.

## Layer Normalization

sample 하나 내부의 모든 feature를 함께 normalize합니다.

예를 들어 첫 sample:

```text
[10,12,14]
```

자체의 mean과 variance를 계산합니다.

다른 sample 없이 계산할 수 있어 batch size에 의존하지 않습니다.

```text
row-wise / per-example normalization
```

## 원문의 직관적 비교

- BatchNorm: 한 feature를 여러 example에 걸쳐 비교
- LayerNorm: 한 example의 여러 feature를 그 example 안에서 비교

## 핵심 표

| 항목 | BatchNorm | LayerNorm |
|---|---|---|
| 통계 방향 | batch 방향 | feature 방향 |
| 다른 sample 의존 | 있음 | 없음 |
| train/inference | 통계 사용 방식 다름 | 같은 계산 방식 |
| 대표 사용 | CNN·vision | RNN·Transformer·LLM |

원문은 image/CNN과 충분한 batch에서는 BatchNorm, sequence model·Transformer·LLM 또는 작은 batch에서는 LayerNorm이 일반적으로 더 자연스럽다고 설명합니다.

## 다음 단계: RMSNorm

LayerNorm은 mean을 빼는 re-centering과 scale을 맞추는 re-scaling을 모두 합니다.

RMSNorm은 다음 레슨에서 보듯 re-centering을 생략하고 RMS로 scale만 맞춥니다.

## 이해 확인

1. 4×3 데이터에서 BatchNorm은 어느 방향으로 통계를 계산하나요?
2. LayerNorm이 batch size 1에서도 자연스럽게 동작하는 이유는 무엇인가요?
3. BatchNorm이 inference에서 running statistics를 쓰는 이유는 무엇인가요?

## 연결 학습

- 원문: https://outcomeschool.com/blog/batch-normalization-vs-layer-normalization
- 이전: [Dropout](dropout-in-neural-networks.md)
- 다음: [RMSNorm](rmsnorm-root-mean-square-layer-normalization.md)
- [모듈 2](../../module-02.md)
