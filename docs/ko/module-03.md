# 모듈 3 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 3: 생성형 AI와 트랜스포머 아키텍처

이 모듈에서는 생성형 AI가 무엇인지, 그리고 모든 현대 LLM의 핵심 아키텍처인 Transformer가 내부에서 어떻게 동작하는지 배웁니다. 토큰에서 임베딩, 어텐션까지 한 단계씩 살펴봅니다.

모듈을 마치면 Transformer 구조를 직접 그려 설명하고 Q, K, V의 수학을 포함해 각 블록의 역할을 이해할 수 있습니다.

**이 모듈의 레슨:**

1. [생성형 AI란?](https://outcomeschool.com/blog/what-is-generative-ai)

→ [한국어 상세 학습 노트](blogs/module-03/what-is-generative-ai.md)
2. [Autoregressive Model이란?](https://outcomeschool.com/blog/autoregressive-models)

→ [한국어 상세 학습 노트](blogs/module-03/autoregressive-models.md)
3. [LLM의 Byte Pair Encoding(BPE)이란?](https://outcomeschool.com/blog/bpe-in-llms)

→ [한국어 상세 학습 노트](blogs/module-03/bpe-in-llms.md)
4. [Embedding이란?](https://outcomeschool.com/blog/what-are-embeddings)

→ [한국어 상세 학습 노트](blogs/module-03/what-are-embeddings.md)
5. [RNN과 Transformer는 어떻게 다른가?](https://outcomeschool.com/blog/how-do-rnns-and-transformers-differ)

→ [한국어 상세 학습 노트](blogs/module-03/how-do-rnns-and-transformers-differ.md)
6. [Transformer 아키텍처는 어떻게 동작하는가?](https://outcomeschool.com/blog/decoding-transformer-architecture)

→ [한국어 상세 학습 노트](blogs/module-03/decoding-transformer-architecture.md)
7. [Transformer의 Encoder vs Decoder](https://outcomeschool.com/blog/encoder-vs-decoder-in-transformers)

→ [한국어 상세 학습 노트](blogs/module-03/encoder-vs-decoder-in-transformers.md)
8. [Transformer의 Self Attention이란 무엇이며 어떻게 동작하는가?](https://outcomeschool.com/blog/self-attention-in-transformers)

→ [한국어 상세 학습 노트](blogs/module-03/self-attention-in-transformers.md)
9. [Attention은 어떻게 동작하는가? Q, K, V의 수학](https://outcomeschool.com/blog/math-behind-attention-qkv)

→ [한국어 상세 학습 노트](blogs/module-03/math-behind-attention-qkv.md)
10. [왜 Attention을 √dₖ로 스케일링하는가?](https://outcomeschool.com/blog/scaling-dot-product-attention)

→ [한국어 상세 학습 노트](blogs/module-03/scaling-dot-product-attention.md)
11. [Attention의 Causal Masking이란 무엇이며 LLM에 왜 필요한가?](https://outcomeschool.com/blog/causal-masking-in-attention)

→ [한국어 상세 학습 노트](blogs/module-03/causal-masking-in-attention.md)
12. [Transformer의 Multi-Head Attention이란?](https://outcomeschool.com/blog/multi-head-attention-in-transformers)

→ [한국어 상세 학습 노트](blogs/module-03/multi-head-attention-in-transformers.md)
13. [Transformer의 Cross Attention이란?](https://outcomeschool.com/blog/cross-attention-in-transformers)

→ [한국어 상세 학습 노트](blogs/module-03/cross-attention-in-transformers.md)
14. [RoPE(Rotary Position Embedding)란?](https://outcomeschool.com/blog/math-behind-rope-rotary-position-embedding)

→ [한국어 상세 학습 노트](blogs/module-03/math-behind-rope-rotary-position-embedding.md)
15. [LLM의 Feed-Forward Network란 무엇이며 어떤 역할을 하는가?](https://outcomeschool.com/blog/feed-forward-networks-in-llms)

→ [한국어 상세 학습 노트](blogs/module-03/feed-forward-networks-in-llms.md)

---

### 3.1 생성형 AI란?

생성형 AI의 의미와 기존 AI와의 차이, 대규모 예시로부터 학습해 새로운 콘텐츠를 만드는 방식, 일상적인 활용 사례와 한계를 배웁니다.

다음 내용을 다룹니다.

- 생성형 AI란?
- Generative + AI의 의미
- 여기서 “생성한다”는 뜻
- 기존 AI와 생성형 AI의 차이
- 생성형 AI의 학습 방식
- 새로운 결과를 만드는 과정
- 생성 가능한 콘텐츠
- 생성형 AI에서 모델이란?
- 전체 동작 흐름
- 일상에서의 활용
- 알아야 할 한계
- 요약

시작하기: [생성형 AI란?](https://outcomeschool.com/blog/what-is-generative-ai)

→ [한국어 상세 학습 노트](blogs/module-03/what-is-generative-ai.md)

### 3.2 Autoregressive Model이란?

과거의 결과를 바탕으로 다음 단계를 예측하며 한 조각씩 생성하는 Autoregressive Model을 배웁니다.

- Autoregressive Model이란?
- 확률의 Chain Rule
- 생성 루프
- 단계별 수치 예제
- GPT 계열 모델이 autoregressive인 이유
- Causal Masking이 필요한 이유
- KV Cache와의 관계
- Autoregressive vs Non-Autoregressive 생성
- 대표적인 Autoregressive Model
- 장단점
- 빠른 요약

시작하기: [Autoregressive Model이란?](https://outcomeschool.com/blog/autoregressive-models)

→ [한국어 상세 학습 노트](blogs/module-03/autoregressive-models.md)

### 3.3 LLM의 Byte Pair Encoding(BPE)이란?

현대 LLM이 텍스트를 처리하기 전에 작은 단위로 나누는 대표적인 토큰화 알고리즘인 **BPE(Byte Pair Encoding)**를 배웁니다.

- Tokenization이란?
- 텍스트를 토큰으로 나누는 문제
- BPE란?
- BPE의 단계별 동작
- 새로운 텍스트를 BPE로 토큰화하는 방법
- 현대 LLM이 BPE를 사용하는 이유

시작하기: [LLM의 BPE란?](https://outcomeschool.com/blog/bpe-in-llms)

→ [한국어 상세 학습 노트](blogs/module-03/bpe-in-llms.md)

영상 보기: [Tokenization in Large Language Models (LLMs)](https://www.youtube.com/watch?v=sK2s9I84EVI)

### 3.4 Embedding이란?

검색, 추천, 챗봇 등 현대 AI의 핵심 개념인 Embedding을 배웁니다. 의미를 숫자로 표현해 비슷한 항목끼리 가까이 배치하는 방식과 거리 측정, 실제 활용을 살펴봅니다.

- 컴퓨터가 의미를 직접 비교할 수 없는 문제
- Embedding이란?
- 두 숫자로 보는 간단한 예제
- 왜 더 많은 차원이 필요한가?
- 가까움을 어떻게 측정하는가?
- Embedding은 어디에서 오는가?
- 유명한 단어 연산 예제
- 단어 이외의 Embedding
- 주요 활용처
- 주의할 점
- 요약

시작하기: [Embedding이란?](https://outcomeschool.com/blog/what-are-embeddings)

→ [한국어 상세 학습 노트](blogs/module-03/what-are-embeddings.md)

영상 보기: [Embeddings in Machine Learning](https://www.youtube.com/watch?v=LedXW6xl21s)

### 3.5 RNN과 Transformer는 어떻게 다른가?

문장 같은 시퀀스를 처리하는 두 대표 방식인 RNN과 Transformer를 비교합니다. RNN이 순차적으로 읽는 이유, Transformer가 전체를 한 번에 처리할 수 있는 이유, 각각 언제 적합한지 배웁니다.

- 두 구조의 공통 목적
- RNN이란?
- RNN의 문제점
- Transformer란?
- 한 줄로 보는 핵심 차이
- RNN vs Transformer
- 차이 표
- 언제 무엇을 사용할까?
- 요약

시작하기: [RNN과 Transformer는 어떻게 다른가?](https://outcomeschool.com/blog/how-do-rnns-and-transformers-differ)

→ [한국어 상세 학습 노트](blogs/module-03/how-do-rnns-and-transformers-differ.md)

### 3.6 Transformer 아키텍처는 어떻게 동작하는가?

Transformer 아키텍처를 구성 요소별로 분해해 각 요소의 역할, 상호작용, 현대 LLM의 기반이 된 이유를 이해합니다.

- Transformer가 필요했던 이유
- 아키텍처의 두 절반
- Tokenization, Embedding, Positional Encoding
- Attention과 Multi-Head Attention
- Feed-Forward Network, Residual Connection, Layer Normalization
- Encoder와 Decoder의 동작
- 전체 데이터 흐름
- Transformer의 세 가지 변형
- Transformer가 강력한 이유

시작하기: [Transformer 아키텍처는 어떻게 동작하는가?](https://outcomeschool.com/blog/decoding-transformer-architecture)

→ [한국어 상세 학습 노트](blogs/module-03/decoding-transformer-architecture.md)

### 3.7 Transformer의 Encoder vs Decoder

현대 언어 AI의 두 핵심 블록인 Encoder와 Decoder를 비교합니다. 양방향으로 읽는 구조와 과거 방향만 보는 구조의 차이, Transformer의 세 가지 유형과 사용 시점을 배웁니다.

- Transformer란?
- Token
- Encoder란?
- Decoder란?
- 가장 중요한 차이
- Transformer의 세 가지 유형
- 차이 표
- 언제 무엇을 사용할까?
- 요약

시작하기: [Transformer의 Encoder vs Decoder](https://outcomeschool.com/blog/encoder-vs-decoder-in-transformers)

→ [한국어 상세 학습 노트](blogs/module-03/encoder-vs-decoder-in-transformers.md)

### 3.8 Transformer의 Self Attention이란 무엇이며 어떻게 동작하는가?

BERT와 GPT 같은 현대 LLM의 핵심인 Self Attention의 개념과 단계별 동작을 배웁니다.

- Self Attention이란?
- 필요한 이유
- Query, Key, Value 벡터
- 단계별 동작
- 간단한 예제
- Self Attention이 잘 동작하는 이유
- Multi-Head Self Attention
- 사용처

시작하기: [Self Attention이란?](https://outcomeschool.com/blog/self-attention-in-transformers)

→ [한국어 상세 학습 노트](blogs/module-03/self-attention-in-transformers.md)

### 3.9 Attention은 어떻게 동작하는가? Q, K, V의 수학

단계별 수치 예제로 Query(Q), Key(K), Value(V)를 포함한 Attention의 수학을 배웁니다.

- Attention 공식
- 단어에서 벡터로 변환
- Q, K, V 행렬 생성
- Attention Score 계산(Q × Kᵀ)
- Score 스케일링
- Softmax 적용
- 최종 출력 계산(Attention Weight × V)
- 전체 과정 연결

시작하기: [Q, K, V의 수학](https://outcomeschool.com/blog/math-behind-attention-qkv)

→ [한국어 상세 학습 노트](blogs/module-03/math-behind-attention-qkv.md)

영상 보기: [Softmax Activation Function in Machine Learning](https://www.youtube.com/watch?v=2Zx6x01WwWM)

### 3.10 왜 Attention을 √dₖ로 스케일링하는가?

Transformer의 dot-product attention을 √dₖ로 나누는 이유를 수학과 수치 예제로 배웁니다.

- Attention 공식 복습
- 스케일링하지 않을 때의 문제
- dₖ가 커지면 dot product가 커지는 이유
- Dot Product 분산 이해
- 분산이 dₖ가 되는 과정
- 큰 값이 Softmax에 미치는 영향
- √dₖ가 적절한 이유
- 실제 수치 예제
- 전체 과정 연결

시작하기: [왜 Attention을 √dₖ로 스케일링하는가?](https://outcomeschool.com/blog/scaling-dot-product-attention)

→ [한국어 상세 학습 노트](blogs/module-03/scaling-dot-product-attention.md)

### 3.11 Attention의 Causal Masking이란 무엇이며 LLM에 왜 필요한가?

**Causal Masking**의 역할과 구현을 배웁니다.

- Causal Masking이 없을 때
- Causal Masking을 적용했을 때
- 구현 방법
- Causal Mask Matrix

시작하기: [Causal Masking이란?](https://outcomeschool.com/blog/causal-masking-in-attention)

→ [한국어 상세 학습 노트](blogs/module-03/causal-masking-in-attention.md)

### 3.12 Transformer의 Multi-Head Attention이란?

여러 attention head가 서로 다른 관계를 병렬로 학습하는 Multi-Head Attention의 개념과 단계별 동작을 배웁니다.

- Multi-Head Attention이란?
- Self Attention 복습
- 필요한 이유
- 단계별 동작
- 간단한 예제
- 사용처
- 장점

시작하기: [Multi-Head Attention이란?](https://outcomeschool.com/blog/multi-head-attention-in-transformers)

→ [한국어 상세 학습 노트](blogs/module-03/multi-head-attention-in-transformers.md)

### 3.13 Transformer의 Cross Attention이란?

Cross Attention의 개념과 동작, Self Attention과의 차이, 실제 사용처를 배웁니다.

- Cross Attention이란?
- 필요한 이유
- Cross Attention의 Query, Key, Value
- Self Attention vs Cross Attention
- 단계별 동작
- 간단한 예제
- 사용처
- 중요성

시작하기: [Cross Attention이란?](https://outcomeschool.com/blog/cross-attention-in-transformers)

→ [한국어 상세 학습 노트](blogs/module-03/cross-attention-in-transformers.md)

### 3.14 RoPE(Rotary Position Embedding)란?

현대 LLM에서 널리 사용하는 Rotary Position Embedding(RoPE)의 수학과 위치 정보를 표현하는 방식을 배웁니다.

- 큰 그림
- Transformer에 위치 정보가 필요한 이유
- 기존 접근법과 문제점
- RoPE의 핵심 아이디어
- 2D Rotation 수학
- Q와 K에 RoPE를 적용하는 방법
- Dot Product가 상대 위치를 포착하는 이유
- 작은 수치 예제
- 실제 활용
- 빠른 요약

시작하기: [RoPE의 수학](https://outcomeschool.com/blog/math-behind-rope-rotary-position-embedding)

→ [한국어 상세 학습 노트](blogs/module-03/math-behind-rope-rotary-position-embedding.md)

### 3.15 LLM의 Feed-Forward Network란 무엇이며 어떤 역할을 하는가?

Transformer 내부의 Feed-Forward Network(FFN)가 무엇인지, 각 Transformer layer에 왜 필요한지, 모델의 표현력을 어떻게 높이는지 배웁니다.

- Feed-Forward Network란?
- 실생활 비유
- Transformer에서 FFN의 위치
- 단계별 동작
- Expand-then-Contract 패턴
- 확장 후 축소하는 이유
- ReLU와 Activation Function
- FFN이 실제로 학습하는 것
- 전체 모델에서 FFN이 차지하는 비중
- Mixture of Experts의 FFN
- FFN이 중요한 이유

시작하기: [LLM의 Feed-Forward Network란?](https://outcomeschool.com/blog/feed-forward-networks-in-llms)

→ [한국어 상세 학습 노트](blogs/module-03/feed-forward-networks-in-llms.md)

**모듈 3 영상 및 추가 자료:**

- [Softmax Activation Function in Machine Learning](https://www.youtube.com/watch?v=2Zx6x01WwWM) (영상)
- [Inside ChatGPT: What Happens After You Hit Enter](https://outcomeschool.substack.com/p/inside-chatgpt-what-happens-after) (읽기)
- [Tokenization in Large Language Models (LLMs)](https://www.youtube.com/watch?v=sK2s9I84EVI) (영상)
- [Embeddings in Machine Learning](https://www.youtube.com/watch?v=LedXW6xl21s) (영상)
- [Positional Embeddings in LLMs](https://outcomeschool.substack.com/p/positional-embeddings-in-llms) (읽기)

---
