# Contrastive Learning — 원문 흐름을 따라가는 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/contrastive-learning  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 cat/car 예제, positive/negative pair, similarity와 학습 과정을 중심으로 다시 구성한 상세 한국어 학습 노트입니다.

## 핵심

Contrastive Learning은 데이터를 비교하면서 representation을 학습합니다.

목표는 매우 직관적입니다.

```text
비슷한 것 -> embedding space에서 가깝게
다른 것   -> embedding space에서 멀게
```

이렇게 학습된 embedding은 검색, 분류, clustering, recommendation 등 여러 downstream task에 재사용할 수 있습니다.

## 1. 왜 필요한가

전통적인 supervised learning에는 많은 label이 필요합니다.

이미지 수억 장을 사람이 모두:

```text
cat
dog
car
tree
...
```

라고 labeling하는 것은 비싸고 느립니다.

하지만 인터넷에는 label 없는 이미지·텍스트·영상이 훨씬 많습니다.

Contrastive Learning은 **데이터 자체에서 학습 신호를 만들어** 이런 unlabeled data를 활용할 수 있는 self-supervised learning의 대표적인 접근입니다.

## 2. Embedding space

모델은 입력을 vector로 바꾸는 함수를 학습합니다.

```text
input x
  ↓
encoder f(x)
  ↓
embedding vector z
```

좋은 representation이라면 의미가 비슷한 입력의 vector가 가까워야 합니다.

예:

```text
cat photo A ----                 > 가까움
cat photo B ----/

car photo ---------------- 멀리
```

## 3. Positive Pair와 Negative Pair

### Positive Pair

같거나 의미적으로 비슷해서 가까워져야 하는 두 sample입니다.

이미지에서는 같은 원본 이미지에 서로 다른 augmentation을 적용해 만들 수 있습니다.

- crop
- rotate
- flip
- color change

예:

```text
원본 cat
 ├─ crop + color jitter -> View 1
 └─ flip + crop         -> View 2

View 1 + View 2 = Positive Pair
```

### Negative Pair

서로 다른 sample로, embedding space에서 멀어져야 하는 pair입니다.

```text
cat View 1 + car image = Negative Pair
```

## 4. Augmentation이 왜 중요한가

Positive pair를 만들 때 겉모습은 달라져도 의미는 유지되어야 합니다.

고양이를 crop하거나 좌우 반전해도 여전히 고양이입니다.

모델은 이 과정을 통해:

> 색상·각도·crop 같은 표면 변화보다 실제 의미를 나타내는 특징을 유지해야 한다.

는 representation을 배우게 됩니다.

하지만 augmentation이 의미 자체를 바꾸면 잘못된 positive pair를 만들 수 있습니다.

따라서 augmentation 정책은 contrastive learning 성능을 좌우합니다.

## 5. 원문의 단계별 cat/car 예제

### Step 1: 같은 cat 이미지에서 두 view 생성

```text
Cat -> View 1
Cat -> View 2
```

두 view는 positive pair입니다.

### Step 2: 다른 car 이미지 준비

car는 negative sample 역할을 합니다.

### Step 3: Encoder 통과

세 이미지를 neural network에 넣어 embedding을 얻습니다.

```text
View 1 -> z1
View 2 -> z2
Car    -> z3
```

### Step 4: Similarity 계산

원문은 cosine similarity를 사용해 설명합니다.

```text
cosine_similarity(a, b)
= (a · b) / (||a|| ||b||)
```

값이 1에 가까울수록 방향이 비슷합니다.

학습 초기 예로 원문은 다음처럼 모델이 잘못 판단하는 상황을 제시합니다.

```text
sim(View1, View2) = 0.3
sim(View1, Car)   = 0.6
sim(View2, Car)   = 0.5
```

현재 모델은 같은 cat의 두 view보다 cat과 car가 더 비슷하다고 보고 있습니다.

좋지 않은 representation입니다.

### Step 5: Contrastive Loss

Loss는 모델에게:

```text
positive similarity ↑
negative similarity ↓
```

방향으로 학습 압력을 줍니다.

### Step 6: Weight Update

Backpropagation과 optimizer를 통해 encoder weight를 수정합니다.

### Step 7: 반복

많은 image와 pair에 대해 반복하면 embedding space가 점점 의미 중심으로 정리됩니다.

## 6. 학습 후 기대하는 모습

학습 전:

```text
cat1   car   cat2
        |     /
  의미 구조가 뒤섞임
```

학습 후:

```text
[cat1 cat2 cat3]          [car1 car2 car3]
      가까움                    가까움

       <------ 서로 멂 ------>
```

이제 새 이미지를 embedding으로 바꾸면 의미적으로 가까운 데이터를 찾기 쉬워집니다.

## 7. Loss의 직관

Contrastive loss 계열의 구체적인 식은 방법마다 다르지만 공통 목표는 같습니다.

anchor `i`에 대해 positive `j`의 score는 높이고, 다른 negative들의 score는 상대적으로 낮춥니다.

InfoNCE 계열을 개념적으로 쓰면:

```text
Loss_i
= -log(
    exp(sim(i,j)/τ)
    /
    Σ_k exp(sim(i,k)/τ)
  )
```

`τ`는 temperature입니다.

positive가 다른 후보보다 훨씬 비슷하면 loss가 낮아집니다.

## 8. Negative sample의 역할

너무 쉬운 negative만 있으면 모델이 단순한 특징만으로 구분할 수 있습니다.

반대로 의미가 매우 비슷하지만 실제로는 다른 **hard negative**는 더 정교한 representation을 학습하는 데 도움을 줄 수 있습니다.

하지만 잘못된 negative, 즉 사실상 같은 의미인 sample을 negative로 처리하면 학습 신호가 오염됩니다.

## 9. 이미지 이외에도 적용된다

### Text

의미가 같은 두 문장을 positive pair로 만들 수 있습니다.

### Image–Text

이미지와 해당 caption을 positive pair로 만들 수 있습니다.

이 원리는 multimodal representation learning과 연결됩니다.

### Search

query와 관련 document를 가깝게, 관련 없는 document를 멀게 학습할 수 있습니다.

## 10. 학습된 representation의 활용

Contrastive pretraining 후 encoder를 다음에 활용할 수 있습니다.

- Classification
- Semantic Search
- Image Retrieval
- Recommendation
- Clustering
- Similarity Matching

적은 label만 추가해 fine-tuning하거나 embedding 자체를 검색에 사용할 수 있습니다.

## 11. 반드시 기억할 문장

```text
Contrastive Learning
= 무엇이 같은 의미이고 무엇이 다른지를 비교하면서
  유용한 embedding space를 학습하는 방법
```

## 이해 확인

1. 같은 cat 이미지에 두 augmentation을 적용한 이유는 무엇인가요?
2. positive pair의 similarity가 negative보다 낮다면 loss는 어떤 방향으로 weight를 바꾸려 할까요?
3. 의미를 바꾸는 augmentation이 위험한 이유는 무엇인가요?
4. 학습된 embedding을 검색에 바로 활용할 수 있는 이유는 무엇인가요?

## 원문 및 연결 학습

- 원문: https://outcomeschool.com/blog/contrastive-learning
- 이전: [Reinforcement Learning](reinforcement-learning.md)
- 모듈 1: [머신러닝 기초](../../module-01.md)
