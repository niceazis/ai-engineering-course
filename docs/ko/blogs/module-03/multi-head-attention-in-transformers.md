# Transformer의 Multi-Head Attention이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/multi-head-attention-in-transformers  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 차원 예제와 2-head attention pattern을 보존한 독립적인 한국어 상세 해설입니다.

## 1. 왜 Attention을 여러 개 쓰는가

Self-attention 하나만 있어도 token 간 관계를 계산할 수 있습니다.

하지만 하나의 Q/K/V projection 공간에서 모든 관계를 동시에 표현하게 하면:

- 문법 관계
- 의미 관계
- 대명사 참조
- 장거리 의존성

같은 서로 다른 패턴이 하나의 attention map에 섞일 수 있습니다.

Multi-Head Attention은 **여러 attention을 서로 다른 projection으로 병렬 실행**합니다.

## 2. 기본 Self-Attention 복습

head 하나의 계산:

[
head=softmax(QK^T/sqrt{d_k})V
]

여기서:

[
Q=XW_Q,quad K=XW_K,quad V=XW_V
]

입니다.

Multi-head에서는 head마다 별도의 (W_Q,W_K,W_V)를 가집니다.

## 3. d_model=512, head=8 예

원문의 전형적인 예:

- (d_{model}=512)
- head 수 (h=8)
- head당 (d_k=64)

즉:

[
512 / 8 = 64
]

각 head는 64차원의 Q/K/V 공간에서 attention을 수행합니다.

그 결과 8개의 64차원 출력을 얻고:

[
8	imes64=512
]

차원으로 다시 concatenate합니다.

## 4. 계산 순서

입력:

[
X in mathbb{R}^{n	imes512}
]

각 head (i):

[
Q_i=XW^Q_i
]

[
K_i=XW^K_i
]

[
V_i=XW^V_i
]

[
head_i=Attention(Q_i,K_i,V_i)
]

모든 head를 합칩니다.

[
H=Concat(head_1,ldots,head_8)
]

마지막 output projection:

[
MultiHead(X)=HW_O
]

(W_O)는 head들의 정보를 다시 섞어 (d_{model}) 차원 표현으로 만듭니다.

## 5. 원문의 2-head “I love AI” 예

원문은 직관을 위해 head 2개를 예로 듭니다.

### Head 1 — subject/verb 관계를 강하게 보는 예

| Query | I | love | AI |
| --- | ---: | ---: | ---: |
| I | 0.100 | 0.800 | 0.100 |
| love | 0.700 | 0.200 | 0.100 |
| AI | 0.300 | 0.400 | 0.300 |

“I”가 “love”에 0.8, “love”가 “I”에 0.7을 주므로 subject-verb 관계를 강하게 포착하는 head로 해석할 수 있습니다.

### Head 2 — verb/object 관계를 강하게 보는 예

| Query | I | love | AI |
| --- | ---: | ---: | ---: |
| I | 0.300 | 0.400 | 0.300 |
| love | 0.100 | 0.200 | 0.700 |
| AI | 0.100 | 0.800 | 0.100 |

이번에는 “love”가 “AI”에 0.7, “AI”가 “love”에 0.8입니다.

같은 sentence라도 projection이 다르면 서로 다른 관계를 강조할 수 있습니다.

## 6. “각 head가 특정 문법 기능을 담당한다”는 표현의 주의점

위 예는 좋은 직관이지만 실제 학습된 모델에서:

- head 1은 항상 주어-동사
- head 2는 항상 동사-목적어

처럼 고정 역할이 보장되지는 않습니다.

일부 head에서 해석 가능한 pattern이 나타나기도 하지만 head 간 기능이 중복되거나 분산될 수도 있습니다.

따라서 “여러 representation subspace를 병렬로 학습한다”가 더 정확한 일반 설명입니다.

## 7. Parameter 관점

표준 구현에서 전체 Q/K/V projection parameter 수는 head를 나누기 전의 (d_{model}) 기준으로 묶어서 구현할 수도 있습니다.

예:

    Q = X WQ  → shape [n, 512]
    reshape   → [n, 8, 64]

즉 코드상 head마다 작은 matrix를 따로 호출하지 않고 큰 matrix multiplication 한 번으로 계산한 뒤 reshape하는 경우가 일반적입니다.

개념적으로는 각 head가 서로 다른 projection slice를 갖는 것과 같습니다.

## 8. Decoder에서의 Multi-Head Attention

Decoder-only LLM에서는 각 head에 동일한 causal mask가 적용됩니다.

각 head가 다른 관계를 학습하더라도 미래 token은 볼 수 없습니다.

Encoder-decoder 구조에서는:

- decoder masked self-attention도 multi-head
- encoder-decoder cross-attention도 multi-head

일 수 있습니다.

## 9. Multi-Head의 장점

- 서로 다른 representation subspace에서 관계를 동시에 탐색
- 문법·의미·위치 등 다양한 signal을 병렬로 결합
- 한 개의 attention map보다 표현력 증가
- 큰 행렬 곱으로 효율적으로 구현 가능

다만 head 수를 무조건 늘린다고 품질이 증가하는 것은 아닙니다. (d_{model})이 고정이면 head당 dimension이 줄어드는 trade-off가 있습니다.

## 핵심 정리

- Multi-Head Attention은 서로 다른 Q/K/V projection을 가진 attention head 여러 개를 병렬 실행합니다.
- (d_{model}=512,h=8)이면 전형적으로 head당 64차원입니다.
- 각 head 결과를 concatenate한 뒤 (W_O)로 다시 projection합니다.
- 원문의 2-head 예는 동일 문장에서 서로 다른 관계를 강조할 수 있음을 보여 줍니다.
- 실제 head의 의미가 사람이 정한 역할로 고정되는 것은 아닙니다.

## 원문

- https://outcomeschool.com/blog/multi-head-attention-in-transformers
