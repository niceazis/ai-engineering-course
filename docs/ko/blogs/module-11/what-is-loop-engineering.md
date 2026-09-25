# Loop Engineering이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/what-is-loop-engineering  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 원문 본문 캐시를 직접 열지 못했습니다. Outcome School 공식 Module 11 레슨 구조와 Agent Loop/Harness Engineering의 공개 개념을 기준으로 독립적으로 설명하며, 원문 고유 수치를 임의로 만들지 않습니다.

## 1. Loop Engineering의 정의

Loop Engineering은 agent가:

    observe → decide → act → verify → repeat

를 수행하는 반복 구조를 **안전하고 종료 가능하며 평가 가능하게 설계하는 일**입니다.

단순 while loop를 만드는 것이 아니라 iteration policy를 engineering합니다.

## 2. 가장 단순한 Loop

    while not done:
        response = llm(state)
        action = parse(response)
        result = tool(action)
        state += result

이 구조만으로는:

- infinite loop
- same action repetition
- context explosion
- cost runaway
- false completion

문제가 생깁니다.

## 3. 설계해야 할 요소

### State

현재 goal, plan, observations, open tasks를 구조화.

### Action Space

허용 tool과 argument schema.

### Completion

무엇을 만족하면 done인지 명시.

### Budget

max steps, tokens, time, money.

### Validation

tool result와 intermediate artifact 검증.

### Recovery

retry/fallback/replan.

## 4. Prompt/Context/Loop Engineering 차이

Prompt Engineering:

    한 call에 무엇을 말할지

Context Engineering:

    model이 무엇을 보게 할지

Loop Engineering:

    **언제 model을 다시 부르고, 결과에 따라 control flow를 어떻게 바꿀지**

를 설계합니다.

## 5. Completion을 Model에게만 맡기지 않는다

나쁜 종료:

    "됐다고 생각하면 끝내"

좋은 종료:

    all tests pass
    AND required files exist
    AND no unresolved checklist
    AND max risk actions approved

Definition of Done과 직접 연결됩니다.

## 6. Duplicate Detection

Agent가 동일한 search/tool call을 반복하는지 hash/signature로 기록할 수 있습니다.

    action_signature
      = tool + normalized_args

같은 실패 action이 반복되면 replan/escalate합니다.

## 7. Retry와 Replan

Transient error:

    timeout → retry

Semantic error:

    no result → query rewrite/replan

Permission error:

    escalate/user action

Error 종류를 구분하지 않은 blind retry는 loop를 악화시킵니다.

## 8. Context Growth

모든 observation을 raw append하면 loop가 길수록 품질/비용이 나빠집니다.

대응:

- structured state
- old trace compaction
- artifact reference
- relevant-only retrieval

## 9. Human-in-the-Loop

High-risk action 전:

    proposed action
      → approval
      → execute

Loop state에 WAITING_APPROVAL 같은 explicit state를 둡니다.

## 10. 잘 맞는 영역

- coding repair/test loop
- research until evidence sufficient
- data cleaning/validation
- iterative generation with checker

불명확한 subjective task는 종료 기준을 만들기 어려워 loop가 wandering하기 쉽습니다.

## 핵심 정리

- Loop Engineering은 반복 자체가 아니라 state·action·validation·termination·budget을 설계하는 일입니다.
- max step만으로 충분하지 않고 완료 조건과 duplicate/recovery policy가 필요합니다.
- Context compaction과 structured state가 long-running loop의 핵심입니다.
- Deterministic validator를 가능한 많이 사용해야 합니다.
- 원문 본문을 직접 확인하지 못한 부분은 Module 11 공식 outline과 일반 agent-engineering 원리로만 보완했습니다.

## 원문

- https://outcomeschool.com/blog/what-is-loop-engineering
