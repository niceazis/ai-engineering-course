# Transformer의 Self Attention이란 무엇이며 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/self-attention-in-transformers  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 대명사 예제, Q/K/V 직관, 수치 attention 예를 보존해 독립적으로 다시 쓴 상세 해설입니다.

## 1. Self-Attention이 필요한 이유

문장에서 어떤 단어의 의미는 주변 문맥에 따라 달라집니다.

원문의 핵심 예:

> “The animal did not cross the street because it was too tired.”

여기서 “it”은 “animal”을 가리킵니다.

반면:

> “The animal did not cross the street because it was too wide.”

이번 “it”은 “street”을 가리킵니다.

같은 대명사라도 주변 단어와의 관계를 봐야 올바른 의미를 만들 수 있습니다.

Self-attention은 **각 token이 같은 sequence의 다른 token들을 얼마나 참고할지 학습하는 메커니즘**입니다.

## 2. 왜 이름이 Self-Attention인가

Q, K, V가 모두 같은 sequence의 representation에서 만들어지기 때문입니다.

    X → Q
    X → K
    X → V

다른 sequence의 K/V를 참고하면 cross-attention이라고 부릅니다.

## 3. Query, Key, Value의 직관

원문은 이를 다음처럼 설명합니다.

- **Query(Q)**: 현재 token이 찾고 있는 정보
- **Key(K)**: 각 token이 어떤 정보를 제공할 수 있는지 나타내는 표지
- **Value(V)**: 실제 전달할 내용

도서관 비유로 보면:

- Query: “내가 찾는 책의 주제”
- Key: 각 책의 색인/분류 정보
- Value: 실제 책 내용

Query와 Key가 잘 맞을수록 그 Value를 더 많이 가져옵니다.

## 4. Step 1 — Q, K, V 만들기

입력 matrix (X)에 학습 가능한 projection matrix를 곱합니다.

    Q = XW_Q
    K = XW_K
    V = XW_V

같은 token embedding이라도 세 projection은 역할이 다르므로 별도 weight를 사용합니다.

## 5. Step 2 — Attention score 계산

각 Query와 모든 Key의 dot product를 계산합니다.

    Scores = QKᵀ

score가 클수록 두 token 사이의 관련성이 높다고 모델이 판단한 것입니다.

sequence 길이가 (n)이면 score matrix 크기는 (n 	imes n)입니다.

## 6. Step 3 — Scale

score를 (sqrt{d_k})로 나눕니다.

    ScaledScores = QKᵀ / √dₖ

(d_k)가 커질수록 dot product 분산도 커지기 때문에 softmax가 지나치게 포화되는 것을 완화합니다.

## 7. Step 4 — Softmax

각 row에 softmax를 적용해 합이 1인 attention weight를 만듭니다.

    A = softmax(ScaledScores)

이제 각 row는 “현재 token이 다른 token을 몇 %씩 참고하는가”로 해석할 수 있습니다.

## 8. Step 5 — Value의 가중합

최종 출력:

    O = A V

즉 각 token의 새 representation은 다른 token Value의 weighted sum입니다.

## 9. 원문의 “I love AI” 수치 예

원문은 세 token의 attention weight를 다음과 같이 제시합니다.

| Query | I | love | AI |
| --- | ---: | ---: | ---: |
| I | 0.070 | 0.707 | 0.223 |
| love | 0.333 | 0.333 | 0.333 |
| AI | 0.168 | 0.533 | 0.299 |

첫 row는 “I” token의 출력이:

    Output(I)
      = 0.070 × V(I)
      + 0.707 × V(love)
      + 0.223 × V(AI)

로 만들어짐을 뜻합니다.

즉 “I”는 이 head에서 “love”의 정보를 가장 강하게 가져옵니다.

## 10. Self-Attention이 잘 작동하는 이유

### 장거리 관계를 직접 연결

멀리 떨어진 두 token도 한 번의 attention layer 안에서 직접 관계를 만들 수 있습니다.

### 문맥에 따라 표현이 달라짐

동일한 token “bank”도 주변 단어에 따라 attention pattern이 달라져 서로 다른 contextual representation을 만들 수 있습니다.

### 학습 병렬화

RNN처럼 이전 hidden state를 기다리지 않고 sequence 전체의 Q/K/V를 행렬 곱으로 한 번에 계산할 수 있습니다.

## 11. Multi-Head Self-Attention

Attention 한 개만 쓰면 하나의 projection 공간에서 관계를 계산합니다.

Multi-head attention은 서로 다른 (W_Q, W_K, W_V)를 가진 여러 head를 동시에 사용합니다.

예를 들어 어떤 head는:

- 주어-동사 관계

다른 head는:

- 대명사 참조

또 다른 head는:

- 문장 내 의미 유사성

을 포착할 수 있습니다.

각 head의 결과는 concatenate한 뒤 (W_O)로 다시 projection합니다.

## 12. Encoder와 Decoder에서의 차이

Encoder self-attention은 보통 입력 전체를 볼 수 있습니다.

Decoder self-attention은 causal mask를 사용해 미래 token을 차단합니다.

따라서 같은 수식이라도 mask 규칙이 다릅니다.

    Encoder:
    softmax(QKᵀ / √dₖ)V

    Decoder:
    softmax((QKᵀ + causal_mask) / √dₖ)V

## 13. 비용과 한계

표준 self-attention의 score matrix는 (n 	imes n)입니다.

따라서 sequence가 2배 길어지면 attention score 원소 수는 약 4배가 됩니다.

이 때문에 긴 문맥을 다루는 모델은:

- sliding window attention
- sparse attention
- FlashAttention 같은 메모리 효율 구현
- KV cache

등을 조합합니다.

## 핵심 정리

- Self-attention은 같은 sequence의 token끼리 중요도를 계산합니다.
- Q는 찾는 정보, K는 매칭 기준, V는 전달 내용입니다.
- 핵심 수식은 (	ext{softmax}(QK^T/sqrt{d_k})V)입니다.
- “I love AI” 예에서 각 row는 다른 token의 Value를 얼마나 섞는지 보여 줍니다.
- Multi-head는 서로 다른 관계를 병렬로 학습하게 합니다.
- Encoder와 Decoder의 핵심 차이 중 하나는 causal mask 여부입니다.

## 원문

- https://outcomeschool.com/blog/self-attention-in-transformers
