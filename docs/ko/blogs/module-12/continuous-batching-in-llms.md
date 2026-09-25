# Continuous Batching이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/continuous-batching-in-llms  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-05-11 공개 원문을 직접 확인해 Static vs Continuous Batching, 4-slot A/B/C/D/E 수치 예제, decode-step 단위 scheduling을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 핵심 아이디어

원문 한 줄 정의:

> 기존 request가 끝나는 즉시 그 batch slot에 새 request를 넣는다.

Static batching은 request 묶음이 모두 끝날 때까지 기다립니다.

Continuous batching은 **매 decode step 뒤 slot을 재구성**합니다.

## 2. 왜 Batching이 중요한가

GPU는 여러 request를 함께 처리할 때 utilization이 좋아집니다.

원문은 8개 request를 동시에 batch하면 하나씩 처리하는 것보다 GPU를 더 효율적으로 활용할 수 있다고 설명합니다.

## 3. Static Batching의 문제

Batch 4개가:

    A = long
    B = short
    C = medium
    D = very long

이면 B가 먼저 끝나도 그 slot은 batch 전체가 끝날 때까지 비어 있을 수 있습니다.

New request E는 기다립니다.

GPU slot이 expensive resource인데 idle하게 됩니다.

## 4. Request-Level vs Token-Level

원문 구분:

    Static Batching
      = request-level batch

    Continuous Batching
      = token/decode-step-level scheduling

매 decode step 후:

1. 끝난 request 제거
2. queue 확인
3. 빈 slot에 새 request 투입
4. 새 request prefill
5. 다음 decode step

을 반복합니다.

## 5. 원문의 수치 예

4 slots:

    A = 100 decode steps
    B = 20
    C = 50
    D = 200

새 request:

    E = 30

Static에서는 E가 현재 batch의 가장 긴 D가 끝날 때까지 기다릴 수 있습니다.

Continuous에서는 B가 20 step에 끝나는 즉시 E가 그 slot에 들어갈 수 있습니다.

## 6. 원문의 Timing 가정

원문은 예시로:

    each decode step = 50 ms
    batch slots = 4
    A=100, B=20, C=50, D=200, E=30

을 둡니다.

핵심은 continuous scheduling이 비어 있는 slot의 wasted GPU work와 queue wait를 줄인다는 것입니다.

실제 speedup은 request-length distribution과 batch size에 따라 달라집니다.

## 7. Prefill과의 충돌

새 request가 중간에 들어오면 prefill이 필요합니다.

Modern engine은:

- chunked prefill
- scheduler priority
- separate prefill/decode policy

로 decode latency jitter를 관리합니다.

## 8. PagedAttention과의 결합

Request가 끝나면:

    KV blocks free
      → new request gets memory
      → batch slot also reused

그래서 PagedAttention과 Continuous Batching은 memory/utilization 측면에서 잘 결합됩니다.

## 9. 장점

- GPU utilization 증가
- queue latency 감소
- throughput 증가
- heterogeneous output length 처리에 강함

## 10. 주의점

- scheduling overhead
- prefill/decode interference
- starvation/fairness
- latency SLO
- memory admission control

Throughput만 최적화하면 interactive TPOT가 나빠질 수 있습니다.

## 핵심 정리

- Continuous Batching은 batch를 request 단위가 아니라 decode step 단위로 동적으로 재구성합니다.
- 원문 예에서 B가 20 step에 끝나면 E가 즉시 빈 slot에 들어갑니다.
- Static batching의 idle slot과 queue wait를 줄입니다.
- PagedAttention과 함께 modern serving engine의 핵심입니다.
- Throughput과 per-user latency/fairness를 같이 측정해야 합니다.

## 원문

- https://outcomeschool.com/blog/continuous-batching-in-llms
