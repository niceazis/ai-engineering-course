# Approximate Nearest Neighbor(ANN) 검색은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-approximate-nearest-neighbor-ann-search-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 원문 본문 캐시를 직접 열지 못했습니다. Outcome School 공식 Module 9 레슨 구조와 ANN의 공개 표준 알고리즘을 교차검증해 작성하며, 원문에서 확인하지 못한 수치를 원문 내용이라고 단정하지 않습니다.

## 1. Nearest Neighbor 문제

Query vector q와 데이터 vector x_i 사이 distance/similarity를 계산해 가장 가까운 k개를 찾습니다.

Exact search:

    for every x_i:
        score(q, x_i)

Dataset이 작을 때는 단순하고 정확합니다.

문제는 vector가 수백만~수십억 개일 때입니다.

## 2. ANN의 목표

Approximate Nearest Neighbor는 exact top-k를 100% 보장하는 대신 훨씬 적은 후보만 검사합니다.

핵심 목표:

    높은 recall
    + 낮은 latency
    + 감당 가능한 memory

ANN 설계는 항상 속도/정확도/메모리의 trade-off입니다.

## 3. KD-Tree

공간을 축별로 반복 분할하는 tree입니다.

낮은 차원에서는 효과적이지만 dimension이 커지면 pruning 효과가 급격히 떨어집니다. 이를 흔히 curse of dimensionality와 연결합니다.

현대 text embedding처럼 수백 차원에서는 KD-tree가 일반적으로 주력 선택이 아닙니다.

## 4. Locality-Sensitive Hashing(LSH)

비슷한 vector가 같은 bucket에 들어갈 확률이 높도록 hash function을 설계합니다.

검색:

    query
      → hash buckets
      → nearby candidate bucket
      → exact score among candidates

장점은 이론적 성질이 명확하다는 점이고, 단점은 실전 high-recall tuning에서 많은 table/memory가 필요할 수 있다는 점입니다.

## 5. IVF

Dataset을 coarse cluster로 나눕니다.

Training:

    vectors → k-means centroids

Index:

    each vector → nearest centroid list

Query:

1. query와 centroid 비교
2. 가까운 nprobe cluster 선택
3. 그 안의 vector만 검색

nprobe가 ANN quality/latency를 직접 조절합니다.

## 6. HNSW

Hierarchical Navigable Small World graph는 vector를 neighbor graph로 연결합니다.

검색은 높은 layer에서 시작해 greedy하게 query에 가까운 node로 이동한 뒤 아래 layer로 내려갑니다.

대표 tuning:

- M: node당 edge 수
- efConstruction: build 품질/비용
- efSearch: query recall/latency

efSearch를 높이면 일반적으로 recall은 좋아지고 latency도 증가합니다.

## 7. 왜 Graph Search가 빠른가

좋은 graph에는 local edge뿐 아니라 먼 지역으로 건너가는 shortcut edge가 있습니다.

따라서 모든 point를 보지 않고:

    coarse jump
      → closer region
      → local refinement

으로 탐색할 수 있습니다.

## 8. Quantization과 조합

ANN candidate generation에 PQ/SQ 같은 compression을 결합할 수 있습니다.

예:

    IVF → compressed candidates
        → top 100
        → original vector exact rerank
        → top 10

두 단계로 speed와 quality를 균형 잡습니다.

## 9. Recall 측정

ANN 평가에서 “accuracy” 대신 recall@k를 많이 봅니다.

    recall@10
      = ANN top-10 안에
        exact top-10이 얼마나 포함됐는가

Latency만 낮추고 recall이 크게 떨어지면 검색 품질이 나쁩니다.

## 10. Index 선택

### HNSW가 잘 맞는 경우

- high recall
- RAM 여유
- low-latency online query

### IVF/PQ가 잘 맞는 경우

- 매우 큰 dataset
- memory 절감 중요
- batch/offline build 가능

### Flat exact search

- dataset 작음
- GPU brute-force가 충분히 빠름
- 100% exact가 필요

## 11. Filtering과 ANN

Metadata filter가 매우 강하면 ANN index가 선택한 후보가 filter에서 제거될 수 있습니다.

따라서 vector DB는:

- filtered HNSW
- partition
- pre-filter
- dynamic candidate expansion

같은 전략을 사용합니다.

## 핵심 정리

- ANN은 exact top-k 보장을 일부 포기해 대규모 vector search를 빠르게 만듭니다.
- KD-tree, LSH, IVF, HNSW가 대표 접근입니다.
- 현대 embedding search에서는 HNSW와 IVF/PQ가 특히 많이 쓰입니다.
- 성능은 latency 하나가 아니라 recall@k, memory, build/update cost를 함께 봐야 합니다.
- 원문 본문을 직접 확인하지 못한 부분은 공개 ANN 지식으로 보완했으며 원문 고유 예제로 표시하지 않았습니다.

## 원문

- https://outcomeschool.com/blog/how-does-approximate-nearest-neighbor-ann-search-work
