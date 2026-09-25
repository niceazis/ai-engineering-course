# 순환 신경망(RNN)이란? — 원문 기반 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/recurrent-neural-network  
> Amit Shekhar / Outcome School · 2019-08-02  
> 원문은 짧은 개념 소개 글입니다. 아래에서는 원문의 핵심 비유와 설명을 먼저 정리하고, 이해에 필요한 보충 설명은 별도로 구분합니다.

## 원문이 강조하는 핵심

일반적인 feed-forward network는 입력들을 독립적으로 처리하는 반면, RNN은 **이전 시점의 정보를 내부 상태로 이어받아 다음 입력을 처리**할 수 있습니다.

원문은 영화를 보는 상황에 비유합니다. 영화의 현재 장면을 이해하려면 앞에서 본 내용의 맥락을 기억해야 합니다. 문장의 다음 단어를 예측할 때도 이전 단어들이 문맥을 만듭니다.

RNN은 이런 sequence context를 유지하기 위해 network 안에 반복 연결을 둡니다.

## 시간축으로 펼쳐 보기

한 시점의 계산을 개념적으로 쓰면:

```text
현재 입력 x_t
   +
이전 hidden state h_(t-1)
   ↓
새 hidden state h_t
   ↓
현재 output y_t
```

같은 RNN cell이 시간에 따라 반복 사용됩니다.

```text
x1 -> [RNN] -> h1
             ↓
x2 -> [RNN] -> h2
             ↓
x3 -> [RNN] -> h3
```

이 때문에 현재 output이 과거 입력의 영향을 받을 수 있습니다.

## 원문의 대표 사용 맥락

원문은 sequence context가 중요한 예로 다음을 언급합니다.

- 연결된 손글씨 인식
- 음성 인식
- 문장에서 다음 단어 예측

공통점은 현재 입력 하나만으로 판단하기보다 앞뒤 순서와 맥락이 중요하다는 것입니다.

## 보충: hidden state가 '모든 것'을 완벽히 기억하는 것은 아니다

원문은 이해를 돕기 위해 RNN이 이전 정보를 기억한다고 표현합니다. 실제 기본 RNN에서는 sequence가 길어질수록 오래된 정보가 희석될 수 있습니다.

Backpropagation Through Time 과정에서 vanishing/exploding gradient 문제가 생기기 쉽고, 이를 완화하기 위해 LSTM과 GRU 같은 구조가 발전했습니다.

이 부분은 원문의 직접 설명을 확장한 보충 내용입니다.

## 보충: RNN과 Transformer의 차이

RNN은 시간 순서대로 hidden state를 전달하는 구조라 sequence를 본질적으로 순차 처리합니다.

Transformer는 self-attention으로 여러 token 관계를 병렬적으로 계산할 수 있어 대규모 언어 모델에서는 Transformer가 주류가 되었습니다.

그렇다고 RNN 개념이 불필요한 것은 아닙니다. sequence modeling에서 **상태를 시간축으로 전달한다**는 아이디어를 이해하는 데 중요한 기반입니다.

## 핵심 구분

```text
Feed-forward:
입력 -> 출력
각 입력 처리에 이전 상태가 필수는 아님

RNN:
현재 입력 + 이전 상태 -> 새 상태/출력
sequence의 순서와 context를 반영
```

## 이해 확인

1. 다음 단어 예측에 이전 단어 정보가 필요한 이유는 무엇인가요?
2. RNN의 hidden state는 어떤 역할을 하나요?
3. 긴 sequence에서 기본 RNN이 어려움을 겪는 이유는 무엇인가요?

## 연결 학습

- 원문: https://outcomeschool.com/blog/recurrent-neural-network
- 이전: [RMSNorm](rmsnorm-root-mean-square-layer-normalization.md)
- 다음: [PyTorch](how-does-pytorch-work.md)
- [모듈 2](../../module-02.md)
