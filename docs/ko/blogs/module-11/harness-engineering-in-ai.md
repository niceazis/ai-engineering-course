# Harness Engineering이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/harness-engineering-in-ai  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-04-02 공개 원문을 직접 확인해 harness 구성 요소, agent/evaluation harness와 best practice를 반영한 독립적인 한국어 해설입니다.

## 1. Harness의 정의

AI model이 engine이라면 Harness는 model 주변의 **production control layer**입니다.

원문의 핵심:

    model alone
      + prompt/context management
      + tools
      + memory
      + validation
      + guardrails
      + error handling
      + evaluation
      + monitoring
      = usable AI system

Model 자체는 input→output만 수행합니다. 실제 제품의 신뢰성은 주변 code가 좌우합니다.

## 2. 주요 구성 요소

### Prompt / Context Management

System instruction, examples, memory, retrieved evidence를 조립합니다.

### Tool Orchestration

어떤 tool이 model에 보이고, call을 실제로 어떻게 실행/검증할지 관리합니다.

### Memory Management

무엇을 유지/압축/삭제할지 결정합니다.

### Input / Output Processing

Schema parsing, formatting, validation, filtering.

### Error Handling

API/tool failure, malformed output, timeout에 retry/fallback.

### Guardrails

권한, safety, privacy, destructive action control.

## 3. Agent Harness

Agent에서는 loop 전체가 harness 책임입니다.

    user goal
      → build context
      → model
      → tool call?
        yes → harness executes
             → observation
             → model again
        no  → final

중요한 구분:

> model은 tool 사용을 결정하지만 실제 action을 실행하는 것은 harness입니다.

## 4. 원문의 Weather+Email 예

Goal:

    Delhi 날씨를 찾아 email로 보내라

Flow:

1. model이 weather tool 선택
2. harness가 실행 → 32°C Sunny
3. result를 model에 전달
4. model이 email tool 선택
5. harness가 실제 send
6. final result

Permission/side-effect 제어는 harness에 있습니다.

## 5. Evaluation Harness

Model 변경을 수동 감으로 평가하지 않고 동일 dataset/test를 반복 실행합니다.

    dataset
      → model/system
      → outputs
      → rule/judge
      → metrics

Agent는 final answer뿐 아니라:

- plan
- tool calls
- trajectory
- cost/latency

를 평가해야 합니다.

## 6. 왜 Model Benchmark만 부족한가

같은 model이라도:

- tool description
- retrieval
- memory
- retry
- context order

가 다르면 실제 task success가 크게 달라집니다.

따라서 system-level eval이 필요합니다.

## 7. Best Practice

원문 핵심:

- modular harness
- 모든 input/output/tool/error logging
- guardrail from day one
- reliable tools + fallback
- harness 자체도 test
- production latency/error/cost/quality monitoring

## 8. Harness와 Agent Skill

긴 procedure를 항상 system prompt에 넣지 않고 Skill로 분리해 필요한 때만 load할 수 있습니다.

Harness가 skill routing/loading을 담당합니다.

## 핵심 정리

- Harness는 model 주변의 control/runtime layer입니다.
- Prompt, tools, memory, errors, validation, guardrails, evaluation을 관리합니다.
- Agent에서 model은 결정하고 harness가 실제 action과 loop를 실행합니다.
- 좋은 model + 나쁜 harness는 나쁜 product가 될 수 있습니다.
- Production AI는 model eval이 아니라 harness 포함 end-to-end system eval이 필요합니다.

## 원문

- https://outcomeschool.com/blog/harness-engineering-in-ai
