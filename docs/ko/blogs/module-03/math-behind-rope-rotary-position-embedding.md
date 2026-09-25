# RoPE(Rotary Position Embedding)의 수학 — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/math-behind-rope-rotary-position-embedding  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 2차원 회전, 상대 위치 성질, 수치 예제를 따라 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Transformer에는 왜 위치 정보가 필요한가

Self-attention은 기본적으로 token의 순서를 자동으로 알지 못합니다.

예:

    cat chases dog
    dog chases cat

같은 token 집합이라도 순서가 바뀌면 의미가 달라집니다.

따라서 attention score에 token position 정보를 반영해야 합니다.

## 2. 기존 위치 표현

대표적인 방식:

- sinusoidal positional encoding
- learned absolute positional embedding

이들은 position마다 별도의 위치 vector를 token representation에 더하는 방식으로 이해할 수 있습니다.

RoPE(Rotary Position Embedding)는 다른 접근을 취합니다.

> 위치를 별도 vector로 더하는 대신, **Q와 K의 component 쌍을 위치에 따라 회전**시킵니다.

## 3. 2차원 회전부터 이해하기

2D vector:

[
x=
egin{bmatrix}
x_1\
x_2
end{bmatrix}
]

를 각도 (	heta)만큼 회전하면:

[
R(	heta)=
egin{bmatrix}
cos	heta&-sin	heta\
sin	heta&cos	heta
end{bmatrix}
]

[
x'=R(	heta)x
]

component로 쓰면:

[
x'_1=x_1cos	heta-x_2sin	heta
]

[
x'_2=x_1sin	heta+x_2cos	heta
]

RoPE는 이 회전을 고차원 Q/K의 component pair마다 적용합니다.

## 4. 고차원 vector를 pair로 나누기

예를 들어 dimension (d=8)이면 4개의 2D pair로 나눕니다.

    (x1, x2)
    (x3, x4)
    (x5, x6)
    (x7, x8)

각 pair에는 서로 다른 회전 frequency가 적용됩니다.

원문의 일반적인 frequency 형태:

[
	heta_i=10000^{-2(i-1)/d}
]

position (m)에서는 회전각이:

[
m	heta_i
]

가 됩니다.

낮은 frequency의 pair는 위치 변화에 천천히 회전하고, 높은 frequency의 pair는 더 빠르게 회전합니다.

## 5. RoPE를 Q와 K에 적용

position (m)의 Query:

[
Q'_m=R_mQ_m
]

position (n)의 Key:

[
K'_n=R_nK_n
]

Value는 일반적인 RoPE attention에서 회전시키지 않습니다.

핵심은 attention score:

[
(Q'_m)^T K'_n
]

에 위치 차이가 자연스럽게 들어간다는 점입니다.

## 6. 상대 위치가 나타나는 수학

회전 행렬의 성질:

[
R_m^T R_n=R_{n-m}
]

따라서:

[
(R_mQ)^T(R_nK)
=Q^TR_m^TR_nK
=Q^TR_{n-m}K
]

즉 dot product가 절대 위치 (m,n) 자체보다 **차이 (n-m)**에 의존하는 형태가 됩니다.

이것이 RoPE의 가장 중요한 직관입니다.

## 7. 원문의 상대 거리 예

두 token이 position 2와 6에 있다고 합시다.

거리:

[
6-2=4
]

둘을 모두 한 칸 옮겨 position 3과 7로 만들면:

[
7-3=4
]

상대 거리는 그대로입니다.

RoPE의 Q/K dot product 구조는 이런 상대 위치 정보를 자연스럽게 반영합니다.

## 8. 작은 수치 예제

Query:

[
Q=[1,0]
]

기본 frequency를 단순화해:

[
	heta=pi/4
]

라고 합시다.

position (m=1)이라면 회전각은 (pi/4).

[
R(pi/4)[1,0]
=[cos(pi/4),sin(pi/4)]
]

[
approx[0.707,0.707]
]

Key도:

[
K=[1,0]
]

이고 position (n=2)라면 회전각은:

[
2	heta=pi/2
]

따라서:

[
K'=[0,1]
]

dot product:

[
Q'cdot K'
=0.707×0+0.707×1
=0.707
]

이는 두 위치 차이에 따른 회전 관계가 attention score에 들어간 간단한 예입니다.

## 9. 여러 frequency가 필요한 이유

하나의 frequency만 있으면 회전이 주기적으로 반복되어 멀리 떨어진 위치가 동일한 angle pattern을 만들 수 있습니다.

여러 pair에 서로 다른 frequency를 사용하면:

- 짧은 거리 변화
- 중간 거리 변화
- 긴 거리 변화

를 여러 scale로 표현할 수 있습니다.

이는 sinusoidal positional encoding이 여러 주파수를 쓰는 이유와도 연결됩니다.

## 10. 실제 구현에서의 배열 방식

수학 설명에서는 인접 component를 pair로 묶는 표현이 흔합니다.

실제 코드에서는:

- 앞 절반/뒤 절반을 짝짓기
- even/odd index를 짝짓기

등 서로 다른 memory layout을 사용할 수 있습니다.

중요한 것은 **동일한 2D rotation을 여러 pair에 적용하는 수학적으로 동등한 구현인지**입니다.

LLaMA/Mistral 계열 구현을 읽을 때 array permutation 때문에 수식과 달라 보일 수 있습니다.

## 11. RoPE와 긴 Context

RoPE는 현대 LLM에서 널리 사용되지만 기본 학습 범위를 훨씬 넘어서는 context length로 단순 확장하면 position frequency 분포가 학습 때와 달라집니다.

그래서 실전에는:

- frequency scaling
- position interpolation
- NTK-aware scaling 등

여러 확장법이 사용됩니다.

이 부분은 모델별 구현 차이가 크므로 context length를 늘릴 때 tokenizer 설정만 바꾸면 된다고 생각하면 안 됩니다.

## 핵심 정리

- RoPE는 Q와 K의 component pair를 position에 따라 회전시킵니다.
- 2D rotation matrix가 기본 수학입니다.
- ((R_mQ)^T(R_nK)=Q^TR_{n-m}K) 성질 덕분에 attention score가 상대 위치 차이를 자연스럽게 포함합니다.
- Q/K에 적용하고 일반적으로 V에는 적용하지 않습니다.
- 여러 dimension pair에 서로 다른 frequency를 사용해 다양한 거리 scale을 표현합니다.
- 구현 layout은 달라도 핵심 회전 수학이 같을 수 있습니다.

## 원문

- https://outcomeschool.com/blog/math-behind-rope-rotary-position-embedding
