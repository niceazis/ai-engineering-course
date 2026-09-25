# Embeddings in Machine Learning — 한국어 상세 영상 학습 노트

> 영상: https://www.youtube.com/watch?v=LedXW6xl21s  
> 제공: Outcome School  
> 검증 범위: 영상 URL과 제목은 Outcome School 공식 자료에서 확인했습니다. **영상 자막 전문은 직접 검증하지 못했습니다.** 아래 내용은 공식 영상 주제와 Outcome School의 Embedding 원문 레슨을 근거로 재구성한 상세 학습 노트입니다.

## 1. Embedding이 해결하는 문제

컴퓨터는 문자열의 의미를 직접 비교하지 못합니다.

예:

- “How do I reset my password?”
- “I forgot my login details.”

단어는 다르지만 의미는 가깝습니다.

반대로:

- “river bank”
- “bank account”

는 “bank”라는 문자열이 같지만 의미는 다릅니다.

Embedding은 이러한 의미를 vector 공간의 위치로 표현합니다.

## 2. Vector 표현

Outcome School 원문 예:

    password question
    [0.21, -0.48, 0.83, 0.02, ...]

    login question
    [0.19, -0.44, 0.79, 0.05, ...]

비슷한 의미의 항목은 가까운 vector가 되도록 모델을 학습합니다.

## 3. 2차원 직관

과일을 두 숫자로만 표현한다고 단순화하면:

- Apple: [7, 5]
- Banana: [8, 5]
- Lemon: [1, 3]
- Watermelon: [6, 10]

Apple과 Banana는 공간에서 가깝습니다.

실제 embedding은 수백~수천 차원이며, 각 dimension을 사람이 한 가지 의미로 해석할 수 있다고 보장되지는 않습니다.

Outcome School 레슨은 384~3072 차원의 embedding을 예시 범위로 설명합니다.

## 4. Similarity 계산

### Cosine similarity

[
cos(A,B)=rac{Acdot B}{||A||||B||}
]

방향이 비슷한지를 봅니다.

### Dot product

[
Acdot B=sum_i A_iB_i
]

embedding이 정규화되어 있다면 cosine과 밀접하게 연결됩니다.

### Euclidean distance

[
d(A,B)=sqrt{sum_i(A_i-B_i)^2}
]

어떤 metric을 써야 하는지는 embedding model의 학습 방식과 vector database 설정에 맞춰야 합니다.

## 5. Embedding은 어떻게 학습되는가

핵심 아이디어는 의미가 비슷한 항목을 가까이, 다른 항목을 멀리 배치하는 것입니다.

언어의 경우 비슷한 문맥에 반복 등장하는 단어는 관련 의미를 학습할 수 있습니다.

Outcome School 예:

- tea와 coffee가 “I drank a cup of …” 같은 문맥에서 반복
- 두 단어가 유사한 관계를 갖는 representation을 형성

현대 sentence embedding model은 contrastive objective나 supervised pair 데이터 등을 사용할 수 있습니다.

## 6. Vector arithmetic 직관

고전적인 예:

    king - man + woman ≈ queen

    Paris - France + Italy ≈ Rome

이것은 embedding 공간에서 관계 방향이 나타날 수 있음을 보여 주는 직관입니다.

모든 embedding model과 모든 단어에서 정확한 등식처럼 성립하는 규칙은 아닙니다.

## 7. Semantic Search

문서와 query를 같은 embedding model로 vector화합니다.

    query
      → embedding
      → nearest-neighbor search
      → 관련 문서

키워드가 일치하지 않아도 의미가 비슷한 문서를 찾을 수 있습니다.

## 8. RAG에서의 역할

RAG의 기본 retrieval 흐름:

    문서
      → chunking
      → embeddings
      → vector database

    질문
      → query embedding
      → nearest-neighbor search
      → top-k chunks
      → LLM context

Embedding 품질뿐 아니라 chunking과 검색 전략도 결과를 크게 바꿉니다.

## 9. 다른 모달리티

Embedding은 텍스트뿐 아니라:

- 이미지
- 오디오
- 코드
- 사용자
- 상품

등에도 사용할 수 있습니다.

멀티모달 모델은 서로 다른 modality를 비교 가능한 representation space에 정렬하기도 합니다.

## 10. 실무에서 확인할 것

- embedding model 버전
- vector dimension
- query/document 입력 방식
- normalization 여부
- similarity metric
- top-k
- retrieval recall
- latency와 storage 비용

서로 다른 embedding model이 만든 vector를 같은 공간이라고 가정해 직접 비교해서는 안 됩니다.

## 핵심 정리

- Embedding은 의미를 vector 공간의 위치로 바꿉니다.
- 유사도는 cosine, dot product, Euclidean distance 등으로 계산합니다.
- semantic search, RAG, 추천, clustering의 핵심 표현입니다.
- dimension 수만 높다고 무조건 좋은 embedding은 아닙니다.
- 이 노트는 영상 자막을 직접 번역한 것이 아니라 공식 영상 주제와 Outcome School 원문 레슨을 근거로 만든 상세 학습 노트입니다.
