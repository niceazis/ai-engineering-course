# 모듈 5 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 5: 현대 LLM 아키텍처

이 모듈에서는 기본 Transformer 위에 현대 LLM이 추가한 개선 사항을 배웁니다. 모델을 더 크게 만들면서도 더 빠르게 실행하고 더 긴 입력을 처리하는 방법을 살펴보고, 마지막에는 실제 모델에서 이러한 아이디어가 어떻게 결합되는지 확인합니다.

**이 모듈의 레슨:**

1. [LLM 아키텍처의 진화](https://outcomeschool.com/blog/evolution-of-llm-architecture)

→ [한국어 상세 학습 노트](blogs/module-05/evolution-of-llm-architecture.md)
2. [Mixture of Experts(MoE)란 무엇이며 어떻게 동작하는가?](https://outcomeschool.com/blog/mixture-of-experts)

→ [한국어 상세 학습 노트](blogs/module-05/mixture-of-experts.md)
3. [Grouped Query Attention(GQA)이란 무엇이며 LLM은 왜 사용하는가?](https://outcomeschool.com/blog/grouped-query-attention)

→ [한국어 상세 학습 노트](blogs/module-05/grouped-query-attention.md)
4. [Sliding Window Attention은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-sliding-window-attention-work)

→ [한국어 상세 학습 노트](blogs/module-05/how-does-sliding-window-attention-work.md)
5. [Attention Sink는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-do-attention-sinks-work)

→ [한국어 상세 학습 노트](blogs/module-05/how-do-attention-sinks-work.md)
6. [Flash Attention이란 무엇이며 왜 빠른가?](https://outcomeschool.com/blog/decoding-flash-attention)

→ [한국어 상세 학습 노트](blogs/module-05/decoding-flash-attention.md)
7. [DeepSeek-V4란 무엇이며 어떻게 동작하는가?](https://outcomeschool.com/blog/decoding-deepseek-v4)

→ [한국어 상세 학습 노트](blogs/module-05/decoding-deepseek-v4.md)

---

### 5.1 LLM 아키텍처의 진화

대규모 언어 모델의 설계가 단순한 순차 처리 모델에서 오늘날의 거대한 AI 모델까지 어떻게 발전했는지 단계별로 배웁니다.

- LLM 아키텍처란?
- 1단계: 한 단어씩 읽기(RNN)
- 2단계: Attention
- 3단계: Transformer
- 4단계: Scaling
- 5단계: Mixture of Experts(MoE)
- 6단계: 새로운 방향
- 진화 과정 요약

시작하기: [LLM 아키텍처의 진화](https://outcomeschool.com/blog/evolution-of-llm-architecture)

→ [한국어 상세 학습 노트](blogs/module-05/evolution-of-llm-architecture.md)

### 5.2 Mixture of Experts(MoE)란 무엇이며 어떻게 동작하는가?

Expert의 의미, Router가 Expert를 선택하는 방식, MoE가 대형 모델을 더 빠르고 저렴하게 실행하게 하는 이유를 배웁니다.

- MoE가 필요했던 이유
- “Expert”의 실제 의미
- Router와 Expert 선택
- Transformer 안에서 MoE의 위치
- Sparse Activation과 계산량 절감
- Expert 간 Load Balancing
- MoE의 장점과 과제
- 현대 LLM에서 널리 쓰이는 이유

시작하기: [Mixture of Experts(MoE)](https://outcomeschool.com/blog/mixture-of-experts)

→ [한국어 상세 학습 노트](blogs/module-05/mixture-of-experts.md)

### 5.3 Grouped Query Attention(GQA)이란?

GQA와 Multi-Head Attention(MHA)의 차이를 배웁니다.

- 큰 그림
- MHA 복습
- MHA의 문제
- Multi-Query Attention(MQA)이란?
- Grouped-Query Attention(GQA)이란?
- GQA 동작 방식
- MHA와 MQA를 일반화한 GQA
- GQA vs MHA vs MQA
- 실제 사용 사례
- 용어 정리
- Uptraining: MHA를 GQA로 변환
- 빠른 요약

시작하기: [Grouped Query Attention(GQA)](https://outcomeschool.com/blog/grouped-query-attention)

→ [한국어 상세 학습 노트](blogs/module-05/grouped-query-attention.md)

### 5.4 Sliding Window Attention은 어떻게 동작하는가?

긴 텍스트에서 일반 Attention의 계산 비용이 커지는 문제와 Sliding Window Attention이 이를 줄이는 방식을 배웁니다.

- Attention 복습
- 일반 Attention의 문제
- Sliding Window Attention이란?
- 단계별 예제
- 먼 거리 정보가 전달되는 방법
- 일반 Attention과 비교
- 사용처
- 장점과 trade-off

시작하기: [Sliding Window Attention](https://outcomeschool.com/blog/how-does-sliding-window-attention-work)

→ [한국어 상세 학습 노트](blogs/module-05/how-does-sliding-window-attention-work.md)

### 5.5 Attention Sink는 어떻게 동작하는가?

긴 대화를 streaming할 때 생기는 문제, 첫 토큰들이 Attention Sink가 되는 이유, StreamingLLM이 이를 이용하는 방식을 배웁니다.

- LLM이란?
- Attention이란?
- 긴 대화 Streaming의 문제
- 단순한 해결책이 실패하는 이유
- Attention Sink란?
- 첫 토큰이 Sink가 되는 이유
- 단계별 수치 예제
- 코드 수준의 해결 방식
- StreamingLLM과 현대 Attention Sink
- 중요성

시작하기: [Attention Sink](https://outcomeschool.com/blog/how-do-attention-sinks-work)

→ [한국어 상세 학습 노트](blogs/module-05/how-do-attention-sinks-work.md)

### 5.6 Flash Attention이란 무엇이며 왜 빠른가?

표준 Attention이 느린 이유와 GPU 메모리를 효율적으로 이용하는 Flash Attention의 핵심 아이디어를 배웁니다.

- 표준 Attention 복습
- 표준 Attention이 느린 이유
- GPU 메모리 구조(HBM vs SRAM)
- Flash Attention의 핵심 아이디어
- Tiling
- 전체 행렬 없이 Softmax를 계산하는 Online Softmax
- Backward Pass의 Recomputation
- Flash Attention 2
- Flash Attention 3
- 장점과 영향

시작하기: [Flash Attention](https://outcomeschool.com/blog/decoding-flash-attention)

→ [한국어 상세 학습 노트](blogs/module-05/decoding-flash-attention.md)

### 5.7 DeepSeek-V4란 무엇이며 어떻게 동작하는가?

백만 토큰 컨텍스트를 기본 지원하면서 추론 비용을 크게 낮추는 오픈 MoE 언어 모델 계열인 DeepSeek-V4의 아키텍처를 살펴봅니다.

- 큰 그림
- DeepSeek-V4-Pro와 DeepSeek-V4-Flash
- CSA와 HCA를 이용한 Hybrid Attention
- Manifold-Constrained Hyper-Connections(mHC)
- Muon Optimizer
- FP4 Quantization-Aware Training
- Pre-Training
- Post-Training: Specialist Training과 On-Policy Distillation
- Reasoning Mode
- 전체 구조 연결
- 빠른 요약

시작하기: [DeepSeek-V4 아키텍처](https://outcomeschool.com/blog/decoding-deepseek-v4)

→ [한국어 상세 학습 노트](blogs/module-05/decoding-deepseek-v4.md)

---
