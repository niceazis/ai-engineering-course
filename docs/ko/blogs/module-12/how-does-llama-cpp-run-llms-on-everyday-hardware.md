# llama.cpp는 일반 하드웨어에서 LLM을 어떻게 실행하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-llama-cpp-run-llms-on-everyday-hardware  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 GGUF, quantization, mmap, SIMD와 CPU/GPU layer offload 흐름을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. llama.cpp의 목표

거대한 LLM을 datacenter GPU만이 아니라 laptop CPU, Apple Silicon, consumer GPU, mixed CPU/GPU에서 실행할 수 있게 highly optimized native runtime을 제공합니다.

## 2. Quantization

FP16/FP32 weight를 Q4/Q5/Q8로 줄여 RAM/VRAM requirement와 memory bandwidth를 낮춥니다.

Local inference에서는 compute보다 weight memory 이동이 bottleneck인 경우가 많아 low-bit의 효과가 큽니다.

## 3. GGUF

llama.cpp는 GGUF에서 architecture metadata, tokenizer, quantized tensors를 읽습니다.

Single file로 model을 배포하기 쉽습니다.

## 4. 원문의 mmap 설명

Normal loading:

    disk full model
      → copy all
      → RAM
      → start

mmap:

    file mapped into virtual memory
      → needed pages loaded on demand

원문은 이 방식이 startup을 빠르게 하고 같은 model을 여러 process가 읽을 때 OS page sharing 이점도 준다고 설명합니다.

## 5. SIMD

CPU에서 동일 연산을 여러 값에 한 번에 적용합니다.

Platform에 따라 AVX, NEON 등 최적화 kernel이 사용될 수 있습니다.

정확한 지원은 build/runtime에 따라 다릅니다.

## 6. GPU Offload

모든 layer가 VRAM에 안 들어가면 일부 layer만 GPU에 올리고 나머지는 CPU에서 계산할 수 있습니다.

    selected layers → GPU
    remaining       → CPU

PCIe/Unified Memory architecture에 따라 optimal split이 달라집니다.

Apple Silicon은 CPU/GPU가 unified memory를 공유하는 점이 별도 특성입니다.

## 7. 전체 Prompt 흐름

원문 순서:

1. GGUF open + mmap
2. prompt tokenization
3. token이 Transformer layers 통과
4. quantized weight로 matrix ops
5. CPU/GPU가 workload 분담
6. logits 계산
7. sampling
8. token을 text로 decode
9. streaming 출력

## 8. Local Serving의 Trade-off

장점:

- privacy
- offline
- API cost 없음
- commodity hardware

한계:

- frontier model quality/size 제한
- long-context KV memory
- lower throughput than datacenter GPU
- manual model/quantization choice

## 핵심 정리

- llama.cpp는 quantization+GGUF+mmap+SIMD+GPU offload를 조합해 local inference를 가능하게 합니다.
- 원문은 mmap이 full upfront copy 없이 필요한 page를 on-demand load한다고 설명합니다.
- CPU-only뿐 아니라 partial/full GPU offload도 가능합니다.
- Local performance는 model size, quantization, context, hardware memory bandwidth에 크게 좌우됩니다.

## 원문

- https://outcomeschool.com/blog/how-does-llama-cpp-run-llms-on-everyday-hardware
