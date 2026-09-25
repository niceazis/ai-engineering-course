# Knowledge Distillation은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-knowledge-distillation-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문을 직접 확인해 Hard/Soft Label, Dark Knowledge, Temperature, KL 기반 distillation loss, 세 종류의 distillation을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Knowledge Distillation의 목표

Knowledge Distillation은 큰 **teacher model의 지식과 decision boundary를 더 작은 student model로 전달**하는 학습 방법입니다.

목적:

- mobile/edge deployment
- lower latency
- lower serving cost
- smaller memory
- teacher에 가까운 품질 유지

Student는 teacher weight를 복사하는 것이 아니라 **teacher의 output distribution과 내부 representation에서 학습**합니다.

## 2. Hard Label만으로 부족한 이유

일반 supervised training의 hard label:

    cat = 1
    dog = 0
    car = 0
    horse = 0

이 정보는 정답이 cat이라는 것만 알려 줍니다.

Teacher는 더 풍부한 정보를 갖습니다.

예:

    cat   = 0.90
    dog   = 0.08
    horse = 0.015
    car   = 0.005

여기에는:

- cat과 dog는 어느 정도 비슷함
- cat과 car는 거의 관련 없음

같은 class 관계가 들어 있습니다.

## 3. Dark Knowledge

원문은 hard label에 사라지는 teacher의 class relationship 정보를 **dark knowledge**라고 설명합니다.

Teacher가 dog에 8%, car에 거의 0%를 준다면, 단순 정답 label보다 더 많은 구조를 전달합니다.

Student가 teacher의 full probability distribution을 모방하면 작은 model이어도 더 좋은 representation을 배울 수 있습니다.

## 4. Teacher가 너무 확신하면?

Teacher output:

    cat = 0.99
    dog = 0.009
    car = 0.0005
    horse = 0.0005

처럼 너무 sharp하면 작은 probability에 담긴 dark knowledge가 거의 보이지 않습니다.

이를 부드럽게 만드는 것이 softmax temperature입니다.

## 5. Temperature Softmax

기본:

    p_i = exp(z_i) / sum_j exp(z_j)

Temperature T:

    p_i(T) = exp(z_i / T) / sum_j exp(z_j / T)

T > 1이면 distribution이 더 flat해집니다.

원문 수치:

### T = 1

    cat = 0.95
    dog = 0.04
    car = 0.005
    horse = 0.005

### T = 4

    cat = 0.70
    dog = 0.22
    car = 0.05
    horse = 0.03

이제 dog/car/horse 사이의 관계가 더 잘 드러납니다.

## 6. Teacher와 Student의 Soft Label 비교

Teacher:

    [0.70, 0.22, 0.05, 0.03]

Student:

    [0.50, 0.30, 0.15, 0.05]

두 distribution의 차이를 KL divergence 등으로 측정합니다.

    L_distill = KL(p_teacher^T || p_student^T)

실제 formulation은 framework마다 direction/scaling이 다를 수 있지만 핵심은 teacher distribution을 student가 따라가게 하는 것입니다.

## 7. Hard Label Loss도 함께 쓰는 이유

Teacher도 틀릴 수 있습니다.

Student가 teacher만 무조건 복제하면 teacher error도 따라 배웁니다.

그래서 원문은 두 loss를 섞습니다.

    Total Loss
      = alpha * Distillation Loss
      + (1-alpha) * Normal Loss

- Distillation Loss: teacher soft label과 student 비교
- Normal Loss: ground-truth hard label과 student 비교

Hard label이 student를 실제 truth에 anchor합니다.

## 8. Step-by-Step Training

1. 큰 teacher model 준비
2. 작은 student model 준비
3. 같은 input을 teacher와 student에 넣음
4. 높은 T로 teacher soft labels 생성
5. 같은 T로 student probabilities 계산
6. KL 등 distillation loss 계산
7. 정상 T에서 ground-truth loss 계산
8. 두 loss weighted sum
9. student parameter만 update
10. dataset 전체 반복

Teacher는 일반적으로 freeze합니다.

## 9. Temperature Scaling 주의

Original distillation literature에서는 gradient scale을 보정하기 위해 distillation term에 T²를 곱하는 formulation이 자주 사용됩니다.

개념:

    L = alpha * T^2 * KL(...)
        + (1-alpha) * CE(...)

Outcome School의 학습 포인트는 **높은 T가 작은 probability 관계를 드러낸다**는 것입니다.

Inference에서는 다시 T=1 수준의 정상 output을 사용합니다.

## 10. Response-Based Distillation

Student가 teacher의 최종 output/logits를 모방합니다.

가장 단순하고 흔한 형태입니다.

LLM에서는 teacher가 만든 response를 SFT data로 사용하거나 token-level logits를 따라가는 방식으로 확장할 수 있습니다.

## 11. Feature-Based Distillation

Teacher의 intermediate hidden representation을 student가 맞춥니다.

예:

    teacher layer 24 hidden
      ↔ projected student layer 8 hidden

단점:

- dimension/layer mapping 필요
- loss design 복잡

장점:

- output만으로는 보이지 않는 internal representation을 전달 가능

## 12. Relation-Based Distillation

개별 example의 output보다 example 간 관계를 전달합니다.

예:

- embedding distance
- attention relationship
- pairwise similarity

Student가 teacher의 representation geometry를 학습합니다.

## 13. LLM Distillation

Modern LLM distillation에서는 다양한 방식이 섞입니다.

### Response Distillation

큰 teacher가 instruction-response data를 생성하고 작은 student가 SFT.

### Logit Distillation

Token별 teacher probability/logits를 따라감.

### Reasoning Distillation

Teacher의 reasoning trajectory 또는 compressed rationale로 student를 학습.

### On-Policy Distillation

Student가 자기 trajectory를 만들고 teacher가 그 상태에서 distribution을 제공.

Module 5의 DeepSeek-V4 OPD와 연결됩니다.

## 14. 장점

- model size 감소
- latency 감소
- edge deployment 가능
- teacher보다 저렴한 serving
- hard label만 학습하는 것보다 richer supervision

## 15. 한계

- teacher bias/error 전이
- student capacity가 너무 작으면 underfit
- teacher inference/data generation cost
- logit access가 없는 proprietary API에서는 response distillation만 가능할 수 있음
- distribution mismatch

## 16. Distillation vs Quantization

Distillation:

    큰 model의 behavior를 작은 model architecture에 학습

Quantization:

    같은 model weight를 낮은 precision으로 저장/계산

둘을 결합할 수 있습니다.

    teacher
      → distilled student
      → quantized student

## 핵심 정리

- Distillation은 teacher의 soft output과 dark knowledge를 student에 전달합니다.
- 높은 softmax temperature는 class 간 작은 probability 관계를 드러냅니다.
- 원문 cat 예에서 T=1의 0.95/0.04/...가 T=4에서 0.70/0.22/...로 부드러워집니다.
- Distillation loss와 hard-label loss를 섞어 teacher 지식과 ground truth를 동시에 학습합니다.
- Response/feature/relation distillation이 대표 유형입니다.
- 작은 student의 capacity와 teacher quality가 최종 한계입니다.

## 원문

- https://outcomeschool.com/blog/how-does-knowledge-distillation-work
