# Cursor는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-cursor-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 codebase indexing, Tab/Chat/Agent, diff 적용과 model routing을 독립적으로 정리했습니다. 제품 동작과 privacy 설정은 버전에 따라 바뀌므로 현재 Cursor 공식 문서를 확인해야 합니다.

## 1. Cursor의 기본 구조

Cursor는 code editor 위에:

- autocomplete
- chat
- codebase search
- agent/tool execution
- edit/diff application

을 통합합니다.

AI가 현재 file뿐 아니라 repository context를 찾는 것이 핵심입니다.

## 2. Codebase Indexing

큰 repository를 전부 매 prompt에 넣을 수 없습니다.

그래서 code를 chunk/symbol 단위로 index하고 query와 관련 있는 부분을 retrieval합니다.

개념:

    repository
      → parse/chunk
      → embeddings/index

    question
      → search
      → relevant code context
      → model

정확한 indexing 구현은 제품 버전에 따라 달라질 수 있습니다.

## 3. Tab Autocomplete

현재:

- cursor 주변 code
- nearby file
- recent edit

를 보고 다음 edit/code completion을 예측합니다.

Low latency가 중요하므로 chat/agent와 다른 model/serving path를 사용할 수 있습니다.

## 4. Chat

사용자가 codebase에 대해 질문합니다.

    "이 auth flow 어디서 시작해?"

Retriever가 관련 file/symbol을 context에 넣고 model이 설명합니다.

좋은 answer를 위해 source/reference file을 확인하는 것이 중요합니다.

## 5. Agent Mode

단순 설명을 넘어:

- search
- edit file
- run command
- test
- iterate

하는 coding-agent loop를 사용합니다.

Claude Code와 마찬가지로 model이 action을 결정하고 editor/runtime가 실제 tool을 실행합니다.

## 6. Diff 기반 적용

Model이 entire file을 무작정 덮는 대신 targeted edit/diff를 적용하면:

- change review
- conflict handling
- undo

가 쉬워집니다.

큰 generated patch는 반드시 diff와 test로 검증합니다.

## 7. Model Routing

Task마다 요구가 다릅니다.

- autocomplete → speed
- hard refactor → reasoning quality
- large context → context capacity

제품은 여러 model을 선택/route할 수 있습니다.

## 8. Privacy

Codebase indexing이 local/remote 중 어디에서 처리되고 무엇이 저장되는지는 조직 보안에 매우 중요합니다.

확인:

- code retention
- training use policy
- remote indexing
- enterprise controls
- secret filtering

현재 정책을 공식 문서에서 확인해야 합니다.

## 9. Failure Mode

- wrong code retrieval
- stale index
- partial architecture understanding
- compile failure
- wide unintended edit

대응:

    search evidence
    small diff
    build/test
    git review

## 10. 전체 흐름

    user intent
      → codebase retrieval
      → model
      → suggestion/tool calls
      → editor applies diff
      → test/observation
      → iterate

## 핵심 정리

- Cursor의 핵심은 editor + codebase retrieval + model + edit/tool loop입니다.
- Repository 전체를 prompt에 넣지 않고 indexing/search로 relevant context를 찾습니다.
- Tab, Chat, Agent는 latency/권한/작업 범위가 다릅니다.
- 실제 변경은 diff와 test로 검증해야 합니다.
- Privacy/indexing 정책은 최신 공식 제품 문서를 기준으로 확인해야 합니다.

## 원문

- https://outcomeschool.com/blog/how-does-cursor-work
