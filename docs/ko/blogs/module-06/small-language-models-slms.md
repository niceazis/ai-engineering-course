# Small Language Model(SLM)이란 무엇이며 언제 사용해야 하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/small-language-models-slms  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-05-11 공개 원문을 직접 확인해 크기 기준, 대표 모델, 비용·latency·memory 수치, use case, hybrid routing 예를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. SLM의 정의

원문은 SLM을 다음처럼 정의합니다.

> 충분히 작아서 저렴하고 빠르게 실행할 수 있고, 노트북이나 휴대폰에서도 돌릴 수 있으면서 많은 실제 task에는 충분한 language model.

핵심은 단순히 parameter 수가 적다는 것보다 **deployment trade-off를 의도적으로 선택한 모델**이라는 점입니다.

    일부 general knowledge / deep reasoning
      ↔ speed / cost / privacy / local deployment

## 2. 어느 정도가 Small인가

원문은 엄격한 표준이 없다고 전제하고 대략 다음 구간을 사용합니다.

- SLM: 보통 0.5B~약 10B
- 중간 회색지대: 10B~30B
- LLM: 대략 30B 이상
- frontier: 70B, 400B, 또는 그 이상

“Small”은 시대에 따라 움직이는 상대적 기준입니다.

## 3. Language Model 복습

Language model은 이전 token을 조건으로 다음 token을 예측합니다.

    "The sky is"
      → "blue"

생성된 token을 다시 입력에 붙여 반복합니다.

Parameter는 training으로 학습된 숫자입니다.

원문 예:

- 1B = 1,000,000,000 parameters
- 70B = 70배 많은 parameter

Parameter가 많으면 더 많은 pattern·fact·reasoning shortcut을 담을 capacity가 커질 수 있지만, 크기만으로 품질이 결정되지는 않습니다.

## 4. 원문의 대표 SLM

원문 표의 주요 예:

| Model | Size | 특징 |
| --- | ---: | --- |
| Phi-4-mini | 3.8B | reasoning, 128K context |
| Gemma 4 E2B | 2B effective | phone, multimodal, 128K |
| Gemma 4 E4B | 4B effective | edge, 128K |
| Llama 3.2 | 1B / 3B | mobile/edge, 128K |
| Qwen 3.5 | 0.8B / 2B / 4B / 9B | 최대 256K |
| SmolLM3 | 3B | open instruct/reasoning, 128K |

모델 사양은 버전별로 달라질 수 있으므로 실제 배포에서는 model card를 다시 확인해야 합니다.

## 5. 작은 모델이 과거보다 강해진 이유

원문은 세 가지를 강조합니다.

### 1) Better Data

무작정 internet 전체를 넣는 대신 filtering·cleaning을 강화합니다.

원문은 현대 SLM training 규모를 대략 1T~15T high-quality tokens 범위로 예시합니다.

### 2) Better Training

- knowledge distillation
- 더 좋은 optimizer
- 더 긴 training

으로 parameter 하나당 성능을 높입니다.

### 3) Better Architecture

- GQA
- RoPE
- 효율적인 attention/FFN 선택

같은 architecture 개선을 사용합니다.

## 6. 비용

원문은 1M output tokens의 매우 거친 예를 듭니다.

- frontier API: 약 $25
- self-hosted 3B SLM: 약 $0.10~$0.20의 electricity/hardware time

대략 100~200배 차이 예입니다.

100M tokens/day라면 원문 계산 예:

- frontier: $2,500/day
- SLM self-hosted: 약 $15/day

실제 비용은 GPU 가격, utilization, API price에 따라 크게 달라집니다.

## 7. Latency

원문 예:

- 70B on single GPU: TTFT 약 2초
- 3B on same hardware: 약 100ms

약 20배 차이의 교육용 예입니다.

Voice assistant나 interactive UI에서는 수백 ms가 체감 품질을 크게 바꿉니다.

## 8. Privacy와 On-Device

SLM은 local execution이 가능해:

- 의료 데이터
- 금융 정보
- 사내 문서
- offline use

에서 cloud 전송을 피할 수 있습니다.

원문은:

- 3B → modern phone
- 1B → small laptop CPU
- 0.5B → tiny edge device

가능성을 예로 들고 GGUF + llama.cpp 같은 배포 경로를 연결합니다.

## 9. Fine-Tuning

원문 비교:

- 70B fine-tuning → 큰 GPU 자원
- 3B fine-tuning → single consumer GPU에서도 현실적

작은 domain model을 자체 데이터로 빠르게 반복 학습할 수 있다는 것이 중요한 장점입니다.

## 10. Reliability와 Control

Self-hosting하면:

- external API outage
- rate limit
- 갑작스러운 가격 변경

의존도가 줄어듭니다.

다만 model operation, security update, observability 책임은 직접 가져옵니다.

## 11. SLM vs LLM

원문 표의 핵심 범위:

| 관점 | SLM | LLM |
| --- | --- | --- |
| Parameters | 0.5B~약 10B | 30B~400B+ |
| Memory | 1~18GB | 60~800GB+ |
| Hardware | phone/laptop/single GPU | multi-GPU server |
| TTFT | 약 50~200ms | 약 500ms~3s |
| 1M output 비용 | 약 $0.10~$1 | 약 $5~$30 |
| General knowledge | 제한적 | 넓음 |
| Complex reasoning | 약~중간 | 강함 |
| Privacy | local이 쉬움 | cloud 의존 가능 |

모두 원문의 이해용 범위이며 실제 수치는 모델/정밀도/hardware에 따라 달라집니다.

## 12. 크기 Spectrum

원문:

    Tiny       <0.5B
    SLM        0.5B~10B
    Mid        10B~30B
    Large      30B~70B
    Frontier   100B~1T+

이는 공식 산업 표준이 아니라 실용적 구분입니다.

## 13. On-Device Assistant

원문 예:

1B model:

- memory 약 2GB
- modern phone 약 30 tokens/s

수준의 illustrative deployment를 제시합니다.

Writing assistant, code helper, offline chat이 대표 예입니다.

## 14. Classification

Support ticket:

    billing
    technical
    account

처럼 label을 고르는 task는 큰 LLM이 필요하지 않을 수 있습니다.

원문은 fine-tuned 0.5B model이 single CPU에서 매우 높은 throughput을 낼 수 있다는 예를 듭니다.

## 15. Structured Extraction

Email에서:

- sender
- date
- action item
- deadline

을 JSON으로 뽑는 narrow task는 SLM과 constrained decoding이 잘 맞습니다.

## 16. Agent Task Heads

Agent의 모든 step에 최고가 LLM을 호출하는 대신:

- routing
- tool selection
- formatting
- relevance classification

같은 작은 판단을 SLM에 맡깁니다.

Hard reasoning에만 큰 model을 호출합니다.

## 17. Domain Fine-Tuning

원문 예:

3B SLM을 특정 legal contract domain의 10,000 examples로 fine-tune하면 generic 70B보다 **그 좁은 domain task**에서 더 나을 수 있습니다.

핵심은 general capability가 아니라 task-distribution fit입니다.

## 18. High-Volume Pipeline

원문 illustrative example:

- 10M customer reviews/day
- LLM API 약 $10,000/day
- self-hosted SLM 약 $100/day

실제 비용 산정 전에는 token size와 hardware utilization을 재계산해야 합니다.

## 19. SLM의 한계

### General Knowledge

작은 capacity 때문에 rare facts에 약합니다.

### Complex Reasoning

긴 수학 chain, 복잡한 planning에서 frontier model보다 약할 수 있습니다.

### Long Context Quality

128K를 “지원”해도 100K context 안의 evidence를 제대로 활용하는 quality는 큰 model보다 낮을 수 있습니다.

### Prompt Fragility

작은 phrasing 변화에 더 민감할 수 있습니다.

### Long-form Writing

긴 창작/일관성에서 큰 model과 차이가 날 수 있습니다.

## 20. 언제 SLM을 선택할까

원문 권장 조건:

- narrow task
- millions of calls/day
- under 200ms latency 필요
- private data
- offline/on-device
- fine-tuning data 보유

LLM:

- deep multi-step reasoning
- broad knowledge
- highest possible quality

## 21. Hybrid Pattern

원문 예:

    Input
      → SLM router
         ├─ simple 90% → SLM
         └─ complex 10% → LLM

모든 request에 비싼 LLM을 쓰지 않고 난이도에 따라 route합니다.

이 패턴이 Module 16의 LLM Routing과 직접 연결됩니다.

## 핵심 정리

- SLM은 보통 10B 미만을 가리키지만 절대 기준은 아닙니다.
- 현대 SLM은 better data, distillation, architecture 개선으로 과거보다 훨씬 강해졌습니다.
- 비용, latency, privacy, local deployment에서 강합니다.
- 복잡한 reasoning·broad knowledge·long-context 활용은 상대적 약점입니다.
- Narrow/high-volume task에서는 작은 model부터 검증하는 것이 합리적입니다.
- SLM+LLM hybrid routing은 비용과 품질을 동시에 조절하는 실용적 구조입니다.

## 원문

- https://outcomeschool.com/blog/small-language-models-slms
