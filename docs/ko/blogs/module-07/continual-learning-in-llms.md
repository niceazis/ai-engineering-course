# LLM의 Continual Learning이란? Catastrophic Forgetting 해결 — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/continual-learning-in-llms  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-06-01 공개 원문을 직접 확인해 Catastrophic Forgetting, Replay·Regularization(EWC)·Parameter Isolation(LoRA), RAG 대안을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Continual Learning이란?

Continual Learning은 model이 시간에 따라 **새로운 지식이나 task를 배우면서 기존 능력을 최대한 유지하는 문제**입니다.

일반 training:

    fixed dataset
      → train once
      → deploy

Continual Learning:

    old model
      → new data
      → update
      → more new data
      → update
      → ...

현실 세계는 계속 바뀌므로 model update가 필요합니다.

## 2. 왜 LLM에 필요한가

예:

- new laws
- new products
- current events
- company policy changes
- new language/domain
- user personalization

하지만 LLM weight를 새 data에만 fine-tune하면 기존 knowledge가 손상될 수 있습니다.

## 3. Catastrophic Forgetting

원문의 예:

Base LLM이:

    Math
    History
    Science

를 잘 압니다.

Sports data에만 계속 fine-tune하면:

    Sports ↑
    Math/History/Science ↓

가 될 수 있습니다.

새 gradient가 기존 parameter를 덮어쓰기 때문입니다.

## 4. Stability-Plasticity Dilemma

Continual learning의 핵심 trade-off:

- **Plasticity**: 새 정보를 잘 배워야 함
- **Stability**: 기존 정보를 유지해야 함

너무 stable:

    새 지식을 못 배움

너무 plastic:

    기존 지식 잊음

이 균형이 문제의 본질입니다.

## 5. Approach 1 — Replay

새 data에 old data 일부를 섞습니다.

    batch
      = new examples
      + replayed old examples

원문 Sports 예:

    Sports
      + Math/History/Science samples
      → train

기존 task를 계속 연습하기 때문에 forgetting이 줄어듭니다.

### 장점

- 단순
- 효과적

### 단점

- old data 저장 필요
- privacy/storage 문제
- 매 update마다 compute 증가
- replay가 커지면 재학습 비용이 커짐

## 6. Replay Buffer 설계

모든 과거 data를 저장하기 어렵다면 대표 sample만 저장합니다.

선택 전략:

- random reservoir
- class-balanced
- hard examples
- diverse embeddings
- synthetic replay

Replay selection 자체가 품질에 큰 영향을 줍니다.

## 7. Approach 2 — Regularization

기존 knowledge에 중요한 parameter를 크게 바꾸지 못하도록 penalty를 줍니다.

대표: EWC(Elastic Weight Consolidation)

개념:

    L_total
      = L_new
      + lambda * Σ importance_i * (theta_i - theta_old_i)^2

importance가 큰 parameter일수록 원래 값에서 벗어날 때 큰 penalty가 생깁니다.

## 8. EWC의 직관

Old task에 매우 중요한 weight:

    거의 lock

Old task에 덜 중요한 weight:

    새 task 학습에 더 자유롭게 사용

장점:

- old raw data를 보관하지 않아도 됨

한계:

- parameter importance 추정 어려움
- 너무 많은 parameter를 보호하면 plasticity 감소
- 대규모 LLM에서 계산/저장 overhead 존재

## 9. Approach 3 — Parameter Isolation

기존 weight를 freeze하고 새 task용 parameter만 추가합니다.

대표:

- LoRA
- adapters
- prefix tuning

원문은 LoRA를 대표 예로 듭니다.

    base model frozen
      + new LoRA adapter

새 학습이 base weight를 직접 덮어쓰지 않기 때문에 forgetting을 크게 줄일 수 있습니다.

## 10. Parameter Isolation의 Trade-off

Task가 늘어날수록:

    adapter_1
    adapter_2
    adapter_3
    ...

가 계속 쌓입니다.

관리해야 할 문제:

- 어떤 adapter를 선택할지
- 여러 adapter composition
- storage 증가
- task boundary가 불명확할 때 routing

## 11. 세 접근 비교

| 접근 | 기존 weight | Old data | 추가 parameter | 핵심 비용 |
| --- | --- | --- | --- | --- |
| Replay | update | 필요 | 없음 | retraining compute |
| Regularization | 제한적 update | 불필요 가능 | importance metadata | stability tuning |
| Isolation | freeze | 불필요 | 증가 | adapter 관리 |

실전에서는 조합할 수 있습니다.

예:

    LoRA + small replay buffer

## 12. RAG는 Continual Learning인가?

원문은 아니라고 구분합니다.

RAG:

- LLM weight unchanged
- external DB에 새 knowledge
- query 때 retrieve

즉 model이 새 knowledge를 “학습”한 것이 아니라 읽어서 사용합니다.

하지만 최신 정보 유지 관점에서는 매우 실용적입니다.

## 13. Continual Learning vs RAG 선택

### Weight에 학습해야 하는 것

- style
- skill
- task behavior
- domain-specific pattern

→ continual fine-tuning/adapter

### 자주 바뀌는 factual knowledge

- current policy
- product catalog
- news
- stock/data

→ RAG가 보통 더 적합

## 14. Evaluation

새 task 성능만 보면 안 됩니다.

각 update마다:

    score_new
    score_old_task_1
    score_old_task_2
    ...

를 함께 측정합니다.

대표 지표:

- average accuracy
- forgetting measure
- forward transfer
- backward transfer

Production에서는 regression suite가 필수입니다.

## 15. 데이터 순서 문제

Continual learning은 task/data arrival order에 민감할 수 있습니다.

A→B→C와 C→B→A가 다른 결과를 만들 수 있습니다.

따라서 training log에:

- data version
- adapter version
- evaluation result
- base checkpoint

를 함께 관리해야 재현성이 생깁니다.

## 16. 실제 사용 사례

원문:

- current event update
- domain adaptation
- personalization
- mistake correction
- new language

다만 current facts는 RAG가 더 비용 효율적인 경우가 많습니다.

## 핵심 정리

- Continual Learning은 새 지식을 배우면서 old capability를 유지하는 문제입니다.
- Catastrophic Forgetting은 새 gradient가 기존 useful weight를 덮으면서 생깁니다.
- 원문은 Replay, Regularization(EWC), Parameter Isolation(LoRA) 세 접근을 설명합니다.
- RAG는 weight를 업데이트하지 않으므로 엄밀한 continual learning은 아니지만 최신 knowledge 유지에 강력한 대안입니다.
- 핵심은 stability와 plasticity의 균형이며 old-task regression evaluation이 필수입니다.

## 원문

- https://outcomeschool.com/blog/continual-learning-in-llms
