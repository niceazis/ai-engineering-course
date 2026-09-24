# 모듈 10 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 10: AI 에이전트와 에이전틱 시스템

이 모듈에서는 LLM이 단순히 질문에 답하는 수준을 넘어 실제 작업을 수행하는 시스템으로 발전하는 과정을 배웁니다. 단일 Agent에서 시작해 Tool과 Memory를 사용하는 방식, 여러 Agent가 협업하는 시스템까지 확장합니다.

**이 모듈의 레슨:**

1. [AI Agent란? 어떻게 동작하는가](https://outcomeschool.com/blog/ai-agent)
2. [LLM의 Function Calling은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-function-calling-work-in-llms)
3. [AI Agent Loop란?](https://outcomeschool.com/blog/ai-agent-loop)
4. [ReAct Agent란?](https://outcomeschool.com/blog/react-agent)
5. [Plan-and-Execute Agent란?](https://outcomeschool.com/blog/plan-and-execute-agent)
6. [Reflection Agent란?](https://outcomeschool.com/blog/reflection-agent)
7. [AI Agent Memory는 어떻게 동작하는가?](https://outcomeschool.com/blog/ai-agent-memory)
8. [MCP(Model Context Protocol)란?](https://outcomeschool.com/blog/what-is-mcp-model-context-protocol)
9. [Agent Skills란?](https://outcomeschool.com/blog/what-are-agent-skills)
10. [OKF(Open Knowledge Format)란?](https://outcomeschool.com/blog/what-is-okf-open-knowledge-format)
11. [Multi-Agent System이란?](https://outcomeschool.com/blog/multi-agent-systems)
12. [AI SubAgent란?](https://outcomeschool.com/blog/ai-subagents)
13. [AI Agent는 어떻게 통신하는가?](https://outcomeschool.com/blog/how-ai-agents-communicate)
14. [AI Orchestration이란?](https://outcomeschool.com/blog/ai-orchestration)
15. [Sakana Fugu란?](https://outcomeschool.com/blog/decoding-sakana-fugu)
16. [Computer-Use Agent는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-do-computer-use-agents-work)

---

### 10.1 AI Agent란? 어떻게 동작하는가

일반 LLM과 Agent의 차이, 다섯 가지 핵심 구성 요소, end-to-end 동작, 주요 유형과 사용 시점을 배웁니다.

- 큰 그림
- AI Agent란?
- AI Agent vs Plain LLM vs Chatbot
- 다섯 가지 핵심 구성 요소
- End-to-End 동작
- Research Agent 예제
- AI Agent 유형
- 현재 가능한 작업
- 사용 시점
- 흔한 실패 모드
- 빠른 요약

시작하기: [AI Agent](https://outcomeschool.com/blog/ai-agent)

영상 보기: [AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization](https://www.youtube.com/watch?v=lnfWvX66FUk)

### 10.2 LLM의 Function Calling은 어떻게 동작하는가?

LLM이 외부 함수를 선택하고 인자를 만들지만 직접 함수를 실행하지는 않는 Function Calling의 핵심 구조를 배웁니다.

- Function Calling이란?
- 필요한 이유
- 핵심: 모델이 함수를 직접 실행하지 않음
- 단계별 동작
- get_weather(city) 예제
- Conversation Loop
- Multi-Step / Parallel Function Calling
- Structured Output·JSON Mode와의 관계
- AI Agent의 기반
- 빠른 요약

시작하기: [Function Calling](https://outcomeschool.com/blog/how-does-function-calling-work-in-llms)

### 10.3 AI Agent Loop란?

Agent를 움직이는 Think-Act-Observe 사이클과 종료 조건, 흔한 실패 유형을 배웁니다.

- 큰 그림
- Agent Loop란?
- Loop가 필요한 이유
- Think-Act-Observe
- 단계별 흐름
- 실제 코드
- 한 Turn의 Parallel Tool Call
- 종료 판단
- 흔한 Loop 실패
- 빠른 요약

시작하기: [AI Agent Loop](https://outcomeschool.com/blog/ai-agent-loop)

### 10.4 ReAct Agent란?

Reasoning과 Acting을 번갈아 수행하는 ReAct Agent의 구조와 동작, 구현과 실패 대응을 배웁니다.

- ReAct Agent란?
- ReAct Agent vs 일반 AI Agent
- 구조
- ReAct Prompt Template
- 생각하고 행동하는 방식
- Full Trace 예제
- 구현
- 흔한 실패와 해결책
- 빠른 요약

시작하기: [ReAct Agent](https://outcomeschool.com/blog/react-agent)

### 10.5 Plan-and-Execute Agent란?

먼저 계획을 만들고 각 단계를 실행하는 Agent 패턴을 배웁니다.

- Plan-and-Execute Agent란?
- 일반 AI Agent와의 차이
- 구조
- 계획과 실행 과정
- Full Trace 예제
- ReAct Agent와 비교
- 흔한 실패와 해결책
- 빠른 요약

시작하기: [Plan-and-Execute Agent](https://outcomeschool.com/blog/plan-and-execute-agent)

### 10.6 Reflection Agent란?

자신의 결과를 생성하고 비평한 뒤 수정하는 Reflection Agent를 배웁니다.

- Reflection Agent란?
- 일반 AI Agent와의 차이
- 구조
- 동작 방식
- Full Trace 예제
- ReAct Agent와 비교
- 흔한 실패와 해결책
- 빠른 요약

시작하기: [Reflection Agent](https://outcomeschool.com/blog/reflection-agent)

### 10.7 AI Agent Memory는 어떻게 동작하는가?

Agent Memory가 필요한 이유, Memory Stack, Write·Read·Update·Forget 네 가지 핵심 연산과 런타임 흐름을 배웁니다.

- 큰 그림
- Memory가 필요한 이유
- Memory Stack
- 네 가지 핵심 연산
- Runtime Memory Flow
- 저장할 것과 저장하지 말아야 할 것
- 흔한 실수와 해결책
- 빠른 요약

시작하기: [AI Agent Memory](https://outcomeschool.com/blog/ai-agent-memory)

### 10.8 MCP(Model Context Protocol)란?

AI 모델과 외부 Tool·Data Source를 표준화된 방식으로 연결하는 MCP를 배웁니다.

- MCP 이전의 문제
- MCP란?
- Model + Context + Protocol
- USB-C 비유
- 일반 API와의 차이
- MCP의 세 구성 요소
- 단계별 요청 흐름
- 연결 과정
- 실제 예제
- 중요성
- 주의할 점
- 요약

시작하기: [MCP](https://outcomeschool.com/blog/what-is-mcp-model-context-protocol)

### 10.9 Agent Skills란?

Agent가 필요한 지침·지식·코드를 필요할 때만 불러오는 Skill 구조와 Progressive Disclosure를 배웁니다.

- Agent Skills 이전의 문제
- Agent Skills란?
- Skill 내부 구성
- Description이 Trigger 역할을 하는 방식
- Progressive Disclosure
- Skill에 실제 코드를 포함하는 방법
- Skill 위치
- 직접 만드는 방법
- Agent Skills vs MCP
- 실제 예제
- 중요성
- 주의할 점
- 요약

시작하기: [Agent Skills](https://outcomeschool.com/blog/what-are-agent-skills)

### 10.10 OKF(Open Knowledge Format)란?

흩어진 데이터 지식을 AI Agent와 Tool이 읽을 수 있는 평문 Markdown 폴더 형태로 정리하는 Open Knowledge Format을 배웁니다.

- 지식이 흩어지는 문제
- OKF란?
- Open + Knowledge + Format
- OKF Bundle 내부
- Frontmatter와 필수 필드
- Cross-link로 Graph 만들기
- Plain Markdown을 쓰는 이유
- Agent가 사용하는 방식
- OKF, MCP, Agent Skills의 관계
- 현재 제공되는 구성
- 요약

시작하기: [OKF](https://outcomeschool.com/blog/what-is-okf-open-knowledge-format)

### 10.11 Multi-Agent System이란?

여러 Agent가 역할을 나눠 협업하는 시스템의 구성 원리와 trade-off를 배웁니다.

- 큰 그림
- Multi-Agent System이란?
- 세 가지 Pillar
- 대표 Agent Role
- Agent Communication
- Coordination
- Multi-Agent vs Single Agent
- 흔한 실수
- 사용 시점
- 빠른 요약

시작하기: [Multi-Agent System](https://outcomeschool.com/blog/multi-agent-systems)

### 10.12 AI SubAgent란?

큰 작업을 분해해 전문화된 하위 Agent에 맡기는 SubAgent 구조를 배웁니다.

- AI Agent란?
- SubAgent란?
- 필요한 이유
- 동작 방식
- 예제
- 장점
- 과제
- Best Practice

시작하기: [AI SubAgent](https://outcomeschool.com/blog/ai-subagents)

### 10.13 AI Agent는 어떻게 통신하는가?

여러 Agent가 복잡한 작업을 수행하기 위해 메시지를 주고받는 방식과 프로토콜을 배웁니다.

- Agent Communication이란?
- 필요한 이유
- 통신에 필요한 요소
- 메시지 흐름
- 통신 방식
- Direct Communication
- Centralized Communication
- Broadcast Communication
- Shared Memory Communication
- 메시지 형식
- 통신 규칙
- 과제
- Best Practice

시작하기: [AI Agent Communication](https://outcomeschool.com/blog/how-ai-agents-communicate)

### 10.14 AI Orchestration이란?

여러 LLM, Tool, Step을 조율해 실제 AI 제품을 구성하는 Orchestration을 배웁니다.

- AI Orchestration이란?
- 필요한 이유
- AI Orchestration vs AI Agent
- 구성 요소
- 동작 방식
- Sequential Pattern
- Parallel Pattern
- Conditional Pattern
- Loop Pattern
- Orchestrator-Worker Pattern
- 관련 Tool
- 과제
- Best Practice

시작하기: [AI Orchestration](https://outcomeschool.com/blog/ai-orchestration)

### 10.15 Sakana Fugu란?

여러 AI 모델 팀을 지휘하는 Conductor처럼 동작하는 Sakana Fugu 모델 계열을 살펴봅니다.

- Sakana Fugu란?
- 필요한 이유
- 큰 그림
- Collective Intelligence
- Fugu와 Fugu-Ultra
- Lightweight Selection Head
- Supervised Fine-Tuning
- Evolutionary Strategy
- Fugu-Ultra의 Conductor
- GRPO를 이용한 학습
- Agent 간 복제 방지
- 성능
- 스스로 발견한 전략
- 빠른 요약

시작하기: [Sakana Fugu](https://outcomeschool.com/blog/decoding-sakana-fugu)

### 10.16 Computer-Use Agent는 어떻게 동작하는가?

화면을 보고 판단해 마우스·키보드 같은 컴퓨터 조작을 수행하는 Agent를 배웁니다.

- Computer-Use Agent란?
- 필요한 이유
- Perceive-Think-Act Loop
- 화면을 보는 방식
- 행동을 결정하는 방식
- 행동 실행
- 단계별 예제
- System Prompt와 Tool
- Safety와 Guardrail
- 한계
- 결론

시작하기: [Computer-Use Agent](https://outcomeschool.com/blog/how-do-computer-use-agents-work)

---
