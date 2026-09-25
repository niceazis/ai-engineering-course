# 모듈 12 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 12: LLM 추론 엔지니어링

이 모듈에서는 LLM을 더 빠르고 저렴하게 실행하는 방법을 배웁니다. 추론 과정에서 시작해 Cache, Batching, Speculation, Quantization, Serving Engine까지 이어집니다.

모듈을 마치면 TTFT, TPOT, Throughput을 이해하고 각각의 병목에 맞는 최적화 기법을 선택할 수 있습니다.

**이 모듈의 레슨:**

1. [LLM Inference Optimization](https://outcomeschool.com/blog/llm-inference-optimization)
   ↳ [한국어 상세 학습 노트](blogs/module-12/llm-inference-optimization.md)

2. [Prefill vs Decode](https://outcomeschool.com/blog/prefill-vs-decode-llm-inference-optimization)
   ↳ [한국어 상세 학습 노트](blogs/module-12/prefill-vs-decode-llm-inference-optimization.md)

3. [Prefill-Decode Disaggregation이란?](https://outcomeschool.com/blog/prefill-decode-disaggregation)
   ↳ [한국어 상세 학습 노트](blogs/module-12/prefill-decode-disaggregation.md)

4. [LLM의 KV Cache](https://outcomeschool.com/blog/kv-cache-in-llms)
   ↳ [한국어 상세 학습 노트](blogs/module-12/kv-cache-in-llms.md)

5. [KV Cache Compression이란?](https://outcomeschool.com/blog/kv-cache-compression)
   ↳ [한국어 상세 학습 노트](blogs/module-12/kv-cache-compression.md)

6. [Paged Attention이란?](https://outcomeschool.com/blog/paged-attention-in-llms)
   ↳ [한국어 상세 학습 노트](blogs/module-12/paged-attention-in-llms.md)

7. [Continuous Batching이란?](https://outcomeschool.com/blog/continuous-batching-in-llms)
   ↳ [한국어 상세 학습 노트](blogs/module-12/continuous-batching-in-llms.md)

8. [Speculative Decoding이란?](https://outcomeschool.com/blog/speculative-decoding)
   ↳ [한국어 상세 학습 노트](blogs/module-12/speculative-decoding.md)

9. [N-gram Speculation이란?](https://outcomeschool.com/blog/n-gram-speculation-in-llms)
   ↳ [한국어 상세 학습 노트](blogs/module-12/n-gram-speculation-in-llms.md)

10. [Medusa란?](https://outcomeschool.com/blog/decoding-medusa)
   ↳ [한국어 상세 학습 노트](blogs/module-12/decoding-medusa.md)

11. [EAGLE이란?](https://outcomeschool.com/blog/decoding-eagle)
   ↳ [한국어 상세 학습 노트](blogs/module-12/decoding-eagle.md)

12. [Model Quantization은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-model-quantization-work)
   ↳ [한국어 상세 학습 노트](blogs/module-12/how-does-model-quantization-work.md)

13. [GGUF는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-gguf-work)
   ↳ [한국어 상세 학습 노트](blogs/module-12/how-does-gguf-work.md)

14. [llama.cpp는 일반 하드웨어에서 LLM을 어떻게 실행하는가?](https://outcomeschool.com/blog/how-does-llama-cpp-run-llms-on-everyday-hardware)
   ↳ [한국어 상세 학습 노트](blogs/module-12/how-does-llama-cpp-run-llms-on-everyday-hardware.md)

15. [vLLM은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-vllm-work)
   ↳ [한국어 상세 학습 노트](blogs/module-12/how-does-vllm-work.md)

16. [SGLang은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-sglang-work)
   ↳ [한국어 상세 학습 노트](blogs/module-12/how-does-sglang-work.md)

17. [TensorRT-LLM은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-tensorrt-llm-work)
   ↳ [한국어 상세 학습 노트](blogs/module-12/how-does-tensorrt-llm-work.md)


---

### 12.1 LLM Inference Optimization

LLM 텍스트 생성과 Attention, KV Cache, 그리고 KV Cache를 줄이기 위한 주요 최적화 접근을 배웁니다.

- LLM과 텍스트 생성
- Attention
- KV Cache
- KV Cache가 커지는 이유
- KV Cache Compression
- Quantization
- Token Eviction
- Head 간 Key/Value Sharing
- Low-Rank Compression
- 접근법 비교
- 선택 기준

시작하기: [LLM Inference Optimization](https://outcomeschool.com/blog/llm-inference-optimization)

→ [한국어 상세 학습 노트](blogs/module-12/llm-inference-optimization.md)


영상 보기: [LLM Inference Optimization](https://www.youtube.com/watch?v=jV2sCj4lHYk)

### 12.2 Prefill vs Decode

LLM 추론의 두 단계인 Prefill과 Decode, 그리고 두 단계를 연결하는 KV Cache를 배웁니다.

- LLM Inference란?
- Prefill과 Decode
- Prefill 설명
- Decode 설명
- 두 단계와 KV Cache 흐름
- KV Cache의 역할
- Decode 단계별 예제
- Prefill vs Decode
- Compute-bound vs Memory-bound
- TTFT, TPOT, Throughput, End-to-End Latency
- 단계별 최적화 기법
- 결론

시작하기: [Prefill vs Decode](https://outcomeschool.com/blog/prefill-vs-decode-llm-inference-optimization)

→ [한국어 상세 학습 노트](blogs/module-12/prefill-vs-decode-llm-inference-optimization.md)


영상 보기: [The First-Token Latency Problem in LLMs](https://www.youtube.com/watch?v=XD8DD4cEHu0)

### 12.3 Prefill-Decode Disaggregation이란?

Prompt를 읽는 Prefill과 답을 생성하는 Decode를 별도 Machine/GPU로 분리해 각각의 하드웨어 특성에 맞게 최적화하는 방식을 배웁니다.

- LLM 요청 처리 과정
- KV Cache란?
- Prefill은 Compute-heavy, Decode는 Memory-heavy
- 같은 GPU에서 함께 실행할 때의 문제
- TTFT vs TPOT
- 단순 접근의 한계
- Prefill-Decode Disaggregation
- 동작 방식
- 요청 하나의 흐름
- 장점
- 단점
- 적합한 환경과 과도한 환경
- Co-located vs Disaggregated Serving

시작하기: [Prefill-Decode Disaggregation](https://outcomeschool.com/blog/prefill-decode-disaggregation)

→ [한국어 상세 학습 노트](blogs/module-12/prefill-decode-disaggregation.md)


### 12.4 LLM의 KV Cache

이전 Token의 Key와 Value를 재사용해 반복 계산을 줄이는 KV Cache를 배웁니다.

- LLM 텍스트 생성
- 모델 내부 동작
- 반복 계산 문제
- KV Cache
- Query가 아니라 Key·Value만 Cache하는 이유
- 속도 향상
- Speed vs Memory Trade-off

시작하기: [KV Cache](https://outcomeschool.com/blog/kv-cache-in-llms)

→ [한국어 상세 학습 노트](blogs/module-12/kv-cache-in-llms.md)


### 12.5 KV Cache Compression이란?

대화 기록을 기억하기 위해 사용하는 KV Cache의 메모리 사용량을 줄이는 기법들을 배웁니다.

- LLM과 Attention
- KV Cache
- Cache가 커지는 이유
- KV Cache Compression
- Quantization
- Token Eviction
- Head 간 Key/Value Sharing
- Low-Rank Compression
- 접근법 비교
- 선택 기준

시작하기: [KV Cache Compression](https://outcomeschool.com/blog/kv-cache-compression)

→ [한국어 상세 학습 노트](blogs/module-12/kv-cache-compression.md)


### 12.6 Paged Attention이란?

KV Cache의 메모리 낭비를 줄여 더 많은 사용자를 동시에 처리할 수 있게 하는 Paged Attention을 배웁니다.

- KV Cache 복습
- 메모리 낭비 문제
- Paged Attention이란?
- 동작 방식
- 효과적인 이유
- Request 간 Memory Sharing

시작하기: [Paged Attention](https://outcomeschool.com/blog/paged-attention-in-llms)

→ [한국어 상세 학습 노트](blogs/module-12/paged-attention-in-llms.md)


### 12.7 Continuous Batching이란?

생성 과정의 각 단계에서 Batch를 동적으로 구성해 GPU를 계속 활용하고 동시 처리량을 높이는 Continuous Batching을 배웁니다.

- 큰 그림
- LLM Token 생성 복습
- Batching이 중요한 이유
- Static Batching
- Static Batching의 문제
- Continuous Batching
- Ride-share 비유
- 단계별 동작
- 수치 예제
- 실제 Speedup
- 장점
- 주의점
- 빠른 요약

시작하기: [Continuous Batching](https://outcomeschool.com/blog/continuous-batching-in-llms)

→ [한국어 상세 학습 노트](blogs/module-12/continuous-batching-in-llms.md)


### 12.8 Speculative Decoding이란?

작은 Draft Model이 여러 Token을 미리 제안하고 큰 Target Model이 한 번에 검증해 생성 속도를 높이는 Speculative Decoding을 배웁니다.

- 해결하려는 문제
- 큰 그림
- LLM 생성이 느린 이유
- 핵심 아이디어
- 단계별 동작
- Verification
- 실제 Speedup
- 사용처
- Trade-off
- 빠른 요약

시작하기: [Speculative Decoding](https://outcomeschool.com/blog/speculative-decoding)

→ [한국어 상세 학습 노트](blogs/module-12/speculative-decoding.md)


### 12.9 N-gram Speculation이란?

별도의 Draft Model 대신 이미 본 텍스트의 N-gram을 이용해 다음 Token 후보를 추측하는 기법을 배웁니다.

- LLM 텍스트 생성
- 느린 이유
- Speculative Decoding
- Draft Model 비용
- N-gram이란?
- N-gram Speculation
- 단계별 동작
- 출력이 동일하게 유지되는 이유
- 잘 동작하는 곳과 실패하는 곳
- Draft Model 방식과 비교

시작하기: [N-gram Speculation](https://outcomeschool.com/blog/n-gram-speculation-in-llms)

→ [한국어 상세 학습 노트](blogs/module-12/n-gram-speculation-in-llms.md)


### 12.10 Medusa란?

하나의 모델에 여러 추가 Head를 붙여 여러 미래 Token을 동시에 예측하고 검증하는 Medusa를 배웁니다.

- Medusa란?
- 텍스트 생성이 느린 이유
- Speculative Decoding 복습
- Draft Model이 필요한 문제
- 하나의 모델에 여러 Head
- Tree Attention
- 작은 수치로 보는 Speedup
- 결과
- 이후 발전
- 빠른 요약

시작하기: [Medusa](https://outcomeschool.com/blog/decoding-medusa)

→ [한국어 상세 학습 노트](blogs/module-12/decoding-medusa.md)


### 12.11 EAGLE이란?

Token Level이 아니라 Feature Level에서 Draft를 수행해 Speculative Decoding 성능을 높이는 EAGLE을 배웁니다.

- EAGLE이란?
- Speculative Decoding 복습
- Token-level Draft의 문제
- Feature-level Draft
- Token을 다시 입력해 불확실성 해소
- 작은 수치로 보는 Speedup
- EAGLE-2와 Dynamic Draft Tree
- 이후 발전
- 빠른 요약

시작하기: [EAGLE](https://outcomeschool.com/blog/decoding-eagle)

→ [한국어 상세 학습 노트](blogs/module-12/decoding-eagle.md)


### 12.12 Model Quantization은 어떻게 동작하는가?

모델 숫자를 더 적은 Bit로 표현해 Memory를 줄이고 추론을 빠르게 만드는 Quantization을 배웁니다.

- Model Quantization이란?
- FP32, INT8, INT4
- 적은 Bit가 Memory와 Speed에 미치는 영향
- Scale과 Zero-point
- Symmetric vs Asymmetric
- Per-tensor vs Per-channel
- PTQ vs QAT
- Weight-only vs Weight-and-activation
- LLM Outlier 문제
- GPTQ, AWQ, bitsandbytes, GGUF/llama.cpp
- Accuracy Trade-off와 Local LLM
- 정리

시작하기: [Model Quantization](https://outcomeschool.com/blog/how-does-model-quantization-work)

→ [한국어 상세 학습 노트](blogs/module-12/how-does-model-quantization-work.md)


### 12.13 GGUF는 어떻게 동작하는가?

Local Inference에 필요한 Model Weight와 Metadata를 하나의 효율적인 파일 형식으로 담는 GGUF를 배웁니다.

- Model과 Weight
- Local Inference
- GGUF 이전의 문제
- GGUF란?
- GGUF 파일 내부
- Quantization
- Q4_K_M 같은 이름의 의미
- Memory Mapping
- Cross-platform과 Extensibility
- 실제 활용

시작하기: [GGUF](https://outcomeschool.com/blog/how-does-gguf-work)

→ [한국어 상세 학습 노트](blogs/module-12/how-does-gguf-work.md)


### 12.14 llama.cpp는 일반 하드웨어에서 LLM을 어떻게 실행하는가?

Quantization, GGUF, Memory Mapping, CPU/GPU 분할을 이용해 일반 PC에서 LLM을 실행하는 llama.cpp를 배웁니다.

- llama.cpp란?
- 필요한 이유
- LLM 복습
- 모델이 너무 큰 문제
- Quantization
- Q4_K_M 같은 이름
- GGUF
- Memory Mapping
- CPU 최적화
- GPU와 작업 분담
- Prompt 실행의 전체 과정
- 사용처

시작하기: [llama.cpp](https://outcomeschool.com/blog/how-does-llama-cpp-run-llms-on-everyday-hardware)

→ [한국어 상세 학습 노트](blogs/module-12/how-does-llama-cpp-run-llms-on-everyday-hardware.md)


### 12.15 vLLM은 어떻게 동작하는가?

PagedAttention과 Continuous Batching을 중심으로 많은 사용자에게 LLM을 효율적으로 Serving하는 vLLM을 배웁니다.

- LLM Serving이란?
- Prefill, Decode, KV Cache 복습
- KV Cache GPU Memory 문제
- 단순 Serving의 낭비
- vLLM이란?
- PagedAttention
- Memory Sharing
- Continuous Batching
- OpenAI-compatible API Server
- 장점
- 실제 활용

시작하기: [vLLM](https://outcomeschool.com/blog/how-does-vllm-work)

→ [한국어 상세 학습 노트](blogs/module-12/how-does-vllm-work.md)


### 12.16 SGLang은 어떻게 동작하는가?

RadixAttention을 이용한 Prefix Reuse와 Runtime 최적화로 LLM Serving 성능을 높이는 SGLang을 배웁니다.

- SGLang이란?
- LLM 생성 복습
- 해결하는 문제
- RadixAttention
- 과거 계산 재사용
- Frontend Language
- Runtime과 Frontend 협업
- Continuous Batching
- Structured Output과 빠른 Decoding
- End-to-End 흐름
- 고급 기능
- vLLM과 비교

시작하기: [SGLang](https://outcomeschool.com/blog/how-does-sglang-work)

→ [한국어 상세 학습 노트](blogs/module-12/how-does-sglang-work.md)


### 12.17 TensorRT-LLM은 어떻게 동작하는가?

NVIDIA GPU에서 가능한 최고 수준의 추론 성능을 목표로 Build-time 최적화와 Kernel Fusion, Quantization, Paged KV Cache 등을 적용하는 TensorRT-LLM을 배웁니다.

- Inference란?
- GPU와 Kernel
- GPU가 시간을 낭비하는 지점
- TensorRT-LLM이란?
- 미리 Model을 준비하는 핵심 아이디어
- Model에서 Engine으로 Build
- Kernel Fusion
- Quantization
- Custom Attention Kernel
- Paged KV Cache
- In-flight Batching
- CUDA Graph
- Speculative Decoding
- Multi-GPU
- 실제 Serving
- PyTorch Backend
- 요청 하나의 전체 과정
- TensorRT-LLM vs vLLM
- 강점과 한계

시작하기: [TensorRT-LLM](https://outcomeschool.com/blog/how-does-tensorrt-llm-work)

→ [한국어 상세 학습 노트](blogs/module-12/how-does-tensorrt-llm-work.md)


**모듈 12 영상 및 추가 자료:**

- [LLM Inference Optimization](https://www.youtube.com/watch?v=jV2sCj4lHYk) (영상)
  ↳ [한국어 상세 영상 학습 노트](videos/module-12/llm-inference-optimization.md)
- [The First-Token Latency Problem in LLMs](https://www.youtube.com/watch?v=XD8DD4cEHu0) (영상)
  ↳ [한국어 상세 영상 학습 노트](videos/module-12/first-token-latency-problem.md)
- [LLM Inference Engineering (complete series)](https://github.com/amitshekhariitbhu/llm-inference-engineering) (시리즈)

---
