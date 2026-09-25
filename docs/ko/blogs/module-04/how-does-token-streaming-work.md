# Token Streaming은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-token-streaming-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-06-10 공개 원문을 직접 확인해 원문의 설명 순서, 500-token 예, SSE 형식, 종료 marker, SSE/WebSocket 비교를 보존한 독립적 한국어 해설입니다.

## 1. Token Streaming이란?

Token streaming은 모델의 전체 답변이 완성될 때까지 기다리지 않고 **생성되는 조각을 준비되는 즉시 사용자에게 보내는 방식**입니다.

ChatGPT나 Claude에서 답변이 조금씩 화면에 나타나는 경험이 대표적인 예입니다.

핵심은 autoregressive LLM이 이미 token을 하나씩 생성하고 있으므로, server가 이를 모두 모았다가 마지막에 보내는 대신 생성 직후 전송할 수 있다는 점입니다.

## 2. LLM 생성 복습

원문의 예:

    Step 1: The
    Step 2: The cat
    Step 3: The cat sat
    Step 4: The cat sat on
    Step 5: The cat sat on the
    Step 6: The cat sat on the mat

각 step은 지금까지의 token을 조건으로 다음 token을 생성합니다.

두 가지 전송 방식이 가능합니다.

1. 모든 token을 만든 뒤 전체 response를 한 번에 전송
2. 각 token 또는 chunk가 준비될 때마다 streaming

## 3. 왜 Streaming이 필요한가

원문은 500-token 답변을 예로 듭니다.

Streaming이 없다면 사용자는 500 token 전체가 생성될 때까지 빈 화면을 보게 됩니다.

### Without streaming

    user asks
      → model writes all 500 tokens
      → full reply appears

### With streaming

    user asks
      → token 1 appears
      → token 2
      → token 3
      → ...
      → done

이 차이는 사용자 체감 latency를 크게 바꿉니다.

## 4. Time To First Token

TTFT(Time To First Token)는 request 후 첫 출력 token을 보기까지 걸리는 시간입니다.

원문은 streaming이 사용자에게 첫 결과를 빨리 보여 주는 핵심이라고 설명합니다.

주의할 점:

Streaming이 model의 실제 prefill 계산을 없애지는 않습니다.

Prompt 전체를 읽고 첫 token을 계산하기까지의 시간은 그대로 필요합니다. Streaming의 효과는 **첫 token이 준비된 뒤 전체 completion까지 기다리지 않고 즉시 전달한다**는 데 있습니다.

## 5. SSE란?

원문은 browser로 token을 보내는 대표 기술로 SSE(Server-Sent Events)를 설명합니다.

SSE는 하나의 HTTP connection을 열어 둔 상태에서 server가 client로 여러 event를 계속 보냅니다.

일반 request-response:

    browser  → request      → server
    browser  ← one response ← server
    connection closes

SSE:

    browser  → request  → server
    browser  ← piece 1  ← server
    browser  ← piece 2  ← server
    browser  ← piece 3  ← server
    connection remains open

## 6. HTTP Connection을 열어 두기

SSE response는 다음 Content-Type을 사용합니다.

    Content-Type: text/event-stream

Browser/client는 이를 보고 response가 하나의 완성된 body로 끝나는 것이 아니라 지속적으로 들어오는 event stream임을 알 수 있습니다.

Server는 각 piece를 보낸 뒤 connection을 닫지 않고 다음 piece를 계속 보냅니다.

## 7. SSE Message Format

원문의 단순 예:

    data: The

    data: cat

    data: sat

각 event는 data:로 시작하고 빈 줄로 event 경계를 구분합니다.

실제 LLM API에서는 text만 보내기보다 JSON payload, event type, tool-call delta, usage metadata 등을 함께 보낼 수 있습니다.

## 8. Server에서 Screen까지 전체 Walkthrough

원문의 순서:

1. Browser가 질문을 HTTP request로 server에 보냄
2. Server가 text/event-stream으로 response 시작
3. Model이 첫 token The를 생성
4. Server가 data: The event를 즉시 전송
5. Browser가 화면에 The를 append
6. Model이 cat을 생성
7. Server가 data: cat 전송
8. Browser가 The cat으로 append
9. 같은 과정을 종료까지 반복

도식:

    MODEL          SERVER              BROWSER
    The      →     data: The      →   The
    cat      →     data: cat      →   The cat
    sat      →     data: sat      →   The cat sat

## 9. 종료 Marker

원문은 다음 application-level marker를 예로 듭니다.

    data: sat

    data: [DONE]

Client는 [DONE]을 읽으면 stream이 끝났다고 판단합니다.

중요한 점은 [DONE]이 SSE 표준 자체의 필수 규칙은 아니라는 것입니다. 실제 API의 종료 event는 provider protocol을 따라야 합니다.

## 10. SSE vs WebSocket

원문의 비교:

| 항목 | SSE | WebSocket |
| --- | --- | --- |
| 방향 | server → client | 양방향 |
| 기반 | HTTP streaming | WebSocket protocol |
| 설정 | 비교적 단순 | 양방향 session 관리 필요 |
| 적합한 예 | streamed reply, live update | game, chat room, collaboration |
| reconnect | EventSource는 자동 재연결 지원 | 보통 애플리케이션 정책 필요 |

LLM 답변은 client가 질문을 한번 보내고 그 뒤 server가 연속 결과를 보내는 패턴이므로 SSE가 자연스럽습니다.

## 11. Token과 Network Event는 항상 1:1이 아니다

교육용 예에서는 token 하나마다 data event 하나를 보냅니다.

Production에서는 다음 이유로 1:1이 아닐 수 있습니다.

- 여러 token을 한 network chunk로 묶음
- UTF-8 text 경계와 model token 경계가 다름
- tool-call delta나 metadata를 별도 event로 전송
- server buffering/flush 정책

따라서 client는 model token 개수보다 **API가 정의한 stream event schema**를 기준으로 구현해야 합니다.

## 12. Production에서 추가로 볼 문제

- 사용자가 중단했을 때 generation cancel
- load balancer/proxy idle timeout
- 느린 client와 backpressure
- partial response 저장 여부
- retry 시 중복 event 처리
- connection 종료/오류 event

Streaming은 단순 UI 효과가 아니라 end-to-end serving 설계입니다.

## 13. 실제 활용

원문이 예로 드는 시스템:

- chat assistant
- coding assistant
- writing tool
- customer-support bot

사용자는 전체 답이 완성되기 전에 읽기 시작할 수 있어 체감 속도가 크게 개선됩니다.

## 핵심 정리

- Autoregressive LLM은 token을 순차 생성하므로 streaming과 자연스럽게 결합됩니다.
- Streaming은 전체 completion을 기다리지 않고 생성 중간 결과를 즉시 전송합니다.
- SSE는 text/event-stream HTTP connection을 유지하며 server→client event를 보냅니다.
- 원문은 data: event와 [DONE] 종료 marker를 예로 듭니다.
- SSE는 단방향 server push, WebSocket은 양방향 realtime 통신에 적합합니다.
- Streaming은 모델 계산 시간을 없애지 않지만 perceived latency를 줄입니다.

## 원문

- https://outcomeschool.com/blog/how-does-token-streaming-work
