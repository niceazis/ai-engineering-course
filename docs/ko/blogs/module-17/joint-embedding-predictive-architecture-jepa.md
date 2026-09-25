# JEPA(Joint Embedding Predictive Architecture)란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/joint-embedding-predictive-architecture-jepa  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-06-07 공개 원문을 직접 확인해 인간 학습 비유, raw-pixel prediction과 contrastive learning의 한계, JEPA building block, energy view, I-JEPA, V-JEPA와 world-model 연결을 원문 순서대로 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 인간은 세상을 어떻게 배우는가

원문은 아기가 컵을 테이블 끝으로 밀다가 떨어지는 장면을 관찰하는 예로 시작합니다.

아기는 누군가가 공식을 가르쳐 주지 않아도:

    edge를 넘으면 물체가 떨어진다

는 규칙을 관찰에서 학습합니다.

핵심 질문은:

> Machine도 raw observation만 보고 세상의 구조를 배울 수 있는가?

입니다.

## 2. Yann LeCun의 Autonomous Machine Intelligence 비전

원문은 2022년 Yann LeCun의 Autonomous Machine Intelligence 비전을 소개합니다.

목표는 단순 pattern matching이 아니라:

- world를 관찰
- 내부 representation 학습
- future를 예측
- goal을 향해 plan

할 수 있는 system입니다.

JEPA는 이 비전의 핵심 building block 중 하나로 설명됩니다.

## 3. 가려진 사진 비유

거리 사진의 오른쪽 절반을 가렸다고 합시다.

왼쪽에는:

- dog
- grass
- tree

가 보입니다.

사람은 hidden half의 exact pixel은 모르지만:

- grass가 이어질 것
- tree 일부가 있을 것
- dog tail이 이어질 수 있음

같은 gist는 예상할 수 있습니다.

JEPA의 핵심은 **exact pixel이 아니라 hidden part의 meaning/representation을 예측**하는 것입니다.

## 4. JEPA의 이름

JEPA:

    Joint
    Embedding
    Predictive
    Architecture

### Joint

Context와 target 두 부분을 함께 다룹니다.

### Embedding

Raw data를 의미 있는 compact representation으로 바꿉니다.

### Predictive

Visible context representation에서 hidden target representation을 예측합니다.

### Architecture

이 흐름을 구현하는 전체 design입니다.

## 5. Embedding Space

Image의 raw pixel은 수백만 개 값입니다.

Embedding은 그중 task-relevant meaning을 압축한 vector입니다.

예:

    dog image
      → representation

비슷한 dog image는 embedding space에서 가깝고 car image는 멀리 위치할 수 있습니다.

JEPA는 pixel space보다 이 representation space에서 예측합니다.

## 6. Raw Pixel Prediction의 문제

Hidden image를 pixel-by-pixel 복원하려면:

- exact grass texture
- random noise
- lighting detail
- tiny shadows

까지 맞혀야 합니다.

이 정보는 context만으로 예측할 수 없는 경우가 많습니다.

원문 비유:

> 사진을 기억만으로 먼지 한 점까지 똑같이 다시 그리라는 것과 비슷하다.

즉 model capacity를 predictable semantics보다 unpredictable detail에 낭비할 수 있습니다.

## 7. Contrastive Learning의 문제

Contrastive method는:

    same object views
      → close

    different examples
      → far

를 학습합니다.

원문이 지적하는 부담:

- negative examples
- data augmentation
- carefully designed transformations

JEPA는 negative-pair engineering 없이 prediction objective로 representation을 학습하려 합니다.

## 8. JEPA의 핵심 아이디어

Generative model:

    visible
      → hidden pixels를 생성

JEPA:

    visible representation
      → hidden representation을 예측

즉:

> predictable meaning만 맞히고 unpredictable pixel detail은 무시한다.

이 때문에 JEPA는 원문에서 non-generative라고 설명됩니다.

## 9. Building Block

원문 conceptual notation:

- x: visible context
- y: hidden target
- x-encoder: context representation s_x
- y-encoder: target representation s_y
- predictor: s_x에서 target representation 예측
- position: 어느 hidden region을 예측하는지 알려 줌
- latent variable z: context만으로 결정되지 않는 uncertainty를 표현

흐름:

    visible x
      → x-encoder
      → s_x
      → predictor + target position
      → predicted target representation

    hidden y
      → y-encoder
      → actual target representation

    predicted vs actual
      → error

## 10. Energy-Based View

원문은 energy를 wrongness score로 설명합니다.

    low energy
      = predicted representation과 target representation이 가까움

    high energy
      = 둘이 멂

Training은 matching context-target pair의 energy를 낮추는 방향입니다.

## 11. I-JEPA

I-JEPA는 image에 JEPA를 적용합니다.

흐름:

1. Image를 ViT patch로 나눔
2. Large context block 선택
3. 여러 target block 선택
4. Target patch는 context에서 제거
5. Context encoder가 visible part representation 생성
6. Target encoder가 full image representation을 생성한 뒤 target 위치 representation 추출
7. Predictor가 context + target position으로 target representation 예측
8. Predicted representation과 target representation을 비교

## 12. Representation Collapse

두 encoder가 모두 자유롭게 update되면 모든 input에 똑같은 representation을 출력해 loss를 쉽게 낮출 수 있습니다.

이를 representation collapse라고 합니다.

## 13. EMA Target Encoder

원문은 I-JEPA가 collapse를 막기 위해 asymmetric design을 사용한다고 설명합니다.

- context encoder: normal gradient update
- target encoder: context encoder의 slow EMA copy
- target side: stop-gradient

즉 target encoder가 고정된 answer key처럼 천천히 따라오게 합니다.

## 14. I-JEPA Training Scale

원문은 large I-JEPA가 ImageNet raw image를 label 없이 사용해:

    16 GPUs
    under 72 hours

에 학습된 예를 언급합니다.

이는 해당 experiment 조건의 수치이며 모든 JEPA training의 일반 비용을 뜻하지 않습니다.

## 15. V-JEPA

V-JEPA는 같은 아이디어를 video에 확장합니다.

Video 일부 region/time span을 숨기고 visible part에서 hidden representation을 예측합니다.

Pixel generation 없이 temporal/world dynamics representation을 학습합니다.

## 16. V-JEPA 2와 World Model

원문은 V-JEPA 2가 robot control/world-model vision과 연결된다고 설명합니다.

Goal image를 주고:

- current observation
- imagined outcome
- action planning

을 representation space에서 수행하는 방향입니다.

## 17. JEPA가 중요한 이유

- pixel-level unpredictable detail을 버림
- semantic representation 학습에 집중
- negative example 의존 감소
- self-supervised raw data 활용
- image/video/world model로 확장 가능

## 핵심 정리

- JEPA는 visible part의 embedding에서 hidden part의 embedding을 예측합니다.
- Raw pixel 생성보다 semantic prediction에 집중합니다.
- Contrastive learning의 negative-pair/augmentation 부담을 줄이는 방향입니다.
- I-JEPA는 context encoder와 EMA target encoder를 비대칭으로 사용해 collapse를 막습니다.
- V-JEPA는 video/world dynamics representation으로 확장됩니다.

## 원문

- https://outcomeschool.com/blog/joint-embedding-predictive-architecture-jepa
