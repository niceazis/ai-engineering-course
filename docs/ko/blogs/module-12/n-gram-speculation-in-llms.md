# N-gram Speculation이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/n-gram-speculation-in-llms  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 Outcome School 원문 본문은 웹 캐시에서 직접 열리지 않았습니다. 공식 Module 12 목차와 prompt-lookup / n-gram speculative decoding의 공개 구현 원리를 기준으로 작성하며, 원문 고유 수치라고 확인되지 않은 값은 사용하지 않습니다.

## 1. 문제

일반 speculative decoding은 작은 draft model을 하나 더 유지해야 합니다.

대가:

- extra GPU memory
- tokenizer/model management
- draft inference cost

N-gram speculation은 별도 model 없이 **이미 context에서 본 token sequence를 이용해 draft**합니다.

## 2. N-gram

N-gram은 연속된 N개 token입니다.

예:

    "the quick brown fox"

3-gram:

    the quick brown
    quick brown fox

현재 suffix와 같은 N-gram이 과거 context에 있으면 그 뒤 token들도 반복될 가능성이 있습니다.

## 3. Prompt Lookup

현재 output suffix:

    "... import torch"

과 prompt 이전 어딘가에:

    "import torch
from torch..."

가 있었다면:

    "from torch..."

부분을 draft candidate로 제안할 수 있습니다.

Code, structured documents, repetitive text에서 특히 잘 맞습니다.

## 4. Verification

Draft token은 target model이 병렬로 검증합니다.

따라서:

    n-gram lookup = draft generator
    target model = authority

입니다.

Speculative decoding과 같은 acceptance rule을 사용하면 target output semantics를 유지할 수 있습니다.

## 5. 장점

- 별도 draft model 없음
- 거의 zero extra model memory
- repeated context에서 빠름
- prompt-heavy code/document task에 적합

## 6. 한계

- 새로운 창작 문장
- short prompt
- context에 반복 pattern 없음

에서는 hit가 낮습니다.

즉 general-purpose drafter라기보다 **copy/repetition-heavy workload 최적화**입니다.

## 7. N 선택

작은 N:

- match 많음
- false continuation 가능성 큼

큰 N:

- match 정확
- match 자체가 드묾

Runtime이 여러 N 길이를 시도할 수 있습니다.

## 8. Draft Length

Match를 찾은 뒤 얼마나 긴 continuation을 proposal할지도 tuning 대상입니다.

너무 길면 mismatch 뒤쪽 검증 cost가 낭비됩니다.

## 9. Code에서 강한 이유

Code에는:

- boilerplate
- repeated identifiers
- imports
- function pattern
- copied template

이 많아 n-gram reuse 가능성이 높습니다.

## 핵심 정리

- N-gram speculation은 별도 draft model 대신 context 안의 repeated token sequence를 draft source로 사용합니다.
- Target model이 최종 검증하므로 speculative decoding의 한 변형입니다.
- Code·template·repetitive context에서 특히 효과적입니다.
- Novel prose에서는 match가 적어 이득이 제한됩니다.
- Outcome School 원문 본문을 직접 검증하지 못했으므로 특정 수치를 원문 값으로 단정하지 않았습니다.

## 원문

- https://outcomeschool.com/blog/n-gram-speculation-in-llms
