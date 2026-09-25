# Cloud vs On-device Model Deployment — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/cloud-vs-on-device-model-deployment  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문 URL은 현재 직접 열리지 않았습니다. Outcome School 공식 2026-08-08 뉴스레터의 핵심 설명과 공개된 원문 캐시의 구체 예제를 교차검증해 독립적으로 재구성했습니다. 직접 검증하지 못한 문장을 원문이라고 단정하지 않습니다.

## 1. Deployment란?

Training이 끝난 model을 실제 사용자 request를 처리할 수 있는 위치에 두는 것이 deployment입니다.

큰 선택은 두 가지입니다.

### Cloud

    user data
      → network
      → remote server/model
      → response

### On-device

    model
      → user's phone/laptop/car
      → local inference

Outcome School 공식 요약은 차이를 한 문장으로 정리합니다.

    Cloud: data가 model로 이동
    On-device: model이 data로 이동

## 2. Training vs Inference

Training은 model weight를 학습하는 단계이고 deployment는 주로 inference를 어디서 실행할지 결정하는 문제입니다.

Cloud와 on-device는 같은 model architecture라도 latency, privacy, cost, update 방식이 크게 달라집니다.

## 3. Cloud Deployment

장점:

- 큰 GPU/TPU 사용 가능
- frontier model 운영 가능
- model update가 중앙에서 즉시 반영
- client hardware 제약이 적음

단점:

- network round trip
- server cost
- privacy/data transfer
- offline 불가

## 4. On-device Deployment

장점:

- network latency 없음
- offline 가능
- raw data가 device 밖으로 안 나갈 수 있음
- per-request cloud compute 비용 감소

단점:

- memory/compute 제한
- battery/thermal
- model size 제한
- update 배포 필요

## 5. Round Trip 문제

Cloud inference latency:

    upload
    + network
    + server queue
    + inference
    + download

으로 구성됩니다.

실시간 control에서는 network delay가 치명적일 수 있습니다.

## 6. 원문의 자율주행 예

공개 원문 캐시는 시속 100km로 움직이는 자동차가 cloud 판단을 200ms 기다리면 약 5m 이동한다고 설명합니다.

    100 km/h
      ≈ 27.8 m/s

    0.2 s
      → 약 5.6 m

Network가 2초 끊기면 50m 이상 이동할 수 있습니다.

이런 safety-critical workload는 local inference가 필수적일 수 있습니다.

## 7. Privacy

On-device:

    camera/audio/keyboard data
      → local model

Cloud:

    data
      → server

민감한 data를 cloud로 보내지 않는 것이 제품 요구사항이라면 on-device의 가치가 커집니다.

하지만 local inference도 device compromise나 logging 문제까지 자동 해결하는 것은 아닙니다.

## 8. Model Size

Cloud는 large accelerator cluster를 사용할 수 있어 훨씬 큰 model을 실행할 수 있습니다.

On-device에서는:

- quantization
- pruning
- distillation
- small language model

이 중요합니다.

## 9. 비용 부담

Cloud:

    provider/company가 inference compute 비용 부담

On-device:

    사용자의 device compute와 battery를 사용

대규모 consumer product에서는 request volume에 따라 cloud cost가 매우 커질 수 있습니다.

## 10. Shipping / Update 문제

Cloud model은 server version을 바꾸면 전체 사용자에게 즉시 적용됩니다.

On-device model은 application/model file을 device에 새로 배포해야 합니다.

Version fragmentation, download size, rollback을 관리해야 합니다.

## 11. Network가 없을 때

- face unlock
- keyboard suggestion
- noise cancellation
- camera effect

같은 feature는 offline availability가 중요합니다.

원문 공식 요약은 instant, private, offline 요구가 강하면 on-device를 우선한다고 설명합니다.

## 12. Hybrid Approach

실전에서는 둘 중 하나만 선택할 필요가 없습니다.

    simple/private/fast task
      → on-device small model

    hard reasoning
      → cloud large model

Router가 complexity, privacy, connectivity를 보고 선택할 수 있습니다.

## 13. 선택 기준

### On-device 우선

- latency가 매우 중요
- offline 필수
- sensitive raw data
- workload가 작은 model로 해결 가능

### Cloud 우선

- maximum intelligence
- very large model
- centralized updates
- heavy compute

### Hybrid

두 조건이 모두 중요할 때.

## 핵심 정리

- Cloud는 data가 model로, on-device는 model이 data로 이동합니다.
- On-device는 latency, privacy, offline에 강하고 cloud는 model capability와 centralized operations에 강합니다.
- 원문 자율주행 예는 100km/h에서 200ms 지연만으로 약 5m 이상 이동할 수 있음을 보여 줍니다.
- 실제 제품에서는 small local model + large cloud model의 hybrid routing이 실용적입니다.
- 원문 URL을 직접 열지 못한 부분은 Outcome School 공식 뉴스레터와 공개 캐시로만 교차검증했습니다.

## 원문

- https://outcomeschool.com/blog/cloud-vs-on-device-model-deployment
