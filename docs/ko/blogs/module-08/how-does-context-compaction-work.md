# Context Compaction은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-context-compaction-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문을 직접 확인해 3000→200 token 직관, 850→270 token 수치 예, naive sliding-window와 summarize+recent 구현을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 문제: 대화는 계속 늘어나지만 Context Window는 유한하다

Agent/chat session이 길어지면 history token이 계속 증가합니다.

결국:

    system
    + tools
    + memory
    + conversation history
    + tool results
    + current message

합계가 context limit 또는 실용적인 budget을 넘습니다.

단순 해결책은 오래된 message를 버리는 것이지만 중요한 fact까지 잃을 수 있습니다.

## 2. Naive Sliding Window

가장 단순한 방식:

    keep last N messages

Code:

    def naive(messages, n):
        return messages[-n:]

장점:

- 구현 간단
- token bound 명확

단점:

- 초기에 나온 user name
- project goal
- 중요한 decision
- constraint

를 통째로 잃을 수 있습니다.

## 3. Context Compaction의 정의

오래된 raw history를 **더 짧은 structured summary/state로 바꾸고**, 최근 message는 full detail로 유지합니다.

    old raw history
      → summarize/compact
      → compact state

    final context
      = compact state
      + recent detailed messages

## 4. Summarization과 Compaction의 차이

Summarization:

    text → shorter text

Compaction:

    전체 context management policy

입니다.

Compaction은:

- 언제 trigger할지
- 무엇을 압축할지
- 무엇을 반드시 보존할지
- recent window는 얼마나 둘지
- summary를 어떻게 다시 갱신할지

까지 포함합니다.

## 5. 원문의 3000→200 Token 예

원문 직관:

    old messages: 3000 tokens
      → summarizer
      → summary: 200 tokens

Raw 3000 token을 버리고 200-token note만 context에 둡니다.

중요한 facts는 short note에 남깁니다.

## 6. 원문의 850→270 Token 수치

Compaction 전:

    old messages    700
    recent messages 150
    total           850

Context limit을 넘었다고 가정합니다.

Old 700 tokens를 summarize:

    summary = 120 tokens

Compaction 후:

    summary         120
    recent          150
    total           270

절감:

    850 - 270 = 580 tokens

입니다.

## 7. 왜 Recent Message는 그대로 남기는가

최근 turn에는:

- pronoun reference
- exact wording
- immediate tool output
- unfinished task state

같은 local detail이 중요합니다.

너무 일찍 summarize하면 이런 정보가 손실될 수 있습니다.

그래서 common pattern:

    compact old
    + preserve recent

를 사용합니다.

## 8. 반복 Compaction

대화가 다시 길어지면 기존 summary와 새 old messages를 합쳐 다시 압축합니다.

    summary_v1
    + messages_101..150
      → summary_v2

이렇게 recursive compaction을 수행할 수 있습니다.

## 9. Summary Drift

반복 summary에는 위험이 있습니다.

작은 오류가:

    summary_v1 error
      → summary_v2에 포함
      → summary_v3에서 사실처럼 굳어짐

할 수 있습니다.

이를 summary drift라고 볼 수 있습니다.

중요 fact는 free-form summary만 믿지 말고 structured durable state로 별도 유지하는 것이 좋습니다.

## 10. Structured Compaction

예:

    {
      "user_goal": "...",
      "constraints": [...],
      "decisions": [...],
      "open_tasks": [...],
      "important_entities": {...}
    }

Narrative summary보다 stable field를 만들면 중요 정보 보존을 검증하기 쉽습니다.

## 11. 원문의 Code Pattern

개념:

    old = messages[:-recent_count]
    recent = messages[-recent_count:]

    summary = summarize(old)

    return [summary] + recent

핵심은 raw old history를 그대로 유지하지 않고 summary로 교체한다는 점입니다.

## 12. Trigger Policy

매 turn summarize하면 비용이 큽니다.

일반적인 trigger:

- context token > threshold
- history token > budget
- agent step count > N
- topic boundary
- tool result burst

예:

    if context_tokens > 0.75 * max_budget:
        compact()

## 13. Hard Facts와 Soft Summary 분리

다음은 별도 structured state로 보존하는 것이 좋습니다.

- explicit user requirement
- selected option
- exact ID/path
- deadline
- API result
- completed step

다음은 summary로 압축하기 좋습니다.

- discussion narrative
- repeated explanation
- obsolete alternatives
- low-priority chatter

## 14. Agent에서의 Compaction

Long-running agent는 chat뿐 아니라 다음이 쌓입니다.

- plan
- tool calls
- tool results
- errors
- intermediate files

모든 raw trace를 context에 유지하면 비용과 confusion이 커집니다.

Agent compaction:

    raw trace
      → state summary
      → current task state

로 변환합니다.

## 15. Context Compaction vs Memory

Compaction:

- 현재 session context를 줄이는 목적

Memory:

- 미래 session에서도 필요한 durable facts를 저장

Compaction summary를 memory처럼 영구 저장할 수도 있지만 두 목적은 구분하는 편이 좋습니다.

## 16. Compaction vs RAG

RAG:

- external knowledge에서 relevant information retrieval

Compaction:

- 현재 accumulated context 자체를 압축

둘을 함께 사용합니다.

    external docs → RAG
    long interaction → compaction

## 17. Lossy Compression임을 인정해야 한다

Summary는 원문과 동일하지 않습니다.

항상 information loss가 있습니다.

따라서 high-risk task에서는:

- raw source pointer 유지
- summary와 original provenance 연결
- 필요 시 원문 다시 retrieve

할 수 있어야 합니다.

## 18. Evaluation

Compaction policy를 평가할 때:

- token reduction ratio
- key-fact retention
- task success before/after
- contradiction rate
- latency/cost
- long-session accuracy

를 측정합니다.

특히 synthetic long-chat test에서 초반 fact를 나중에 질문해 보존률을 확인할 수 있습니다.

## 핵심 정리

- Context Compaction은 오래된 raw history를 짧은 state/summary로 바꾸고 최근 detail을 유지합니다.
- 원문 예에서 850-token context를 120-token summary + 150 recent = 270 tokens로 줄여 580 tokens를 확보합니다.
- Naive sliding window는 old facts를 완전히 삭제하는 문제가 있습니다.
- Compaction은 반복할 수 있지만 summary drift 위험이 있습니다.
- 중요한 exact state는 structured memory로 별도 보존하고 free-form summary만 의존하지 않는 것이 좋습니다.
- Compaction은 lossy compression이므로 provenance와 re-retrieval 경로가 중요합니다.

## 원문

- https://outcomeschool.com/blog/how-does-context-compaction-work
