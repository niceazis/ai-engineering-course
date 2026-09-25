# One-hot Encoding in Machine Learning — 한국어 상세 영상 학습 노트

> 원본 영상: https://www.youtube.com/watch?v=6AmedU5i9go  
> 채널: Outcome School  
> 문서 성격: 영상 전체 자막을 번역·재게시한 문서가 아니라, 영상 주제인 One-hot Encoding을 단계별 예제와 실무 주의점까지 한국어로 상세하게 설명한 학습 노트입니다.
>
> **검증 범위:** 현재 YouTube 자막 원문은 직접 가져오지 못했습니다. 따라서 영상의 세부 발화 순서를 검증한 자막 번역본이 아니라, 영상 제목과 코스 연결 맥락에 맞춰 개념을 상세히 설명한 노트입니다. 확인되지 않은 영상 고유 발화·수치 예제는 임의로 “영상 내용”이라고 단정하지 않습니다.

## 왜 One-hot Encoding이 필요한가

머신러닝 데이터에는 숫자가 아닌 범주형 값이 자주 있습니다.

```text
Color = Red / Green / Blue
City  = Seoul / Busan / Jeju
Plan  = Free / Plus / Pro
```

많은 수치 기반 모델은 문자열을 그대로 계산할 수 없습니다.

따라서 category를 숫자 표현으로 바꿔야 합니다.

## 1. 단순 번호 부여의 문제

Color를 다음처럼 바꾼다고 하겠습니다.

```text
Red   -> 1
Green -> 2
Blue  -> 3
```

컴퓨터 입장에서는 숫자 사이에 다음 관계가 생깁니다.

```text
Blue(3) > Green(2) > Red(1)
distance(Blue, Red) = 2
distance(Green, Red) = 1
```

하지만 색상 category에는 이런 순서나 수치 거리가 없습니다.

모델이 숫자의 크기를 의미로 오해할 수 있습니다.

## 2. One-hot Encoding

각 category마다 별도 column을 만들고 해당 category만 1, 나머지는 0으로 표시합니다.

원래 데이터:

| Color |
|---|
| Red |
| Blue |
| Green |
| Red |

변환 후:

| Color_Red | Color_Green | Color_Blue |
|---:|---:|---:|
| 1 | 0 | 0 |
| 0 | 0 | 1 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |

각 행에서 하나의 category만 활성화되어 있기 때문에 **one-hot**이라고 부릅니다.

## 3. 무엇이 해결되는가

이제 Red, Green, Blue는 서로 독립적인 feature가 됩니다.

```text
Red   = [1,0,0]
Green = [0,1,0]
Blue  = [0,0,1]
```

1,2,3처럼 임의의 순서를 강제로 부여하지 않습니다.

## 4. 모델에서는 어떻게 사용되나

선형 모델을 생각하면:

```text
score
= w_red * Color_Red
+ w_green * Color_Green
+ w_blue * Color_Blue
```

Red sample에서는:

```text
score = w_red
```

가 되고 Blue sample에서는:

```text
score = w_blue
```

가 됩니다.

즉 모델은 category별 효과를 별도의 weight로 학습할 수 있습니다.

## 5. Binary category에서도 필요한가

category가 두 개뿐이면 하나의 0/1 column으로 표현할 수 있습니다.

```text
No  -> 0
Yes -> 1
```

항상 두 개의 one-hot column을 만들어야 하는 것은 아닙니다.

## 6. Dummy Variable Trap

선형 회귀처럼 완전한 다중공선성이 문제가 될 수 있는 모델에서는 category K개 중 K-1개 column만 사용하는 방식도 흔합니다.

예:

```text
Red   -> [0,0]
Green -> [1,0]
Blue  -> [0,1]
```

여기서 Red가 baseline category입니다.

모델 종류와 구현체에 따라 처리 방식이 다르므로 무조건 column 하나를 삭제해야 한다고 외우기보다 **모델과 library의 동작을 확인**하는 것이 좋습니다.

## 7. High Cardinality 문제

category가 3개가 아니라 100만 개라면 one-hot vector도 매우 커집니다.

예:

```text
user_id = 1,000,000 categories
       ↓
1,000,000-dimensional sparse vector
```

문제:

- 차원 폭증
- 메모리 사용 증가
- 희소성 증가
- 새로운 category 처리 어려움

이럴 때는:

- hashing
- frequency encoding
- target encoding
- learned embedding

등 다른 방법을 검토할 수 있습니다.

## 8. Unknown Category

학습 데이터에는 없던 category가 inference 때 나타날 수 있습니다.

예:

```text
Train: Red, Green, Blue
Serving: Yellow
```

pipeline이 unknown category를 어떻게 처리할지 미리 정해야 합니다.

- all-zero
- unknown 전용 category
- encoder의 handle_unknown 옵션

등이 가능합니다.

## 9. Ordinal Encoding과의 차이

실제로 순서가 있는 category라면 one-hot만이 유일한 답은 아닙니다.

예:

```text
Small < Medium < Large
Low < Medium < High
```

이 경우 순서 정보를 유지하는 ordinal encoding이 더 자연스러울 수 있습니다.

따라서 핵심 질문은:

> 이 category 사이에 실제 순서가 존재하는가?

입니다.

## 10. Embedding과의 연결

LLM에서 token을 one-hot vector처럼 거대한 희소 vector로 직접 처리하면 비효율적입니다.

그래서 token ID를 dense embedding vector로 변환합니다.

```text
token id
   ↓
embedding lookup
   ↓
dense vector
```

One-hot Encoding을 이해하면 embedding이 왜 필요한지도 더 쉽게 이해할 수 있습니다.

## 핵심 요약

```text
One-hot Encoding
= 순서가 없는 category마다 독립적인 0/1 column을 만들어
  숫자 크기나 거리라는 가짜 의미를 부여하지 않는 표현법
```

적합:

- category 수가 비교적 적음
- category에 자연스러운 순서가 없음

주의:

- high cardinality
- unknown category
- train/serving encoder 불일치
- 모델에 따른 다중공선성

## 이해 확인

1. Red=1, Green=2, Blue=3이 왜 잘못된 수치 관계를 만들 수 있나요?
2. category가 50만 개라면 one-hot이 부담스러운 이유는 무엇인가요?
3. Small/Medium/Large에는 one-hot과 ordinal 중 어떤 표현을 먼저 검토할 수 있을까요?

## 관련 자료

- 원본 영상: https://www.youtube.com/watch?v=6AmedU5i9go
- [Feature Engineering 상세 영상 학습 노트](feature-engineering-in-machine-learning.md)
- [Feature Engineering 상세 블로그 학습 노트](../../blogs/module-01/feature-engineering.md)
- 모듈 1: [머신러닝 기초](../../module-01.md)
