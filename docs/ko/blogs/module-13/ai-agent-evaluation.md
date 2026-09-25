# AI Agent를 어떻게 평가할까? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/ai-agent-evaluation  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-05-23 공개 원문을 직접 확인해 Outcome·Trajectory·Tool Use·Planning Evaluation의 네 유형과 flight/weather 예제를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Agent Evaluation이 LLM Evaluation과 다른 이유

LLM output만 보면:

    prompt → answer

Agent는:

    goal
      → plan
      → tool calls
      → observations
      → retries
      → final result

를 거칩니다.

Final answer만 맞아도 잘못된 tool을 수십 번 호출했거나 위험한 경로를 탔을 수 있습니다.

따라서 **결과와 과정 모두** 평가해야 합니다.

## 2. 네 가지 유형

원문:

1. Outcome Evaluation
2. Trajectory Evaluation
3. Tool Use Evaluation
4. Planning Evaluation

실전에서는 조합합니다.

## 3. Outcome Evaluation

최종 goal이 달성됐는지 봅니다.

원문 flight example:

    "금요일 Delhi→Bangalore 가장 싼 비행기를 예약"

핵심 metric:

- Task Success Rate
- Final Answer Accuracy
- Goal Completion

장점:

- user value와 직접 연결

한계:

- 왜 실패했는지 모름
- 우연히 맞은 trajectory를 구분 못함
- cost/steps 낭비를 놓침

## 4. Trajectory Evaluation

전체 action path를 봅니다.

원문 weather 예:

1. Bangalore tomorrow weather tool call
2. rain chance 70% 확인
3. umbrella recommendation
4. answer

Tool을 호출하지 않고 우연히 "우산 가져가라"라고 답했다면 outcome은 맞아도 trajectory는 잘못됐습니다.

## 5. Trajectory Match

원문 방식:

### Exact Match

Expected sequence와 완전히 같아야 함.

### In-Order Match

Required steps가 올바른 순서에 있되 extra step 허용.

### Any-Order Match

필수 step이 모두 있으면 순서 무관.

### Precision

Agent가 한 step 중 useful step 비율.

### Recall

필요한 step 중 실제 수행한 비율.

한 개의 canonical trajectory를 강제하면 valid alternative를 잘못 penalize할 수 있습니다.

## 6. Tool Use Evaluation

원문이 보는 항목:

- Tool Selection
- Argument Correctness
- Tool Call Success
- Result Handling
- No Hallucinated Tools

예:

    search_flights
      → book_flight
      → send_email

이어야 하는데 book_flight를 먼저 호출하거나 존재하지 않는 cancel_flight를 만들면 실패입니다.

Tool call은 structured data라 자동 평가하기 좋습니다.

## 7. Planning Evaluation

원문 trip plan 예:

1. flight search
2. schedule에 맞는 최저가 선택
3. hotel search
4. budget 내 best-rated hotel
5. itinerary 전송

평가:

- Completeness
- Correctness/order
- Feasibility
- Efficiency

Plan-first agent에 특히 유용합니다.

## 8. 주요 Metric

Agent evaluation에서 함께 볼 것:

- task success
- steps/task
- tool-call success
- argument accuracy
- unnecessary-tool rate
- cost/task
- latency/task
- retry count
- safety violation
- human-escalation correctness

단순 성공률만 높고 비용이 10배이면 production에서는 나쁜 agent일 수 있습니다.

## 9. Benchmark

Task에 따라:

- SWE-bench Verified: coding
- τ-bench: customer-service agent
- GAIA: general assistant
- WebArena: browser agent
- BFCL: function calling

등을 사용할 수 있습니다.

Public benchmark는 model 비교용이고, 실제 제품에는 custom scenario가 더 중요합니다.

## 10. Evaluation Dataset

각 case에:

    initial state
    user goal
    available tools
    ground-truth outcome
    required/forbidden actions
    budget

을 저장하면 재현 가능한 agent regression test가 됩니다.

## 11. Simulator

실제 결제/email 같은 side effect를 매 eval마다 실행할 수 없으므로 mock/sandbox environment를 만듭니다.

Agent가 실제 production과 비슷한 feedback을 받아야 합니다.

## 12. Evaluation과 Observability 연결

Trajectory eval을 하려면 실제 agent step이 capture돼야 합니다.

그래서:

    Observability
      → trace data

    Evaluation
      → trace를 score

관계입니다.

## 핵심 정리

- Agent 평가는 final answer뿐 아니라 trajectory, tool use, plan을 봐야 합니다.
- 원문은 Outcome·Trajectory·Tool Use·Planning 네 축을 제시합니다.
- Trajectory는 exact/in-order/any-order와 step precision/recall로 평가할 수 있습니다.
- Tool call은 structured라 automation하기 좋은 평가 대상입니다.
- Production에서는 success뿐 아니라 steps, cost, latency, safety를 함께 평가해야 합니다.

## 원문

- https://outcomeschool.com/blog/ai-agent-evaluation
