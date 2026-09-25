# Transformer의 Cross Attention이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/cross-attention-in-transformers  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 번역 예제와 Q/K/V 출처 차이를 보존해 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Cross-Attention이란?

Self-attention에서는 Q, K, V가 모두 같은 sequence에서 나옵니다.

Cross-attention에서는 **Query와 Key/Value의 출처가 서로 다릅니다.**

Encoder-decoder Transformer라면:

[
Q = Decoder state cdot W_Q
]

[
K = Encoder output cdot W_K
]

[
V = Encoder output cdot W_V
]

그리고 계산식 자체는 동일합니다.

[
CrossAttention(Q,K,V)
=softmaxleft(rac{QK^T}{sqrt{d_k}}ight)V
]

## 2. 왜 필요한가

번역을 생각해 봅니다.

입력 영어:

    How are you

출력 스페인어:

    Cómo estás

Decoder가 “Cómo” 다음 token을 만들 때 단순히 지금까지 생성한 스페인어만 보는 것으로는 부족합니다.

원래 영어 문장의 어떤 부분과 현재 생성 위치가 관련 있는지도 알아야 합니다.

Cross-attention이 decoder와 encoder 사이의 다리 역할을 합니다.

## 3. Query, Key, Value의 출처

### Self-Attention

    Q ← 현재 sequence
    K ← 현재 sequence
    V ← 현재 sequence

### Cross-Attention

    Q ← decoder sequence
    K ← encoder sequence
    V ← encoder sequence

즉 decoder가 질문(Query)을 만들고 encoder의 입력 표현에서 관련 정보(Key/Value)를 찾습니다.

## 4. Shape가 다른 이유

입력 token 수가 3개:

    ["How", "are", "you"]

출력 token 수가 현재 2개라면:

    ["Cómo", "estás"]

Cross-attention score matrix는:

[
n_{target}	imes n_{source}
]

크기가 됩니다.

즉 self-attention처럼 반드시 정사각형일 필요가 없습니다.

예:

    decoder query 2개 × encoder key 3개
    → 2×3 attention map

## 5. 원문의 “Cómo 다음 token” 예

원문은 decoder가 다음 token을 예측하는 한 순간을 단순화합니다.

Encoder token:

- How
- are
- you

현재 decoder가 “Cómo”까지 생성했다고 합시다.

Cross-attention weight가:

- How: 0.050
- are: 0.500
- you: 0.450

이라면 cross-attention output은:

[
0.05V(How)+0.50V(are)+0.45V(you)
]

입니다.

즉 현재 decoder state가 “are you”에 해당하는 입력 정보를 주로 가져옵니다.

## 6. Vocabulary 확률로 연결

Cross-attention 결과와 decoder의 나머지 layer를 거친 뒤 vocabulary logits를 만듭니다.

원문의 단순 확률 예:

- estás: 0.70
- gracias: 0.20
- Hola: 0.10

가장 높은 후보 “estás”가 선택될 수 있습니다.

이 예는 cross-attention이 번역 alignment를 어떻게 돕는지 보여 줍니다.

## 7. Self-Attention vs Cross-Attention

| 항목 | Self-Attention | Cross-Attention |
| --- | --- | --- |
| Q 출처 | 같은 sequence | decoder/consumer sequence |
| K/V 출처 | 같은 sequence | encoder/source sequence |
| score shape | 보통 n×n | target length × source length |
| 대표 역할 | sequence 내부 관계 | 두 sequence/모달리티 연결 |
| decoder mask | causal일 수 있음 | 일반적으로 source 전체를 볼 수 있음 |

Encoder-decoder cross-attention에서는 source 입력 전체가 이미 주어졌기 때문에 일반적으로 causal mask가 필요하지 않습니다.

## 8. Encoder K/V는 재사용 가능

Autoregressive decoding에서 source sentence는 바뀌지 않습니다.

따라서 encoder output에서 만든 K/V는 한 번 계산해 두고 여러 decoder step에서 재사용할 수 있습니다.

    Encoder(source)
      → K_encoder, V_encoder  [고정]

    Decoder step 1 → Q1 → cross-attention
    Decoder step 2 → Q2 → cross-attention
    Decoder step 3 → Q3 → cross-attention

이 재사용은 encoder-decoder inference를 이해할 때 중요합니다.

## 9. 번역 이외의 활용

Cross-attention은 서로 다른 정보 stream을 연결하는 일반 메커니즘입니다.

예:

- text decoder가 image encoder feature를 참고
- speech decoder가 audio encoder feature를 참고
- multimodal model에서 modality 간 정보 결합
- diffusion image model에서 image latent가 text condition을 참고

다만 구체 모델마다 architecture는 다르므로 “멀티모달이면 항상 cross-attention”이라고 일반화해서는 안 됩니다.

## 핵심 정리

- Cross-attention은 Q와 K/V가 서로 다른 source에서 나옵니다.
- Encoder-decoder에서는 Q가 decoder, K/V가 encoder에서 옵니다.
- 공식은 self-attention과 동일하지만 데이터 흐름이 다릅니다.
- 원문의 “How are you” → “Cómo estás” 예에서 decoder는 “are/you”에 높은 weight를 둡니다.
- source K/V는 decoding step마다 재사용할 수 있습니다.
- 번역뿐 아니라 서로 다른 sequence나 modality를 연결하는 데 사용됩니다.

## 원문

- https://outcomeschool.com/blog/cross-attention-in-transformers
