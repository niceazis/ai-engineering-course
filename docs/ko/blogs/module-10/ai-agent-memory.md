# AI Agent Memory는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/ai-agent-memory  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 memory stack과 Write·Read·Update·Forget 네 연산을 중심으로 독립적으로 정리했습니다.

## 1. 왜 Memory가 필요한가

LLM API call은 기본적으로 stateless합니다.

Agent가 장기 task를 수행하려면:

- 무엇을 이미 했는지
- user preference
- 중요한 decision
- tool 결과
- 진행 상태

를 외부에 보존해야 합니다.

## 2. Memory Stack

실용적으로 세 층으로 나눌 수 있습니다.

### Working / Short-Term

현재 run의 conversation, tool trace, active plan.

### Episodic

과거 session에서 있었던 사건/결과.

### Semantic / Profile

장기적으로 유효한 user/project facts.

모든 것을 한 저장소에 넣기보다 lifespan과 retrieval 방식에 따라 분리하는 것이 좋습니다.

## 3. 네 핵심 Operation

### Write

무엇을 memory에 저장할지 결정.

### Read

현재 task에 relevant한 memory를 검색.

### Update

기존 fact가 바뀌었을 때 최신 상태로 수정.

### Forget

오래되거나 잘못되거나 더 이상 필요하지 않은 memory를 제거.

저장만 하고 갱신/삭제가 없으면 stale context가 누적됩니다.

## 4. Write Policy

저장 가치가 높은 것:

- explicit preference
- durable project constraint
- confirmed decision
- recurring workflow state

저장하면 안 되는 것:

- transient tool noise
- unverified inference
- 쉽게 재계산 가능한 중간 token
- sensitive information without need/permission

## 5. Read Policy

모든 memory를 context에 넣으면 context stuffing이 됩니다.

    current task
      → retrieve relevant memory
      → freshness/permission filter
      → context

Relevance뿐 아니라 access scope와 timestamp를 봐야 합니다.

## 6. Update와 Conflict

같은 field가 바뀌면 append-only로 둘 경우 모순이 생깁니다.

예:

    preferred_city = Seoul
    later = Busan

Memory system은 version/current-state semantics가 필요합니다.

## 7. Forgetting

Forget은 storage 최적화만이 아닙니다.

- stale info 제거
- privacy request
- outdated constraint
- noise suppression

에 필요합니다.

## 8. Vector Memory

Free-form episode를 embedding해 semantic search할 수 있습니다.

하지만 exact state:

    account_id
    selected_plan
    deadline

같은 것은 structured DB가 더 안전합니다.

Vector DB 하나로 모든 memory를 처리할 필요는 없습니다.

## 9. Runtime Flow

    observe event
      → memory write decision
      → store

    new task
      → memory query
      → retrieve
      → filter
      → context
      → agent decision

Task 끝에는 summary/state consolidation을 할 수 있습니다.

## 10. Context Compaction과 차이

Compaction:

    현재 session의 긴 context 압축

Long-term memory:

    session을 넘어 필요한 state 유지

둘을 같이 쓰지만 목적은 다릅니다.

## 11. Failure Mode

- every-message memory → noise
- stale fact → wrong action
- unverified inference 저장 → 오류 고착
- cross-user memory leak
- duplicate/conflicting memory

따라서 provenance와 user/tenant isolation이 중요합니다.

## 핵심 정리

- Agent memory는 model parameter가 아니라 외부 runtime state입니다.
- Working/episodic/semantic layer로 나눌 수 있습니다.
- Write, Read, Update, Forget 네 연산을 모두 설계해야 합니다.
- Free-form 기억은 vector search, exact state는 structured store가 적합합니다.
- Relevance·freshness·permission filter 없이 memory를 context에 넣으면 오히려 agent 품질이 나빠집니다.

## 원문

- https://outcomeschool.com/blog/ai-agent-memory
