# Paged Attention이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/paged-attention-in-llms  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-03-29 공개 원문을 직접 확인해 2,048-token 예약 낭비, 16-slot vs 4-token block 예제, block table과 prefix sharing을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 해결하려는 문제

KV Cache는 decode를 빠르게 만들지만 request마다 얼마나 긴 response가 나올지 미리 알 수 없습니다.

전통적인 연속 메모리 방식은 최대 길이를 크게 잡고 한 덩어리로 예약할 수 있습니다.

원문 예:

    reserve = 2,048 token slots
    actual response = 50 tokens
    wasted = 1,998 slots

낭비는 두 가지입니다.

- 내부 단편화: 예약했지만 쓰지 않은 공간
- 외부 단편화: free space가 여러 군데 흩어져 있어 큰 contiguous block으로 못 씀

## 2. OS Paging에서 빌린 아이디어

Paged Attention은 KV Cache를 작은 fixed-size block/page로 나눕니다.

    logical KV blocks
      → block table
      → physical GPU memory blocks

각 request의 block이 실제 memory에서 서로 붙어 있을 필요가 없습니다.

## 3. 원문의 16-slot 예

Traditional:

    16 slots upfront

실제 10 tokens만 사용:

    [I love teaching AI and Machine Learning at Outcome School __ __ __ __ __ __]

6 slots가 낭비됩니다.

Paged, block size 4:

    Block 1: [I love teaching AI]
    Block 2: [and Machine Learning at]
    Block 3: [Outcome School __ __]

마지막 block의 2 slots만 낭비합니다.

## 4. Block Table

원문 예:

    logical block 0 → physical location 5
    logical block 1 → physical location 12
    logical block 2 → physical location 3

Attention kernel은 block table을 따라 과거 K/V를 읽습니다.

Logical sequence는 연속이지만 physical memory는 흩어져 있어도 됩니다.

## 5. 왜 효율적인가

### Internal Waste 감소

필요할 때 block 단위로 추가 allocation.

### External Fragmentation 감소

모든 block 크기가 같아 어떤 free block도 사용할 수 있습니다.

### Concurrency 증가

같은 GPU memory로 더 많은 request의 KV Cache를 유지할 수 있습니다.

## 6. Prefix Memory Sharing

두 request가 동일 prefix를 가지면 prefix KV block을 공유할 수 있습니다.

예:

    common system prompt
      → block B1, B2
         ↙      ↘
       user A   user B

각 request는 unique suffix block만 따로 유지합니다.

Parallel sampling, beam search, common system prompt workload에서 효과적입니다.

## 7. PagedAttention이 Attention 수학을 바꾸는가

아닙니다.

- FlashAttention: attention 계산의 IO 최적화
- PagedAttention: KV Cache memory allocation/lookup 최적화

문제를 푸는 층위가 다릅니다.

## 8. Trade-off

- block table lookup
- custom kernel/runtime 필요
- block size tuning
- prefix-sharing bookkeeping

하지만 high-concurrency serving에서는 memory utilization 이득이 큽니다.

## 핵심 정리

- Paged Attention은 KV Cache를 fixed-size block으로 나눠 필요할 때만 할당합니다.
- 원문 16-slot 예에서는 traditional waste 6 slots가 paged 방식에서 마지막 block 2 slots로 줄어듭니다.
- Block table이 logical sequence와 physical memory를 연결합니다.
- Identical prefix block을 request끼리 공유할 수도 있습니다.
- vLLM의 핵심 아이디어 중 하나입니다.

## 원문

- https://outcomeschool.com/blog/paged-attention-in-llms
