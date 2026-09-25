# LangChain은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-langchain-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 Prompt, Chain, Parser, Memory, Retrieval, Tool/Agent 구성 요소를 현재 개념 수준에서 독립적으로 설명합니다. LangChain API는 빠르게 바뀌므로 실제 코드 작성 시 공식 최신 문서를 확인해야 합니다.

## 1. LangChain이 해결하는 문제

LLM application은 단순 API call보다 많은 조립이 필요합니다.

    prompt
    model
    parser
    retrieval
    tools
    memory/history
    control flow

LangChain은 이런 component를 공통 abstraction으로 연결하는 application framework입니다.

## 2. Model

Provider별 API 차이를 감싼 model interface를 사용합니다.

실제 system에서는 model capability, tool calling, structured output, streaming support를 확인해야 합니다.

## 3. Prompt Template

Dynamic variable을 넣어 reusable prompt를 만듭니다.

    template:
      "다음 문서를 {language}로 요약: {text}"

Application state와 prompt construction을 분리합니다.

## 4. Chain

여러 runnable/component를 순서대로 연결합니다.

    prompt
      → model
      → parser

또는:

    retriever
      → context builder
      → prompt
      → model

과 같은 pipeline입니다.

## 5. Output Parser

LLM text를 application이 사용할 structure로 변환합니다.

현대 model의 native structured output이 가능한 경우 parser 부담을 줄일 수 있습니다.

그래도 schema validation은 필요합니다.

## 6. Memory라는 표현의 주의점

과거 LangChain API에서는 Memory component라는 이름이 많이 쓰였지만, 현재 agent framework에서는 message/state persistence가 LangGraph/checkpointer 쪽으로 이동한 부분이 있습니다.

개념적으로 중요한 것은:

> model 자체가 stateful한 것이 아니라 application이 history/state를 저장하고 다음 call에 주입한다.

는 점입니다.

## 7. Retrieval/RAG

    documents
      → vector store

    query
      → retriever
      → documents
      → prompt
      → LLM

LangChain은 retriever interface로 다양한 vector/search backend를 연결합니다.

## 8. Tools

Tool은:

    name
    description
    input schema
    executable function

의 contract로 model/agent에 제공됩니다.

Tool description과 validation이 agent behavior에 큰 영향을 줍니다.

## 9. Agent

Agent는 fixed chain이 아니라 model이 next tool/action을 선택하는 loop입니다.

LangChain ecosystem에서는 더 복잡하고 stateful한 agent control flow에 LangGraph를 함께 사용하는 방향이 중요합니다.

## 10. LCEL / Composable Pipeline

LangChain의 핵심 철학 중 하나는 작은 runnable을 조합하는 것입니다.

장점:

- streaming
- batch
- tracing
- replaceable components

를 공통 interface에서 다루기 쉽습니다.

## 11. 언제 쓰나

유용:

- 여러 provider/tool/retriever를 빠르게 조립
- tracing/eval ecosystem 활용
- framework abstraction이 팀 생산성을 높임

불필요:

- model call 1~2개뿐인 작은 service
- framework abstraction보다 직접 SDK가 단순한 경우

## 12. Framework Risk

- API churn
- hidden abstraction cost
- debugging stack 복잡
- provider-specific feature lag

따라서 core business logic을 framework object에 과도하게 결합하지 않는 것이 좋습니다.

## 핵심 정리

- LangChain은 LLM application component를 조립하는 framework입니다.
- Prompt, model, parser, retriever, tools, agent abstraction이 핵심입니다.
- Model state는 framework/runtime가 관리하지 model 자체가 영구 기억하는 것이 아닙니다.
- 복잡한 stateful workflow는 LangGraph와 연결됩니다.
- 실제 API는 빠르게 바뀌므로 최신 공식 문서 기준으로 구현해야 합니다.

## 원문

- https://outcomeschool.com/blog/how-does-langchain-work
