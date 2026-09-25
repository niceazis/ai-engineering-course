# Epoch, Batch, Batch Size, Iteration — 한국어 상세 영상 학습 노트

> 원본 영상: https://www.youtube.com/watch?v=NFLlXE-6vno  
> 제작: Outcome School / Amit Shekhar  
> 영상 자막은 직접 확보하지 못했습니다. 공개된 영상 소개에서 확인되는 네 용어의 정의를 기준으로 상세 해설했습니다.

## 네 용어

- Epoch: 전체 training dataset을 한 번 모두 사용하는 주기
- Batch: 한 번에 처리하는 sample 묶음
- Batch Size: 한 batch의 sample 수
- Iteration: 한 batch를 처리하는 한 optimization step

관계:

```text
iterations per epoch
≈ training samples / batch size
```

나누어떨어지지 않으면 마지막 batch 때문에 일반적으로 올림합니다.

## 수치 예제

sample 1,000개, batch size 100이면 한 epoch에 10 iteration입니다.

5 epoch이면 약 50번의 parameter update가 발생합니다.

batch size를 250으로 바꾸면 한 epoch당 4 iteration이 됩니다.

## Batch를 사용하는 이유

mini-batch는 전체 dataset을 한 번에 처리할 때의 memory 부담과 sample 하나씩 처리할 때의 noisy gradient 사이를 절충합니다.

GPU의 병렬 계산도 활용하기 좋습니다.

## 한 iteration의 흐름

```text
batch
 -> forward
 -> loss
 -> gradient
 -> optimizer update
 -> next batch
```

모든 batch를 처리하면 한 epoch가 끝납니다.

## Batch Size 변화

작은 batch:
- memory 요구가 작음
- iteration 수 증가
- gradient가 더 noisy할 수 있음

큰 batch:
- 병렬 처리에 유리할 수 있음
- iteration 수 감소
- memory 요구 증가
- learning rate와 함께 조정할 필요가 있음

## Epoch와 overfitting

epoch를 늘린다고 항상 성능이 좋아지는 것은 아닙니다. training metric은 계속 좋아지는데 validation metric이 나빠지면 overfitting 신호일 수 있습니다.

## 이해 확인

1. 10,000 sample에 batch size 128이면 한 epoch의 iteration 수는 어떻게 계산하나요?
2. batch size가 커지면 iteration 수는 어떻게 변하나요?
3. epoch 수를 validation 성능과 함께 봐야 하는 이유는 무엇인가요?

## 연결 학습

- 원본 영상: https://www.youtube.com/watch?v=NFLlXE-6vno
- [Gradient Descent](../../blogs/module-02/math-behind-gradient-descent.md)
- [모듈 2](../../module-02.md)
