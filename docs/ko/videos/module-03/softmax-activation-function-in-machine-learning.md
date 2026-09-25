# Softmax Activation Function in Machine Learning — 한국어 상세 영상 학습 노트

> 영상: https://www.youtube.com/watch?v=2Zx6x01WwWM  
> 제공: Outcome School  
> 검증 범위: 영상 URL과 제목은 Outcome School 공식 자료에서 확인했습니다. **YouTube 자막 전문은 직접 검증하지 못했습니다.** 아래 내용은 공식 영상 주제와 Outcome School의 Attention 수치 예제에서 실제로 사용하는 Softmax 계산을 근거로 구성했습니다.

## 1. Softmax가 하는 일

Softmax는 여러 개의 실수 score(logit)를 합이 1인 확률 형태로 바꿉니다.

[
softmax(z_i)=rac{e^{z_i}}{sum_j e^{z_j}}
]

출력 특징:

- 각 값은 0보다 큼
- 전체 합은 1
- 큰 logit일수록 더 큰 확률

## 2. 작은 예제

logits:

    [1, 2, 3]

지수:

    e¹ ≈ 2.718
    e² ≈ 7.389
    e³ ≈ 20.086

합:

    30.193

Softmax:

    [0.090, 0.245, 0.665]

가장 큰 logit 3이 약 66.5% 확률을 얻습니다.

## 3. 왜 단순히 합으로 나누지 않는가

logit에는 음수도 있을 수 있고 일반적인 확률 점수가 아닙니다.

Exponential을 사용하면:

- 모든 값을 양수로 변환
- logit 순서를 보존
- 차이를 비선형적으로 강조
- 미분 가능한 확률 분포 생성

이 가능합니다.

## 4. 수치 안정성: max를 빼기

직접 (e^{1000})을 계산하면 overflow가 발생할 수 있습니다.

Softmax는 모든 logit에서 같은 상수를 빼도 결과가 같습니다.

[
softmax(z)=softmax(z-c)
]

보통:

[
c=max(z)
]

를 사용합니다.

예:

    [1000, 1001, 1002]
      ↓ max 1002 빼기
    [-2, -1, 0]

이렇게 바꿔도 softmax 확률은 동일하지만 계산은 안정적입니다.

## 5. Multi-Class Classification에서의 Softmax

분류 모델의 마지막 layer가 class별 logit을 냅니다.

    cat:  2.1
    dog:  0.8
    bird: -0.2

Softmax를 적용하면 class distribution을 얻을 수 있습니다.

Training에서는 일반적으로 softmax와 cross-entropy를 수치적으로 결합한 loss 구현을 사용합니다. 프레임워크의 CrossEntropyLoss에 이미 log-softmax 성질이 포함돼 있는지 확인해야 합니다.

## 6. Attention에서의 Softmax

Module 3에서 Softmax가 직접 등장하는 곳은 attention입니다.

[
A=softmax(QK^T/sqrt{d_k})
]

각 Query row의 score에 softmax를 적용해 “다른 token Value를 얼마나 섞을 것인가”를 정합니다.

Outcome School의 “I love AI” Q/K/V 예에서:

[
Aapprox
egin{bmatrix}
0.070&0.707&0.223\
0.333&0.333&0.333\
0.168&0.533&0.299
end{bmatrix}
]

각 row 합은 1입니다.

## 7. 큰 Logit 차이와 Saturation

Outcome School의 scaling 레슨은 exponential 증가를 다음처럼 보여 줍니다.

- (e^1≈2.718)
- (e^5≈148.4)
- (e^{10}≈22,026)
- (e^{20}≈485,165,195)

logit 차이가 커지면 softmax는 거의 one-hot처럼 뾰족해집니다.

Attention에서 (sqrt{d_k}) scaling을 하는 중요한 이유가 이것입니다.

## 8. Temperature와 Softmax

Generation에서 temperature (T)를 쓰면:

[
p_i=softmax(z_i/T)
]

- (T<1): 분포가 더 뾰족
- (T>1): 더 평평
- (T\to0): 최대 logit 선택에 가까워짐

Attention scaling의 (sqrt{d_k})와 수학 형태는 유사하지만 목적은 다릅니다.

## 9. Causal Mask와 Softmax

Future position score에 (-infty)를 더하면:

[
e^{-infty}=0
]

따라서 softmax 후 masked position의 확률이 0이 됩니다.

이 방식이 decoder causal attention에서 사용됩니다.

## 10. 실무 주의점

- 직접 exp를 구현하기보다 framework의 안정화된 softmax 사용
- loss 함수가 logits를 원하는지 probabilities를 원하는지 확인
- attention에서는 어느 dimension에 softmax를 적용하는지 확인
- mask를 softmax 전 score에 적용
- half precision에서는 overflow/underflow 안정성이 더 중요

## 핵심 정리

- Softmax는 logits를 합이 1인 distribution으로 변환합니다.
- max-logit subtraction으로 수치 안정성을 확보합니다.
- classification뿐 아니라 Transformer attention의 핵심 연산입니다.
- attention scaling, causal mask, sampling temperature가 모두 softmax와 연결됩니다.
- 이 노트는 영상 자막 직역이 아니라 공식 영상 identity와 Outcome School 공식 수치 자료를 근거로 한 상세 보조 노트입니다.
