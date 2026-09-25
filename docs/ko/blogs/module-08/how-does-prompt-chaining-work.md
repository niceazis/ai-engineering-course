# Prompt Chaining은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-prompt-chaining-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-07-10 공개 원문을 직접 확인해 summarize→social post→review 코드 예, Extract-then-Use·Generate-then-Check 패턴과 주의점을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 정의

Prompt Chaining은 큰 task를 여러 LLM call로 나누고 **앞 call의 output을 다음 call의 input으로 연결하는 workflow**입니다.

    Prompt 1 → Output 1
                 ↓
    Prompt 2 → Output 2
                 ↓
    Prompt 3 → Final

한 prompt에 모든 요구를 넣는 것과 다릅니다.

## 2. 왜 필요한가

복잡한 one-shot prompt:

    긴 article을 읽고
    핵심을 요약하고
    LinkedIn 글을 쓰고
    사실 오류를 검토하고
    tone을 수정해라

Model이 한 call에서 모든 objective를 동시에 만족해야 합니다.

Chaining:

    summarize
      → draft
      → review/fix

로 분리하면 각 step의 objective가 좁아집니다.

## 3. Step-by-Step 예

### Step 1 — Summarize

Input:

    full article

Prompt:

    핵심 사실과 수치를 5개 bullet로 요약하라.

Output:

    summary

### Step 2 — Generate

Input:

    summary

Prompt:

    위 summary를 바탕으로 짧은 social post 작성.

Output:

    post

### Step 3 — Review

Input:

    post + summary

Prompt:

    summary와 비교해 사실 오류를 고치고 final post 출력.

Output:

    final_post

## 4. 원문의 Python 구조

원문은 개념적으로 다음 pattern을 사용합니다.

    summary = ask_ai(
        "Summarize: " + article
    )

    post = ask_ai(
        "Write social post from: " + summary
    )

    final_post = ask_ai(
        "Review and improve: " + post
    )

중요한 것은 model API가 아니라 **data dependency graph**입니다.

## 5. Pattern 1 — Break Down, Then Combine

큰 task를 독립 subtask로 나눕니다.

예:

    document
      → extract risks
      → extract dates
      → extract obligations
      → combine report

병렬화 가능한 subtask는 동시에 실행할 수도 있습니다.

## 6. Pattern 2 — Extract, Then Use

원문 예:

    message
      → extract name/email
      → write personalized reply

첫 step은 structured extraction, 두 번째는 generation입니다.

장점:

- downstream prompt가 작은 structured state를 받음
- parsing/evaluation이 쉬움

## 7. Pattern 3 — Generate, Then Check

원문 예:

    generate code
      → review code
      → fix bugs

Reflection Agent의 기본 구조와 같습니다.

한 call의 self-review보다 별도 call이 더 효과적일 수 있는 이유는 second call이 fresh context에서 critique objective에 집중하기 때문입니다.

## 8. Pattern 4 — Classify, Then Route

첫 call:

    category = billing / technical / sales

그 뒤 branch:

    billing → billing prompt
    technical → technical prompt

이는 agent routing의 단순 형태입니다.

## 9. Chain의 장점

### Narrow Objective

각 call이 하나의 작은 목표에 집중.

### Intermediate Inspection

Step output을 log/evaluate할 수 있습니다.

### Retry

실패한 step만 재실행.

### Different Models

Extraction에는 small model, hard reasoning에는 large model처럼 step별 model 선택 가능.

### Cost Control

Long input을 첫 call에서 요약한 뒤 downstream에는 compact output만 전달.

## 10. 가장 큰 위험 — Error Propagation

Step 1이 잘못되면:

    wrong summary
      → wrong post
      → polished wrong final

이 됩니다.

Chain이 길다고 accuracy가 자동 증가하지 않습니다.

각 중요한 boundary에 validation이 필요합니다.

## 11. Interface를 Text가 아니라 Schema로 만들기

가능하면 intermediate output을 free-form prose 대신 structured data로 만듭니다.

예:

    {
      "facts": [...],
      "dates": [...],
      "risks": [...]
    }

이렇게 하면 downstream step과 program code가 안정적입니다.

## 12. Context 최소화

다음 step에 필요한 정보만 전달합니다.

나쁜 방식:

    Step 1 output + full article + full history + all tools

좋은 방식:

    validated summary + relevant source snippets

Context bloat는 cost와 confusion을 늘립니다.

## 13. Deterministic Check는 Code로

다음은 LLM에게 시키지 않는 편이 좋습니다.

- exact arithmetic
- regex validation
- schema validation
- database lookup
- unit tests

Code/tool이 더 정확한 부분은 deterministic checker를 사용합니다.

## 14. Branching과 Loop

Prompt chain은 단순 직선만이 아닙니다.

    generate
      → test
        ├─ pass → finish
        └─ fail → fix → test

이 구조가 agent loop/harness engineering으로 발전합니다.

## 15. 언제 사용하나

- 복잡한 multi-stage transformation
- intermediate result를 검증해야 하는 task
- extraction + generation
- generation + critique
- heterogeneous model/tool 조합

Simple one-shot question에는 chain overhead가 불필요합니다.

## 16. Observability

Production에서는 step별로 기록해야 합니다.

- input hash/version
- prompt version
- model/version
- output
- latency
- token cost
- validator result

Chain 전체 실패를 root-cause하려면 intermediate trace가 필수입니다.

## 핵심 정리

- Prompt Chaining은 이전 call output을 다음 call input으로 연결합니다.
- 원문 예는 article → summary → post → review 흐름입니다.
- Extract-then-Use, Generate-then-Check, Route, Map/Reduce가 대표 pattern입니다.
- 장점은 decomposition, retry, model specialization, observability입니다.
- 가장 큰 위험은 upstream error propagation입니다.
- Intermediate interface를 structured schema로 만들고 deterministic validation을 넣는 것이 중요합니다.

## 원문

- https://outcomeschool.com/blog/how-does-prompt-chaining-work
