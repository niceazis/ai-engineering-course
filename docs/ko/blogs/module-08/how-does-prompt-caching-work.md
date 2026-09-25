# Prompt Caching은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-prompt-caching-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문을 직접 확인해 exact-prefix rule, cache write/read, TTL 5분·1시간 예, stable-prefix 설계를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Prompt Caching이란?

Prompt Caching은 여러 request에서 반복되는 **동일한 prompt prefix의 model intermediate computation을 재사용**해 input processing cost와 latency를 줄이는 기술입니다.

대표 상황:

    [같은 system prompt]
    [같은 tool schema]
    [같은 긴 document]
    [사용자 질문만 다름]

첫 request에서 공통 prefix를 처리하고 이후 request가 cache를 재사용합니다.

## 2. 왜 효과가 있는가

Transformer prefill은 input token 전체를 처리해 각 layer의 K/V state를 계산합니다.

Long prefix가 매 request마다 같다면 동일 계산을 반복합니다.

Prompt cache hit:

    cached prefix K/V
      + new suffix
      → continue prefill/decode

로 중복 계산을 줄일 수 있습니다.

## 3. Cache와 Response Cache는 다르다

### Response Cache

동일 question에 완성된 answer를 그대로 반환.

### Prompt Cache

Model의 prefix computation만 재사용하고 **new suffix에 대해서는 model이 새 answer를 생성**합니다.

따라서 user question이 달라도 shared prefix가 같으면 유용합니다.

## 4. Exact-Prefix Rule

원문이 가장 중요하게 강조하는 규칙:

> Cached part는 prompt의 시작이어야 하고 정확히 동일하게 match해야 한다.

즉 cacheable common data는 앞에 배치해야 합니다.

좋은 구조:

    [stable system]
    [stable tools]
    [stable docs]
    [dynamic user question]

나쁜 구조:

    [current timestamp]
    [stable system]
    [stable docs]

앞쪽 timestamp가 매번 달라지면 뒤의 긴 stable part까지 prefix match가 깨질 수 있습니다.

## 5. Character-for-Character라는 설명의 의미

원문은 교육적으로 "character for character"라고 설명합니다.

실제 provider implementation은 tokenized prefix/block boundary를 기준으로 cache hit을 계산할 수 있으므로 정확한 matching rule은 provider 문서를 확인해야 합니다.

하지만 설계 원칙은 동일합니다.

> 변하는 것을 뒤로, 반복되는 것을 앞으로.

## 6. Cache Write

첫 request:

    long stable prefix
      → full prefill compute
      → cache entry write

Write는 일반 input 처리보다 같은 비용이거나 provider에 따라 별도 cache-write 가격이 적용될 수 있습니다.

## 7. Cache Read

다음 request:

    same prefix + new suffix

이면 cached prefix state를 읽고 suffix만 추가 계산합니다.

효과:

- lower TTFT
- lower repeated-input cost
- higher throughput

## 8. TTL

원문:

- common default TTL 예: 5분
- longer option 예: 1시간

TTL(Time To Live)은 cache가 유지되는 시간입니다.

    hit within TTL → read
    expired → next request writes again

Provider별 지원 TTL과 가격은 다를 수 있습니다.

## 9. Longer TTL Trade-off

긴 TTL:

- request 간격이 길어도 hit 가능

하지만 provider에 따라:

- cache write premium
- storage policy

가 달라질 수 있습니다.

따라서 request arrival pattern을 보고 선택합니다.

## 10. 무엇을 Cache Prefix에 넣나

원문이 권장하는 stable content:

- system instruction
- large static document
- tool/function definitions
- long examples
- reusable reference material

Dynamic content:

- current user message
- current timestamp
- latest tool result
- user-specific changing state

는 뒤에 둡니다.

## 11. 예시

Support agent:

    system prompt      3K tokens
    policies          40K tokens
    tool schemas       5K tokens
    user message       100 tokens

공통 prefix:

    48K tokens

사용자 message만 바뀐다면 prompt caching 효과가 큽니다.

반대로 system/policy를 request마다 조금씩 serialize 다르게 하면 hit rate가 떨어집니다.

## 12. Stable Serialization

Cache hit을 높이려면:

- JSON key order 고정
- whitespace 안정화
- tool order 고정
- timestamp를 prefix에서 제거
- nondeterministic IDs 제거

가 중요합니다.

같은 의미여도 byte/token sequence가 달라지면 cache miss가 날 수 있습니다.

## 13. Tool Schema와 Agent

Agent는 수십 개 tool schema를 매 turn prompt에 넣을 수 있습니다.

Tool list가 stable하다면 caching하기 좋은 prefix입니다.

하지만 dynamic tool filtering을 매 turn 다르게 하면 cache hit과 context size 사이 trade-off가 생깁니다.

## 14. Prompt Caching과 Context Engineering

Prompt caching을 잘하려면 context ordering 자체를 cache-friendly하게 설계해야 합니다.

즉 performance optimization이 prompt wording 문제가 아니라 **context layout 문제**가 됩니다.

## 15. Cache Hit Metric

Production에서 측정할 것:

- cached input tokens
- cache hit ratio
- write/read cost
- TTFT
- request interval distribution
- prefix invalidation frequency

Cache를 켰다는 사실보다 실제 hit rate가 중요합니다.

## 16. 언제 효과가 작나

- 매 request prefix가 거의 다름
- prompt가 짧음
- request가 TTL보다 드물게 옴
- dynamic context를 항상 앞에 둠

이 경우 complexity 대비 이득이 작습니다.

## 핵심 정리

- Prompt Caching은 동일한 prompt prefix의 prefill computation을 재사용합니다.
- Response cache와 달리 새로운 suffix에 대해 새 response를 생성합니다.
- 가장 중요한 원칙은 exact/stable prefix입니다.
- 원문은 5분 default TTL, 1시간 long TTL 예를 설명합니다.
- Stable system/tool/docs는 앞, dynamic user/tool state는 뒤에 배치합니다.
- Cache hit ratio와 TTFT/cost를 실제 workload에서 측정해야 합니다.

## 원문

- https://outcomeschool.com/blog/how-does-prompt-caching-work
