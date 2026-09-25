# The First-Token Latency Problem in LLMs — 한국어 상세 영상 학습 노트

> 영상: https://www.youtube.com/watch?v=XD8DD4cEHu0  
> 제공: Outcome School / Amit Shekhar  
> 검증 범위: 영상 URL과 Module 12 공식 Prefill/Decode 자료는 확인했습니다. **YouTube 자막 전문은 직접 검증하지 못했습니다.** 아래 내용은 같은 주제의 Outcome School 공식 블로그를 기반으로 정리한 상세 보조 노트입니다.

## 1. First-Token Latency란?

사용자가 request를 보낸 시점부터 첫 출력 token을 받기까지의 시간을 TTFT(Time To First Token)라고 합니다.

    request
      → queue
      → prefill
      → first token

Streaming을 사용해도 prefill이 끝나기 전에는 첫 token을 보낼 수 없습니다.

## 2. Prompt가 길수록 느려지는 이유

Prefill은 prompt token 전체를 Transformer layer에 통과시킵니다.

Prompt가 길어지면:

- attention compute
- memory traffic
- queue scheduling

비용이 증가합니다.

## 3. TTFT와 TPOT를 분리해야 한다

TTFT:

    "언제 답변이 시작되는가?"

TPOT:

    "답변이 시작된 뒤 token이 얼마나 빨리 이어지는가?"

긴 prompt에서는 TTFT가 나쁘고 decode는 빠를 수 있습니다.

반대로 작은 prompt + 큰 model에서는 TTFT는 괜찮지만 TPOT가 느릴 수 있습니다.

## 4. TTFT 최적화

- prompt/context 줄이기
- prefix/prompt caching
- FlashAttention
- chunked prefill
- scheduler queue 개선
- prefill-decode disaggregation

## 5. Prefix Reuse

많은 request가 같은 system prompt를 사용한다면 이미 계산한 prefix KV를 재사용해 prefill cost를 낮출 수 있습니다.

SGLang의 RadixAttention, serving-engine prefix cache와 연결됩니다.

## 6. Prefill-Decode Disaggregation

Prefill workload와 decode workload를 별도 GPU pool에 두면 큰 prefill job이 interactive decode를 막는 interference를 줄일 수 있습니다.

대신 KV Cache transfer와 orchestration overhead가 생깁니다.

## 7. 실제 관측 지표

- queue time
- prefill time
- first-token emission time
- prompt tokens
- cache hit
- p50/p95/p99 TTFT

평균만 보면 tail latency를 놓칠 수 있습니다.

## 핵심 정리

- First-token latency는 주로 queue + prefill의 영향을 받습니다.
- TTFT와 TPOT는 서로 다른 문제이므로 따로 측정해야 합니다.
- 긴 prompt에서는 prompt caching과 prefill optimization이 중요합니다.
- 이 노트는 자막 직역이 아니라 공식 Prefill/Decode 자료로 교차검증한 학습 노트입니다.
