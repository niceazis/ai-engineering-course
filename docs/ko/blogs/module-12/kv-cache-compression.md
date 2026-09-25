# KV Cache Compression이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/kv-cache-compression  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 원문 본문 캐시를 직접 열지 못했습니다. Outcome School 공식 Module 12의 Quantization·Token Eviction·K/V Sharing·Low-Rank Compression 구조를 기준으로 독립적으로 설명합니다.

## 1. 왜 압축하는가

KV Cache memory는:

    context length
    × layers
    × KV heads
    × head dimension

에 비례합니다.

Long context/high concurrency에서는 model weight보다 KV cache가 capacity를 제한할 수 있습니다.

## 2. Quantization

FP16/BF16 K/V를 FP8/INT8/더 낮은 precision으로 저장합니다.

장점:

- memory 감소
- memory bandwidth 감소

위험:

- attention score/output 품질 손실
- layer/head별 scale tuning 필요

## 3. Token Eviction

모든 과거 token을 유지하지 않습니다.

전략:

- oldest 제거
- local window
- attention importance
- sink token 유지

Memory는 bounded하지만 오래된 정보 retrieval이 약해질 수 있습니다.

## 4. K/V Head Sharing

MHA:

    query heads = KV heads

GQA/MQA:

    여러 query head가 K/V 공유

Cache element 수 자체를 줄입니다.

Architecture-level optimization이라 runtime compression과 구분합니다.

## 5. Low-Rank Compression

K/V representation을 더 낮은-dimensional latent로 압축하고 필요할 때 projection합니다.

메모리를 줄이지만 추가 compute와 approximation error가 생깁니다.

## 6. 선택 기준

High concurrency:

    GQA + paged allocation + lower precision

Long streaming:

    eviction/window/sink

Quality-sensitive:

    conservative quantization + full retention

## 7. 평가

- perplexity/task accuracy
- long-context retrieval
- bytes/token
- TPOT
- max concurrency

## 핵심 정리

- KV Cache Compression은 quantization, token eviction, head sharing, low-rank 등 여러 계층의 방법을 포함합니다.
- 메모리를 줄이는 대신 quality, compute, old-context retention과 trade-off합니다.
- 하나의 기법보다 workload에 맞는 조합이 중요합니다.

## 원문

- https://outcomeschool.com/blog/kv-cache-compression
