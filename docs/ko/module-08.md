# 모듈 8 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 8: 프롬프트 엔지니어링과 컨텍스트 엔지니어링

이 모듈에서는 LLM과 효과적으로 대화해 더 좋은 답을 얻는 방법과 컨텍스트 윈도우에 들어가는 모든 정보를 관리하는 방법을 배웁니다.

**이 모듈의 레슨:**

1. [Chain-of-Thought(CoT) Prompting은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-chain-of-thought-prompting-work)

→ [한국어 상세 학습 노트](blogs/module-08/how-does-chain-of-thought-prompting-work.md)
2. [Prompt Chaining은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-prompt-chaining-work)

→ [한국어 상세 학습 노트](blogs/module-08/how-does-prompt-chaining-work.md)
3. [Prompt Caching은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-prompt-caching-work)

→ [한국어 상세 학습 노트](blogs/module-08/how-does-prompt-caching-work.md)
4. [Context Engineering이란?](https://outcomeschool.com/blog/context-engineering)

→ [한국어 상세 학습 노트](blogs/module-08/context-engineering.md)
5. [Context Compaction은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-context-compaction-work)

→ [한국어 상세 학습 노트](blogs/module-08/how-does-context-compaction-work.md)

---

### 8.1 Chain-of-Thought(CoT) Prompting은 어떻게 동작하는가?

모델이 바로 답을 내릴 때 생기는 문제와 단계별 추론을 유도하는 CoT Prompting의 효과를 배웁니다.

- Prompt란?
- LLM이란?
- 바로 답할 때의 문제
- CoT Prompting이란?
- CoT 적용 전후 예제
- Zero-shot CoT vs Few-shot CoT
- 단계별 Reasoning Chain
- CoT가 동작하는 이유
- 유용한 사용처
- 주의할 점

시작하기: [Chain-of-Thought Prompting](https://outcomeschool.com/blog/how-does-chain-of-thought-prompting-work)

→ [한국어 상세 학습 노트](blogs/module-08/how-does-chain-of-thought-prompting-work.md)

### 8.2 Prompt Chaining은 어떻게 동작하는가?

하나의 Prompt 출력을 다음 Prompt 입력으로 넘겨 복잡한 작업을 더 안정적으로 해결하는 방법을 배웁니다.

- Prompt란?
- Prompt Chaining이란?
- 필요한 이유
- 단계별 동작
- 실제 예제
- 코드 예제
- 대표 패턴
- 장점
- 주의할 점
- 사용 시점

시작하기: [Prompt Chaining](https://outcomeschool.com/blog/how-does-prompt-chaining-work)

→ [한국어 상세 학습 노트](blogs/module-08/how-does-prompt-chaining-work.md)

### 8.3 Prompt Caching은 어떻게 동작하는가?

반복되는 Prompt Prefix를 재사용해 비용과 지연을 줄이는 Prompt Caching의 내부 동작을 배웁니다.

- Prompt란?
- LLM이 Prompt를 읽는 방식 복습
- Prompt Caching이란?
- 필요한 이유
- 핵심 아이디어
- Exact-prefix Rule
- Cache Write vs Read와 TTL
- Cache에 넣을 내용
- 장점
- 실제 시스템에서의 활용

시작하기: [Prompt Caching](https://outcomeschool.com/blog/how-does-prompt-caching-work)

→ [한국어 상세 학습 노트](blogs/module-08/how-does-prompt-caching-work.md)

### 8.4 Context Engineering이란?

신뢰할 수 있는 AI 애플리케이션을 만드는 핵심 기술인 Context Engineering을 배웁니다. Prompt Engineering과의 차이, Context 구성 요소, RAG·Few-shot Example·Tool·Memory 같은 대표 패턴을 살펴봅니다.

- Context Engineering이란?
- 큰 그림
- 중요한 이유
- Prompt Engineering vs Context Engineering
- Context의 구성 요소
- 대표 패턴
- 피해야 할 실수
- Best Practice
- 빠른 요약

시작하기: [Context Engineering](https://outcomeschool.com/blog/context-engineering)

→ [한국어 상세 학습 노트](blogs/module-08/context-engineering.md)

### 8.5 Context Compaction은 어떻게 동작하는가?

긴 대화가 Context Window를 넘는 문제를 해결하기 위해 오래된 메시지를 중요한 정보만 남기고 요약하는 Context Compaction을 배웁니다.

- LLM이란?
- Context Window란?
- Context란?
- 긴 대화의 문제
- 단순한 해결책이 실패하는 이유
- Context Compaction이란?
- Summarization을 이용한 압축
- 단계별 동작
- 코드에서의 Compaction
- 실제 AI Agent에서의 사용
- 중요한 이유

시작하기: [Context Compaction](https://outcomeschool.com/blog/how-does-context-compaction-work)

→ [한국어 상세 학습 노트](blogs/module-08/how-does-context-compaction-work.md)

---
