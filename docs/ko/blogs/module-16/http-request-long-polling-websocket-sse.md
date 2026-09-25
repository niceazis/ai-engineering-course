# HTTP Request vs Polling vs Long-Polling vs WebSocket vs SSE — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/http-request-long-polling-websocket-sse  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2022-09-19 공개 원문을 직접 확인해 일반 HTTP, 1~2초 polling 예, long-poll timeout/reconnect, WebSocket full-duplex, SSE server-push와 WhatsApp/stock-price 예제를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 일반 HTTP Request

기본 흐름:

    client
      → request
      → server
      → response
      → connection 종료

Request-response가 명확한 작업에 적합합니다.

원문 예:

    Facebook profile 정보 가져오기

실시간 지속 update에는 비효율적일 수 있습니다.

## 2. HTTP Polling

Client가 정해진 간격으로 계속 request를 보냅니다.

원문 예:

    every 1~2 seconds
      → "새 데이터 있어?"

문제:

- update가 없는데도 request 발생
- battery/network 낭비
- poll interval만큼 delay 가능

## 3. 원문의 WhatsApp Polling 예

2초마다 poll한다고 가정하면:

- message가 도착해도 최대 약 2초 기다릴 수 있음
- 대부분 request는 empty response일 수 있음

Chat에는 좋지 않습니다.

반면 delivery location처럼 2초 정도 delay가 허용된다면 단순 polling도 사용할 수 있습니다.

## 4. HTTP Long Polling

Client가 request를 보내고 server가 바로 empty response를 주지 않습니다.

    client request
      → server holds connection
      → new event 발생
      → response
      → connection close
      → client immediately reconnect

Timeout이 발생해도 다시 연결합니다.

## 5. Long Polling 장점

일반 polling보다:

- empty response 감소
- event 발생 즉시 전달 가능

합니다.

단점:

- response마다 reconnect
- connection 관리 비용
- bidirectional real-time에는 덜 자연스러움

## 6. WebSocket

원문 설명:

> 하나의 TCP connection 위에서 client와 server가 양방향 full-duplex message를 지속적으로 주고받습니다.

초기 handshake 후 connection을 유지합니다.

    client ⇄ server

양쪽 모두 언제든 message를 보낼 수 있습니다.

## 7. WebSocket이 Chat에 잘 맞는 이유

Chat은:

- client → server message
- server → client new message

둘 다 빈번합니다.

원문은 WhatsApp chat use case에서 WebSocket을 좋은 해결책으로 설명합니다.

한 번 연결 후 지속적으로 양방향 communication이 가능하기 때문입니다.

## 8. WebSocket 장점

- bidirectional
- low overhead after handshake
- low-latency event delivery
- persistent connection

단점:

- connection state 관리
- proxy/load balancer 설정
- reconnect
- horizontal scaling 시 connection routing

이 필요합니다.

## 9. Server-Sent Events

SSE는 server에서 client로 **단방향 stream**을 보내는 방식입니다.

    client
      → HTTP connection
      ← event stream from server

Client가 server에 보내는 일반 data는 별도 HTTP request를 사용합니다.

## 10. SSE가 잘 맞는 경우

원문 예:

    real-time stock price

Server가 계속 update를 보내고 client는 그 channel에서 별로 보낼 것이 없다면 SSE가 단순합니다.

또:

- LLM token streaming
- monitoring event
- notification feed

에도 잘 맞습니다.

## 11. SSE vs WebSocket

| 항목 | SSE | WebSocket |
| --- | --- | --- |
| 방향 | server → client | 양방향 |
| Protocol | HTTP 기반 | WebSocket protocol |
| Text event | 강함 | binary/text 모두 |
| Reconnect | browser API 지원 | 직접 처리 필요 가능 |
| Chat | 제한적 | 적합 |
| Token stream | 적합 | 가능 |

## 12. 선택 기준

### Plain HTTP

단발성 CRUD/request-response.

### Polling

update 빈도가 낮고 간단함이 중요.

### Long Polling

Legacy/browser compatibility 상황의 pseudo real-time.

### SSE

server→client streaming이 중심.

### WebSocket

양방향 low-latency communication.

## 13. AI System에서의 예

### LLM Streaming

보통 SSE/HTTP streaming으로 충분합니다.

### Voice AI / Multiplayer Tool

지속적인 bidirectional data가 필요하면 WebSocket/WebRTC 계열이 더 적합할 수 있습니다.

### Background Status

Job progress update는 SSE나 polling으로 충분할 수 있습니다.

## 핵심 정리

- Polling은 주기적으로 묻고, Long Polling은 event가 생길 때까지 request를 열어 둡니다.
- 원문 polling 예는 1~2초 간격과 empty-response/battery 문제를 설명합니다.
- WebSocket은 persistent full-duplex channel이라 chat에 적합합니다.
- SSE는 server→client 단방향 event stream이라 stock price나 LLM token streaming에 적합합니다.
- 실시간이라는 이유만으로 항상 WebSocket을 선택하지 말고 communication 방향과 운영 복잡도로 결정해야 합니다.

## 원문

- https://outcomeschool.com/blog/http-request-long-polling-websocket-sse
