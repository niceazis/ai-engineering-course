# Context Engineering이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/context-engineering  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문을 직접 확인해 Prompt Engineering과의 범위 차이, 8개 context 구성 요소, RAG·Few-shot·Tool·Memory·History 관리 pattern을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Context Engineering의 정의

Context Engineering은 LLM 한 번의 call에 **어떤 정보를 넣고, 어떤 순서로, 어느 정도 길이로, 어떤 구조로 조립할지 설계하는 discipline**입니다.

Prompt Engineering이 한 instruction의 wording을 다듬는 문제라면, Context Engineering은 model이 보는 **전체 information environment**를 설계합니다.

## 2. Prompt Engineering과의 차이

원문 비교의 핵심:

| 관점 | Prompt Engineering | Context Engineering |
| --- | --- | --- |
| 범위 | 한 instruction | 전체 context window |
| 주요 요소 | wording, phrasing | system, examples, RAG, tools, memory, history, results |
| 적합 | simple one-shot | RAG, agent, multi-step production system |
| 실패 원인 | 표현이 애매 | 정보가 빠짐/오래됨/너무 많음/순서가 나쁨 |

즉 Prompt Engineering은 Context Engineering의 일부입니다.

## 3. Context Window에 들어가는 8가지

원문은 다음 8가지를 구분합니다.

1. System prompt
2. Few-shot examples
3. Retrieved documents(RAG)
4. Tools and tool descriptions
5. Memory
6. Conversation history
7. Tool results
8. Current user message

이 모든 것이 하나의 finite context budget을 경쟁합니다.

## 4. System Prompt

역할:

- role
- global rules
- safety constraints
- output format
- tool policy

좋은 system prompt는 짧기만 한 것이 아니라 conflict가 적고 priority가 명확해야 합니다.

매 request마다 거의 동일하므로 prompt caching과도 잘 맞습니다.

## 5. Few-Shot Example

Input-output example은 원하는 behavior를 말로 설명하는 대신 pattern을 보여 줍니다.

원문은 2~5개를 시작 범위 예로 듭니다.

선택 기준:

- 대표성
- edge case
- task distribution
- contradictory example 제거

Example이 너무 많으면 context를 차지하고 irrelevant pattern을 주입할 수 있습니다.

## 6. Retrieved Documents(RAG)

전체 knowledge base를 넣는 대신 query에 relevant한 chunk만 선택합니다.

Pipeline:

    query
      → retrieval
      → reranking
      → top relevant chunks
      → context

RAG의 핵심은 retrieval 자체보다 **최종 context에 어떤 evidence를 넣는가**입니다.

## 7. Tool Descriptions

Agent는 tool 이름만 아는 것이 아니라:

- description
- parameter schema
- constraints
- examples

를 context로 받습니다.

Tool description이 모호하면 잘못된 tool selection이나 argument hallucination이 생길 수 있습니다.

## 8. Memory

Memory는 session을 넘어 유지할 가치가 있는 state입니다.

예:

- user preference
- project facts
- persistent goals

모든 과거 대화를 memory로 넣는 것은 아닙니다.

Memory retrieval도 relevance/freshness policy가 필요합니다.

## 9. Conversation History

현재 session의 최근 turn입니다.

History가 길어지면:

- token cost
- lost in the middle
- stale instruction
- contradiction

문제가 생깁니다.

필요하면 summarize/compact해야 합니다.

## 10. Tool Results

Agent가 search/database/code tool을 실행한 결과가 다음 turn의 context가 됩니다.

중요한 원칙:

- raw output 전체를 무조건 넣지 않기
- relevant field만 normalize
- provenance 유지
- stale result 재사용 주의

## 11. Current User Message

가장 최근 request는 context의 목적을 결정하는 핵심 signal입니다.

Long prompt에서 user question이 evidence와 멀리 떨어져 있으면 attention/usefulness가 떨어질 수 있으므로 ordering을 설계해야 합니다.

## 12. Context는 매 Turn 다시 Assemble된다

원문이 강조하는 점:

> Context는 하나의 영구 blob이 아니라 매 LLM call 전에 여러 source에서 다시 조립된다.

개념:

    system store
    memory store
    RAG
    examples
    tools
    history
    current message
      ↓
    context assembler
      ↓
    LLM

이 assembler가 production AI system의 핵심 component입니다.

## 13. Pattern 1 — RAG

Knowledge base 전체 대신 top relevant evidence만 넣습니다.

좋은 RAG는:

- chunking
- embedding/search
- hybrid retrieval
- reranking
- source metadata

까지 포함합니다.

## 14. Pattern 2 — Few-Shot Selection

Fixed example만 쓰지 않고 task/query에 맞춰 dynamic example retrieval을 할 수 있습니다.

예:

    current issue = refund
      → refund-specific examples

Relevant example이 generic example보다 효과적일 수 있습니다.

## 15. Pattern 3 — Tool Calling

Tool schema를 context에 주고 model이 tool/action을 선택합니다.

하지만 deterministic rule로 선택 가능한 것은 code가 처리하는 편이 더 안정적입니다.

## 16. Pattern 4 — Memory Injection

모든 memory를 넣지 않고 current task에 relevant한 것만 검색합니다.

    memory store
      → relevance filter
      → fresh valid memory
      → context

Sensitive/stale memory를 무분별하게 주입하면 위험합니다.

## 17. Pattern 5 — History Management

전략:

- recent turns full
- old turns summarized
- important facts separately structured
- irrelevant turn drop

Context Compaction이 다음 레슨과 연결됩니다.

## 18. Pattern 6 — Structured Output Instruction

Context에는 input 정보뿐 아니라 desired output schema도 포함됩니다.

예:

    {
      "answer": "...",
      "sources": [...],
      "confidence": ...
    }

Schema validator를 code에 추가하면 generation reliability가 올라갑니다.

## 19. Pattern 7 — Per-Step Context for Agents

Agent step마다 필요한 context가 다릅니다.

예:

### Planning step

- goal
- constraints
- high-level state

### Tool-selection step

- relevant tools
- current state

### Verification step

- output
- evidence
- checker criteria

매 step에 모든 history/tool을 다 넣을 필요가 없습니다.

## 20. Common Mistake — Context Stuffing

"Context window가 크니 전부 넣자"는 방식은 실패하기 쉽습니다.

문제:

- higher prefill latency
- token cost
- attention dilution
- conflicting evidence
- lost-in-the-middle

Quality는 context quantity가 아니라 **relevance density**와 연결됩니다.

## 21. Common Mistake — 너무 적은 Context

반대로 필요한 policy/evidence를 빼면 model은 부족한 정보를 추정하려 합니다.

Production failure는 model intelligence보다 missing context 때문에 생기는 경우가 많습니다.

## 22. Ordering

일반 설계 원칙:

- stable high-priority rules
- relevant evidence
- examples/tools
- recent state
- explicit current task

정답은 model/provider에 따라 다르므로 eval로 검증합니다.

Prompt caching 때문에 stable prefix를 앞에 두는 성능 요구도 같이 고려할 수 있습니다.

## 23. Freshness와 Provenance

Context item마다 metadata를 유지하면 좋습니다.

    source
    timestamp
    version
    confidence
    access scope

최신 policy와 오래된 policy가 동시에 들어가면 model이 잘못된 것을 고를 수 있습니다.

## 24. Context Budget

각 category에 budget을 둘 수 있습니다.

예:

    system        3K
    tools         8K
    retrieved    20K
    memory        2K
    history       8K
    current       1K

초과 시 priority에 따라 trim/compact합니다.

## 25. Evaluation

Context change는 prompt change와 마찬가지로 versioning해야 합니다.

측정:

- answer correctness
- retrieval recall
- citation support
- tool success rate
- context tokens
- TTFT
- cache hit rate

"더 많은 context"가 아니라 "더 좋은 final task metric"이 성공 기준입니다.

## 핵심 정리

- Context Engineering은 LLM이 보는 전체 정보 환경을 설계하는 일입니다.
- Prompt Engineering은 그중 instruction wording 부분입니다.
- 원문은 system, examples, RAG, tools, memory, history, tool results, current message 8요소를 구분합니다.
- Context는 매 turn source들에서 새로 조립됩니다.
- 핵심 목표는 relevance, freshness, priority, token budget을 최적화하는 것입니다.
- Production AI 품질은 model 선택만큼 context assembler 설계에 크게 좌우됩니다.

## 원문

- https://outcomeschool.com/blog/context-engineering
