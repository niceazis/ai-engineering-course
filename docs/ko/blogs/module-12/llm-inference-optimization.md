# LLM Inference Optimization — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/llm-inference-optimization  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-06-14 공개 원문을 직접 확인해 KV Cache, PagedAttention, FlashAttention, GQA, Speculative Decoding, Continuous Batching, Prefill/Decode의 관계를 독립적으로 정리했습니다.

## 1. Inference Optimization의 목표

LLM serving은 단순히 "tokens/s를 높이는 것"이 아닙니다.

주요 목표:

- TTFT(Time To First Token)
- TPOT(Time Per Output Token)
- throughput
- GPU memory
- cost/request

각 병목에 맞는 기법이 다릅니다.

## 2. Prefill과 Decode

### Prefill

Prompt 전체를 병렬 처리해 첫 token 직전의 KV Cache를 만듭니다.

주로 compute-heavy입니다.

### Decode

한 token씩 생성하며 과거 KV Cache를 읽습니다.

주로 memory-bandwidth/memory-capacity 영향을 크게 받습니다.

## 3. KV Cache

과거 token의 Key/Value를 저장해 매 step 재계산을 피합니다.

속도는 좋아지지만:

    memory ∝ layers × tokens × kv_heads × head_dim

으로 context/batch가 커질수록 GPU memory를 많이 사용합니다.

## 4. KV Memory 최적화

- GQA/MQA: K/V head 공유
- Quantization: K/V precision 축소
- Eviction: 중요도가 낮은/오래된 token 제거
- Low-rank/compression: representation 압축
- PagedAttention: allocation fragmentation 감소

## 5. Compute/IO 최적화

### FlashAttention

N×N intermediate를 HBM에 materialize하지 않고 tiling/online softmax로 memory traffic을 줄입니다.

### Continuous Batching

Request가 끝나는 즉시 새로운 request를 batch slot에 넣어 GPU idle을 줄입니다.

### Speculative Decoding

작은 drafter가 여러 token을 제안하고 target model이 한 번에 검증해 decode step 수를 줄입니다.

## 6. Serving Engine

vLLM, SGLang, TensorRT-LLM 같은 engine은 여러 최적화를 하나의 scheduler/runtime으로 결합합니다.

따라서 알고리즘 하나보다 workload에 맞는 engine 구성과 measurement가 중요합니다.

## 7. 어떤 지표를 우선할까

Interactive chat:

    TTFT + TPOT

Batch generation:

    throughput + cost/token

Long-context:

    prefill latency + KV memory

High concurrency:

    batching + cache allocation

## 핵심 정리

- Prefill과 Decode는 병목이 달라 별도로 최적화해야 합니다.
- KV Cache는 decode 속도의 핵심이지만 GPU memory의 큰 소비자입니다.
- FlashAttention은 memory IO, Continuous Batching은 utilization, Speculative Decoding은 sequential decode step을 줄입니다.
- 실제 성공 기준은 benchmark tokens/s가 아니라 서비스 SLO와 cost입니다.

## 원문

- https://outcomeschool.com/blog/llm-inference-optimization
