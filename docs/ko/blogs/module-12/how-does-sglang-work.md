# SGLang은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-sglang-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 RadixAttention, prefix reuse, frontend/runtime, continuous batching과 structured output을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. SGLang의 중심 문제

Agent, few-shot, multi-turn workload는 긴 prefix를 반복합니다.

    "You are a helpful assistant..."
    + same tools/examples
    + changing suffix

매번 같은 prefix prefill을 다시 계산하는 것은 낭비입니다.

## 2. RadixAttention

원문의 핵심:

    Radix tree
      + KV Cache
      = RadixAttention

Request text의 shared prefix를 radix tree node로 관리하고 해당 prefix의 KV Cache를 재사용합니다.

## 3. 원문의 예

Request A:

    You are a helpful assistant.
    What is the capital of France?

Request B:

    You are a helpful assistant.
    What is the capital of Japan?

공유 부분의 KV를 한 번만 계산하고 France/Japan suffix부터 분기합니다.

## 4. 새 Request

Italy query가 오면:

1. radix tree에서 longest prefix match
2. 해당 KV reuse
3. "Italy?" 부분만 새 prefill
4. 새로운 branch를 tree에 추가
5. decode

## 5. 왜 PagedAttention과 다른가

PagedAttention은 **fixed-size KV block memory allocation**이 핵심입니다.

RadixAttention은 **text prefix identity를 tree로 추적해 computation reuse**하는 것이 핵심입니다.

둘 다 serving cache 최적화지만 focus가 다릅니다.

## 6. Continuous Batching

SGLang도 dynamic batching을 사용합니다.

원문은 RadixAttention이 repeated work를 줄이고 continuous batching이 GPU utilization을 유지하는 조합을 강조합니다.

## 7. Frontend Language

SGLang은 generation program에서 generation, branching, parallelism, structured output 같은 high-level operation을 표현하고 runtime이 scheduling/cache를 최적화하는 구조를 제공합니다.

API 세부는 버전별로 바뀔 수 있습니다.

## 8. Structured Output

JSON/regex/grammar constraint를 runtime decoding에 적용하면 invalid token을 미리 막을 수 있습니다.

Post-hoc retry보다 효율적일 수 있습니다.

## 9. Distributed Prefix Reuse

원문은 multi-machine에서 cache-aware load balancing으로 shared prefix가 이미 cache된 worker에 request를 보내 reuse를 유지하는 방향도 설명합니다.

## 10. vLLM과 비교

둘 다 continuous batching, KV optimization, serving API를 제공할 수 있습니다.

원문에서 SGLang을 구별하는 핵심은 RadixAttention 기반 prefix reuse입니다.

## 핵심 정리

- SGLang의 대표 아이디어는 radix tree로 shared text prefix의 KV Cache를 재사용하는 RadixAttention입니다.
- 새 request는 longest cached prefix를 찾고 unique suffix만 계산합니다.
- Continuous Batching과 결합해 compute utilization도 높입니다.
- Repeated long-prefix agent/workflow에서 특히 유리합니다.
- 실제 기능/성능은 최신 release별 benchmark가 필요합니다.

## 원문

- https://outcomeschool.com/blog/how-does-sglang-work
