# LLM 아키텍처의 진화 — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/evolution-of-llm-architecture  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문 전체 번역이 아닌 독립적인 한국어 상세 해설입니다. 현재 원문 본문은 웹 캐시에서 직접 열리지 않았습니다. Outcome School 공식 홈페이지의 2026-09-21 글 소개와 공식 Module 5 레슨 개요에서 확인한 진화 순서를 기준으로 작성하고, 세부 기술 설명은 각 기술의 공개 논문·공식 자료와 교차검증했습니다. 확인하지 못한 문장을 원문 내용이라고 단정하지 않습니다.

## 1. 이 레슨의 질문

LLM 아키텍처의 역사는 단순히 모델 파라미터가 커진 역사만이 아닙니다.

각 세대는 이전 세대의 병목을 해결하면서 바뀌었습니다.

    RNN
      → 긴 거리 기억과 병렬화 문제
    Attention
      → 필요한 과거 위치를 직접 참고
    Transformer
      → recurrence 제거, 대규모 병렬 학습
    Scaling
      → data/model/compute 확대
    MoE
      → 전체 파라미터와 token당 compute 분리
    Modern efficient attention
      → 긴 context와 serving 비용 최적화

Outcome School의 공식 소개도 이 흐름을 “단어를 한 개씩 읽던 모델에서 오늘날 대형 모델까지”의 변화로 설명합니다.

## 2. Stage 1 — RNN: 한 단어씩 읽기

RNN은 sequence를 순서대로 처리합니다.

    h_t = f(x_t, h_(t-1))

현재 hidden state는 현재 token과 이전 hidden state에 의존합니다.

장점:

- sequence 순서를 자연스럽게 반영
- streaming 입력에 직관적
- 작은 모델에서는 구조가 단순

문제:

- step t는 t-1을 기다려야 하므로 sequence 내부 병렬화가 어렵습니다.
- 먼 과거 정보가 여러 recurrent step을 거쳐야 합니다.
- 긴 sequence에서 vanishing/exploding gradient와 장기 의존성 문제가 나타납니다.

LSTM과 GRU는 gate로 기억 문제를 완화했지만 순차 계산 자체를 제거하지는 못했습니다.

## 3. Stage 2 — Attention: 필요한 위치를 직접 본다

Attention의 핵심 아이디어는 현재 위치가 모든 관련 위치에 직접 score를 계산하는 것입니다.

    Attention(Q, K, V)
      = softmax(QK^T / sqrt(d_k)) V

이제 token 100이 token 1의 정보를 얻기 위해 99개의 recurrent transition을 통과할 필요가 없습니다.

Attention은 특히 encoder-decoder 번역 모델에서 긴 문장 관계를 개선하는 데 중요한 역할을 했습니다.

하지만 초기 attention 시스템은 여전히 RNN과 함께 쓰이는 경우가 많았고, recurrent bottleneck이 완전히 사라진 것은 아니었습니다.

## 4. Stage 3 — Transformer: Recurrence를 제거하다

2017년 Transformer는 recurrence 없이 attention을 중심으로 sequence를 처리합니다.

핵심 블록:

1. token embedding
2. positional information
3. multi-head attention
4. feed-forward network
5. residual connection
6. normalization

학습 시 한 sequence의 여러 token을 큰 matrix operation으로 병렬 처리할 수 있어 GPU/TPU 확장성이 크게 좋아졌습니다.

이 변화가 BERT, GPT 계열 등 현대 LLM의 공통 기반이 됐습니다.

## 5. Encoder, Decoder, Decoder-only

Transformer는 세 가지 큰 형태로 발전했습니다.

### Encoder-only

입력 전체를 양방향으로 봅니다.

대표: BERT 계열

### Encoder-decoder

source를 encoder가 읽고 target을 decoder가 생성합니다.

대표: T5 계열

### Decoder-only

causal mask를 사용해 다음 token prediction을 반복합니다.

대표: GPT 계열과 다수 현대 LLM

대규모 사전학습과 in-context learning이 중요해지면서 decoder-only 구조가 범용 생성 모델의 중심으로 자리 잡았습니다.

## 6. Stage 4 — Scaling

Transformer는 architecture가 행렬 연산 중심이라 model/data/compute를 크게 확장하기 쉬웠습니다.

Scaling이 의미하는 것은 단순히 layer 수만 늘리는 것이 아닙니다.

- 파라미터 수
- 학습 token 수
- training FLOPs
- context length
- batch/parallelism
- inference infrastructure

를 함께 확장해야 합니다.

대형 모델에서는 작은 architecture 차이도 전체 compute·memory 비용에 큰 영향을 줍니다.

## 7. Scaling의 새 병목

Dense Transformer에서 모든 token이 모든 FFN parameter를 사용하면 model size 증가가 곧 token당 compute 증가로 연결됩니다.

또 full attention은 sequence length N에 대해 N×N score matrix를 다루므로 long context에서 비용이 커집니다.

따라서 “더 크게” 다음에는 “더 효율적으로 크게”가 핵심 문제가 됐습니다.

## 8. Stage 5 — Mixture of Experts

MoE는 Transformer의 FFN 부분을 여러 expert로 나누고 router가 token마다 일부 expert만 활성화합니다.

예:

    experts = 8
    top-k = 2

라면 token 하나는 8개 expert 전체가 아니라 2개만 통과합니다.

이를 통해:

- 총 parameter capacity는 크게 유지
- token당 active parameter와 compute는 상대적으로 작게 유지

할 수 있습니다.

이것이 total parameters와 active parameters를 구분하는 이유입니다.

## 9. Modern Attention Efficiency

현대 LLM에서는 attention의 memory/compute 병목을 줄이는 여러 기법이 결합됩니다.

### GQA/MQA

여러 Query head가 Key/Value를 공유해 KV cache를 줄입니다.

### Sliding Window Attention

각 token이 제한된 local window만 보게 해 attention 범위를 줄입니다.

### FlashAttention

attention 수학을 바꾸지 않고 GPU memory traffic을 줄이는 IO-aware implementation입니다.

### Sparse/Compressed Attention

모든 과거 위치를 동일하게 처리하지 않고 중요 후보만 보거나 압축 representation을 사용합니다.

## 10. Position Encoding의 변화

초기 Transformer는 sinusoidal absolute positional encoding을 사용했습니다.

현대 LLM은 RoPE 같은 relative-position 성질이 좋은 방식을 널리 사용합니다.

Long context를 늘릴 때는 positional representation도 함께 고려해야 하며, 단순히 maximum length만 바꾸는 것으로 충분하지 않습니다.

## 11. Normalization과 FFN의 변화

원 Transformer 이후에도 layer 내부는 계속 바뀌었습니다.

대표 변화:

- Post-Norm → Pre-Norm 계열
- LayerNorm → RMSNorm
- ReLU/GELU → SwiGLU
- dense FFN → MoE FFN

이 변화들은 training stability, compute efficiency, quality를 개선하기 위해 도입됐습니다.

## 12. Long-Context 방향

현대 model의 중요한 요구는 수십만~백만 token context입니다.

하지만 context capacity가 늘면:

- attention compute
- KV cache
- prefill latency
- 위치 일반화
- lost-in-the-middle

문제가 커집니다.

그래서 효율적 attention, cache compression, reranking/RAG, context compaction이 architecture와 system 양쪽에서 함께 발전합니다.

## 13. 모델 아키텍처는 단독으로 평가하지 않는다

최신 LLM을 비교할 때 다음을 함께 봐야 합니다.

| 축 | 질문 |
| --- | --- |
| Attention | MHA/GQA/MQA/SWA/sparse인가? |
| FFN | dense인가 MoE인가? |
| Position | 어떤 positional scheme인가? |
| Norm | LayerNorm/RMSNorm, pre/post 구조인가? |
| Context | 실제 활용 가능한 길이는 얼마인가? |
| Precision | BF16/FP8/FP4 등 어떤 training/inference 전략인가? |
| Serving | KV cache, batching, speculative decoding을 어떻게 쓰는가? |

Architecture와 serving system은 실제 비용·latency에서 분리하기 어렵습니다.

## 14. 진화 과정을 문제-해결로 정리

| 세대 | 핵심 문제 | 주요 해결 |
| --- | --- | --- |
| RNN | 장기 의존성, 순차 병목 | LSTM/GRU, Attention |
| Attention+RNN | recurrence가 남음 | Transformer |
| Transformer | scale 확대 필요 | 대규모 pretraining |
| Dense scaling | 모든 parameter를 매 token 사용 | MoE |
| Full MHA | KV cache 큼 | GQA/MQA |
| Full attention | 긴 sequence 비용 | SWA/sparse/FlashAttention |
| Long context | memory·quality 문제 | compression, efficient attention, context engineering |

## 핵심 정리

- LLM 아키텍처의 진화는 병목을 하나씩 제거한 과정입니다.
- RNN은 sequence를 순차 처리했고, attention은 먼 위치를 직접 연결했습니다.
- Transformer는 recurrence를 제거해 대규모 병렬 학습을 가능하게 했습니다.
- Scaling 이후에는 token당 compute와 memory를 줄이는 MoE·GQA·FlashAttention·SWA가 중요해졌습니다.
- 현대 모델은 하나의 기법이 아니라 여러 최적화를 결합합니다.
- 공식 원문 본문을 직접 열지 못한 부분은 Outcome School 공식 소개와 공개 기술 자료를 기준으로만 설명했습니다.

## 원문

- https://outcomeschool.com/blog/evolution-of-llm-architecture
