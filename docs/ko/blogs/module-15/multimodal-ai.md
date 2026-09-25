# Multimodal AI란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/multimodal-ai  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-05-10 공개 원문을 직접 확인해 modality 정의, shared embedding space, 세 가지 대표 유형과 실제 활용·실패 요인을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Multimodal AI란?

Multimodal AI는 하나의 데이터 형식만 처리하지 않고 **텍스트, 이미지, 음성, 영상 등 서로 다른 modality를 함께 이해하거나 생성하는 AI 시스템**입니다.

대표 modality:

- Text
- Image
- Audio
- Video
- Sensor / structured data

핵심은 단순히 여러 파일 형식을 입력받는 것이 아니라, 서로 다른 modality의 정보를 **같은 문제를 푸는 하나의 의미 공간에서 연결**하는 것입니다.

## 2. Unimodal vs Multimodal

Unimodal 시스템은 한 종류의 입력만 처리합니다.

예:

    text → text classifier

Multimodal 시스템은 다음처럼 여러 신호를 결합할 수 있습니다.

    image + text
      → question answering

    audio + video
      → event understanding

    text
      → image generation

## 3. 왜 필요한가

현실의 정보는 본래 multimodal입니다.

예를 들어 상품 페이지에는 이미지, 제목, 설명, 가격, 리뷰가 함께 있습니다.

Image만 보거나 text만 보면 일부 정보가 빠집니다.

Multimodal AI는 여러 modality를 결합해 더 완전한 representation을 만들 수 있습니다.

## 4. 전체 동작 방식

원문의 큰 흐름:

    each modality
      → modality-specific encoder
      → shared / aligned representation
      → multimodal model
      → output

예:

    image → vision encoder ┐
                           ├→ shared embedding / fusion → answer
    text  → text encoder  ┘

각 encoder는 입력 특성에 맞는 representation을 만들고, fusion/alignment 단계가 modality 간 관계를 학습합니다.

## 5. Shared Embedding Space

텍스트 "cat"과 실제 고양이 사진이 서로 가까운 vector가 되도록 학습할 수 있습니다.

개념:

    text("cat")  ─┐
                  ├─ nearby vectors
    image(cat)   ─┘

반면 자동차 이미지는 멀리 떨어집니다.

이 alignment가 cross-modal retrieval의 기반입니다.

## 6. CLIP 식 Contrastive Alignment

CLIP 계열은 같은 image-text pair를 가까이, 관계없는 pair를 멀리 두도록 학습합니다.

Batch에 여러 image-caption pair가 있으면:

    correct image-text pair
      → similarity ↑

    incorrect pair
      → similarity ↓

이렇게 image encoder와 text encoder가 같은 semantic space를 공유하게 됩니다.

## 7. 유형 1 — Multimodal Understanding

여러 modality를 받아 하나의 판단이나 답을 만듭니다.

예:

    image + question
      → visual question answering

대표 task:

- Visual Question Answering
- document understanding
- video understanding
- chart/table interpretation

## 8. 유형 2 — Cross-Modal Generation

한 modality를 조건으로 다른 modality를 생성합니다.

예:

    text → image
    text → audio
    image → text caption

Text-to-image diffusion model도 이 범주에 들어갑니다.

## 9. 유형 3 — Cross-Modal Alignment / Retrieval

한 modality로 다른 modality를 검색합니다.

예:

    text: "beach at sunset"
      → image embedding search
      → matching photos

Image embedding 레슨과 직접 연결됩니다.

## 10. Fusion 방식

### Early Fusion

여러 modality feature를 비교적 이른 단계에서 결합합니다.

장점은 modality 간 세밀한 interaction이고, 단점은 입력 형식·길이가 크게 다르면 구현이 복잡하다는 점입니다.

### Late Fusion

각 modality를 독립적으로 처리한 뒤 score/representation을 나중에 결합합니다.

Modular하고 각 encoder를 따로 최적화하기 쉽습니다.

### Cross-Attention

한 modality의 token이 다른 modality representation을 attention하도록 합니다.

현대 vision-language model에서 흔한 형태입니다.

## 11. 실제 사례

- 이미지 질문 답변
- 의료 영상 + 임상 텍스트
- 음성 assistant
- product image + description 검색
- video captioning
- autonomous system의 camera/sensor fusion

## 12. 흔한 오해

### Multimodal = Text + Image만

Text-image가 가장 유명하지만 audio, video, sensor, structured data도 modality입니다.

### Modality를 많이 넣을수록 좋다

불필요한 modality는 latency, inference cost, alignment 난도, noise를 늘립니다.

추가 modality가 실제 task metric을 개선하는지 평가해야 합니다.

## 13. Alignment 실패

Image encoder와 text encoder가 같은 개념을 일관되게 표현하지 못하면 cross-modal search나 reasoning이 실패합니다.

특히 domain-specific image, rare object, multilingual text, OCR-heavy document에서는 alignment quality를 별도로 검증해야 합니다.

## 14. 평가

전체 score 하나만 보면 부족합니다.

- text-only subset
- image-only subset
- text+image subset
- conflicting-modality case
- missing-modality case

를 나눠 평가해야 어떤 component가 문제인지 알 수 있습니다.

## 핵심 정리

- Multimodal AI는 여러 modality를 하나의 문제 안에서 함께 이해·생성합니다.
- 일반적인 구조는 modality별 encoder → aligned/shared representation → multimodal reasoning/generation입니다.
- 대표 유형은 Multimodal Understanding, Cross-Modal Generation, Cross-Modal Alignment입니다.
- CLIP 같은 contrastive learning은 image/text를 같은 embedding space에 정렬합니다.
- Modality 수를 늘리는 것이 목적이 아니라 실제 task에 필요한 정보를 가장 효율적으로 결합하는 것이 목적입니다.

## 원문

- https://outcomeschool.com/blog/multimodal-ai
