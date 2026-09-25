# Vector Database는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-a-vector-database-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문을 직접 확인해 embedding·similarity metric·ANN·HNSW/IVF/PQ와 수치 예제를 반영한 독립적인 한국어 학습 노트입니다.

## 1. Vector Database가 필요한 이유

일반 DB는 ID, 날짜, 문자열 같은 정확한 조건 검색에 강합니다. 하지만 “이 문장과 의미가 비슷한 문서”를 찾으려면 텍스트를 embedding vector로 바꾸고 가까운 vector를 검색해야 합니다.

Vector DB는 보통 다음을 함께 저장합니다.

    id
    vector
    original text / object
    metadata

검색은 query를 같은 embedding model로 vector화한 뒤 가장 가까운 항목을 찾는 흐름입니다.

## 2. Embedding 복습

원문 예처럼 의미가 가까운 단어는 vector 공간에서도 가까운 위치를 가질 수 있습니다.

    "king"   → [0.91, 0.12, 0.55]
    "queen"  → [0.89, 0.15, 0.58]
    "banana" → [0.10, 0.95, 0.03]

실제 embedding은 수백~수천 차원이며, 서로 다른 embedding model의 vector를 직접 섞어 비교하면 안 됩니다.

## 3. Similarity Metric

### Cosine Similarity

    cos(A,B) = (A·B) / (||A|| ||B||)

원문의 A=[2,3], B=[4,6] 예에서는 두 vector가 같은 방향이라 cosine similarity가 약 1입니다.

### Dot Product

    A·B = Σ A_i B_i

A=[1,2,3], B=[4,5,6]이면:

    1×4 + 2×5 + 3×6 = 32

### Euclidean Distance

    d(A,B) = sqrt(Σ(A_i-B_i)^2)

A=[1,2], B=[4,6]이면 distance=5입니다.

Embedding model이 어떤 metric을 전제로 학습됐는지 확인해야 합니다.

## 4. Brute-Force Search

가장 정확한 방식은 query vector와 모든 stored vector를 비교하는 것입니다.

    1 query
      × N vectors
      × d dimensions

N이 수백만~수십억이면 latency가 커집니다.

그래서 production에서는 Approximate Nearest Neighbor(ANN) index를 주로 사용합니다.

## 5. ANN의 Trade-off

ANN은 모든 vector를 완전 탐색하지 않고 **가까울 가능성이 높은 후보만 탐색**합니다.

Trade-off:

    speed ↑
    memory/index cost ↑
    recall은 exact search보다 약간 낮을 수 있음

따라서 latency와 recall@k를 함께 측정합니다.

## 6. HNSW

HNSW는 vector를 multi-layer graph로 연결합니다.

검색:

1. 상위 sparse layer에서 큰 폭으로 이동
2. query와 가까운 node 방향으로 탐색
3. 아래 layer로 내려감
4. 가장 촘촘한 layer에서 local search

장점:

- 높은 recall
- 빠른 query

단점:

- index memory 큼
- build/update 비용 존재

## 7. IVF

IVF(Inverted File Index)는 vector 공간을 여러 cluster로 나눕니다.

    vectors
      → centroids
      → inverted lists

Query는 가장 가까운 몇 개 centroid만 선택하고 그 cluster 안에서 검색합니다.

조절값:

- cluster 수
- nprobe: query 시 몇 cluster를 볼지

nprobe가 커지면 recall은 높아지고 latency도 증가합니다.

## 8. Product Quantization(PQ)

PQ는 vector를 여러 subvector로 나누고 각 부분을 작은 codebook index로 압축합니다.

목적:

- memory 감소
- distance calculation 가속

대규모 billion-scale index에서 IVF+PQ 조합이 자주 사용됩니다.

정확도 손실이 있으므로 compression ratio와 recall을 함께 평가합니다.

## 9. Metadata Filtering

실전 검색은 vector similarity만 쓰지 않습니다.

예:

    tenant_id = 42
    language = "ko"
    created_at >= ...
    document_type = "policy"

원문이 구분하는 두 방식:

### Pre-filter

metadata 조건으로 후보를 먼저 줄인 뒤 vector search.

### Post-filter

vector top-k를 먼저 찾고 metadata로 제거.

필터가 강하면 post-filter는 필요한 결과 수를 못 채울 수 있어 pre-filter가 유리한 경우가 많습니다.

## 10. RAG에서의 위치

    documents
      → chunking
      → embedding
      → vector DB

    user query
      → embedding
      → ANN search
      → top-k chunks
      → LLM context

Vector DB는 답을 생성하지 않습니다. **관련 evidence 후보를 빠르게 찾는 retrieval layer**입니다.

## 11. Production 지표

- recall@k
- precision@k
- query p50/p95 latency
- index build time
- RAM/SSD footprint
- update/delete latency
- metadata-filter performance
- cost per million vectors

## 핵심 정리

- Vector DB는 embedding vector와 원문/metadata를 저장하고 similarity search를 제공합니다.
- Cosine, dot product, Euclidean distance가 대표 metric입니다.
- Exact brute force는 정확하지만 대규모에서 느리므로 ANN을 사용합니다.
- HNSW는 graph, IVF는 clustering, PQ는 compression 접근입니다.
- RAG에서는 retrieval 후보를 만드는 역할이며 최종 품질은 chunking·embedding·reranking까지 함께 좌우합니다.

## 원문

- https://outcomeschool.com/blog/how-does-a-vector-database-work
