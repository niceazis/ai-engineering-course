# TensorRT-LLM은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-tensorrt-llm-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 Outcome School 원문 본문은 웹 캐시에서 직접 열리지 않았습니다. 공식 Module 12 outline과 NVIDIA TensorRT-LLM 공식 문서를 교차검증해 작성하며, 원문 고유 수치를 임의로 단정하지 않습니다.

## 1. TensorRT-LLM의 목표

NVIDIA GPU에서 LLM inference를 최대한 hardware-aware하게 최적화하는 serving/runtime stack입니다.

핵심 층:

- optimized kernels
- quantization
- KV cache management
- batching/scheduler
- speculative decoding
- multi-GPU
- CUDA Graph

## 2. Build/Optimization

전통적으로 model definition/checkpoint를 TensorRT-LLM이 최적화 가능한 engine/runtime representation으로 준비합니다.

최근 backend/API는 버전에 따라 build workflow가 달라질 수 있으므로 최신 NVIDIA 문서를 기준으로 해야 합니다.

## 3. Kernel Fusion

여러 작은 GPU kernel을 하나의 fused kernel로 합치면 launch overhead와 intermediate HBM traffic을 줄이고 data locality를 높일 수 있습니다.

## 4. Quantization

지원 범위는 GPU generation/model에 따라 다르지만 FP8, INT8, INT4/weight-only, newer low-precision formats를 활용할 수 있습니다.

## 5. Custom Attention

Fused MHA/FMHA 계열 kernel, paged KV cache, context/decode-specific kernel로 attention workload를 최적화합니다.

## 6. Paged KV Cache

KV Cache를 block/page 단위로 관리해 fragmentation과 dynamic sequence allocation을 개선합니다.

## 7. In-Flight Batching

Serving backend는 request를 decode iteration에 동적으로 추가/제거하는 in-flight batching을 지원합니다.

NVIDIA 문서는 scheduler policy로 최대 utilization과 no-evict 성향의 선택지를 제공합니다.

## 8. CUDA Graph

반복되는 GPU execution graph를 capture/replay해 CPU launch overhead를 줄입니다.

Shape/dynamic behavior에 따라 graph cache 관리가 필요합니다.

## 9. Speculative Decoding

TensorRT-LLM ecosystem은 Medusa 등 speculative decoding mode를 지원할 수 있습니다.

Draft/acceptance method와 model artifact가 맞아야 합니다.

## 10. Multi-GPU

큰 model을 tensor parallel, pipeline parallel, expert parallel 등으로 여러 GPU에 분산합니다.

Network/NVLink topology가 performance에 큰 영향을 줍니다.

## 11. vLLM과 비교 관점

TensorRT-LLM은 NVIDIA hardware-specific optimization 깊이가 강하고, vLLM은 broad open-source serving ecosystem과 단순한 adoption이 강점입니다.

실제 선택은 model, GPU, batch, context, latency SLO로 benchmark해야 합니다.

## 핵심 정리

- TensorRT-LLM은 NVIDIA GPU 특화 LLM inference optimization stack입니다.
- Kernel fusion, quantization, paged KV cache, in-flight batching, CUDA Graph, speculative decoding을 조합합니다.
- Performance 잠재력은 높지만 hardware/version-specific tuning과 build complexity가 있습니다.
- Outcome School 원문 본문은 직접 확인하지 못해 NVIDIA 공식 자료와 Module 12 outline으로만 보완했습니다.

## 원문

- https://outcomeschool.com/blog/how-does-tensorrt-llm-work
