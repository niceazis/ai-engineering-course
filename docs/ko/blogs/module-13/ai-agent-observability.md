# AI Agent Observability란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/ai-agent-observability  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 Logs·Metrics·Traces 세 pillar, Session→Trace→Span hierarchy, flight-agent 7-span 예와 핵심 metric을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Observability란?

Monitoring은 미리 정의한 metric을 보는 데 가깝고, Observability는 **외부에서 기록한 telemetry로 내부 system 상태와 failure 원인을 이해할 수 있게 만드는 것**입니다.

Agent는 여러 LLM/tool step을 수행하므로 final error 하나만 보면 원인을 찾기 어렵습니다.

## 2. 전통 Observability와 Agent Observability

전통 service:

- HTTP request
- DB query
- CPU/memory
- error code

Agent:

- model input/output
- prompt/version
- tool call/arguments
- retrieved evidence
- token usage
- model/provider
- retry/branch
- final task result

Semantic trace가 더 중요합니다.

## 3. 세 Pillar

원문:

### Logs

이벤트의 text/structured record.

예:

    flight search tool called

### Metrics

시간에 따른 숫자.

예:

- token
- cost
- latency
- error rate

### Traces

한 request의 전체 execution path.

Agent에서는 trace가 특히 중요합니다.

## 4. Span과 Trace

Span:

    하나의 operation

Trace:

    한 task/run을 구성하는 여러 span의 tree

원문 flight booking trace는 7개 step으로 설명합니다.

1. user request
2. planning/model decision
3. flight search tool
4. search result read
5. cheapest flight selection
6. booking tool
7. final confirmation

각 span에:

- input
- output
- duration
- error

를 기록합니다.

## 5. Session Hierarchy

원문 구조:

    Session
      ├─ Trace 1
      │   ├─ Span
      │   └─ Span
      └─ Trace 2
          ├─ Span
          └─ Span

Long chat은 여러 request trace를 하나의 session으로 묶을 수 있습니다.

## 6. 무엇을 Observe할까

### LLM span

- model/version
- prompt template version
- input/output tokens
- latency
- cost
- structured output validity

### Tool span

- tool name
- args
- response/error
- latency

### Retrieval span

- query
- top-k IDs/scores
- filters
- reranker result

### Workflow span

- current state
- branch
- retry
- completion reason

## 7. 원문의 핵심 Metric

- Latency
- Token Usage
- Cost
- Number of Steps
- Tool Call Success Rate
- Error Rate
- Task Success Rate

Number of Steps가 갑자기 늘면 loop/wandering의 early signal일 수 있습니다.

## 8. Instrumentation Flow

원문:

1. Instrumentation
2. Data collection
3. Store/connect spans into traces
4. Dashboard visualization
5. Alerting

즉:

    Agent
      → traces/spans/metrics
      → observability backend
      → dashboard + alerts

## 9. OpenTelemetry

원문은 OpenTelemetry를 공통 telemetry standard로 소개합니다.

GenAI semantic convention을 사용하면 model name, token usage 등 AI-specific field를 공통 형태로 기록할 수 있습니다.

지원 상태는 도구/version에 따라 확인해야 합니다.

## 10. Observability vs Evaluation

Observability:

    무엇이 일어났는가?
    어디서 느렸는가?
    어떤 tool이 실패했는가?

Evaluation:

    결과/과정이 좋은가?
    success 기준을 충족했는가?

Observability data는 evaluation의 입력이 될 수 있습니다.

## 11. Privacy와 보안

Prompt/tool result에는 민감 정보가 들어갈 수 있습니다.

따라서:

- PII redaction
- secret filtering
- access control
- retention policy

가 필요합니다.

"모든 것을 logging"하는 것이 항상 옳지는 않습니다.

## 12. Production Alert

예:

    p95 latency ↑
    cost/task 2×
    tool error rate ↑
    average steps ↑
    task success ↓

를 기준으로 alert할 수 있습니다.

Quality metric과 infra metric을 연결해 봐야 합니다.

## 핵심 정리

- Agent Observability는 Logs·Metrics·Traces로 내부 실행을 이해하게 합니다.
- Trace는 한 run, Span은 한 operation이며 Session은 여러 trace를 묶을 수 있습니다.
- Agent에서는 tool/LLM/retrieval/state transition을 모두 instrument해야 합니다.
- Task Success, Steps, Cost, Latency, Tool Success가 핵심 metric입니다.
- Observability는 원인 분석, Evaluation은 quality 판정이라는 역할 차이가 있습니다.

## 원문

- https://outcomeschool.com/blog/ai-agent-observability
