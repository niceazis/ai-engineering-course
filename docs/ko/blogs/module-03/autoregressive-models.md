# Autoregressive Model이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/autoregressive-models  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 학습 순서·수치 예제·비교를 보존하되 문장은 독립적으로 다시 쓴 한국어 해설입니다.

## 1. Autoregressive Model의 뜻

원문은 먼저 token을 “모델이 읽고 쓰는 작은 텍스트 조각”으로 정의한 뒤 Autoregressive라는 이름을 분해합니다.

- Auto: 자기 자신의 이전 출력도 다음 입력의 일부로 사용
- Regressive: 과거 값을 바탕으로 다음 값을 예측

따라서 autoregressive language model은 **이전까지의 모든 토큰을 조건으로 다음 토큰 하나를 예측하고, 그 결과를 다시 문맥에 붙여 같은 작업을 반복하는 모델**입니다.

“I love AI”를 단순화하면 다음과 같습니다.

1. “I”를 보고 “love”를 예측
2. “I love”를 보고 “AI”를 예측
3. “I love AI”를 보고 다음 토큰 또는 종료 토큰을 예측

## 2. 확률의 Chain Rule

전체 시퀀스의 결합확률은 다음처럼 조건부 확률의 곱으로 분해됩니다.

    P(x1, x2, ..., xn)
      = P(x1)
      × P(x2 | x1)
      × P(x3 | x1, x2)
      × ...
      × P(xn | x1, ..., x(n-1))

“I love AI”라면:

    P("I love AI")
      = P("I")
      × P("love" | "I")
      × P("AI" | "I", "love")

즉 모델이 반복해서 푸는 문제는 동일합니다.

> “지금까지 본 모든 토큰이 주어졌을 때 다음 토큰의 확률은 얼마인가?”

## 3. 생성 루프

원문의 생성 루프는 네 단계입니다.

1. 지금까지의 past tokens를 모델에 넣습니다.
2. vocabulary 전체에 대한 다음 토큰 확률을 얻습니다.
3. greedy, temperature sampling 등의 방법으로 토큰 하나를 고릅니다.
4. 선택한 토큰을 past에 붙이고 반복합니다.

의사코드로 쓰면:

    past = [start_token]

    while not done:
        probs = model(past)
        next_token = sample(probs)
        past = past + [next_token]

        if next_token == end_token:
            done = True

100개의 새 토큰을 생성하려면 기본적인 autoregressive decoding에서는 모델의 decode step도 100번 이어집니다. 이 순차 의존성이 생성 품질의 장점과 지연 시간의 단점을 동시에 만듭니다.

## 4. 원문의 단계별 수치 예제

원문은 vocabulary를 5개로 제한합니다.

    ["I", "love", "AI", "code", "<end>"]

### Step 1: “I” 다음

    I       0.05
    love    0.60
    AI      0.15
    code    0.15
    <end>   0.05

greedy decoding이라면 “love”를 선택합니다.

### Step 2: “I love” 다음

    I       0.05
    love    0.05
    AI      0.70
    code    0.15
    <end>   0.05

“AI”가 0.70으로 가장 높으므로 선택합니다.

### Step 3: “I love AI” 다음

    I       0.05
    love    0.05
    AI      0.05
    code    0.05
    <end>   0.80

종료 토큰이 선택되어 생성이 끝납니다.

### Step 4: 전체 시퀀스 확률

원문은 시작 확률을 P("I") = 0.20으로 두고 다음을 계산합니다.

    P("I love AI <end>")
      = 0.20 × 0.60 × 0.70 × 0.80
      = 0.0672

핵심은 모델이 전체 문장 확률을 한 번에 계산하는 것이 아니라, **각 단계의 조건부 확률을 이어서 전체 시퀀스를 구성한다**는 점입니다.

## 5. GPT 계열이 autoregressive인 이유

GPT 계열 decoder-only Transformer의 기본 학습 목표는 next-token prediction입니다.

추론 시에는:

1. prompt가 초기 past가 됩니다.
2. next token을 예측합니다.
3. 예측 토큰을 past에 추가합니다.
4. 새 past로 다시 next token을 예측합니다.
5. 종료 조건까지 반복합니다.

이 구조 때문에 출력 길이를 유연하게 늘릴 수 있고 token streaming도 가능합니다.

## 6. Causal Masking이 필요한 이유

학습에서는 효율을 위해 문장 전체 토큰을 한 번에 GPU에 넣을 수 있습니다. 하지만 각 위치가 정답인 미래 토큰을 미리 보면 next-token prediction이 성립하지 않습니다.

“I love AI”의 causal mask를 단순화하면:

    현재 토큰   I   love   AI
    I           1    0      0
    love        1    1      0
    AI          1    1      1

1은 볼 수 있는 위치, 0은 차단된 미래 위치입니다.

실제 attention에서는 미래 score에 매우 큰 음수, 개념적으로 −∞를 더한 뒤 softmax를 적용해 해당 위치의 weight를 0으로 만듭니다.

학습에서는 전체 문장을 보되 mask로 미래 접근을 막고, 추론에서는 애초에 미래 토큰이 존재하지 않습니다. 이 둘이 같은 autoregressive 규칙을 따르게 됩니다.

## 7. KV Cache와의 관계

autoregressive decoding의 비효율은 이전 토큰의 K와 V를 매 step 다시 계산하는 데서 커집니다.

1,000개 토큰을 생성한다고 가정하면 원문의 단순 계산은:

    1 + 2 + 3 + ... + 1000 = 500,500

이전 K/V를 매번 다시 만든다면 약 500,500 단위의 K/V 계산이 필요합니다.

KV Cache를 사용하면 이미 계산한 과거 K/V를 저장하고 새 토큰의 K/V만 추가하므로 약 1,000 단위로 줄어듭니다.

주의할 점은 attention 자체의 모든 비용이 500,500에서 1,000으로 줄어든다는 뜻이 아니라, **과거 토큰의 K/V projection 재계산을 제거한다는 설명**입니다.

## 8. Autoregressive vs Non-Autoregressive

| 항목 | Autoregressive | Non-Autoregressive |
| --- | --- | --- |
| 생성 순서 | 한 토큰씩 순차 | 여러 위치를 병렬 생성 가능 |
| 의존성 | 이전 생성 토큰 전체 | 제한적 또는 다른 방식 |
| 지연 | 출력 길이에 따라 증가 | 병렬화에 유리 |
| 일반적 특성 | 유창성과 일관성에 강함 | 빠르지만 목적에 따라 품질 trade-off |
| 예 | GPT, PixelCNN, WaveNet | 일부 병렬 decoder, diffusion 계열 |

원문은 VAE와 GAN을 “전체 결과를 한 번에 생성하는 비-autoregressive 예”로 소개하고, 텍스트에서는 Diffusion Language Model을 병렬 생성 방향의 대표 예로 연결합니다.

## 9. 텍스트 이외의 Autoregressive Model

- GPT 계열: token by token
- PixelCNN: pixel by pixel
- WaveNet: audio sample by sample
- 일부 음악 모델: note by note

원문은 WaveNet 예에서 16 kHz 오디오라면 1초를 16,000개 sample로 볼 수 있음을 들어 순차 생성 비용을 직관적으로 설명합니다.

## 10. 장점과 한계

### 장점

- 이전 전체 문맥을 조건으로 하므로 자연스럽고 일관된 생성에 유리
- 학습 목표가 next-token prediction으로 단순
- 출력 길이가 유연
- 하나의 모델을 번역, 요약, 질의응답, 코드 생성 등 여러 작업에 사용할 수 있음

### 한계

- token t+1은 token t가 정해져야 계산 가능하므로 decode 병렬화가 어렵습니다.
- 출력이 길수록 latency가 증가합니다.
- 초반의 잘못된 토큰이 이후 문맥에 들어가 오류가 누적될 수 있습니다.

이를 완화하기 위해 KV Cache, speculative decoding, sampling 개선 등이 사용됩니다.

## 핵심 정리

- Autoregressive = 이전 출력까지 포함한 과거를 사용해 다음 값을 예측합니다.
- 수학적 기반은 확률의 chain rule입니다.
- GPT 계열은 next-token prediction을 반복하는 decoder-only autoregressive model입니다.
- causal masking은 학습 시 미래 정보 누출을 막습니다.
- KV Cache는 과거 K/V projection 재계산을 제거합니다.
- 핵심 trade-off는 순차 생성으로 인한 latency와 높은 생성 품질입니다.

## 원문

- https://outcomeschool.com/blog/autoregressive-models
