# Sakana Fugu란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/decoding-sakana-fugu  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School이 해설한 Sakana Fugu Technical Report를 직접 확인해 Fugu/Fugu-Ultra, selection head, Conductor, GRPO와 공개 benchmark 결과를 독립적으로 정리했습니다.

## 1. 핵심 아이디어

Sakana Fugu 계열은 하나의 model이 모든 문제를 직접 푸는 대신 **여러 frontier model을 상황에 맞게 선택·조합하는 orchestrator model**입니다.

핵심 가정:

> 어떤 단일 model도 모든 task에서 최고가 아니며, 올바르게 조율된 team이 개별 member보다 강할 수 있다.

## 2. 두 Variant

### Fugu

빠른 orchestrator.

현재 state를 읽고 다음 step에 어떤 worker model을 사용할지 선택합니다.

### Fugu-Ultra

하나의 worker만 고르는 수준을 넘어 **여러 subtask와 worker, access relation을 포함하는 전체 workflow**를 생성합니다.

Quality 중심의 richer orchestration입니다.

## 3. Fugu Selection Head

Fugu는 긴 text reasoning으로 worker를 선택하기보다 hidden state를 읽는 lightweight selection head로 model score를 계산합니다.

목적:

- routing latency 감소
- token generation 없이 빠른 model selection

처음에는 supervised signal로 어떤 worker가 어떤 task에 강한지 학습합니다.

## 4. Collective Intelligence

여러 model의 강점이 다릅니다.

- coding
- debugging/security
- math
- niche facts

Orchestrator는 task/subtask별로 적합한 worker를 배치합니다.

단순 majority ensemble이 아니라 **역할 분담과 정보 접근 구조를 학습**합니다.

## 5. Fugu-Ultra Conductor

Workflow는 개념적으로:

    subtasks
    worker_ids
    access_lists

를 정의합니다.

Access list는 worker가 다른 agent의 어떤 output을 볼 수 있는지 제한해 독립성을 유지합니다.

이는 모든 worker가 서로의 답을 그대로 복사하는 collapse를 줄입니다.

## 6. Aggregation

원문 사례에서는 어려운 trivia에서 Gemini와 GPT가 독립 시도한 뒤 다른 Gemini가 두 결과의 필요한 부분을 결합합니다.

문제에 따라 final aggregator model도 바뀔 수 있습니다.

즉 final combiner를 한 model로 고정하지 않습니다.

## 7. GRPO Training

Fugu-Ultra는 workflow quality를 reward로 학습합니다.

원문 reward:

    malformed workflow → 0
    valid but wrong    → 0.5
    valid and correct  → 1

한 question에 G개의 workflow를 생성하고 group-relative advantage를 계산합니다.

    A_i
      = (r_i - mean(r))
        / std(r)

좋은 workflow probability를 높이고 나쁜 workflow를 낮춥니다.

## 8. 공개 Benchmark 예

Outcome School이 인용한 report 표에는 다음 score가 제시됩니다.

    SWE Bench Pro:
      Fugu-Ultra 73.7
      Fugu       59.0

    Terminal Bench 2.1:
      Fugu-Ultra 82.1
      Fugu       80.2

    GPQA Diamond:
      95.5 / 95.5

이 수치는 해당 technical report 기준 결과이며 다른 evaluation/version과 직접 비교할 때 조건을 확인해야 합니다.

## 9. Emergent Strategy

원문은 training으로 다음 pattern이 나타났다고 설명합니다.

- debate + aggregation
- build + debug
- specialist 호출

즉 orchestrator가 사람에게 hard-code된 fixed workflow만 따르는 것이 아니라 reward를 통해 model 조합 전략을 학습합니다.

## 10. Trade-off

장점:

- best model per subtask
- heterogeneous strengths
- parallelism
- team capability

비용:

- 여러 frontier call
- orchestration latency
- complex credit assignment
- provider dependency
- reproducibility

모든 task에 Ultra-style team을 쓰면 비효율적입니다.

## 핵심 정리

- Fugu는 frontier model pool에서 적절한 worker를 고르는 orchestrator입니다.
- Fugu-Ultra는 multi-agent workflow 자체를 생성하는 Conductor 방식입니다.
- Access list로 intra-workflow isolation을 유지합니다.
- GRPO는 valid/correct workflow reward를 group-relative하게 학습합니다.
- Report의 benchmark는 orchestration으로 individual model보다 높은 결과를 얻을 수 있음을 보여 주지만 cost/latency trade-off가 큽니다.

## 원문

- https://outcomeschool.com/blog/decoding-sakana-fugu
