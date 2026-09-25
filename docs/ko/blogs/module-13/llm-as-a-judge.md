# LLM as a Judge란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/llm-as-a-judge  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-05-21 공개 원문을 직접 확인해 Judge 유형, Prompt Template, G-Eval과 bias, human validation을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 정의

LLM as a Judge는 강한 LLM이 다른 model/system의 output을 rubric에 따라 평가해:

- score
- verdict
- pairwise preference
- error reason

을 반환하는 방식입니다.

Open-ended text는 exact match가 어려워 human evaluation을 자동화하는 중간 지점으로 사용됩니다.

## 2. 왜 필요한가

Human evaluation:

- high quality
- expensive/slow

BLEU/ROUGE:

- cheap
- semantic nuance 부족

LLM Judge:

- semantic evaluation
- large-scale automation
- human보다 저렴

을 노립니다.

원문은 strong judge와 human agreement가 일부 연구에서 80% 이상 수준으로 보고됐다고 설명하지만, 이는 task/judge 설계마다 달라지므로 universal guarantee가 아닙니다.

## 3. Single-Answer Scoring

하나의 answer를 rubric으로 score합니다.

예:

    Helpfulness: 1~5
    Factuality: 1~5
    Conciseness: 1~5

Dimension을 분리하면 aggregate score보다 failure reason을 이해하기 쉽습니다.

## 4. Pairwise Comparison

두 answer A/B 중 더 나은 것을 선택합니다.

장점:

- absolute score보다 쉬운 판단
- preference data와 잘 맞음

주의:

- position bias를 막기 위해 A/B 순서를 swap한 두 evaluation을 돌릴 수 있습니다.

## 5. Reference-Based

Ground truth/reference answer가 있으면 judge에 함께 제공합니다.

    question
    reference
    candidate

Reference가 없으면 criterion-based evaluation이 됩니다.

## 6. Judge Prompt 구성

좋은 prompt:

1. Role
2. Evaluation criteria
3. Scoring scale의 구체적 정의
4. Input
5. Candidate answer
6. Required output schema

예:

    score 1 = wrong/unhelpful
    score 3 = partially correct
    score 5 = fully correct, concise, supported

점수 의미를 구체적으로 정의해야 calibration이 좋아집니다.

## 7. G-Eval

원문 설명:

    G-Eval
      = evaluation steps 생성
      + criteria 적용
      + final score

직접 점수만 고르기보다 먼저 평가 절차를 구성하고 각 criterion을 점검하게 합니다.

실무에서는 raw hidden chain-of-thought를 저장/노출할 필요 없이 structured checklist 결과를 요구할 수 있습니다.

## 8. 주요 Bias

### Position Bias

Pairwise에서 앞/뒤 위치 자체를 선호.

대응:

    A/B order randomization
    swap-and-average

### Verbosity Bias

긴 답을 더 좋아하는 경향.

대응:

- concise criterion 명시
- unnecessary detail penalty

### Self-Preference Bias

같은 model family의 style/output을 더 선호할 가능성.

대응:

- 다른 family judge
- human calibration

### Style Bias

Formatting이나 polished prose가 factual error를 가릴 수 있습니다.

## 9. Judge 검증

Judge도 평가 대상입니다.

Validation set:

    human labels
      ↔ judge labels

측정:

- accuracy
- Cohen's kappa / rank correlation
- bias slice
- score calibration

Judge prompt/model을 바꾸면 다시 regression test합니다.

## 10. Deterministic Rule과 조합

예:

    JSON valid?        → code
    required field?    → code
    source supports?   → retrieval/checker
    answer helpful?    → LLM judge

기계적 조건을 judge에게 넘기지 않는 것이 더 안정적입니다.

## 11. Cost Control

Eval 전체에 최고가 model을 쓰지 않고:

- cheap first-pass judge
- uncertain sample only strong judge/human

cascade를 만들 수 있습니다.

## 12. Production Use

- daily regression
- RAG groundedness
- support answer quality
- agent final result
- prompt A/B
- synthetic data filtering

등에 사용할 수 있습니다.

## 핵심 정리

- LLM Judge는 open-ended output을 scalable하게 평가하는 방법입니다.
- Absolute scoring과 pairwise comparison이 대표 pattern입니다.
- G-Eval은 평가 절차를 먼저 만들고 그 기준으로 score합니다.
- Position·verbosity·self-preference·style bias를 반드시 test해야 합니다.
- Human-labeled sample로 judge 자체를 검증해야 합니다.
- Deterministic checker가 가능한 조건은 code로 처리하는 것이 더 정확합니다.

## 원문

- https://outcomeschool.com/blog/llm-as-a-judge
