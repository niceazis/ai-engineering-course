# RMSNorm — 원문 기반 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/rmsnorm-root-mean-square-layer-normalization  
> Amit Shekhar / Outcome School · 2026-04-25  
> 아래 내용은 원문의 학습 순서와 예제를 참고해 독립적으로 설명한 요약입니다.

## 먼저 LayerNorm과 비교하기

LayerNorm은 한 벡터의 평균을 빼 중심을 0 근처로 옮긴 뒤, 분산을 이용해 크기도 조절합니다. 마지막에는 학습 가능한 scale과 shift를 적용합니다.

RMSNorm은 이 가운데 **평균을 빼는 과정은 생략하고 크기 조절에 집중**합니다. 그래서 계산 구조가 더 단순합니다.

## RMS가 의미하는 것

벡터 원소를 각각 제곱하고 평균한 뒤 제곱근을 취하면 RMS가 됩니다. 이 값은 벡터 전체의 전형적인 크기를 나타냅니다.

RMSNorm은 각 원소를 이 크기로 나누고 학습 가능한 scale을 곱합니다. 전체 magnitude가 지나치게 커지거나 작아지는 것을 완화하면서도 dimension별 표현력을 유지하려는 구조입니다.

## 원문의 수치 예제

원문은 `[2, 4, 4, 8]`을 사용합니다. 제곱값의 평균은 25이고 RMS는 5입니다. 따라서 RMS로 나눈 값은 `[0.4, 0.8, 0.8, 1.6]`이 됩니다.

이 예제에서 중요한 점은 평균을 먼저 빼지 않았다는 것입니다. LayerNorm과 달리 입력의 중심을 재조정하지 않고 scale만 맞춥니다.

## LayerNorm과 RMSNorm 비교

- LayerNorm: 중심 이동과 scale 조정을 모두 수행
- RMSNorm: scale 조정만 수행
- LayerNorm: 보통 scale과 shift 두 종류의 학습 parameter 사용
- RMSNorm: 주로 scale parameter 사용
- RMSNorm: 평균 계산 단계를 생략해 더 단순한 연산 경로

실제 구현에서는 0에 가까운 값에서 수치 문제를 피하기 위해 작은 epsilon을 포함합니다.

## 현대 Transformer에서의 의미

원문은 RMSNorm이 여러 현대 LLM에서 널리 채택된 이유로 단순한 계산과 안정적인 scale 관리를 강조합니다. Transformer에서는 attention이나 feed-forward block 주변 normalization 위치에서 사용되며, 정확한 위치는 architecture 설계에 따라 달라집니다.

## 학습 포인트

1. RMSNorm이 LayerNorm에서 제거한 단계가 무엇인지 설명할 수 있어야 합니다.
2. RMS가 단순 평균이 아니라 제곱 평균의 제곱근이라는 점을 구분해야 합니다.
3. normalization 뒤 학습 가능한 scale이 필요한 이유를 이해해야 합니다.

## 연결 학습

- 원문: https://outcomeschool.com/blog/rmsnorm-root-mean-square-layer-normalization
- 이전: [BatchNorm vs LayerNorm](batch-normalization-vs-layer-normalization.md)
- 다음: [RNN](recurrent-neural-network.md)
- [모듈 2](../../module-02.md)
