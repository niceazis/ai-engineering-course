# LPU는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-an-lpu-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문 URL은 현재 직접 열리지 않았습니다. Outcome School의 공식 2026-09-05 뉴스레터와 공식 inference-engineering lesson index에서 확인한 설명 순서인 memory bottleneck, on-chip SRAM, ahead-of-time compiler scheduling, deterministic network, assembly-line execution을 기준으로 독립적으로 재구성했습니다. 직접 확인하지 못한 세부 수치는 원문 내용으로 단정하지 않습니다.

## 1. LPU란?

Outcome School은 LPU, Language Processing Unit를 이미 학습된 large language model을 매우 빠르게 추론하는 데 초점을 둔 processor로 설명합니다.

Training보다 token generation latency와 throughput 최적화가 중심입니다.

## 2. LLM Decode의 진짜 병목

한 output token을 만들 때 model은 큰 weight를 반복해서 읽어야 합니다.

Modern accelerator에서는 arithmetic 자체보다 weight와 activation 이동, memory bandwidth, synchronization이 bottleneck이 될 수 있습니다.

즉 FLOPS가 높아도 data가 compute unit에 늦게 도착하면 chip은 기다립니다.

## 3. Idea 1 — Model을 Chip 가까이에

Outcome School 공식 newsletter는 LPU의 핵심을 external memory에서 계속 weight를 가져오지 말고 SRAM처럼 chip 가까운 memory를 적극 활용하는 방향으로 설명합니다.

목표는 data movement latency를 줄이는 것입니다.

## 4. On-Chip Memory의 한계

SRAM은 빠르지만 매우 비싸고 용량이 작습니다.

Large model 전체를 한 chip SRAM에 넣는 것은 어렵기 때문에 여러 chip에 model을 나누고 각 chip이 자기 부분을 보유하도록 구성할 수 있습니다.

## 5. Idea 2 — Compiler가 실행을 미리 계획

LPU-style architecture는 compiler가 어느 operation을 어느 chip/unit에서 어느 cycle에 어떤 data와 함께 실행할지를 ahead of time에 정해 runtime overhead를 줄이는 방향을 택합니다.

## 6. Deterministic Execution

LLM layer graph는 inference 시 구조가 반복적입니다.

이 특성을 이용해 runtime decision을 줄이고 deterministic schedule을 만들면 queueing, synchronization, scheduling overhead를 줄일 수 있습니다.

## 7. Idea 3 — 기다리지 않는 Network

여러 chip이 model layer나 partition을 나눠 처리하면 chip 간 communication이 필요합니다.

Outcome School 공식 설명은 shared clock과 deterministic network를 통해 communication wait를 최소화하는 assembly-line 구조를 강조합니다.

## 8. Assembly Line

개념:

    Chip 1 → Chip 2 → Chip 3 → ... → Chip N

각 chip이 model의 자기 부분을 처리하고 결과를 다음 stage로 전달합니다.

Pipeline이 차면 여러 token/request가 서로 다른 stage에서 동시에 처리될 수 있습니다.

## 9. Prompt가 들어오면

1. Prompt tokenization
2. Prefill 계산
3. Model partition을 따라 data 이동
4. 각 chip이 자기 operation 수행
5. Logits 생성
6. Next token 선택
7. Decode loop 반복

핵심은 scheduling과 data movement를 최대한 예측 가능하게 만드는 것입니다.

## 10. LPU가 잘 맞는 경우

- already-trained LLM inference
- low latency token generation
- stable model graph
- high-throughput serving

## 11. 덜 맞는 경우

- arbitrary GPU workload
- training
- custom dynamic kernels
- rapidly changing operator support

Specialized architecture의 장점은 곧 flexibility의 trade-off입니다.

## 12. LPU vs GPU

| 항목 | GPU | LPU식 접근 |
| --- | --- | --- |
| 목적 | 범용 parallel compute | LLM inference 특화 |
| Runtime flexibility | 높음 | 낮고 deterministic |
| Memory | HBM 중심 | on-chip/local memory 적극 활용 |
| Scheduling | dynamic capability 큼 | ahead-of-time 강조 |
| Training | 강함 | inference 중심 |

## 핵심 정리

- LPU는 LLM inference의 memory movement와 scheduling overhead를 줄이는 데 초점을 둔 architecture입니다.
- Outcome School 공식 설명의 핵심은 on-chip SRAM, compiler preplanning, deterministic interconnect, assembly-line execution입니다.
- GPU보다 specialization을 높여 inference latency를 줄이는 대신 flexibility를 희생합니다.
- 원문 페이지를 직접 열지 못했기 때문에 특정 benchmark 수치는 원문 값으로 재현하지 않았습니다.

## 원문

- https://outcomeschool.com/blog/how-does-an-lpu-work
