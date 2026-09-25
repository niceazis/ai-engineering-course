# Claude Code는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-claude-code-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 coding-agent loop, tool use, CLAUDE.md, permission, plan/subagent/hook 개념을 독립적으로 정리했습니다. 제품 기능은 버전에 따라 달라질 수 있으므로 현재 Anthropic 문서를 우선해야 합니다.

## 1. 일반 Chatbot과 Coding Agent의 차이

일반 chat:

    code snippet 질문
      → text answer

Coding agent:

    repository 탐색
      → file read/search
      → edit
      → command/test
      → error 관찰
      → 수정 반복

즉 실제 workspace와 tool loop를 갖습니다.

## 2. Agent Loop

    task
      → inspect repo
      → plan next action
      → tool
      → observation
      → edit/test
      → repeat
      → final summary

Model이 모든 codebase를 처음부터 context에 넣지 않고 필요한 file/symbol을 탐색합니다.

## 3. Tool

대표 capability:

- file read/write
- search/grep
- shell command
- git
- test/build
- web/docs depending environment

Tool permission이 실제 agent 권한을 결정합니다.

## 4. Bug Fix Example

1. Error/reproduction 확인
2. 관련 symbol search
3. file read
4. 원인 hypothesis
5. minimal edit
6. test
7. 실패하면 log 읽고 재수정
8. regression pass

Definition of Done이 test로 명확할수록 agent가 잘 작동합니다.

## 5. Large Project Search

모든 file을 읽지 않고:

    query/symbol
      → grep/index
      → relevant files
      → deeper read

하는 retrieval pattern을 사용합니다.

이는 RAG와 유사한 context engineering 문제입니다.

## 6. Self-Verification

"수정했다"는 model의 선언보다:

- test output
- compiler
- lint
- git diff

가 강한 verifier입니다.

Coding agent harness는 이 deterministic feedback을 loop에 넣습니다.

## 7. CLAUDE.md

Project-specific instructions를 repository에 둬 agent에게:

- build/test command
- coding convention
- architecture
- restrictions

를 알려 줄 수 있습니다.

Documentation이 stale하면 agent도 잘못된 workflow를 따를 수 있으므로 유지관리 대상입니다.

## 8. Permission

Shell/file action은 실제 side effect가 있습니다.

Permission system은:

- allowed command
- edit scope
- network
- destructive operations

을 제한합니다.

Autonomous coding의 안전은 model 자체보다 runtime permission에 크게 의존합니다.

## 9. Plan Mode

바로 edit하지 않고 먼저 codebase를 분석하고 plan을 제시하는 mode/pattern은 큰 변경에서 useful합니다.

Plan과 execution을 분리해 scope creep을 줄입니다.

## 10. SubAgent

Research/test/review 같은 subtask를 별도 context의 worker에 맡겨 parent context를 보호할 수 있습니다.

## 11. Hooks

특정 lifecycle event에 deterministic command를 붙일 수 있습니다.

예:

    after edit → formatter
    before commit → tests

Agent 판단과 code-enforced policy를 결합합니다.

## 핵심 정리

- Claude Code 같은 coding agent는 repository tool loop를 가진 harness입니다.
- Search→edit→test→observe→repair가 핵심 cycle입니다.
- CLAUDE.md는 project-specific context, permission은 action boundary 역할을 합니다.
- Verification은 self-critique보다 compiler/test/diff가 강합니다.
- 제품 세부 기능은 빠르게 변하므로 현재 공식 문서 기준으로 사용해야 합니다.

## 원문

- https://outcomeschool.com/blog/how-does-claude-code-work
