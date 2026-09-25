# Transformer 아키텍처는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/decoding-transformer-architecture  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 구성 순서와 구체 예시를 유지하되 문장은 독립적으로 다시 쓴 한국어 학습 노트입니다.

## 1. Transformer가 등장한 이유

Transformer 이전의 대표 sequence model인 RNN/LSTM은 입력을 한 단계씩 순차 처리합니다.

긴 문장에서 초반 정보를 뒤쪽까지 전달하기 어렵고, 같은 sequence 안의 계산을 병렬화하기도 어렵습니다.

2017년 논문 **Attention Is All You Need**는 recurrence를 제거하고 attention을 중심으로 sequence를 처리하는 Transformer를 제안했습니다.

핵심 변화는 다음과 같습니다.

> “이전 hidden state를 순서대로 전달하지 말고, 현재 token이 다른 모든 관련 token을 직접 참고하게 하자.”

## 2. 원래 Transformer의 두 절반

원 논문의 Transformer는 크게 두 부분입니다.

- **Encoder**: 입력 sequence를 읽고 contextual representation을 만듭니다.
- **Decoder**: encoder의 표현과 지금까지 생성한 출력 token을 참고해 다음 token을 생성합니다.

번역을 예로 들면:

    입력: "I love learning"
           ↓
        Encoder
           ↓
    문맥화된 표현
           ↓
        Decoder
           ↓
    "J'adore apprendre"

현대 모델은 이 구조 전체를 항상 쓰지는 않습니다.

- BERT: encoder-only
- GPT 계열: decoder-only
- T5: encoder-decoder

## 3. Tokenization

문자열을 그대로 신경망에 넣을 수 없으므로 먼저 token으로 나눕니다.

    "I love learning"
       ↓
    ["I", "love", "learning"]
       ↓
    token IDs

실제 tokenizer는 단어가 아니라 subword/byte 단위일 수 있습니다. 앞 레슨의 BPE가 이 단계와 연결됩니다.

## 4. Token Embedding

각 token ID는 학습 가능한 embedding table을 통해 (d_{model}) 차원 vector로 변환됩니다.

    token_id → embedding vector

예를 들어 (d_{model}=512)라면 token 하나는 512개의 숫자로 표현됩니다.

Embedding은 token의 기본 의미 표현이지만 아직 문맥은 충분히 반영되지 않았습니다. “bank”가 강둑인지 은행인지는 주변 token과 상호작용한 뒤 구체화됩니다.

## 5. Positional Information

Self-attention 자체는 token 집합의 순서를 자동으로 알지 못합니다.

    "dog bites man"
    "man bites dog"

은 순서가 다르므로 의미도 달라집니다.

그래서 위치 정보를 embedding에 더하거나 Q/K를 회전시키는 방식 등을 사용합니다.

- 원 Transformer: sinusoidal positional encoding
- 일부 모델: learned positional embedding
- 현대 LLM 다수: RoPE

## 6. Self-Attention

Self-attention은 token 하나가 같은 sequence 안의 다른 token을 얼마나 참고할지 계산합니다.

핵심 수식:

    Attention(Q, K, V)
      = softmax(QKᵀ / √dₖ)V

각 token 표현 (X)에서 세 projection을 만듭니다.

    Q = XWQ
    K = XWK
    V = XWV

직관은 다음과 같습니다.

- Q(Query): 내가 무엇을 찾는가
- K(Key): 내가 어떤 정보를 제공하는가
- V(Value): 실제로 전달할 정보는 무엇인가

## 7. 왜 √dₖ로 나누는가

Q·K dot product는 차원 (d_k)가 커질수록 값의 분산이 커집니다.

큰 score를 softmax에 바로 넣으면 분포가 지나치게 뾰족해져 gradient가 불안정해질 수 있습니다.

그래서 score를 (sqrt{d_k})로 나눠 scale을 안정화합니다.

이 수학은 별도 레슨인 “Scaling Dot-Product Attention”에서 자세히 다룹니다.

## 8. Multi-Head Attention

Attention 하나만 쓰지 않고 여러 head를 병렬로 사용합니다.

(d_{model}=512), head 8개라면 흔한 구성에서 head당 (d_k=64)입니다.

각 head는 서로 다른 projection matrix를 가지므로:

- 문법적 관계
- 주어-동사 관계
- 대명사 참조
- 의미적 유사성

같은 서로 다른 패턴을 병렬로 포착할 수 있습니다.

각 head 결과를 concatenate한 뒤 output projection을 적용합니다.

## 9. Feed-Forward Network

Attention 뒤에는 token별로 독립적으로 같은 FFN을 적용합니다.

전형적인 형태:

    FFN(x) = activation(xW1 + b1)W2 + b2

Attention이 token 사이에서 정보를 섞는 단계라면, FFN은 **각 token 위치에서 표현을 비선형적으로 변환하는 단계**입니다.

현대 LLM에서는 ReLU 대신 GELU, SwiGLU 등이 흔합니다.

## 10. Residual Connection과 Layer Normalization

깊은 Transformer에서는 각 sublayer 주변에 residual connection과 normalization을 둡니다.

개념적으로:

    y = LayerNorm(x + Sublayer(x))

원 논문은 post-norm 형태를 사용했지만, 현대 LLM은 다음처럼 sublayer 전에 normalization하는 pre-norm 변형을 많이 사용합니다.

    y = x + Sublayer(Norm(x))

Residual connection은 정보와 gradient가 깊은 layer를 통과하기 쉽게 합니다. LayerNorm/RMSNorm은 activation scale을 안정화합니다.

## 11. Encoder의 흐름

Encoder layer의 전형적인 흐름:

1. 입력 embedding + 위치 정보
2. multi-head self-attention
3. residual + normalization
4. feed-forward network
5. residual + normalization
6. 다음 encoder layer로 전달

원문은 “I love learning”이 여러 encoder layer를 통과하면서 각 token 표현이 점점 문맥화되는 예를 듭니다.

초기 embedding은 단어 자체의 기본 표현에 가깝지만, 상위 layer의 “love”는 주어 “I”, 목적어/대상 “learning”과의 관계가 반영된 표현이 됩니다.

## 12. Decoder의 흐름

Encoder-decoder Transformer의 decoder에는 세 핵심 sublayer가 있습니다.

1. **Masked self-attention**  
   아직 생성하지 않은 미래 token을 보지 못하게 causal mask를 적용합니다.

2. **Cross-attention**  
   decoder의 Q가 encoder 출력의 K/V를 참고합니다.

3. **FFN**  
   각 위치의 표현을 비선형 변환합니다.

이후 최종 hidden state에 linear layer를 적용해 vocabulary 크기의 logits를 만듭니다.

예를 들어 vocabulary가 50,000개라면 마지막 projection은 다음 token 후보 50,000개에 대한 score를 출력합니다.

    hidden state
      → Linear
      → 50,000 logits
      → Softmax / sampling
      → next token

## 13. 전체 데이터 흐름

Encoder-decoder 번역을 한 줄로 연결하면:

    text
    → tokenizer
    → token IDs
    → embeddings + position
    → encoder layers
    → contextual encoder states
    → decoder masked self-attention
    → cross-attention to encoder
    → decoder FFN
    → vocabulary logits
    → next token
    → 반복

## 14. Transformer의 세 가지 형태

### Encoder-only

입력 전체를 양방향으로 읽고 표현을 만드는 데 강합니다.

대표: BERT  
용도: 분류, token tagging, embedding 계열 작업

### Decoder-only

causal mask를 사용해 이전 token만 보고 다음 token을 생성합니다.

대표: GPT 계열  
용도: 텍스트 생성, 챗봇, 코드 생성

### Encoder-decoder

입력을 encoder가 읽고 decoder가 출력을 생성합니다.

대표: T5  
용도: 번역, 요약, sequence-to-sequence

## 15. Transformer가 강력한 이유

1. 학습 시 sequence token을 행렬 연산으로 병렬 처리할 수 있습니다.
2. attention으로 먼 token도 직접 연결합니다.
3. 같은 블록을 깊게 쌓아 규모를 확장하기 쉽습니다.
4. 언어뿐 아니라 이미지, 오디오, 멀티모달 입력에도 같은 기본 구조를 확장할 수 있습니다.

단, 표준 attention은 sequence 길이에 대해 (O(n^2)) 비용이므로 긴 문맥에서는 최적화가 필요합니다.

## 핵심 정리

- Transformer의 핵심은 attention 기반 token 간 직접 상호작용입니다.
- 입력은 tokenization → embedding → positional information을 거칩니다.
- attention은 Q/K/V로 관계를 계산하고, FFN은 각 token 표현을 변환합니다.
- residual과 normalization은 깊은 학습을 안정화합니다.
- encoder-only, decoder-only, encoder-decoder 세 형태가 있습니다.
- 현대 LLM은 주로 decoder-only Transformer를 대규모로 확장한 형태입니다.

## 원문

- https://outcomeschool.com/blog/decoding-transformer-architecture
