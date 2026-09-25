# Mixture of Experts(MoE)란 무엇이며 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/mixture-of-experts  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-04-09 공개 원문을 직접 확인해 설명 순서, router 수식, 8-expert 예, Mixtral 수치, load balancing과 weighted sum을 보존하면서 독립적으로 다시 쓴 한국어 해설입니다.

## 1. 큰 그림

MoE는 하나의 큰 dense network를 모든 input에 쓰는 대신 **여러 expert network 중 일부만 token별로 활성화**합니다.

구성:

    many experts + router

원문은 병원의 전문의 비유를 사용합니다.

환자가 모든 의사를 만나는 것이 아니라 접수 담당이 적합한 전문의에게 보내는 것처럼, router가 token마다 사용할 expert를 고릅니다.

## 2. Dense Model의 문제

원문은 100B dense model을 예로 듭니다.

Dense model에서는 token 하나가 지나갈 때 전체 100B parameter가 계산에 참여합니다.

두 문제:

1. model이 커질수록 token당 compute와 GPU cost 증가
2. 모든 input이 모든 network capacity를 사용해야 해 불필요한 계산 발생

MoE의 목표는 총 parameter 수를 크게 유지하면서 실제 token당 active compute는 작게 만드는 것입니다.

## 3. Expert란 무엇인가

현대 LLM의 MoE에서 expert는 일반적으로 Transformer의 **Feed-Forward Network**입니다.

예를 들어 한 MoE layer에:

- 8 experts
- 64 experts
- 128 experts

를 둘 수 있습니다.

중요한 오해:

Expert가 사람이 “수학 전문가”, “법률 전문가”처럼 label을 붙여 훈련한 network라는 뜻은 아닙니다.

원문은 실제 specialization이 punctuation, token shape, word type 같은 낮은 수준 pattern으로 나타날 수 있고 training 중 스스로 형성된다고 설명합니다.

## 4. Router

Router는 token representation을 보고 모든 expert의 score를 만듭니다.

원문의 수식:

    Router(x) = Softmax(x × W_router)

8 expert라면 8개 score/probability가 나옵니다.

그 뒤 top-k expert만 선택합니다.

일반적인 예:

    k = 2

Switch Transformer 같은 구조는 k=1을 사용할 수 있습니다.

## 5. 8 Expert, Top-2 예

Router가:

    Expert 3: 0.7
    Expert 5: 0.3

을 선택했다고 합시다.

다른 6 expert는 해당 token에 대해 실행하지 않습니다.

이것을 sparse activation이라고 합니다.

## 6. Transformer에서 어디에 들어가는가

일반 Transformer layer:

    attention
      → FFN

MoE Transformer:

    attention
      → router
      → selected expert FFNs
      → combine

원문은 **attention layer를 MoE로 바꾸는 것이 아니라 FFN sub-layer를 expert 집합으로 교체**한다고 명확히 설명합니다.

또 모든 layer가 MoE일 필요는 없고 dense layer와 MoE layer를 번갈아 배치할 수도 있습니다.

## 7. Layer마다 Router가 따로 있다

원문의 32-layer 예:

    MoE Layer 1  → Router 1
    MoE Layer 2  → Router 2
    ...
    MoE Layer 32 → Router 32

Router weight는 layer 사이에 공유하지 않습니다.

각 layer가 자기 expert 집합에 대해 독립적인 routing pattern을 학습합니다.

## 8. Total Parameters vs Active Parameters

원문의 단순 예:

    8 experts
    each expert = 10B
    total expert parameters = 80B

top-2만 사용한다면 expert compute는 token당 20B 규모입니다.

총 capacity와 active compute가 분리됩니다.

## 9. Mixtral 8x7B 예

원문 수치:

- 8 experts
- total size 약 47B
- active parameters/token 약 13B

8×7=56B가 아닌 이유는 attention, embedding, normalization 등 shared parameter가 expert마다 복제되지 않기 때문입니다.

따라서 모델 이름만 곱해 total parameter를 계산하면 틀릴 수 있습니다.

## 10. Load Imbalance 문제

Router가 늘 같은 expert 두 개만 고르면:

- 일부 expert에 traffic 집중
- 나머지 expert는 거의 학습되지 않음
- 전체 capacity 낭비

가 발생합니다.

원문은 이를 load imbalance라고 설명합니다.

## 11. Auxiliary Load-Balancing Loss

Training 중 main objective에 보조 loss를 추가해 token이 expert에 더 고르게 분산되도록 유도합니다.

이 방식은 Switch Transformer, GShard 같은 MoE 계열 연구에서 사용됐습니다.

목적은 router가 극소수 expert에 collapse하는 것을 막는 것입니다.

## 12. Expert Capacity

각 expert가 한 batch에서 처리할 수 있는 token 수에는 practical capacity limit이 있을 수 있습니다.

한 expert로 너무 많은 token이 몰리면 overflow token을:

- drop
- next-best expert로 reroute

하는 정책을 사용할 수 있습니다.

따라서 load balancing은 품질뿐 아니라 distributed system 운영에도 중요합니다.

## 13. 여러 Expert Output을 합치는 방법

Top-k expert는 각각 output vector를 만듭니다.

원문 예:

    score(E3) = 0.7
    score(E5) = 0.3

최종:

    output = 0.7 × Out_3 + 0.3 × Out_5

즉 hard selection만 하는 것이 아니라 선택 expert output을 router weight로 weighted sum합니다.

원문은 선택된 top-k score에 대해 softmax를 적용해 weight 합이 1이 되게 하는 설명을 사용합니다.

## 14. 장점

### 큰 총 capacity

수백 B~T parameter 규모까지 확장하면서 token당 active parameter를 제한할 수 있습니다.

### 적은 token당 compute

선택 expert만 실행합니다.

### 자연스러운 specialization

Router와 experts가 training 중 역할을 분화할 수 있습니다.

### Scaling efficiency

동일 compute budget에서 dense model보다 더 큰 capacity를 확보할 수 있습니다.

## 15. 과제

### Memory

활성 expert가 일부여도 전체 expert weight는 memory/storage에 존재해야 합니다.

80B total model은 active 20B라도 weight memory는 80B 규모입니다.

### Routing / Load Balance

Router collapse를 막아야 합니다.

### Communication

Expert가 여러 GPU/node에 흩어져 있으면 token dispatch와 gather가 all-to-all communication bottleneck을 만듭니다.

### Fine-Tuning

Fine-tuning으로 routing distribution이 바뀔 수 있어 dense model보다 관리가 어렵습니다.

## 16. 왜 현대 LLM에서 중요한가

원문은 Mixtral, DeepSeek-V2/V3 등을 MoE 사례로 제시합니다.

핵심 목적:

> model capacity를 키우되 token당 계산량을 같은 비율로 키우지 않는다.

이것이 dense scaling의 비용 벽을 낮추는 핵심입니다.

## 핵심 정리

- Expert는 보통 독립 FFN입니다.
- Router는 token마다 expert score를 내고 top-k만 활성화합니다.
- 원문 기본 예는 8 expert 중 top-2입니다.
- MoE는 Transformer의 FFN 부분을 대체하며 attention은 그대로 둘 수 있습니다.
- Total parameters와 active parameters를 반드시 구분해야 합니다.
- Load balancing, expert capacity, distributed communication이 핵심 운영 문제입니다.
- Selected expert output은 router weight로 가중합됩니다.

## 원문

- https://outcomeschool.com/blog/mixture-of-experts
