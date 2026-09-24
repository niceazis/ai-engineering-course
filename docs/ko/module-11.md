# 모듈 11 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 11: 에이전틱 엔지니어링과 에이전트 프레임워크

이 모듈에서는 신뢰할 수 있는 Agent를 만들기 위한 엔지니어링 관행과 대표적인 Agent 프레임워크·코딩 Agent의 내부 구조를 배웁니다.

**이 모듈의 레슨:**

1. [Harness Engineering이란?](https://outcomeschool.com/blog/harness-engineering-in-ai)
   ↳ [한국어 상세 학습 노트](blogs/module-11/harness-engineering-in-ai.md)

2. [Loop Engineering이란?](https://outcomeschool.com/blog/what-is-loop-engineering)
   ↳ [한국어 상세 학습 노트](blogs/module-11/what-is-loop-engineering.md)

3. [Graph Engineering이란?](https://outcomeschool.com/blog/what-is-graph-engineering)
   ↳ [한국어 상세 학습 노트](blogs/module-11/what-is-graph-engineering.md)

4. [AI의 품질은 Definition of Done의 품질을 넘을 수 없다](https://outcomeschool.com/blog/ai-is-only-as-good-as-our-definition-of-done)
   ↳ [한국어 상세 학습 노트](blogs/module-11/ai-is-only-as-good-as-our-definition-of-done.md)

5. [LangChain은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-langchain-work)
   ↳ [한국어 상세 학습 노트](blogs/module-11/how-does-langchain-work.md)

6. [LangGraph는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-langgraph-work)
   ↳ [한국어 상세 학습 노트](blogs/module-11/how-does-langgraph-work.md)

7. [Claude Code는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-claude-code-work)
   ↳ [한국어 상세 학습 노트](blogs/module-11/how-does-claude-code-work.md)

8. [Cursor는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-cursor-work)
   ↳ [한국어 상세 학습 노트](blogs/module-11/how-does-cursor-work.md)


---

### 11.1 Harness Engineering이란?

AI Agent와 평가 시스템을 안정적으로 감싸고 제어하는 Harness의 개념과 구성 요소를 배웁니다.

- AI에서 Harness란?
- Harness Engineering이 필요한 이유
- AI Harness의 구성 요소
- AI Agent를 위한 Harness Engineering
- 평가를 위한 Harness Engineering
- Best Practice
- 전체 구조 연결

시작하기: [Harness Engineering](https://outcomeschool.com/blog/harness-engineering-in-ai)

→ [한국어 상세 학습 노트](blogs/module-11/harness-engineering-in-ai.md)


### 11.2 Loop Engineering이란?

Agent가 작업을 완료할 때까지 반복 실행하는 Loop를 설계하고 제어하는 방법을 배웁니다.

- Loop Engineering이란?
- Loop + Engineering
- 필요한 이유
- AI Agent의 Loop
- 가장 단순한 Loop와 문제점
- 설계해야 할 Loop 구성 요소
- Prompt vs Context vs Loop Engineering
- 흔한 실패
- Loop Engineering 기법
- 완전한 예제
- 잘 동작하는 영역과 실패하는 영역

시작하기: [Loop Engineering](https://outcomeschool.com/blog/what-is-loop-engineering)

→ [한국어 상세 학습 노트](blogs/module-11/what-is-loop-engineering.md)


### 11.3 Graph Engineering이란?

하나의 거대한 Prompt나 끝없는 Loop 대신 작은 단계와 명확한 경로로 AI 시스템을 Graph 형태로 구성하는 방법을 배웁니다.

- Graph Engineering이란?
- Graph = Node + Edge
- 필요한 이유
- Node, Edge, State
- 첫 Graph 만들기
- Conditional Edge
- Cycle
- 한 번의 전체 실행
- Parallel Branch
- Checkpoint
- Human in the Loop
- Graph 내부 오류 처리
- Graph Engineering vs Loop Engineering
- 잘 동작하는 영역
- 실패하는 영역
- Best Practice
- 결론

시작하기: [Graph Engineering](https://outcomeschool.com/blog/what-is-graph-engineering)

→ [한국어 상세 학습 노트](blogs/module-11/what-is-graph-engineering.md)


### 11.4 AI의 품질은 Definition of Done의 품질을 넘을 수 없다

작업이 끝났는지 기계적으로 판정할 수 있는 명확한 완료 기준이 AI 시스템의 신뢰성을 어떻게 높이는지 배웁니다.

- Definition of Done이란?
- 완료 기준이 정확한 작업
- 완료 기준이 모호한 작업
- 측정 가능한 영역에서 AI가 강한 이유
- 더 좋은 Definition of Done 작성법

시작하기: [AI Is Only as Good as Our Definition of Done](https://outcomeschool.com/blog/ai-is-only-as-good-as-our-definition-of-done)

→ [한국어 상세 학습 노트](blogs/module-11/ai-is-only-as-good-as-our-definition-of-done.md)


### 11.5 LangChain은 어떻게 동작하는가?

Prompt, Chain, Memory, Output Parser, Retrieval, Agent를 조합해 LLM 애플리케이션을 만드는 LangChain의 구조를 배웁니다.

- LangChain이란?
- 필요한 이유
- 핵심 아이디어
- LLM과 Prompt Template
- Chain
- Output Parser
- Memory
- Retrieval과 RAG
- Tool과 Agent
- 전체 동작 흐름

시작하기: [LangChain](https://outcomeschool.com/blog/how-does-langchain-work)

→ [한국어 상세 학습 노트](blogs/module-11/how-does-langchain-work.md)


### 11.6 LangGraph는 어떻게 동작하는가?

State, Node, Edge로 Agent Workflow를 Graph로 구성하는 LangGraph를 배웁니다.

- LangGraph란?
- 필요한 이유
- Graph
- State
- Node와 Edge
- Conditional Edge
- 완전한 예제
- Tool과 실제 호출 주체
- Memory와 Persistence
- Human-in-the-loop
- 사용 시점

시작하기: [LangGraph](https://outcomeschool.com/blog/how-does-langgraph-work)

→ [한국어 상세 학습 노트](blogs/module-11/how-does-langgraph-work.md)


### 11.7 Claude Code는 어떻게 동작하는가?

일반 챗봇과 달리 코드베이스를 탐색하고 Tool을 사용하며 작업을 검증하는 Claude Code의 Agent Loop를 배웁니다.

- Claude Code란?
- 일반 AI Chatbot의 한계
- Agent Loop
- Tool
- 버그 수정 예제
- 대규모 프로젝트 검색
- 자체 검증
- CLAUDE.md
- Permission
- Plan Mode, SubAgent, Hook
- 전체 구조

시작하기: [Claude Code](https://outcomeschool.com/blog/how-does-claude-code-work)

→ [한국어 상세 학습 노트](blogs/module-11/how-does-claude-code-work.md)


### 11.8 Cursor는 어떻게 동작하는가?

코드 편집기 위에 AI 기능을 통합한 Cursor가 코드베이스를 Embedding으로 Indexing하고 검색하며, Tab·Chat·Agent Mode에서 변경을 적용하는 방식을 배웁니다.

- Cursor란?
- Code Editor + AI
- 핵심 아이디어
- 코드 이해 방식
- Codebase Indexing
- Tab Autocomplete
- Chat
- Agent Mode
- Diff를 통한 변경 적용
- 작업별 다른 Model 사용
- 코드 Privacy
- 전체 흐름

시작하기: [Cursor](https://outcomeschool.com/blog/how-does-cursor-work)

→ [한국어 상세 학습 노트](blogs/module-11/how-does-cursor-work.md)


---
