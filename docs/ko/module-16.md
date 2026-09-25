# 모듈 16 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 16: AI 인프라, 배포, 시스템 설계

이 모듈에서는 AI 모델을 실행하는 하드웨어, 모델을 어디에 배포할지, 각 요청을 적절한 모델로 라우팅하는 방법, 그리고 완전한 AI 시스템을 처음부터 끝까지 설계하는 방법을 배웁니다.

**이 모듈의 레슨:**

1. [딥러닝에서 GPU는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-a-gpu-work-for-deep-learning)
   ↳ [한국어 상세 학습 노트](blogs/module-16/how-does-a-gpu-work-for-deep-learning.md)

2. [Google TPU는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-a-google-tpu-work)
   ↳ [한국어 상세 학습 노트](blogs/module-16/how-does-a-google-tpu-work.md)

3. [LPU는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-an-lpu-work)
   ↳ [한국어 상세 학습 노트](blogs/module-16/how-does-an-lpu-work.md)

4. [Cloud vs On-device Model Deployment](https://outcomeschool.com/blog/cloud-vs-on-device-model-deployment)
   ↳ [한국어 상세 학습 노트](blogs/module-16/cloud-vs-on-device-model-deployment.md)

5. [Android TensorFlow Lite 머신러닝 예제](https://outcomeschool.com/blog/android-tensorflow-lite-machine-learning-example)
   ↳ [한국어 상세 학습 노트](blogs/module-16/android-tensorflow-lite-machine-learning-example.md)

6. [LLM Routing이란?](https://outcomeschool.com/blog/llm-routing)
   ↳ [한국어 상세 학습 노트](blogs/module-16/llm-routing.md)

7. [실시간 Voice AI Agent 설계](https://outcomeschool.com/blog/design-a-real-time-voice-ai-agent)
   ↳ [한국어 상세 학습 노트](blogs/module-16/design-a-real-time-voice-ai-agent.md)

8. [System Design이란?](https://outcomeschool.com/blog/system-design)
   ↳ [한국어 상세 학습 노트](blogs/module-16/system-design.md)

9. [HTTP Request vs Long-Polling vs WebSocket vs SSE](https://outcomeschool.com/blog/http-request-long-polling-websocket-sse)
   ↳ [한국어 상세 학습 노트](blogs/module-16/http-request-long-polling-websocket-sse.md)

10. [Voice/Video Call은 어떻게 동작하는가?](https://outcomeschool.com/blog/voice-and-video-call)
   ↳ [한국어 상세 학습 노트](blogs/module-16/voice-and-video-call.md)


---

### 16.1 딥러닝에서 GPU는 어떻게 동작하는가?

GPU가 대규모 병렬 연산과 높은 메모리 대역폭을 이용해 딥러닝에 적합한 이유를 배웁니다.

- GPU란?
- 딥러닝에 적합한 이유
- CPU vs GPU
- 수학 교수와 수천 명의 학생 비유
- 딥러닝이 Matrix Multiplication 중심인 이유
- Serial vs Parallel Work
- VRAM과 Memory Bandwidth
- 모델이 VRAM에 들어가야 하는 이유
- Tensor Core와 FP16/BF16/INT8
- CUDA와 cuDNN
- Training vs Inference
- Multi-GPU
- NVIDIA GPU가 현대 AI의 중심이 된 이유

시작하기: [GPU와 딥러닝](https://outcomeschool.com/blog/how-does-a-gpu-work-for-deep-learning)

→ [한국어 상세 학습 노트](blogs/module-16/how-does-a-gpu-work-for-deep-learning.md)


### 16.2 Google TPU는 어떻게 동작하는가?

Google이 머신러닝을 위해 설계한 TPU와 Systolic Array 구조를 배웁니다.

- TPU란?
- Google이 TPU를 만든 이유
- CPU와 GPU 복습
- 가장 중요한 연산
- Systolic Array
- TPU 내부 Data Flow
- 전체 계산 과정
- 빠르고 전력 효율적인 이유
- 사용처
- 한계

시작하기: [Google TPU](https://outcomeschool.com/blog/how-does-a-google-tpu-work)

→ [한국어 상세 학습 노트](blogs/module-16/how-does-a-google-tpu-work.md)


### 16.3 LPU는 어떻게 동작하는가?

학습이 끝난 LLM을 매우 빠르게 추론하도록 설계된 LPU의 구조와 Memory Bottleneck 해결 방식을 배웁니다.

- LPU란?
- LLM이 Token을 생성하는 방식
- 핵심 병목은 Math보다 Memory
- GPU가 어려움을 겪는 이유
- Model을 Chip 가까이에 두기
- On-chip Memory 문제
- Compiler로 실행을 미리 계획하기
- 기다리지 않는 Network
- Assembly Line 구조
- Prompt 처리 과정
- 빠른 이유
- 적합한 사용처
- 부적합한 사용처
- LPU vs GPU
- 선택 기준

시작하기: [LPU](https://outcomeschool.com/blog/how-does-an-lpu-work)

→ [한국어 상세 학습 노트](blogs/module-16/how-does-an-lpu-work.md)


### 16.4 Cloud vs On-device Model Deployment

AI 모델을 Cloud에서 실행하는 방식과 사용자 Device에서 직접 실행하는 방식을 비교합니다.

- Deployment란?
- Training과 Inference
- Cloud Deployment
- On-device Deployment
- 핵심 차이
- Round Trip 문제
- Data 위치
- Model Size
- 비용 부담
- 배포·업데이트 문제
- Network가 없을 때
- Hybrid Approach
- 실제 예제
- 비교 표
- 선택 기준
- 요약

시작하기: [Cloud vs On-device Model Deployment](https://outcomeschool.com/blog/cloud-vs-on-device-model-deployment)

→ [한국어 상세 학습 노트](blogs/module-16/cloud-vs-on-device-model-deployment.md)


### 16.5 Android TensorFlow Lite 머신러닝 예제

Android에서 TensorFlow Lite를 이용해 머신러닝 모델을 실행하는 예제를 살펴봅니다.

시작하기: [Android TensorFlow Lite Machine Learning Example](https://outcomeschool.com/blog/android-tensorflow-lite-machine-learning-example)

→ [한국어 상세 학습 노트](blogs/module-16/android-tensorflow-lite-machine-learning-example.md)


### 16.6 LLM Routing이란?

비용, Latency, 품질을 고려해 각 사용자 Query를 적절한 LLM으로 보내는 Routing 전략을 배웁니다.

- 큰 그림
- LLM Routing이란?
- 필요한 이유
- LLM Router의 구조
- Routing Strategy
- Full Trace 예제
- LLM Routing vs Mixture of Experts
- Routing이 가치 있는 경우
- 흔한 실수와 해결책
- 빠른 요약

시작하기: [LLM Routing](https://outcomeschool.com/blog/llm-routing)

→ [한국어 상세 학습 노트](blogs/module-16/llm-routing.md)


### 16.7 실시간 Voice AI Agent 설계

사람의 음성을 듣고 이해하고, 필요한 Tool을 호출하고, 자연스러운 음성으로 수백 ms 수준에서 응답하는 실시간 Voice AI Agent를 설계합니다.

- Voice AI Agent란?
- Real-Time Voice가 어려운 이유
- Requirements
- Back-of-the-envelope Estimation
- High-Level Architecture
- Audio Transport
- Voice Activity Detection·Turn Detection
- Speech-to-Text
- LLM + Tools
- Text-to-Speech
- Cascaded Pipeline(STT → LLM → TTS)
- Speech-to-Speech Model
- Hybrid Approach
- 방식 비교
- Latency Budget
- Barge-in
- Tool Calling
- Memory와 Context
- Telephony
- Scaling
- Edge Case
- Observability와 Evaluation
- Safety, Security, Privacy
- Cost
- 면접에서 설계를 설명하는 방법

시작하기: [실시간 Voice AI Agent 설계](https://outcomeschool.com/blog/design-a-real-time-voice-ai-agent)

→ [한국어 상세 학습 노트](blogs/module-16/design-a-real-time-voice-ai-agent.md)


**AI System Design 보조 레슨:**

### 16.8 System Design이란?

- System Design이란?
- 왜 필요한가?
- 필요한 핵심 개념은 무엇인가?

시작하기: [System Design](https://outcomeschool.com/blog/system-design)

→ [한국어 상세 학습 노트](blogs/module-16/system-design.md)


### 16.9 HTTP Request vs Long-Polling vs WebSocket vs SSE

서버와 클라이언트가 데이터를 주고받는 주요 방식들을 비교합니다.

- HTTP Request
- HTTP Polling
- HTTP Long Polling
- WebSocket
- Server-Sent Events(SSE)

시작하기: [HTTP Request vs Long-Polling vs WebSocket vs SSE](https://outcomeschool.com/blog/http-request-long-polling-websocket-sse)

→ [한국어 상세 학습 노트](blogs/module-16/http-request-long-polling-websocket-sse.md)


### 16.10 Voice/Video Call은 어떻게 동작하는가?

음성·영상 통화의 High-level 구조를 배웁니다.

- Signaling
- Peer-to-Peer Connection
- STUN Server
- TURN Server

시작하기: [Voice/Video Call](https://outcomeschool.com/blog/voice-and-video-call)

→ [한국어 상세 학습 노트](blogs/module-16/voice-and-video-call.md)


---
