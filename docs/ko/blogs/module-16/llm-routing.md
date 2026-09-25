# LLM Routing이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/llm-routing  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-05-09 공개 원문을 직접 확인해 cost gap, router anatomy, 5가지 routing strategy, full trace, latency rule, LLM Routing vs MoE를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 큰 그림

LLM Routing의 목표:

> 모든 query를 같은 model에 보내지 않고, query 난이도와 성격에 맞는 model을 선택한다.

예:

    easy query
      → small cheap fast model

    coding query
      → code-specialist model

    hard reasoning
      → frontier model

## 2. 왜 필요한가

원문 예시 가격:

    Frontier LLM
      ≈ $15 / 1M output tokens

    Small LLM
      ≈ $0.50 / 1M output tokens

단순 비교:

    15 / 0.5 = 30×

정도의 cost gap입니다.

가격은 시점과 provider에 따라 변하지만 원문의 핵심은 **query마다 필요한 intelligence 수준이 다르다**는 점입니다.

## 3. Router Anatomy

원문은 네 부분으로 설명합니다.

1. Query
2. Router
3. LLM Pool
4. Selected LLM

구조:

    user query
      → router
         ├─ small LLM
         ├─ mid LLM
         ├─ frontier LLM
         └─ specialist LLM

## 4. Router Latency

원문 rule of thumb:

> router 자체 latency는 선택된 LLM latency의 10% 이하가 좋다.

예:

    selected LLM = 1 second
    router target <= 100 ms

Routing으로 100ms를 아끼려다 router가 300ms 걸리면 전체 UX가 악화될 수 있습니다.

## 5. Strategy 1 — Rule-based

원문 예:

    code/function/bug keyword
      → code LLM

    very short query
      → small LLM

    medium length
      → mid LLM

    otherwise
      → frontier LLM

장점:

- 매우 빠름
- model call 없음

단점:

- brittle
- paraphrase에 약함

예를 들어 "Why is my Python script broken?"은 keyword rule에 따라 놓칠 수 있습니다.

## 6. Strategy 2 — Classifier-based

과거 data:

    (query, best_model)

로 작은 classifier를 학습합니다.

가능한 model:

- logistic regression on embeddings
- small neural network

장점:

- 실제 traffic pattern 학습

단점:

- labeled data 필요
- model pool 변경 시 retraining 필요

## 7. Strategy 3 — Embedding-based

각 query와 reference query를 embedding space에서 비교합니다.

예:

    query embedding
      → nearest reference
      → associated model

장점:

- 별도 supervised training 없이 semantic matching

단점:

- reference set 설계 품질에 민감

## 8. Strategy 4 — LLM-as-Router

작고 빠른 LLM이 query를 읽고 target model label을 출력합니다.

장점:

- intent/difficulty를 자연어 수준에서 이해
- prompt로 routing policy 수정 가능

단점:

- routing 자체가 추가 LLM call
- latency/cost 증가

## 9. Strategy 5 — Cascade Routing

가장 싼 model부터 시도하고 confidence가 낮으면 escalation합니다.

    query
      → small
         ├─ confident → return
         └─ uncertain
              → mid
                 ├─ confident → return
                 └─ uncertain
                      → frontier

장점:

- 대부분의 easy query를 cheap model에서 해결 가능

단점:

- hard query는 여러 model call을 순서대로 지불

## 10. Confidence 판단의 함정

원문은 confidence check로:

- self-rating
- verifier model
- heuristic

을 예로 듭니다.

하지만 LLM self-confidence는 calibration되지 않을 수 있습니다.

Production에서는:

- correctness predictor
- rule/checker
- task-specific verifier
- historical error rate

등으로 검증해야 합니다.

## 11. 원문의 Full Trace

### Query 1

    "What is 2 + 2?"

Router:

    small-llm

Latency 예:

    약 100 ms

### Query 2

3-line email summary.

Router:

    mid-llm

Latency 예:

    약 500 ms

### Query 3

Python Fibonacci bug.

Router:

    code-llm

Latency 예:

    약 700 ms

### Query 4

복잡한 medical multi-agent system design.

Router:

    frontier-llm

Latency 예:

    약 3 s

이 수치는 학습용 예제이지 provider benchmark가 아닙니다.

## 12. LLM Routing vs Mixture of Experts

원문 구분:

### LLM Routing

    query level
      → 여러 완전한 model 중 하나 선택

### Mixture of Experts

    token level
      → 하나의 model 내부에서 일부 expert subnetwork 선택

Concept은 비슷해도 architecture layer가 다릅니다.

## 13. Routing이 가치 있는 경우

- model별 가격차가 큼
- query 난이도 분산이 큼
- specialist model 존재
- request volume 큼
- quality fallback 가능

## 14. 흔한 실수

### Query length = difficulty라고 가정

짧은 math proof가 긴 email summary보다 어려울 수 있습니다.

### Router 평가 없이 도입

Routing accuracy와 end-to-end quality를 따로 측정해야 합니다.

### Frontier fallback 없음

Wrong route가 user-visible failure로 이어집니다.

### Cost만 최적화

Latency와 quality regression을 같이 봐야 합니다.

## 15. Evaluation

필수 metric:

- routing accuracy
- end-to-end task success
- quality delta vs all-frontier baseline
- cost/request
- latency
- escalation rate
- fallback rate

## 핵심 정리

- LLM Routing은 query마다 적절한 model을 선택해 cost, latency, quality를 균형 잡습니다.
- 원문은 Rule, Classifier, Embedding, LLM-as-Router, Cascade의 5가지 전략을 설명합니다.
- Router latency는 target LLM latency의 10% 이하를 실용적 기준으로 제시합니다.
- 원문 pricing example은 frontier와 small model 사이 약 30× cost gap입니다.
- MoE와 달리 LLM Routing은 query 단위로 완전한 model을 선택합니다.

## 원문

- https://outcomeschool.com/blog/llm-routing
