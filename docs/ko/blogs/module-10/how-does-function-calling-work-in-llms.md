# LLM의 Function Calling은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-function-calling-work-in-llms  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 function schema, weather 예제와 conversation loop를 독립적으로 재구성했습니다.

## 1. Function Calling의 핵심

Function Calling은 LLM이 외부 함수를 **직접 실행하는 기능이 아니라 어떤 함수를 어떤 인자로 호출할지 구조화해서 선택하는 기능**입니다.

    user
      → LLM
      → {tool:"get_weather", arguments:{city:"Seoul"}}
      → application runtime
      → actual API/function
      → result
      → LLM

## 2. Tool Schema

Tool 정의에는 보통:

    name
    description
    input schema

가 있습니다.

Description이 모호하면 model이 wrong tool을 선택할 수 있으므로 semantic contract가 중요합니다.

## 3. Weather 예

User:

    서울 오늘 날씨 알려줘

LLM은 현재 날씨를 parameter 안에서 알 수 없으므로:

    get_weather(city="Seoul")

를 선택합니다.

Host가 API를 실행하고:

    {"temp":25,"condition":"rain"}

같은 result를 tool message로 되돌립니다.

그 뒤 LLM이 자연어 answer를 생성합니다.

## 4. 전체 Loop

1. User message + tool schemas → LLM
2. LLM이 text 또는 tool call 출력
3. Tool call이면 host가 argument validate
4. 실제 function 실행
5. Tool result를 conversation에 append
6. 다시 LLM call
7. 필요하면 추가 tool call
8. final text

Function calling 자체가 agent loop의 기본 building block입니다.

## 5. Structured Output과 차이

Structured Output/JSON mode:

    최종 response의 shape를 강제

Function Calling:

    외부 action을 선택하고 argument를 생성

둘 다 schema를 쓰지만 목적이 다릅니다.

## 6. Parallel Calls

서로 독립적이면:

    weather(Seoul)
    weather(Busan)
    weather(Jeju)

같은 tool call을 한 turn에 여러 개 낼 수 있습니다.

Runtime이 병렬 실행하면 latency를 줄일 수 있습니다.

## 7. Multi-Step Calls

Tool result에 따라 다음 tool이 달라지는 경우:

    search_customer
      → customer_id
      → get_orders(customer_id)
      → refund_order(order_id)

각 observation 뒤 다시 model 판단이 필요합니다.

## 8. Validation

LLM이 schema를 따르더라도 argument의 의미가 안전한지는 별도 문제입니다.

반드시 확인:

- schema/type
- permission
- business rule
- resource existence
- destructive action confirmation
- idempotency

Typed JSON은 권한 검증을 대신하지 않습니다.

## 9. Tool Error

Runtime은 error도 observation으로 반환할 수 있습니다.

    {"error":"timeout"}

Agent는 retry하거나 다른 tool을 선택할 수 있습니다.

Retry 횟수와 side effect 중복을 제어해야 합니다.

## 핵심 정리

- LLM은 function을 실행하지 않고 call intent와 arguments를 반환합니다.
- 실제 실행·권한·validation은 application runtime 책임입니다.
- Tool result를 다시 model에 넣어 conversation loop를 이어갑니다.
- Parallel call과 multi-step call이 agent workflow의 기반입니다.
- JSON/schema 준수와 실제 action safety는 별개입니다.

## 원문

- https://outcomeschool.com/blog/how-does-function-calling-work-in-llms
