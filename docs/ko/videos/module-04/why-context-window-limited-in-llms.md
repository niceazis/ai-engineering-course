# Why is the context window limited in LLMs? — 한국어 상세 영상 학습 노트

> 영상: https://www.youtube.com/watch?v=CGIhxIaOg3M  
> 제공: Outcome School / Amit Shekhar  
> 검증 범위: YouTube 영상 제목·게시 정보는 확인했습니다. YouTube 자체 자막 API를 직접 읽지는 못했지만, Amit Shekhar가 공식 LinkedIn 게시물에 공개한 **동일 영상 transcript 전문**을 직접 확인해 아래 내용을 작성했습니다.

## 1. Context Window란?

영상은 context window를 **LLM이 한 번에 읽을 수 있는 최대 text 양**으로 설명합니다.

영상 예시에서는 GPT-4의 128K token을 약 300-page book 규모로 직관화합니다.

이 숫자는 영상에서 이해를 돕기 위한 예이며, 실제 제품의 현재 context limit은 model/version에 따라 달라질 수 있습니다.

## 2. 왜 무한대로 늘릴 수 없는가

영상은 세 가지 핵심 이유를 제시합니다.

1. Self-Attention의 quadratic compute cost
2. KV Cache의 GPU memory cost
3. Training data length와 generalization 한계

이 세 가지가 context window를 단순히 무한히 늘릴 수 없는 이유입니다.

## 3. 이유 1 — Attention의 Quadratic Cost

Transformer self-attention에서는 각 token이 다른 token과 관계를 계산합니다.

Sequence length를 n이라고 하면 score matrix 크기는 대략:

    n × n

입니다.

영상의 정확한 수치 예:

### 1,000 tokens

    1,000 × 1,000
    = 1,000,000 comparisons

### 10,000 tokens

    10,000 × 10,000
    = 100,000,000 comparisons

Context가 10배 길어지면 pairwise attention 비교 수는 100배 규모로 늘어납니다.

이것이 quadratic cost입니다.

## 4. 왜 이 비용이 중요한가

Sequence length가 늘면:

- attention score 계산량 증가
- attention intermediate memory 증가
- prefill latency 증가
- batch에 넣을 수 있는 request 수 감소

로 이어질 수 있습니다.

FlashAttention 같은 kernel이 memory access를 크게 개선해도 표준 dense attention의 모든 pair 관계라는 기본 구조 자체가 완전히 사라지는 것은 아닙니다.

## 5. 이유 2 — KV Cache Memory

Autoregressive decoding에서 이전 token의 Key와 Value를 매 step 다시 계산하지 않기 위해 KV Cache를 저장합니다.

Context가 길어질수록 저장해야 할 token의 K/V도 늘어납니다.

개념적으로 KV cache memory는 다음 요인에 비례합니다.

    number of layers
    × sequence length
    × KV heads
    × head dimension
    × K and V
    × bytes per element

영상은 매우 긴 context에서 KV cache가 **수백 GB GPU memory** 규모가 될 수 있다고 설명합니다.

정확한 값은 model architecture, precision, GQA/MQA 사용 여부 등에 따라 달라집니다.

## 6. Context가 길수록 Serving Capacity가 줄 수 있다

GPU memory가 고정되어 있을 때 request 하나가 큰 KV cache를 차지하면 동시에 유지할 수 있는 request 수가 감소합니다.

즉 context window는 단일 request의 기능 문제뿐 아니라:

- concurrency
- throughput
- serving cost

와 직접 연결됩니다.

## 7. 이유 3 — Training Length

영상의 세 번째 이유는 training data length입니다.

Model이 학습 중 주로 짧은 sequence를 봤는데 inference에서 훨씬 더 긴 context를 주면:

- position extrapolation 문제
- 중간 정보 활용 저하
- long-range retrieval 품질 저하

가 나타날 수 있습니다.

즉 architecture가 입력을 “받아들일 수 있다”는 사실과 그 길이 전체를 “잘 활용한다”는 사실은 다릅니다.

## 8. Lost in the Middle과 연결

Module 4의 다음 블로그가 이 문제를 더 구체적으로 다룹니다.

긴 context 안에 정답이 존재해도:

- 시작
- 끝

보다 중간 위치의 정보를 덜 활용할 수 있습니다.

따라서 context window size는 capacity이고, 실제 usable context quality는 별도로 평가해야 합니다.

## 9. 영상이 제시하는 Long-Context 기법

영상 마지막은 연구·시스템 최적화 방향으로 다음을 언급합니다.

### Sparse Attention

모든 token pair를 보지 않고 중요한 일부 관계만 계산합니다.

### Sliding Window Attention

각 token이 주변의 제한된 window만 attention하도록 해 비용을 줄입니다.

### KV Cache Compression

K/V를 줄이거나 압축해 memory cost를 낮춥니다.

Module 5와 Module 12에서 각각 attention 효율화와 KV cache 최적화를 더 자세히 다룹니다.

## 10. 실무에서 Context를 설계하는 기준

큰 context window가 있다고 무조건 모두 넣는 것이 최적은 아닙니다.

검토할 지표:

- input token count
- TTFT
- p95 latency
- KV cache memory/request
- concurrent requests/GPU
- answer accuracy by information position
- cost/request

RAG, reranking, summarization, context compaction으로 **필요한 정보만 유지**하는 것이 더 효율적일 수 있습니다.

## 11. 영상 전체 논리를 한 줄로 연결

    longer context
      ├─ attention pair 수 증가 → compute 증가
      ├─ KV cache 증가 → GPU memory 증가
      └─ training length 밖으로 확장 → quality risk 증가

따라서 context window는 engineering trade-off로 제한됩니다.

## 핵심 정리

- 영상은 context limit의 세 원인을 quadratic attention, KV cache memory, training length로 설명합니다.
- 1K token의 1M 비교가 10K token에서 100M 비교로 증가하는 수치 예를 사용합니다.
- KV cache는 context와 함께 커져 concurrency와 serving cost에 영향을 줍니다.
- 긴 입력을 받아들이는 capacity와 긴 입력 전체를 잘 활용하는 quality는 다릅니다.
- Sparse Attention, Sliding Window, KV Cache Compression이 대표적인 개선 방향입니다.

## 확인 자료

- YouTube: https://www.youtube.com/watch?v=CGIhxIaOg3M
- Amit Shekhar 공식 LinkedIn 동일 영상 transcript
