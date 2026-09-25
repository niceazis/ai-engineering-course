# vLLM은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-vllm-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 PagedAttention, prefix memory sharing, Continuous Batching, OpenAI-compatible server의 순서를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. vLLM의 목표

Open model을 많은 사용자에게 높은 throughput으로 serving할 때 주요 병목은 KV Cache memory, static batching idle slot, repeated prefix processing입니다.

vLLM은 runtime/scheduler 수준에서 이를 줄입니다.

## 2. PagedAttention

원문의 핵심:

    huge contiguous KV allocation
      → fixed-size blocks allocated on demand

Block table이 request의 logical KV sequence와 physical block을 연결합니다.

Memory over-reservation과 fragmentation을 줄입니다.

## 3. Prefix Sharing

동일 system prompt/prefix가 여러 request에 반복되면 같은 KV block을 공유할 수 있습니다.

원문은 여러 request가 common instruction block을 함께 가리키고 unique suffix만 별도 저장하는 방식으로 설명합니다.

## 4. Continuous Batching

매 decode step 후:

- finished request 제거
- memory free
- queue의 새 request 투입

해 GPU slot을 계속 채웁니다.

PagedAttention이 memory를 빠르게 회수하고 Continuous Batching이 compute slot을 재사용합니다.

## 5. 두 기법의 결합

    PagedAttention
      → GPU memory waste 감소

    Continuous Batching
      → GPU compute idle 감소

두 자원을 동시에 높은 utilization로 유지합니다.

## 6. OpenAI-Compatible API

vLLM은 OpenAI-compatible HTTP API server를 제공해 기존 client/tool이 base URL을 바꿔 self-hosted model을 호출할 수 있게 합니다.

정확한 endpoint/model feature compatibility는 현재 vLLM release 문서를 확인해야 합니다.

## 7. Agent Workload

Agent는 매 step 같은 긴 system/tool prompt를 반복하기 쉽습니다.

Prefix caching/sharing과 short-request batching이 이런 workload에 특히 유용합니다.

## 8. Production에서 추가로 볼 것

- tensor/pipeline parallel
- prefix caching
- speculative decoding
- quantization
- chunked prefill
- scheduler policy
- multi-node

기능은 release에 따라 빠르게 변합니다.

## 핵심 정리

- vLLM은 LLM serving engine이며 핵심 개념은 PagedAttention과 Continuous Batching입니다.
- PagedAttention은 KV memory를 block 단위로 관리하고 sharing을 가능하게 합니다.
- Continuous Batching은 decode step마다 batch slot을 재활용합니다.
- OpenAI-compatible API로 application migration이 쉽습니다.
- 실제 성능은 concurrency/context/model/hardware에 맞춰 benchmark해야 합니다.

## 원문

- https://outcomeschool.com/blog/how-does-vllm-work
