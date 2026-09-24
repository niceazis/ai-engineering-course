# Contrastive Learning — 매우 자세한 한국어 학습 노트

> 원문: https://outcomeschool.com/blog/contrastive-learning
> 원저자: Amit Shekhar / Outcome School
> 문서 성격: **원문 전체 번역본이 아닌 독립적인 한국어 상세 해설·학습 노트**

## 핵심 정의

Contrastive Learning은 의미가 비슷한 sample의 embedding은 가깝게, 다른 sample은 멀게 배치되는 representation space를 학습한다.

---

## 1. Embedding Space

- Input을 encoder로 vector embedding으로 변환한다.
- 좋은 embedding은 semantic similarity가 거리나 각도에 반영된다.

## 2. Positive/Negative Pair

- Positive pair는 같은 의미·같은 object·같은 sample의 augmentation 등이다.
- Negative pair는 의미적으로 다른 sample이다.

## 3. Similarity

- Cosine similarity와 Euclidean distance가 대표적이다.
- 학습 objective는 positive similarity를 높이고 negative similarity를 낮춘다.

## 4. Triplet Loss

- Anchor, Positive, Negative를 사용한다.
- d(anchor,positive)+margin < d(anchor,negative)가 되도록 학습한다.

## 5. InfoNCE

- Positive pair score를 높이고 batch 내 negative score를 낮춘다.
- temperature가 softmax sharpness를 조절한다.

## 6. SimCLR

- 같은 이미지에 서로 다른 augmentation을 적용해 positive pair를 만든다.
- 다른 이미지 view는 negative로 활용한다.
- augmentation 설계가 학습할 invariance를 결정한다.

## 7. Hard/False Negative

- Hard negative는 매우 비슷하지만 다른 sample이라 학습에 유용하다.
- False negative는 실제 비슷한데 negative 처리된 sample로 representation을 해칠 수 있다.

## 8. Multimodal과 Retrieval

- CLIP은 image-text pair를 같은 embedding space에 맞춘 대표 사례다.
- Semantic Search, RAG embedding, recommendation, face recognition 등에 연결된다.

## 9. 한계

- 큰 batch 비용, negative sampling, false negative, augmentation 선택, representation collapse 방지가 주요 이슈다.

## 학습 체크리스트

- 핵심 개념을 한 문장으로 설명할 수 있는가?
- 대표 수식이나 기준을 직접 설명할 수 있는가?
- 실무 예시를 하나 들 수 있는가?
- 실패하거나 오해하기 쉬운 조건을 설명할 수 있는가?

## 원문

- https://outcomeschool.com/blog/contrastive-learning
