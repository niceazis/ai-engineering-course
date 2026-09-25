# Prefill-Decode Disaggregation이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/prefill-decode-disaggregation  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 원문 본문 캐시를 직접 열지 못했습니다. 공식 Module 12 outline과 공개 serving architecture를 기준으로 독립적으로 설명하며 원문 고유 수치는 단정하지 않습니다.

## 1. 문제

같은 GPU에서:

    Prefill workload
    + Decode workload

를 함께 돌리면 서로 다른 특성 때문에 interference가 생깁니다.

Prefill은 compute-heavy, Decode는 memory/latency-sensitive입니다.

## 2. Disaggregation

두 phase를 별도 worker pool로 분리합니다.

    request
      → Prefill GPU pool
      → KV Cache transfer
      → Decode GPU pool
      → streaming tokens

각 pool을 서로 다른 hardware/scheduler 목표로 최적화할 수 있습니다.

## 3. 장점

### Resource Specialization

Prefill GPU는 batch/compute utilization, Decode GPU는 low-latency memory bandwidth에 최적화.

### Independent Scaling

긴 prompt traffic이 늘면 Prefill pool만 확장할 수 있습니다.

### Interference 감소

큰 prefill job이 interactive decode token을 지연시키는 문제를 완화합니다.

## 4. 핵심 비용: KV Transfer

Prefill 결과의 KV Cache를 Decode worker로 옮겨야 합니다.

Context가 길수록 transfer size가 커집니다.

따라서:

    compute saved
      ↔ network transfer / orchestration cost

trade-off가 있습니다.

## 5. Co-located가 나은 경우

- traffic 작음
- context 짧음
- single-node deployment
- low complexity priority

Disaggregation은 scale이 충분히 클 때 의미가 큽니다.

## 6. Metrics

- TTFT
- TPOT jitter
- KV transfer latency
- network bandwidth
- queue utilization
- GPU utilization

## 핵심 정리

- Prefill/Decode는 병목이 달라 worker pool을 분리할 수 있습니다.
- Disaggregation은 독립 scaling과 interference 감소가 장점입니다.
- 대가로 KV Cache 전송과 scheduler/network 복잡도가 생깁니다.
- 작은 deployment에는 과도할 수 있습니다.

## 원문

- https://outcomeschool.com/blog/prefill-decode-disaggregation
