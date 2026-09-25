# Attention은 어떻게 동작하는가? Q, K, V의 수학 — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/math-behind-attention-qkv  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 행렬·수치 예제를 직접 따라 계산하면서 독립적으로 다시 쓴 한국어 해설입니다.

## 1. Attention 공식

Scaled Dot-Product Attention의 핵심 수식은 다음과 같습니다.

[
Attention(Q,K,V)=softmaxleft(rac{QK^T}{sqrt{d_k}}ight)V
]

각 항의 역할:

- (Q): 현재 token이 찾는 정보
- (K): 각 token이 제공하는 정보의 식별자
- (V): 실제 전달할 내용
- (QK^T): Query와 Key의 유사도 score
- (sqrt{d_k}): score 크기를 안정화하는 scale
- softmax: score를 합이 1인 weight로 변환

원문은 “I love AI”라는 3-token 문장을 끝까지 수치로 계산합니다.

## 2. Step 1 — 단어를 embedding으로 표현

원문은 이해를 쉽게 하려고 embedding dimension을 4로 둡니다.

[
I=[1,0,1,0]
]

[
love=[0,1,0,1]
]

[
AI=[1,1,0,0]
]

이를 matrix로 쌓으면:

[
X=
egin{bmatrix}
1&0&1&0\
0&1&0&1\
1&1&0&0
end{bmatrix}
]

shape은 (3 \times 4)입니다.

- 3: token 수
- 4: embedding dimension

## 3. Step 2 — Q, K, V projection matrix

원문에서는 (d_k=3)으로 두고 다음 weight matrix를 사용합니다.

[
W_Q=
egin{bmatrix}
1&0&1\
0&1&0\
1&0&0\
0&1&1
end{bmatrix}
]

[
W_K=
egin{bmatrix}
0&1&0\
1&0&1\
0&0&1\
1&1&0
end{bmatrix}
]

[
W_V=
egin{bmatrix}
1&0&0\
0&1&0\
0&0&1\
1&1&0
end{bmatrix}
]

각각 shape은 (4 \times 3)입니다.

실제 모델에서는 이 값들이 학습되지만, 원문 예제에서는 계산 과정을 보여 주기 위해 고정 숫자를 사용합니다.

## 4. Step 3 — Q, K, V 계산

[
Q=XW_Q,quad K=XW_K,quad V=XW_V
]

결과:

[
Q=
egin{bmatrix}
2&0&1\
0&2&1\
1&1&1
end{bmatrix}
]

[
K=
egin{bmatrix}
0&1&1\
2&1&1\
1&1&1
end{bmatrix}
]

[
V=
egin{bmatrix}
1&0&1\
1&2&0\
1&1&0
end{bmatrix}
]

예를 들어 “I”의 Query는:

[
[1,0,1,0]W_Q=[2,0,1]
]

입니다.

## 5. Step 4 — (QK^T) score 계산

모든 Query와 모든 Key의 dot product를 계산합니다.

[
QK^T=
egin{bmatrix}
1&5&3\
3&3&3\
2&4&3
end{bmatrix}
]

첫 row를 직접 확인하면:

- I query · I key  
  (2×0+0×1+1×1=1)
- I query · love key  
  (2×2+0×1+1×1=5)
- I query · AI key  
  (2×1+0×1+1×1=3)

따라서 이 head에서는 “I”의 Query가 “love”의 Key와 가장 강하게 일치합니다.

## 6. Step 5 — √dₖ로 scaling

(d_k=3)이므로:

[
sqrt{3}approx1.732
]

score를 나누면:

[
rac{QK^T}{sqrt{3}}
approx
egin{bmatrix}
0.577&2.887&1.732\
1.732&1.732&1.732\
1.155&2.309&1.732
end{bmatrix}
]

scaling은 순위를 바꾸려는 것이 아니라 softmax에 들어가는 절대 크기를 안정화하려는 것입니다.

## 7. Step 6 — Softmax로 attention weight 만들기

각 row에 softmax를 적용하면 원문 예제의 attention matrix가 나옵니다.

[
Aapprox
egin{bmatrix}
0.070&0.707&0.223\
0.333&0.333&0.333\
0.168&0.533&0.299
end{bmatrix}
]

각 row의 합은 1입니다.

해석:

- I는 love에 약 70.7%의 weight
- love는 세 token을 동일하게 약 33.3%
- AI는 love에 약 53.3%의 weight

## 8. Step 7 — Attention weight × V

최종 출력:

[
O=AV
]

원문 수치에 따라:

[
Oapprox
egin{bmatrix}
1.000&1.637&0.070\
1.000&1.000&0.333\
1.000&1.365&0.168
end{bmatrix}
]

“I”의 첫 출력 row를 직접 계산하면:

[
0.070[1,0,1]+0.707[1,2,0]+0.223[1,1,0]
]

첫 component:

[
0.070+0.707+0.223=1.000
]

두 번째:

[
0+1.414+0.223=1.637
]

세 번째:

[
0.070+0+0=0.070
]

즉 attention은 관련 token의 Value를 weight에 따라 섞어 **문맥화된 새 representation**을 만듭니다.

## 9. 전체 계산을 한 줄로 연결

    X
    → XWQ, XWK, XWV
    → QKᵀ
    → / √dₖ
    → row-wise softmax
    → attention weights
    → × V
    → contextual output

shape도 함께 추적하면 오류를 줄일 수 있습니다.

    X:      3×4
    WQ:     4×3
    Q:      3×3
    K:      3×3
    QKᵀ:    3×3
    A:      3×3
    V:      3×3
    AV:     3×3

## 10. 실제 Transformer에서 달라지는 것

실제 모델에서는:

- embedding dimension이 수천일 수 있고
- head가 여러 개이며
- causal/padding mask가 들어갈 수 있고
- batch dimension도 추가됩니다.

그러나 각 head의 핵심 연산은 동일합니다.

[
softmax(QK^T/sqrt{d_k})V
]

## 핵심 정리

- Q/K dot product가 “얼마나 참고할지”의 raw score를 만듭니다.
- √dₖ scaling이 softmax의 scale을 안정화합니다.
- softmax가 row별 weight를 만들고, 이 weight로 V를 가중합합니다.
- 원문의 “I love AI” 예제는 score → scaled score → weight → output 전체를 수치로 확인할 수 있게 합니다.
- attention의 출력은 원래 token embedding이 아니라 주변 token 정보를 섞은 contextual representation입니다.

## 원문

- https://outcomeschool.com/blog/math-behind-attention-qkv
