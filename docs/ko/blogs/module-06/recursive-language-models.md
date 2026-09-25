# Recursive Language Model(RLM)이란 무엇이며 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/recursive-language-models  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문을 직접 확인해 1M-token 문제, Python environment, call_llm 예, recursive tree, RAG 비교, codebase 사례를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 정의

RLM은 하나의 architecture 이름이라기보다 **language model을 사용하는 실행 방식**입니다.

원문 정의:

> 큰 문제를 풀기 위해 모델이 input의 작은 부분에 다른 language model 또는 자기 자신을 다시 호출하는 방식.

즉:

    Recursive + Language Model

입니다.

## 2. 왜 필요한가

원문 예:

    input = 1,000,000 tokens

큰 input을 한 번에 넣으면:

- context window limit
- context rot / lost-in-the-middle
- 높은 token cost
- 느린 prefill

문제가 생깁니다.

“context window를 크게 만들면 끝”이 아니라 input exploration 전략 자체를 바꿉니다.

## 3. 핵심 Architecture

Full input을 main model context에 직접 넣지 않습니다.

대신:

    huge input
      → Python environment variable

로 보관합니다.

Main model에게는:

- variable 이름
- 사용할 수 있는 code/tool
- 최종 task

만 알려 줍니다.

모델이 code를 작성해 필요한 부분을 읽고 작은 model call을 수행합니다.

## 4. Meeting Transcript 예

긴 meeting transcript가 context 변수에 있다고 합시다.

목표:

    모든 action item 찾기

원문의 단순 code:

    turns = context.split("\n")
    results = [
        call_llm(f"Find action items in: {turn}")
        for turn in turns
    ]
    print(results)

## 5. Step-by-Step

### Step 1

Main model이 Python code를 출력합니다.

### Step 2

Python environment가 code를 실행합니다.

각 turn이 작은 sub-call로 들어갑니다.

### Step 3

각 sub-call은 짧은 result만 반환합니다.

Main model은 전체 transcript 대신 짧은 answer list를 봅니다.

### Step 4

Main model이 결과를 합쳐 final action items를 만듭니다.

필요하면 더 많은 code를 작성해 반복합니다.

## 6. Agentic Loop

원문은 다음 loop를 agentic loop라고 설명합니다.

    model writes code
      → environment executes
      → result returned
      → model decides next code
      → repeat

Model 자체는 Python interpreter가 아닙니다.

“Python code라는 text”를 생성하고 environment가 실행합니다.

call_llm도 runtime이 제공하는 API/tool입니다.

## 7. 왜 더 잘 작동할 수 있는가

Sub-call 하나가 작은 input에 집중합니다.

예:

    full transcript = 200K tokens

대신:

    each call = one turn / one section

이라면 각 call의 relevance density가 높습니다.

Main model도 full document 대신 compact sub-results만 받아 clean context를 유지합니다.

## 8. Recursion

어떤 piece가 여전히 너무 크면 sub-model도 다시 RLM처럼 행동할 수 있습니다.

    root RLM
      ├─ sub-RLM A
      │    ├─ leaf A1
      │    └─ leaf A2
      └─ sub-RLM B
           ├─ leaf B1
           └─ leaf B2

원문은 tree 구조로 설명합니다.

Recursion depth는 input size와 question에 따라 달라지며 model이 전략적으로 결정할 수 있습니다.

## 9. Fixed Chunking과 차이

단순 chunking:

    every 1,000 tokens
    → summarize all

RLM:

- 어떻게 split할지 model이 결정
- 무엇을 물을지 결정
- 필요하면 특정 section만 깊게 탐색
- code로 filtering/aggregation 가능

즉 fixed pipeline보다 dynamic exploration에 가깝습니다.

## 10. “더 인간처럼 읽는다”는 직관

원문은 사람이 책을 읽을 때 모든 page를 동일하게 처리하지 않는다는 비유를 사용합니다.

- skim
- jump
- inspect relevant section
- re-read difficult part

RLM도 question에 따라 탐색 전략을 바꿀 수 있습니다.

## 11. 장점

원문:

- context window보다 훨씬 큰 input
- 작은 context별 집중으로 long-context accuracy 개선 가능
- 필요한 piece만 보내 비용 절감 가능
- modular decomposition
- adaptive splitting

## 12. 한계

원문:

- code execution environment 필요
- 한 question이 많은 model calls 유발
- latency 증가 가능
- sub-call error가 누적
- debugging 어려움

특히 recursive agent가 만든 code는 sandbox, timeout, resource limit이 필요합니다.

## 13. 언제 사용하나

원문 추천:

- very long document QA
- large codebase analysis
- long meeting/transcript
- many files comparison
- independent subtask로 분해 가능한 문제

Short input에는 overhead만 늘 수 있습니다.

## 14. RLM vs RAG

원문 비교:

| Feature | RAG | RLM |
| --- | --- | --- |
| Data 선택 | retrieval search가 먼저 선택 | model이 직접 탐색 |
| Flexibility | retriever에 의존 | adaptive |
| Code execution | 필수 아님 | model-generated code |
| Best for | fixed knowledge QA | complex long-input task |
| Complexity | 낮음 | 높음 |

둘은 경쟁 관계만은 아닙니다. RLM 내부 subtask가 RAG를 호출할 수도 있습니다.

## 15. Large Codebase 사례

원문 use case:

목표:

    hundreds of files에서 security issues 찾기

RLM:

1. codebase를 environment variable에 저장
2. main RLM에게 security audit 요청
3. file loop code 생성
4. 각 file을 작은 model에 검사
5. issue list를 반환
6. main model이 final report 통합

Main model은 전체 codebase를 context에 넣지 않습니다.

## 16. 실패 시나리오

### Decomposition 오류

중요한 cross-file relation을 file별 검사로 쪼개면 놓칠 수 있습니다.

### Aggregation 오류

Sub-call은 맞아도 final merge에서 duplicate/missing issue가 생길 수 있습니다.

### Tool Code 오류

Generated Python 자체가 잘못될 수 있습니다.

따라서 intermediate artifacts와 tool trace를 관찰 가능하게 유지해야 합니다.

## 핵심 정리

- RLM은 큰 input을 context에 직접 넣는 대신 environment에 두고 model이 code로 탐색합니다.
- 작은 piece에 model을 재귀 호출하고 결과를 요약해 상위 model에 올립니다.
- 원문은 meeting transcript와 large codebase 사례를 사용합니다.
- Fixed chunking보다 adaptive하지만 system complexity와 model-call 수가 증가합니다.
- RAG는 retriever가 data를 고르고, RLM은 model이 exploration 전략 자체를 정한다는 차이가 큽니다.

## 원문

- https://outcomeschool.com/blog/recursive-language-models
