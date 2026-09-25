# Image Embedding은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-do-image-embeddings-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-06-26 공개 원문을 직접 확인해 이미지→vector 과정, Cat A/B/Car C 수치 예제, cosine similarity와 cross-modal embedding 사용 사례를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Embedding이란?

Embedding은 복잡한 객체를 fixed-dimensional vector로 표현합니다.

    image
      → encoder
      → [v1, v2, ..., vd]

이 vector가 이미지의 semantic content를 압축해 표현합니다.

## 2. 왜 Pixel 자체를 비교하지 않는가

같은 고양이라도 위치, 배경, 조명, 확대/축소가 다르면 raw pixel distance는 크게 달라질 수 있습니다.

우리가 원하는 것은 pixel equality가 아니라 **semantic similarity**입니다.

## 3. Computer가 Image를 보는 방식

Image는 처음에는 height × width × channels 숫자 tensor입니다.

Vision encoder는 patch/convolution/attention 등을 통해 low-level pixel pattern을 higher-level feature로 바꾸고 최종 global vector를 만듭니다.

## 4. 원문의 간단한 수치 예

    Cat A = [0.90, 0.10, 0.05]
    Cat B = [0.88, 0.12, 0.07]
    Car C = [0.10, 0.95, 0.85]

Cat A와 Cat B는 좌표가 매우 비슷합니다.

Car C는 방향이 크게 다릅니다.

실제 model의 embedding dimension은 훨씬 큽니다.

## 5. Cosine Similarity

    cosine(A, B)
      = A·B / (||A|| ||B||)

범위:

    -1 ~ 1

일반적인 normalized embedding retrieval에서는 1에 가까울수록 의미적으로 유사하다고 봅니다.

원문의 Cat A/B는 cosine similarity가 1에 매우 가까운 예입니다.

## 6. Image Embedding 생성

일반 흐름:

1. Image resize/normalize
2. Vision encoder
3. Global representation
4. optional projection
5. normalization
6. vector 저장

CLIP 같은 model에서는 image encoder와 text encoder output을 같은 공간에 projection합니다.

## 7. Cross-Modal Search

원문 예:

    text = "beach"

Text encoder가 query vector를 만들고 image encoder가 각 photo의 vector를 만듭니다.

동일 embedding space이면 text vector와 image vector cosine similarity를 직접 비교할 수 있습니다.

원문은 clip-ViT-B-32 같은 model을 대표 예로 언급합니다.

## 8. Semantic Image Search

사용자 query:

    "a red sports car at night"

Text embedding을 만든 뒤 image vector DB에서 nearest neighbor를 찾습니다.

Keyword metadata가 없어도 visual concept로 검색할 수 있습니다.

## 9. Similar Product Recommendation

Product photo embedding끼리 가까운 item을 찾습니다.

    shoe image
      → nearest embeddings
      → visually/semantically similar shoes

## 10. Duplicate / Near-Duplicate Detection

이미지를 crop하거나 resize해도 embedding이 비슷하다면 duplicate 후보로 찾을 수 있습니다.

정확한 duplicate는 perceptual hash와 같이 쓰면 더 강합니다.

## 11. Face Grouping

Face encoder를 사용하면 동일 인물의 얼굴 embedding이 가까워지도록 학습할 수 있습니다.

일반 image embedding과 face recognition embedding은 training objective가 다르므로 용도를 구분해야 합니다.

## 12. Recommendation

사용자가 본 image들의 embedding을 profile signal로 사용해 가까운 item을 추천할 수 있습니다.

다만 preference가 visual similarity와 동일한 것은 아니므로 실제 click/purchase signal과 결합하는 것이 좋습니다.

## 13. Vector Database와 연결

    images
      → embeddings
      → vector DB

    query image/text
      → embedding
      → ANN search
      → nearest images

Module 9의 vector database/ANN과 직접 연결됩니다.

## 핵심 정리

- Image Embedding은 image를 semantic vector로 바꿉니다.
- 원문 toy example에서 Cat A/B는 비슷하고 Car C는 크게 다른 vector입니다.
- Cosine similarity로 의미 유사도를 비교할 수 있습니다.
- CLIP 계열은 image와 text를 같은 embedding space에 정렬해 cross-modal search를 가능하게 합니다.
- Semantic search, recommendation, duplicate detection, grouping이 대표 활용입니다.

## 원문

- https://outcomeschool.com/blog/how-do-image-embeddings-work
