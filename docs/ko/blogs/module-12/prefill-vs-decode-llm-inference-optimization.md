# Prefill vs Decode — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/prefill-vs-decode-llm-inference-optimization  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 두 inference phase, KV Cache bridge, TTFT/TPOT와 compute-bound vs memory-bound를 독립적으로 설명합니다.

## 1. 두 단계

LLM request:

    prompt
      → Prefill
      → first token
      → Decode
      → token2
      → token3 ...

## 2. Prefill

Prompt의 모든 token을 한 번에 Transformer에 통과시킵니다.

특징:

- 큰 matrix multiplication
- GPU parallelism 활용
- prompt length에 민감
- TTFT에 큰 영향

Prefill 결과로 각 layer의 prompt K/V가 cache에 저장됩니다.

## 3. Decode

새 token 하나를 생성합니다.

각 step:

1. 새 token의 Q/K/V 계산
2. 과거 cached K/V와 attention
3. logits
4. next token 선택
5. 새 K/V cache append

출력 길이만큼 반복됩니다.

## 4. KV Cache가 Bridge

Prefill에서 만든 prompt K/V를 Decode가 그대로 사용합니다.

Cache가 없다면 decode step마다 prompt 전체를 다시 계산해야 합니다.

## 5. Compute-Bound vs Memory-Bound

Prefill:

- 큰 GEMM
- compute utilization이 핵심

Decode:

- 작은 batch/token 연산
- 매 step 큰 weight/KV를 읽음
- memory bandwidth 영향을 크게 받음

그래서 같은 GPU 최적화가 두 단계에 똑같이 효과적이지 않습니다.

## 6. 주요 Metric

### TTFT

request → first token.

Prefill, queueing, scheduling 영향.

### TPOT

출력 token 사이 평균 시간.

Decode 성능.

### Throughput

시간당 처리 token/request.

### End-to-End Latency

TTFT + 전체 decode 시간.

## 7. 최적화 Mapping

Prefill:

- FlashAttention
- prompt/prefix caching
- chunked prefill
- faster compute GPU

Decode:

- KV Cache
- GQA
- continuous batching
- speculative decoding
- quantization

## 핵심 정리

- Prefill은 prompt 전체를 처리하고 KV Cache를 만드는 단계입니다.
- Decode는 KV Cache를 읽으며 token-by-token 생성합니다.
- Prefill은 상대적으로 compute-bound, Decode는 memory-bound 성격이 강합니다.
- TTFT는 Prefill, TPOT는 Decode 문제를 진단하는 핵심 지표입니다.

## 원문

- https://outcomeschool.com/blog/prefill-vs-decode-llm-inference-optimization
