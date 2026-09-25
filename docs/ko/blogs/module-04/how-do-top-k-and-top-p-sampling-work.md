# Top-k와 Top-p Sampling은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-do-top-k-and-top-p-sampling-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 공식 인덱스와 검색 가능한 원문 사본에서 확인한 실제 예제·수치·비교를 보존해 독립적으로 다시 쓴 상세 해설입니다. 현재 원문 URL은 웹 도구에서 직접 열리지 않아 이 한계를 명시합니다.

## 1. 문제: 다음 Token 후보가 너무 많다

문맥:

    The cat sat on the ...

에 대해 모델이 다음 확률을 냈다고 합시다.

| Token | Probability |
| --- | ---: |
| mat | 40% |
| floor | 25% |
| sofa | 15% |
| bed | 10% |
| roof | 5% |
| 나머지 수천 token | 합계 5% |

최고 확률 token만 늘 고르면 단조로울 수 있고, vocabulary 전체에서 sampling하면 아주 낮은 확률의 이상한 token도 누적적으로 선택될 수 있습니다.

Top-k와 Top-p는 **후보 집합을 제한한 뒤 sampling**하는 전략입니다.

## 2. Greedy Decoding

    next_token = argmax(probability)

장점:

- 단순하고 안정적
- 저확률 이상 token 배제

단점:

- 표현이 획일적일 수 있음
- 현재 step의 최고 선택이 전체 sequence 최적을 보장하지 않음

## 3. Pure Sampling의 문제

모든 vocabulary token을 확률대로 뽑으면 tail의 매우 작은 확률도 살아 있습니다.

원문 예에서 나머지 수천 token의 확률 합이 5%라면, 개별 token은 아주 낮아도 전체 tail에서 이상 token이 선택될 가능성은 무시할 수 없습니다.

Autoregressive generation에서는 잘못 뽑힌 token이 이후 문맥 전체에 영향을 줍니다.

## 4. Top-k Sampling

Top-k는 확률이 높은 **상위 k개 token만 남기고 나머지를 제거**합니다.

예를 들어 k=3이면:

    mat    0.40
    floor  0.25
    sofa   0.15

만 남긴 뒤 확률을 다시 정규화해 sampling합니다.

k는 학습되는 값이 아니라 inference 설정입니다.

원문은 흔한 예시 범위로 k=10~50을 제시합니다.

## 5. Top-k의 한계

고정 k는 모델 confidence에 적응하지 못합니다.

### 확실한 경우

    The capital of France is ...

Paris가 95%라면 후보 1개만으로 충분할 수 있습니다. 그런데 k=3이면 약한 후보도 두 개 더 남깁니다.

### 다양한 답이 자연스러운 경우

    My favourite colour is ...

여러 색이 8~12%처럼 비슷하다면 k=3은 좋은 후보를 너무 많이 잘라냅니다.

같은 k가 어떤 step에서는 너무 크고 다른 step에서는 너무 작습니다.

## 6. Top-p Sampling

Top-p는 개수를 고정하지 않고, 확률이 높은 순서대로 더해 **누적 확률이 p 이상이 되는 최소 후보 집합**을 남깁니다.

다른 이름은 Nucleus Sampling입니다.

예:

    p = 0.9

이면 90% 이상의 probability mass를 덮는 top token 집합만 남깁니다.

## 7. 확실한 상황의 Top-p

원문 예:

    The capital of France is ...

| Token | Probability | Running Total |
| --- | ---: | ---: |
| Paris | 95% | 95% |

Paris 하나만으로 0.9를 넘으므로 후보 수는 1입니다.

## 8. 불확실한 상황의 Top-p

원문의 색상 예:

| Token | Probability | Running Total |
| --- | ---: | ---: |
| blue | 12% | 12% |
| red | 11% | 23% |
| green | 11% | 34% |
| black | 10% | 44% |
| purple | 10% | 54% |
| yellow | 9% | 63% |
| white | 9% | 72% |
| pink | 8% | 80% |

8개를 넣어도 80%이므로 p=0.9에 도달할 때까지 더 많은 후보를 포함합니다.

이것이 Top-p가 model confidence에 적응하는 핵심입니다.

## 9. 구현 순서

개념적 알고리즘:

1. logits를 probability로 변환
2. probability 내림차순 정렬
3. cumulative sum 계산
4. 누적합이 p에 도달하는 경계 token까지 유지
5. 그 뒤 token probability를 0으로 설정
6. 남은 확률 renormalize
7. multinomial sampling

경계 token 자체는 포함해야 누적 확률이 p를 넘습니다.

## 10. Top-k vs Top-p

| 항목 | Top-k | Top-p |
| --- | --- | --- |
| 고정하는 것 | token 수 k | 누적 probability p |
| 후보 수 | 항상 k | 매 step 달라짐 |
| 모델이 확실 | 약한 token도 k까지 유지 | 매우 적게 유지 가능 |
| 모델이 불확실 | 좋은 token도 k 밖이면 제거 | 필요한 만큼 늘어남 |
| 다른 이름 | 없음 | Nucleus Sampling |
| 원문 예시 | k=10~50 | p=0.9~0.95 |

## 11. Temperature와 함께 사용

원문은 역할을 다음처럼 구분합니다.

- Temperature: score distribution을 sharp/flat하게 조정
- Top-k/Top-p: sampling 후보 범위를 제한

개념적 순서:

    scores
      → temperature
      → top-k
      → top-p
      → normalize
      → sample

실제 inference engine의 세부 구현 순서는 확인이 필요하지만 학습용 흐름은 이렇습니다.

## 12. 극단값

- k=1 → greedy와 같음
- 매우 큰 k → Top-k 영향 거의 없음
- p=1.0 → Top-p 영향 거의 없음
- p가 매우 작음 → 최고 token만 남을 수 있음

즉 greedy와 pure sampling은 filtering 강도의 양끝으로 볼 수 있습니다.

## 13. 언제 무엇을 쓰는가

원문의 가이드:

### 정확성이 중요한 작업

factual QA, code, summarization에서는 낮은 Temperature와 제한적인 후보 집합을 고려합니다.

### 창의성이 중요한 작업

story, poem, brainstorming에서는 더 큰 k/p와 조금 높은 Temperature를 고려할 수 있습니다.

### Default 선택

Top-p는 confidence에 따라 후보 수가 자동으로 변하므로 일반적인 default로 유용합니다.

하지만 최적값은 model/provider/task별 benchmark로 결정해야 합니다.

## 핵심 정리

- Top-k는 상위 k개 token만 남깁니다.
- Top-p는 누적 확률 p를 덮는 최소 후보 집합을 남깁니다.
- Top-k 후보 수는 고정, Top-p 후보 수는 매 token마다 변합니다.
- Temperature는 분포 모양, k/p는 후보 범위를 조절합니다.
- filtering 후에는 확률을 다시 정규화해 sampling합니다.

## 원문

- https://outcomeschool.com/blog/how-do-top-k-and-top-p-sampling-work
