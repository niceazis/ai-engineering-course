# 왜 Attention을 √dₖ로 스케일링하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/scaling-dot-product-attention  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 분산 유도와 수치 예제를 보존해 다시 설명한 한국어 상세 학습 노트입니다.

## 1. 질문

Attention 공식에는 왜 (sqrt{d_k})가 들어갈까요?

[
Attention(Q,K,V)
=softmaxleft(rac{QK^T}{sqrt{d_k}}ight)V
]

단순히 (QK^T)를 softmax에 넣으면 더 간단해 보입니다.

문제는 (d_k)가 커질수록 dot product의 크기도 통계적으로 커진다는 점입니다.

## 2. Scaling이 없을 때

한 Query와 Key의 dot product:

[
Qcdot K=sum_{i=1}^{d_k}q_i k_i
]

각 component가 평균 0, 분산 1이고 서로 독립이라는 교육용 가정을 둡니다.

각 product (q_i k_i)의 기대값은 0이고 분산은 약 1입니다.

독립인 항 (d_k)개를 더하므로:

[
Var(Qcdot K)approx d_k
]

따라서 표준편차는:

[
Std(Qcdot K)approxsqrt{d_k}
]

입니다.

## 3. 원문의 dₖ=64 직관

(d_k=64)라면 dot product는 64개 항의 합입니다.

분산을 전개하면 총 (64×64=4096)개의 조합 항을 생각할 수 있습니다.

교육용 독립·평균 0 가정에서:

- 64개의 자기 항은 분산에 기여
- 4,032개의 cross term은 기대값이 0

이므로 결과적으로:

[
Var(Qcdot K)=64
]

표준편차는:

[
sqrt{64}=8
]

이 됩니다.

즉 Q/K component 자체가 단위 규모라도 dot product는 훨씬 넓은 범위로 퍼집니다.

## 4. 큰 score가 Softmax에 미치는 영향

Softmax:

[
softmax(z_i)=rac{e^{z_i}}{sum_j e^{z_j}}
]

지수함수는 입력 차이를 매우 빠르게 키웁니다.

원문이 보여 주는 값:

- (e^1 approx 2.718)
- (e^5 approx 148.4)
- (e^{10} approx 22,026)
- (e^{20} approx 485,165,195)
- (e^{50} approx 5,184,705,528,587,072,045)

따라서 score가 너무 커지면 softmax가 거의 one-hot처럼 뾰족해집니다.

그 결과:

- 가장 큰 logit만 거의 1
- 나머지는 거의 0
- softmax gradient가 매우 작아지는 영역이 늘어남

학습이 불안정하거나 느려질 수 있습니다.

## 5. 왜 정확히 √dₖ인가

어떤 random variable (X)의 분산이 (d_k)라고 합시다.

상수 (c)로 나누면:

[
Var(X/c)=rac{Var(X)}{c^2}
]

분산을 약 1로 만들고 싶으면:

[
rac{d_k}{c^2}=1
]

따라서:

[
c^2=d_k
]

[
c=sqrt{d_k}
]

즉 (sqrt{d_k})는 임의로 선택된 숫자가 아니라 **dot-product 분산 증가를 상쇄하는 scale**입니다.

## 6. 작은 수치 예제

원문은 scaling이 분산을 어떻게 줄이는지 직관적으로 보여 줍니다.

값:

    [2, 4, 6]

평균은 4이고 population variance는:

[
rac{(2-4)^2+(4-4)^2+(6-4)^2}{3}
=rac{8}{3}approx2.67
]

각 값을 2로 나누면:

    [1, 2, 3]

평균은 2이고 분산:

[
rac{(1-2)^2+(2-2)^2+(3-2)^2}{3}
=rac{2}{3}approx0.67
]

즉 값을 2로 나누면 분산은 (2^2=4)배 줄어듭니다.

Attention에서도 같은 원리로 (sqrt{d_k})를 나누면 분산 (d_k)가 약 1로 정규화됩니다.

## 7. Scaling 전후 직관

가령 (d_k=64)라면 scale은 8입니다.

raw logits:

    [8, 16, 24]

scaled logits:

    [1, 2, 3]

두 배열은 순서는 같지만 softmax sharpness가 크게 다릅니다.

Scaling의 목적은 어떤 token이 더 중요한지의 순서를 바꾸는 것이 아니라, **softmax가 학습하기 좋은 범위에 있게 하는 것**입니다.

## 8. 이 유도에서의 가정

“분산이 정확히 (d_k)”라는 설명에는 교육용 가정이 있습니다.

- component들이 서로 독립
- 평균 0
- 분산 1
- Q와 K component의 상관이 무시 가능

실제 학습된 network에서는 이 가정이 완벽히 성립하지 않습니다.

그럼에도 initialization과 통계적 scale 관점에서 (sqrt{d_k}) scaling이 매우 잘 작동하며 Transformer 표준 구성으로 자리 잡았습니다.

## 9. Temperature와의 관계

Softmax logit을 어떤 값으로 나누면 분포가 평평해진다는 점에서 temperature와 형태가 비슷합니다.

그러나 목적은 다릅니다.

- attention의 (sqrt{d_k}): 차원 증가에 따른 통계적 scale 보정
- generation temperature: sampling 분포의 다양성을 사용자가 조절

둘을 같은 hyperparameter로 보면 안 됩니다.

## 핵심 정리

- (Q·K)는 (d_k)개 항의 합이므로 분산이 (d_k) 규모로 증가합니다.
- 큰 logit은 softmax를 과도하게 포화시킬 수 있습니다.
- (sqrt{d_k})로 나누면 분산이 약 1 수준으로 돌아옵니다.
- (Var(X/c)=Var(X)/c^2)이므로 (c=sqrt{d_k})가 자연스럽게 나옵니다.
- scaling은 attention 순위를 바꾸는 것이 아니라 softmax의 수치 scale을 안정화합니다.

## 원문

- https://outcomeschool.com/blog/scaling-dot-product-attention
