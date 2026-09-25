# Embedding이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/what-are-embeddings  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 문제 제기 → 2차원 예 → 고차원 → 거리 → 학습 → 벡터 연산 → 활용 순서를 보존한 한국어 상세 해설입니다.

## 1. 문제: 문자열 일치는 의미 일치가 아니다

원문은 두 쌍의 문장으로 시작합니다.

### 의미는 비슷하지만 단어는 다른 경우

- “How do I reset my password?”
- “I forgot my login details.”

사람은 같은 문제라고 이해하지만 핵심 단어가 거의 겹치지 않습니다.

### 같은 단어가 있지만 의미가 다른 경우

- “The bank of the river was muddy.”
- “I need to visit the bank today.”

문자열 “bank”는 같지만 하나는 강둑, 다른 하나는 금융기관입니다.

따라서 단순한 문자/키워드 일치는 의미 유사도를 제대로 표현하지 못합니다.

## 2. Embedding의 정의

Embedding은 어떤 대상의 의미를 숫자 목록, 즉 vector로 바꾼 표현입니다.

원문의 예:

    "How do I reset my password?"
      → [0.21, -0.48, 0.83, 0.02, ...]

    "I forgot my login details."
      → [0.19, -0.44, 0.79, 0.05, ...]

    "The bank of the river."
      → [-0.71, 0.33, -0.12, 0.66, ...]

첫 두 문장은 의미가 비슷하므로 vector 공간에서도 가깝게 배치되는 것이 목표입니다.

즉:

> 의미를 위치로 바꾸면, 컴퓨터는 거리나 각도를 계산해 의미 유사성을 다룰 수 있습니다.

## 3. 2개의 숫자로 보는 직관

원문은 과일을 두 특성, 예를 들어 sweetness와 size로 표현하는 2차원 직관을 사용합니다.

예제의 한 부분:

- Apple = [7, 5]
- Banana = [8, 5]
- Lemon = [1, 3]
- Watermelon = [6, 10]

Apple과 Banana는 좌표가 가까워 유사한 항목으로 볼 수 있고, Lemon은 멀리 떨어집니다.

이 예제의 목적은 실제 embedding의 각 차원이 “단맛” 같은 사람이 붙인 의미를 가진다는 뜻이 아닙니다. **vector가 공간의 한 점이고, 유사한 대상이 가까워질 수 있다는 직관**을 보여 주는 것입니다.

## 4. 왜 2차원으로는 부족한가

과일도 sweetness와 size만 있으면 lemon과 lime 같은 항목을 충분히 구별하기 어렵습니다. 언어의 의미는 훨씬 복잡합니다.

원문은 실제 sentence embedding이 대략 384~3072개의 수를 가질 수 있다고 설명합니다.

    2 dimensions   → 평면
    3 dimensions   → 3차원 공간
    768 dimensions → 사람이 시각화할 수 없지만 계산에는 문제 없음

중요한 점:

- dimension 하나가 반드시 “격식”, “감정”처럼 사람이 이름 붙일 수 있는 독립 의미를 담당하지 않습니다.
- 의미는 여러 차원에 분산되어 나타납니다.

## 5. 가까움을 어떻게 측정하는가

Embedding 검색에서는 대표적으로 cosine similarity, dot product, Euclidean distance를 사용합니다.

### Cosine similarity

두 vector의 방향이 얼마나 비슷한지 봅니다.

    cos(A, B) = (A · B) / (||A|| ||B||)

값이 1에 가까울수록 방향이 유사합니다.

### Euclidean distance

두 점 사이의 직선 거리를 봅니다.

    distance(A, B) = sqrt(Σ(Ai - Bi)^2)

어떤 metric을 쓸지는 embedding model이 어떤 방식으로 학습·정규화되었는지에 맞춰야 합니다.

## 6. Embedding은 어디에서 오는가

원문은 “비슷한 문맥에서 나타나는 단어는 비슷한 의미를 갖는 경향이 있다”는 분포적 의미론의 직관을 설명합니다.

예:

- “I drank a cup of tea in the morning.”
- “I drank a cup of coffee in the morning.”
- “She poured the tea into a cup.”
- “She poured the coffee into a cup.”

tea와 coffee가 반복해서 비슷한 주변 문맥에 등장하므로 모델은 이들을 가까운 공간에 배치하도록 학습할 수 있습니다.

현대 embedding model은 학습 목적에 따라 contrastive learning, next-token prediction, supervised pair/triplet 데이터 등 다양한 신호를 사용합니다.

## 7. 유명한 vector arithmetic 예

원문은 embedding 공간의 관계 구조를 보여 주기 위해 다음 예를 사용합니다.

    king - man + woman ≈ queen

또 다른 예:

    Paris - France + Italy ≈ Rome

이 예의 요지는 실제 시스템에서 항상 정확히 성립하는 산술 법칙이라는 뜻이 아니라, **학습된 vector 공간에 관계 방향이 나타날 수 있다**는 것입니다.

## 8. 텍스트만 embedding되는 것이 아니다

같은 원리를 다른 모달리티에도 적용할 수 있습니다.

- 문장/문서 embedding
- 이미지 embedding
- 오디오 embedding
- 사용자/상품 embedding
- 코드 embedding

중요한 것은 “대상을 vector로 바꾸고, 관련 있는 것끼리 의미 있는 기하 구조를 갖도록 학습한다”는 것입니다.

## 9. 어디에 사용하는가

### Semantic Search

질문과 문서 chunk를 embedding으로 변환하고 가까운 문서를 찾습니다. 단순 키워드가 달라도 의미가 비슷하면 검색할 수 있습니다.

### RAG

질문 embedding과 가까운 chunk를 vector database에서 검색한 뒤 LLM의 context에 넣습니다.

### Recommendation

사용자와 상품을 같은 또는 비교 가능한 vector space에 배치해 가까운 항목을 추천할 수 있습니다.

### Clustering / Classification

embedding을 특징 벡터로 사용해 군집화하거나 downstream classifier에 입력할 수 있습니다.

### Deduplication

의미가 매우 비슷한 문서나 이미지를 탐지할 수 있습니다.

## 10. 주의할 점

- 서로 다른 embedding model의 vector를 직접 비교하면 안 됩니다.
- 같은 model이라도 query/document 전용 prefix가 필요한 경우가 있습니다.
- vector dimension이 크다고 무조건 품질이 좋은 것은 아닙니다.
- cosine similarity 임계값은 데이터셋에서 검증해야 합니다.
- embedding은 학습 데이터의 편향을 반영할 수 있습니다.
- chunking 방식이 RAG 검색 품질에 큰 영향을 줍니다.

## 11. 학습할 때 연결해야 할 개념

Embedding → similarity metric → nearest-neighbor search → vector database → semantic search → RAG가 하나의 연쇄입니다.

또 Transformer 내부의 token embedding은 문맥에 들어가기 전의 표현이고, attention layer를 지난 hidden state는 문맥화된 representation이라는 차이도 구분해야 합니다.

## 핵심 정리

- embedding은 의미를 숫자 vector의 위치로 표현합니다.
- 단순 문자열 일치가 놓치는 의미 유사성을 계산 가능하게 만듭니다.
- 실전 embedding은 수백~수천 차원이며 의미가 여러 차원에 분산됩니다.
- 유사도는 cosine, dot product, Euclidean distance 등으로 계산합니다.
- 검색, RAG, 추천, 군집화의 핵심 표현 방식입니다.

## 원문

- https://outcomeschool.com/blog/what-are-embeddings
