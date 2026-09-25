# Attention Sink는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-do-attention-sinks-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문 전체 번역이 아닌 독립적인 한국어 상세 해설입니다. 현재 Outcome School 원문 본문은 웹 캐시에서 직접 열리지 않았습니다. 공식 Module 5 레슨 개요가 제시하는 StreamingLLM 흐름과 Attention Sink/StreamingLLM 공개 연구를 교차검증해 작성하며, 원문 고유 수치는 확인된 것으로 단정하지 않습니다.

## 1. 문제: 대화가 끝없이 길어지면?

Autoregressive LLM은 과거 token의 K/V를 KV Cache에 저장합니다.

대화가 계속 길어지면 cache도 커집니다.

메모리를 제한하려고 가장 오래된 token을 단순히 제거하면:

    keep last W tokens only

같은 sliding cache가 됩니다.

직관적으로는 그럴듯하지만 실제 연구에서는 **초기 token을 버렸을 때 perplexity가 급격히 나빠질 수 있는 현상**이 관찰됐습니다.

## 2. Attention Sink란?

일부 attention head는 내용적으로 특별하지 않은 초기 token에 지속적으로 큰 attention mass를 보냅니다.

이런 위치를 Attention Sink라고 부릅니다.

중요한 점:

- 첫 token이 항상 의미상 가장 중요해서가 아님
- attention probability는 softmax 때문에 합이 1이어야 함
- 특정 head가 실제로 참고할 내용이 없을 때 남는 attention mass를 안정적으로 흡수하는 위치처럼 동작할 수 있음

## 3. 왜 첫 Token이 Sink가 되기 쉬운가

Causal attention에서는 첫 token은 **모든 이후 token이 볼 수 있는 공통 위치**입니다.

두 번째 token은 첫 번째 이후 query부터 보이지만, 첫 token은 sequence 전체에서 계속 존재합니다.

Training 중 이런 공통 위치가 attention mass를 모으는 안정적인 대상으로 발전할 수 있습니다.

BOS 같은 special token이 sink 역할을 하는 경우도 있습니다.

## 4. Softmax 관점

Attention row는 다음처럼 normalization됩니다.

    weights_i = exp(score_i) / sum_j exp(score_j)

모든 weight 합은 1입니다.

Head가 현재 어떤 context token도 강하게 참고할 필요가 없더라도 1의 attention mass를 어디엔가는 배분해야 합니다.

Sink token은 이 남는 mass를 받아들이는 역할로 해석할 수 있습니다.

## 5. 단순 Sliding Cache가 실패하는 이유

원래 sequence:

    [sink][old context ...][recent W tokens]

최근 W token만 남기면:

    [recent W tokens]

이 됩니다.

Model은 training 동안 늘 존재했던 sink position을 잃고, attention distribution이 갑자기 다른 pattern으로 강제됩니다.

그래서 오래된 content를 버리는 것과 sink까지 버리는 것은 같은 효과가 아닐 수 있습니다.

## 6. StreamingLLM의 핵심 아이디어

StreamingLLM 계열의 핵심 cache 구성:

    [first few sink tokens] + [most recent W tokens]

즉:

- 오래된 중간 context는 제거
- 초기 sink token 몇 개는 고정 유지
- 최근 local context는 sliding window로 유지

이렇게 하면 cache size를 bounded하게 유지하면서 naive window eviction보다 안정적인 품질을 얻을 수 있습니다.

## 7. 숫자로 보는 Cache 구조

설명용 예:

    sink tokens = 4
    recent window = 4092

총 cache:

    4 + 4092 = 4096 tokens

새 token이 들어오면:

1. sink 4개 유지
2. recent window의 가장 오래된 1개 제거
3. 새 token 추가

총 cache 길이는 계속 4096 근처로 유지됩니다.

이 숫자는 개념 예이며 Outcome School 원문의 고유 수치로 확인된 것은 아닙니다.

## 8. 왜 Sink를 재계산하면 안 되는가

Sink token의 K/V는 원래 position에서 계산된 값입니다.

Streaming cache에서 이를 계속 재사용할 때 position encoding, 특히 RoPE 처리와 cache position을 올바르게 유지해야 합니다.

단순히 text token만 맨 앞으로 다시 붙여 매 step 다른 position으로 재계산하는 것과는 다를 수 있습니다.

구현은 사용하는 model/runtime의 position policy를 확인해야 합니다.

## 9. Attention Sink와 의미적 Memory는 다르다

Sink token을 유지한다고 오래된 대화 내용을 기억하는 것은 아닙니다.

Sink의 목적:

- attention distribution 안정화
- streaming cache 품질 유지

Long-term memory의 목적:

- 오래된 사실/사용자 선호/도구 결과 보존

후자는 별도 retrieval, summary, external memory가 필요합니다.

## 10. StreamingLLM이 해결하는 것과 못 하는 것

### 해결하는 쪽

- 무한히 늘어나는 KV cache를 bounded window로 제한
- naive sliding eviction의 급격한 품질 저하 완화
- 긴 streaming sequence의 지속적 decode

### 해결하지 않는 쪽

- 오래 전에 제거한 상세 사실을 다시 복원
- 무한한 semantic memory 제공
- 모든 long-context reasoning 문제 해결

## 11. 현대 Attention Sink 설계

최근 architecture에서는 자연적으로 생긴 sink를 이용하는 것 외에 **learnable sink logit/token**을 명시적으로 설계하기도 합니다.

Module 5의 DeepSeek-V4 원문은 core attention softmax denominator에 learnable sink logits를 넣어 attention sum이 실질적으로 1보다 작게 작동할 수 있는 구조를 설명합니다.

즉 “아무 context도 중요하지 않다”는 선택지를 모델에 명시적으로 주는 방향입니다.

## 12. DeepSeek-V4와 연결

DeepSeek-V4 원문은 CSA/HCA와 함께 learnable attention sink를 사용한다고 설명합니다.

목적:

- 모든 attention mass를 실제 context token에 강제로 배분하지 않음
- head가 불필요한 context를 무리하게 참조하는 것을 완화

StreamingLLM의 관찰된 sink와 목적이 완전히 동일한 구현은 아니지만, “attention을 어디에도 주지 않을 자유”라는 공통 직관이 있습니다.

## 13. 실무 테스트

Streaming cache를 구현한다면 비교해야 합니다.

A:

    recent W only

B:

    sink S + recent (W-S)

측정:

- perplexity
- generation quality
- long-run stability
- KV cache bytes
- tokens/s
- 제거된 오래된 fact를 묻는 retrieval test

## 핵심 정리

- Attention Sink는 초기 token이 큰 attention mass를 지속적으로 흡수하는 현상입니다.
- 첫 token은 모든 이후 query에 노출돼 sink가 되기 쉬운 구조적 위치입니다.
- 단순히 오래된 token을 모두 버리면 sink까지 사라져 품질이 급락할 수 있습니다.
- StreamingLLM은 초기 sink token을 고정하고 최근 token만 sliding해 bounded KV cache를 만듭니다.
- Sink 유지와 long-term semantic memory는 별개입니다.
- 원문 본문을 직접 열지 못했으므로 특정 수치는 공개 연구에 기반한 설명용 예로만 사용했습니다.

## 원문

- https://outcomeschool.com/blog/how-do-attention-sinks-work
