# LLM Inference Optimization — 한국어 상세 영상 학습 노트

> 영상: https://www.youtube.com/watch?v=jV2sCj4lHYk  
> 제공: Outcome School / Amit Shekhar  
> 검증 범위: 영상 URL과 Module 12 공식 자료는 확인했습니다. **YouTube 자막 전문은 직접 검증하지 못했습니다.** 아래 내용은 동일 주제의 Outcome School 공식 블로그와 Module 12 자료를 바탕으로 재구성한 상세 학습 노트이며 자막의 문장별 번역이 아닙니다.

## 1. Inference Optimization의 목적

LLM serving 최적화는 하나의 숫자가 아니라 다음 지표를 함께 다룹니다.

- TTFT: 첫 token이 나오기까지
- TPOT: 출력 token 사이 시간
- throughput: 단위 시간당 처리량
- GPU memory
- cost/request

## 2. Prefill과 Decode

Inference는 크게:

    prompt
      → prefill
      → first token
      → decode
      → next tokens

로 나뉩니다.

Prefill은 prompt 전체를 병렬 처리하고, Decode는 KV Cache를 읽으며 token을 하나씩 생성합니다.

## 3. KV Cache

과거 token의 Key/Value를 저장해 projection 재계산을 피합니다.

장점:

- decode compute 감소

대가:

- context와 concurrency가 커질수록 memory 증가

## 4. Memory 최적화

- GQA/MQA
- KV quantization
- token eviction
- PagedAttention
- low-rank/compressed KV

를 사용할 수 있습니다.

## 5. Compute / IO 최적화

### FlashAttention

HBM↔SRAM traffic을 줄입니다.

### Continuous Batching

finished request slot에 새 request를 즉시 넣어 GPU idle을 줄입니다.

### Speculative Decoding

작은 drafter가 여러 token을 제안하고 큰 model이 한 번에 검증합니다.

## 6. Serving Engine

vLLM, SGLang, TensorRT-LLM은 여러 optimization을 runtime에 결합합니다.

따라서 production에서 중요한 질문은:

> 어떤 technique이 더 좋은가?

보다:

> 현재 workload의 TTFT/TPOT/memory bottleneck을 어떤 조합으로 줄이는가?

입니다.

## 핵심 정리

- Prefill과 Decode는 병목이 달라 따로 최적화해야 합니다.
- KV Cache는 속도를 높이지만 memory를 소비합니다.
- PagedAttention, batching, speculative decoding, quantization은 서로 다른 병목을 해결합니다.
- 이 노트는 영상 자막 직역이 아니라 공식 Module 12 자료로 교차검증한 학습 노트입니다.
