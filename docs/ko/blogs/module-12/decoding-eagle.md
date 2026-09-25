# EAGLE이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/decoding-eagle  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 Outcome School 원문 본문은 웹 캐시에서 직접 열리지 않았습니다. 공식 Module 12 목차와 EAGLE/EAGLE-2 원 논문을 교차검증해 작성하며, 논문 수치를 Outcome School 원문 고유 수치로 단정하지 않습니다.

## 1. Token-Level Draft의 문제

Separate small model이 future token을 바로 예측하면 target model의 hidden representation 차이 때문에 acceptance가 제한될 수 있습니다.

EAGLE은 관점을 바꿉니다.

> token 자체보다 target model의 상위 hidden feature를 autoregressive하게 예측한다.

## 2. Feature-Level Draft

EAGLE은 target model의 **second-to-top-layer feature**를 예측하는 lightweight drafter를 학습합니다.

그 feature를 target LM head에 넣어 token proposal을 얻습니다.

Feature space가 future dynamics를 예측하기 더 쉽다는 관찰이 핵심입니다.

## 3. Feature Uncertainty

Feature만 예측하면 다음 token identity에서 생기는 uncertainty가 누적됩니다.

EAGLE은 한 step 앞선 token sequence도 input으로 같이 제공해 uncertainty를 줄입니다.

즉:

    previous features
    + shifted token
      → future feature

## 4. Verification

Drafted token sequence는 target model이 병렬 검증합니다.

원 논문은 output distribution을 target model과 동일하게 유지하는 lossless speculative sampling을 목표로 합니다.

## 5. 공개 EAGLE 결과

EAGLE 원 논문은 LLaMA2-Chat 70B에서:

    latency speedup = 2.7× ~ 3.5×
    throughput ≈ 2×

를 보고합니다.

Task/model마다 달라집니다.

## 6. EAGLE-2

EAGLE 1은 static draft tree를 사용합니다.

EAGLE-2는 draft model의 confidence가 context별 acceptance rate를 잘 예측한다는 점을 이용해 **dynamic draft tree**를 만듭니다.

High-confidence branch에 더 많은 draft budget을 배정합니다.

## 7. EAGLE-2 공개 결과

논문/ACL 공개 자료는 여러 model/task에서 EAGLE-1보다 20~40% 빠른 수준과 최대 약 5× 사례를 보고합니다.

이는 특정 benchmark 결과이며 production speedup을 보장하지 않습니다.

## 8. Medusa와 비교

Medusa:

    extra future-token heads

EAGLE:

    future hidden feature drafter

두 방식 모두 separate full draft model의 비용을 줄이려는 speculative decoding 변형입니다.

## 9. Trade-off

- extra training/artifact
- runtime integration
- draft-tree scheduling
- target-model-specific adaptation

Acceptance가 낮은 workload에서는 이득이 줄 수 있습니다.

## 핵심 정리

- EAGLE은 token이 아니라 target model 상위 hidden feature를 draft합니다.
- Shifted token input으로 feature uncertainty를 줄입니다.
- EAGLE-2는 context-aware dynamic draft tree를 사용합니다.
- 공개 논문은 2.7~3.5× 등 큰 speedup을 보고하지만 workload에 따라 달라집니다.
- Outcome School 원문 본문은 직접 확인하지 못했으므로 원 논문과 공식 module outline으로만 보완했습니다.

## 원문

- https://outcomeschool.com/blog/decoding-eagle
