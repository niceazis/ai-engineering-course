# AI Engineering Explained — Agent 중심 한국어 상세 영상 학습 노트

> 영상: https://www.youtube.com/watch?v=lnfWvX66FUk  
> 제공: Outcome School / Amit Shekhar  
> 검증 범위: 영상 제목과 Outcome School 공식 소개는 확인했습니다. **YouTube 자막 전문은 직접 검증하지 못했습니다.** 아래 내용은 영상의 Agent/MCP 주제를 Module 10의 Outcome School 공식 블로그들과 연결해 만든 상세 보조 노트이며 자막의 문장별 번역이 아닙니다.

## 1. AI Engineering에서 Agent의 위치

영상이 다루는 큰 구성:

    LLM
    RAG
    MCP
    Agent
    Fine-tuning
    Quantization

Agent는 이 중 다른 요소를 **목표 지향적으로 연결하는 runtime layer**로 볼 수 있습니다.

## 2. LLM과 Agent의 차이

LLM:

    prompt → response

Agent:

    goal
      → decide
      → tool
      → observation
      → decide again
      → final

즉 model 자체보다 surrounding loop와 tools가 중요합니다.

## 3. RAG와 Agent

RAG는 retrieval capability입니다.

Agent는:

- retrieval 필요 여부
- 어떤 source
- query rewrite
- 다시 검색할지

를 결정할 수 있습니다.

그래서 Agentic RAG가 됩니다.

## 4. MCP와 Agent

MCP는 agent가 외부 tool/data provider를 표준 방식으로 발견하고 호출하게 돕는 protocol입니다.

    Agent runtime
      → MCP client
      → MCP server
      → tool/data

Agent logic과 MCP protocol은 역할이 다릅니다.

## 5. Fine-Tuning과 Agent

Agent behavior가 불안정할 때 항상 fine-tuning부터 할 필요는 없습니다.

먼저:

- tool schema
- instructions
- context
- validators
- state machine

을 개선해야 합니다.

Fine-tuning은 반복적인 behavior pattern 자체를 weight에 학습할 가치가 있을 때 고려합니다.

## 6. Quantization과 Agent

Agent는 한 task에 model을 여러 번 호출할 수 있습니다.

따라서 model serving cost가 전체 workflow cost에 곱해집니다.

Small/quantized model을 routing·classification step에 쓰고 hard reasoning만 큰 model로 보내는 orchestration이 중요합니다.

## 7. Production Agent Checklist

- tool permission
- max steps
- timeout
- retry/idempotency
- context compaction
- persistent state
- approval boundary
- tool result validation
- trace/evaluation
- cost budget

Agent의 품질은 model benchmark 하나로 평가할 수 없습니다.

## 핵심 정리

- Agent는 LLM을 tools·memory·loop와 결합한 goal-oriented system입니다.
- RAG는 knowledge retrieval, MCP는 capability connection, Agent는 next-action decision과 orchestration을 담당합니다.
- Agent loop가 길수록 latency/cost와 failure surface가 증가합니다.
- Deterministic workflow는 code에 남기고 semantic decision이 필요한 부분만 model에 맡기는 것이 안정적입니다.
- 이 노트는 영상 자막 직역이 아니라 공식 영상 주제와 Module 10 공식 자료를 연결한 학습 노트입니다.
