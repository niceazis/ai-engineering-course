# LLM의 Feed-Forward Network란 무엇이며 어떤 역할을 하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/feed-forward-networks-in-llms  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 expand-then-contract, 차원 수치, activation, parameter 비중, MoE 연결을 보존한 독립적 한국어 해설입니다.

## 1. Attention 뒤에는 무엇이 있는가

Transformer layer를 attention만으로 생각하기 쉽지만, 각 layer에는 큰 Feed-Forward Network(FFN)가 있습니다.

Attention이 **token 사이의 정보를 섞는 단계**라면 FFN은:

> 각 token 위치에서, attention으로 모은 정보를 비선형적으로 변환하고 정제하는 단계

로 볼 수 있습니다.

FFN은 각 token에 독립적으로 동일한 weight를 적용합니다.

## 2. 기본 FFN 구조

원문의 기본 형태:

[
FFN(x)=ReLU(xW_1+b_1)W_2+b_2
]

두 단계입니다.

1. (d_{model})에서 더 큰 hidden dimension으로 확장
2. activation을 적용한 뒤 다시 (d_{model})로 축소

이를 **expand-then-contract** 패턴이라고 볼 수 있습니다.

## 3. 4096 → 16384 → 4096 예

간단한 Transformer를 생각하면:

    input dimension: 4096
          ↓
    Linear W1
          ↓
    hidden: 16384
          ↓
    activation
          ↓
    Linear W2
          ↓
    output: 4096

중간 차원을 크게 만드는 이유는 더 넓은 feature space에서 비선형 조합을 학습할 수 있게 하기 위해서입니다.

## 4. GPT-3의 수치 예

원문은 GPT-3 규모를 예로 듭니다.

- (d_{model}=12,288)
- FFN hidden dimension (=49,152)
- 4배 expansion

즉 한 token representation이 FFN 내부에서 약 4배 넓어졌다가 다시 원래 차원으로 돌아옵니다.

GPT-3는 96개 layer를 사용하므로 이 큰 FFN이 layer마다 반복됩니다.

## 5. ReLU가 하는 일

ReLU:

[
ReLU(x)=max(0,x)
]

예:

- 5 → 5
- -3 → 0

Linear layer만 여러 개 이어 붙이면 전체도 결국 하나의 linear transformation으로 합칠 수 있습니다.

Activation function이 들어가야 network가 비선형 관계를 표현할 수 있습니다.

현대 LLM에서는 ReLU 대신:

- GELU
- SiLU/Swish
- SwiGLU

같은 activation/gating 구조가 흔합니다.

## 6. SwiGLU

원문은 현대 LLM에서 널리 쓰이는 SwiGLU 형태도 연결합니다.

단순화하면:

[
SwiGLU(x)
=
(Swish(xW_1)odot(xV))W_2
]

즉 두 개의 입력 projection 중 하나를 activation하고 다른 하나와 element-wise 곱한 뒤 output projection을 수행합니다.

기본 2-matrix FFN과 달리 gate용 projection이 추가됩니다.

## 7. LLaMA 계열의 expansion은 단순 4배가 아니다

원문 예:

### LLaMA 2 7B

- model dimension: 4096
- FFN hidden: 11008

비율:

[
11008/4096approx2.69
]

### LLaMA 2 70B

- model dimension: 8192
- FFN hidden: 28672

비율:

[
28672/8192=3.5
]

SwiGLU처럼 projection 수가 달라지면 단순히 hidden dimension만 보고 parameter/compute를 비교하면 안 됩니다.

## 8. FFN이 실제로 학습하는 것

Attention이 문맥에서 필요한 정보를 모았다면 FFN은 각 위치의 representation을 feature-wise로 변환합니다.

연구에서는 FFN의 일부 neuron/feature가 특정 사실·패턴과 연관되는 현상을 분석하기도 하지만, “FFN 하나가 데이터베이스처럼 사실을 한 줄씩 저장한다”고 단순화하면 과합니다.

실무적으로는:

- attention = token mixing
- FFN = channel/feature transformation

이라는 구분이 유용합니다.

## 9. Parameter 비중

표준 Transformer에서 단순 계산해 봅니다.

Attention projection:

- Q: (d^2)
- K: (d^2)
- V: (d^2)
- O: (d^2)

합계 약:

[
4d^2
]

4배 hidden dimension을 쓰는 기본 FFN:

- (W_1: d×4d=4d^2)
- (W_2: 4d×d=4d^2)

합계:

[
8d^2
]

따라서 layer의 주요 dense weight만 보면 FFN이 약 2/3를 차지할 수 있습니다.

원문은 GPT-3 175B 중 대략 110~115B 수준이 FFN 계열 parameter라는 직관적 추정을 제시합니다. 이는 layer 구성과 세부 counting 방식에 따른 근사치로 이해해야 합니다.

## 10. Transformer layer 안에서의 위치

원 Transformer의 post-norm 직관:

    x
    → Attention
    → Add + Norm
    → FFN
    → Add + Norm

현대 pre-norm 모델:

    x
    → Norm
    → Attention
    → Add
    → Norm
    → FFN
    → Add

세부 normalization 위치는 architecture마다 다릅니다.

## 11. Mixture of Experts와 FFN의 관계

MoE Transformer는 모든 token이 동일한 하나의 FFN을 통과하는 대신 여러 FFN expert를 둡니다.

    token
      → router
      → expert 2개 선택
      → selected FFNs
      → combine

원문은 예시로 “8개 또는 64개 expert 중 일부, 흔히 2개를 선택”하는 구조를 설명합니다.

핵심 trade-off:

- 전체 parameter 수는 매우 크게 늘릴 수 있음
- 한 token마다 활성화하는 expert는 일부만 사용
- routing과 분산 통신 비용이 새 문제로 생김

즉 MoE의 “expert”는 Transformer에서 주로 FFN block을 여러 개 둔 것으로 이해하면 쉽습니다.

## 12. 왜 FFN이 중요한가

Attention만 있으면 token 간 weighted averaging과 projection은 가능하지만 깊은 비선형 feature transformation이 부족합니다.

FFN은:

- 표현력 확대
- 비선형 feature 조합
- layer별 representation refinement

을 담당합니다.

대규모 LLM의 parameter와 FLOPs에서 매우 큰 부분을 차지하므로 inference 최적화에서도 중요합니다.

## 핵심 정리

- FFN은 Transformer layer마다 존재하며 각 token에 독립적으로 적용됩니다.
- 기본 구조는 expand → activation → contract입니다.
- GPT-3 예에서는 12,288 → 49,152 → 12,288로 4배 expansion입니다.
- 현대 LLM은 GELU/SwiGLU 등을 많이 사용하며 hidden ratio도 모델마다 다릅니다.
- 표준 dense Transformer에서는 FFN이 주요 parameter의 큰 비중을 차지합니다.
- MoE는 여러 FFN expert 중 일부를 token별로 선택하는 방식으로 이해할 수 있습니다.

## 원문

- https://outcomeschool.com/blog/feed-forward-networks-in-llms
