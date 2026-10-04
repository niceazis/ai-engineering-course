# 모듈 3 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 3: 생성형 AI와 트랜스포머 아키텍처

이 모듈에서는 생성형 AI가 무엇인지, 그리고 모든 현대 LLM의 핵심 아키텍처인 Transformer가 내부에서 어떻게 동작하는지 배웁니다. 토큰에서 임베딩, 어텐션까지 한 단계씩 살펴봅니다.

모듈을 마치면 Transformer 구조를 직접 그려 설명하고 Q, K, V의 수학을 포함해 각 블록의 역할을 이해할 수 있습니다.

**이 모듈의 레슨:**

1. [생성형 AI란?](https://outcomeschool.com/blog/what-is-generative-ai)
   ↳ [한국어 상세 학습 노트](blogs/module-03/what-is-generative-ai.md)

2. [Autoregressive Model이란?](https://outcomeschool.com/blog/autoregressive-models)
   ↳ [한국어 상세 학습 노트](blogs/module-03/autoregressive-models.md)

3. [LLM의 Tokenization](https://outcomeschool.com/blog/tokenization-in-llms)
   ↳ [한국어 상세 학습 노트](blogs/module-03/tokenization-in-llms.md)

4. [LLM의 Byte Pair Encoding(BPE)이란?](https://outcomeschool.com/blog/bpe-in-llms)
   ↳ [한국어 상세 학습 노트](blogs/module-03/bpe-in-llms.md)

5. [Embedding이란?](https://outcomeschool.com/blog/what-are-embeddings)
   ↳ [한국어 상세 학습 노트](blogs/module-03/what-are-embeddings.md)

6. [RNN과 Transformer는 어떻게 다른가?](https://outcomeschool.com/blog/how-do-rnns-and-transformers-differ)
   ↳ [한국어 상세 학습 노트](blogs/module-03/how-do-rnns-and-transformers-differ.md)

7. [Transformer 아키텍처는 어떻게 동작하는가?](https://outcomeschool.com/blog/decoding-transformer-architecture)
   ↳ [한국어 상세 학습 노트](blogs/module-03/decoding-transformer-architecture.md)

8. [Transformer의 Encoder vs Decoder](https://outcomeschool.com/blog/encoder-vs-decoder-in-transformers)
   ↳ [한국어 상세 학습 노트](blogs/module-03/encoder-vs-decoder-in-transformers.md)

9. [Transformer의 Self Attention이란 무엇이며 어떻게 동작하는가?](https://outcomeschool.com/blog/self-attention-in-transformers)
   ↳ [한국어 상세 학습 노트](blogs/module-03/self-attention-in-transformers.md)

10. [Attention은 어떻게 동작하는가? Q, K, V의 수학](https://outcomeschool.com/blog/math-behind-attention-qkv)
   ↳ [한국어 상세 학습 노트](blogs/module-03/math-behind-attention-qkv.md)

11. [왜 Attention을 √dₖ로 스케일링하는가?](https://outcomeschool.com/blog/scaling-dot-product-attention)
   ↳ [한국어 상세 학습 노트](blogs/module-03/scaling-dot-product-attention.md)

12. [Attention의 Causal Masking이란 무엇이며 LLM에 왜 필요한가?](https://outcomeschool.com/blog/causal-masking-in-attention)
   ↳ [한국어 상세 학습 노트](blogs/module-03/causal-masking-in-attention.md)

13. [Transformer의 Multi-Head Attention이란?](https://outcomeschool.com/blog/multi-head-attention-in-transformers)
   ↳ [한국어 상세 학습 노트](blogs/module-03/multi-head-attention-in-transformers.md)

14. [Transformer의 Cross Attention이란?](https://outcomeschool.com/blog/cross-attention-in-transformers)
   ↳ [한국어 상세 학습 노트](blogs/module-03/cross-attention-in-transformers.md)

15. [RoPE(Rotary Position Embedding)란?](https://outcomeschool.com/blog/math-behind-rope-rotary-position-embedding)
   ↳ [한국어 상세 학습 노트](blogs/module-03/math-behind-rope-rotary-position-embedding.md)

16. [LLM의 Feed-Forward Network란 무엇이며 어떤 역할을 하는가?](https://outcomeschool.com/blog/feed-forward-networks-in-llms)
   ↳ [한국어 상세 학습 노트](blogs/module-03/feed-forward-networks-in-llms.md)

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


### 3.3 LLM의 Tokenization

LLM이 문자열을 숫자로 처리하기 위한 첫 단계인 Tokenization을 배웁니다. 문자·단어·subword 단위의 차이, BPE가 vocabulary를 만드는 방식, Token ID와 decoding, special token, 그리고 tokenization이 비용·context·다국어·숫자·코드 처리에 미치는 영향을 연결해서 봅니다.

- Tokenization이란?
- 왜 Tokenization이 필요한가?
- Token이란?
- Character-level Tokenization
- Word-level Tokenization
- Subword-level Tokenization
- BPE가 동작하는 방식
- Vocabulary와 Token ID
- Token ID에서 Text로 Decoding
- 실제 tokenizer 예제
- Special Token
- LLM 실무에서 Tokenization이 미치는 영향
- 잘 동작하는 영역과 한계

시작하기: [LLM의 Tokenization](https://outcomeschool.com/blog/tokenization-in-llms)

→ [한국어 상세 학습 노트](blogs/module-03/tokenization-in-llms.md)

영상 보기: [Tokenization in Large Language Models (LLMs)](https://www.youtube.com/watch?v=sK2s9I84EVI)

→ [한국어 상세 영상 학습 노트](videos/module-03/tokenization-in-large-language-models.md)


### 3.4 LLM의 Byte Pair Encoding(BPE)이란?

현대 LLM이 텍스트를 처리하기 전에 작은 단위로 나누는 대표적인 토큰화 알고리즘인 **BPE(Byte Pair Encoding)**를 배웁니다.

- Tokenization이란?
- 텍스트를 토큰으로 나누는 문제
- BPE란?
- BPE의 단계별 동작
- 새로운 텍스트를 BPE로 토큰화하는 방법
- 현대 LLM이 BPE를 사용하는 이유

시작하기: [LLM의 BPE란?](https://outcomeschool.com/blog/bpe-in-llms)

→ [한국어 상세 학습 노트](blogs/module-03/bpe-in-llms.md)



