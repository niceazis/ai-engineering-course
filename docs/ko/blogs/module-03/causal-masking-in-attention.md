# Attention의 Causal Masking이란 무엇이며 LLM에 왜 필요한가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/causal-masking-in-attention  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 score matrix와 mask 전후 softmax 수치를 보존한 독립적 한국어 해설입니다.

## 1. Causal Masking이 필요한 이유

Autoregressive language model은 다음 token을 예측합니다.

    "I love teaching" → 다음 token?

학습 데이터에는 정답 문장 전체가 이미 존재합니다. Transformer가 학습 효율을 위해 모든 token position을 한 번에 계산할 때, 미래 token까지 attention으로 볼 수 있다면 답을 훔쳐보게 됩니다.

따라서 position (i)는:

- 자기 자신
- 과거 position

만 볼 수 있고, (i+1) 이후 미래는 볼 수 없게 해야 합니다.

이 규칙을 causal masking 또는 autoregressive masking이라고 합니다.

## 2. 원문의 예제

문장:

    I love teaching AI

4개 token의 raw attention score를 다음과 같이 둡니다.

[
S=
egin{bmatrix}
2.0&1.0&3.0&0.5\
1.5&2.5&0.5&1.0\
0.2&1.0&2.0&1.5\
0.1&0.3&0.7&2.5
end{bmatrix}
]

row는 Query token, column은 Key token입니다.

## 3. Mask 없이 Softmax하면 생기는 문제

각 row에 softmax를 적용한 원문의 근사값:

[
Aapprox
egin{bmatrix}
0.23&0.09&0.63&0.05\
0.21&0.58&0.08&0.13\
0.08&0.17&0.47&0.28\
0.07&0.08&0.12&0.73
end{bmatrix}
]

첫 token “I”가 미래의 “teaching”에 0.63의 weight를 주고 있습니다.

학습 목표가 “I 다음 token을 예측”하는 것이라면 미래 정답 정보를 이미 사용하고 있으므로 올바른 autoregressive 학습이 아닙니다.

## 4. Lower-Triangular Causal Mask

허용되는 위치를 1, 차단되는 미래를 0으로 표현하면:

[
M=
egin{bmatrix}
1&0&0&0\
1&1&0&0\
1&1&1&0\
1&1&1&1
end{bmatrix}
]

실제 계산에서는 0/1 mask를 그대로 곱하는 방식보다 차단 위치에 (-infty)에 해당하는 매우 큰 음수를 더하는 구현이 흔합니다.

[
S'=
egin{bmatrix}
2.0&-infty&-infty&-infty\
1.5&2.5&-infty&-infty\
0.2&1.0&2.0&-infty\
0.1&0.3&0.7&2.5
end{bmatrix}
]

## 5. Mask 적용 후 Softmax

원문의 근사 attention weight:

[
A_{masked}approx
egin{bmatrix}
1.00&0&0&0\
0.27&0.73&0&0\
0.11&0.24&0.65&0\
0.07&0.08&0.12&0.73
end{bmatrix}
]

이제:

- I는 I만 봅니다.
- love는 I, love만 봅니다.
- teaching은 I, love, teaching을 봅니다.
- AI는 모든 과거와 자기 자신을 봅니다.

미래 leakage가 사라졌습니다.

## 6. 왜 차단 score를 0이 아니라 −∞로 만드는가

Softmax에서 score 0의 지수는:

[
e^0=1
]

이므로 weight가 0이 되지 않습니다.

반면:

[
e^{-infty}=0
]

이므로 masked position은 softmax 결과가 정확히 0이 됩니다.

실제 float 연산에서는 (-infty) 또는 dtype에 맞는 매우 큰 음수를 사용합니다.

## 7. 학습과 추론의 차이

### 학습

정답 sequence 전체를 한 번에 matrix로 처리하면서 causal mask를 적용합니다.

장점은 token position을 병렬로 계산할 수 있다는 것입니다.

### 추론

미래 token 자체가 아직 생성되지 않았기 때문에 실제 input sequence에는 과거 token만 있습니다.

그래도 구현상 attention kernel이 causal flag를 유지하거나, prompt processing에서 mask를 사용합니다.

## 8. Teacher Forcing과 연결

Autoregressive LM 학습에서는 position별 입력으로 실제 정답 prefix가 사용됩니다.

예:

    입력:  <BOS> I love teaching
    정답:  I     love teaching AI

causal mask가 없다면 각 position이 오른쪽 정답 token을 직접 볼 수 있어 task가 무너집니다.

따라서 teacher-forced parallel training과 causal masking은 함께 이해해야 합니다.

## 9. Padding Mask와 혼동하지 않기

두 mask는 목적이 다릅니다.

- causal mask: 미래 정보 접근 금지
- padding mask: 실제 데이터가 아닌 padding position 무시

batch 처리에서는 두 mask가 동시에 적용될 수 있습니다.

## 핵심 정리

- causal masking은 각 token이 미래 token을 보지 못하게 합니다.
- lower-triangular 구조로 허용 범위를 표현할 수 있습니다.
- 차단 위치에는 softmax 전에 (-infty)를 더해 weight를 0으로 만듭니다.
- 원문 수치 예에서 mask 전에는 “I”가 미래 “teaching”을 0.63 참고하지만, mask 후 미래 weight는 모두 0입니다.
- 이것이 decoder-only LLM의 next-token prediction을 정직하게 유지하는 핵심 장치입니다.

## 원문

- https://outcomeschool.com/blog/causal-masking-in-attention
