# RNN과 Transformer는 어떻게 다른가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-do-rnns-and-transformers-differ  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 공식 글과 과정 개요에서 확인한 설명 흐름을 바탕으로 다시 쓴 독립적인 한국어 해설입니다.

## 1. 두 구조가 풀려는 문제

RNN과 Transformer는 모두 **순서가 있는 데이터(sequence)**를 처리하기 위한 신경망 구조입니다. 문장은 단어 순서가 의미를 바꾸므로 각 token을 서로 독립적으로 볼 수 없습니다.

예를 들어 다음 두 문장은 단어 집합이 비슷하지만 순서가 다릅니다.

- “dog bites man”
- “man bites dog”

따라서 sequence model은 현재 token뿐 아니라 다른 token과의 관계를 표현해야 합니다.

## 2. RNN: 한 단계씩 읽고 상태를 넘긴다

RNN(Recurrent Neural Network)은 token을 순서대로 처리합니다.

    x1 → h1
          ↓
    x2 → h2
          ↓
    x3 → h3
          ↓
         ...

일반적인 형태는 다음과 같습니다.

    h_t = f(x_t, h_(t-1))

현재 hidden state (h_t)는 현재 입력 (x_t)와 이전 상태 (h_{t-1})에 의존합니다.

원문의 직관은 “문장을 한 단어씩 읽으면서 지금까지 읽은 내용을 작은 메모리에 들고 가는 방식”입니다.

## 3. RNN의 두 가지 핵심 한계

### 3.1 순차 계산

(h_t)를 계산하려면 (h_{t-1})이 먼저 필요합니다. 따라서 한 sequence 안의 time step을 완전히 병렬로 계산하기 어렵습니다.

길이가 길어질수록:

- GPU 병렬 처리 효율이 떨어지고
- 학습 시간이 늘어나며
- 긴 문맥 처리 비용이 커집니다.

### 3.2 먼 정보가 약해지는 문제

초반 token의 정보가 여러 hidden state를 거쳐 뒤쪽까지 전달되어야 합니다.

긴 문장에서 첫 번째 단어와 50번째 단어의 관계를 잡아야 한다면 정보가 수십 단계의 recurrent transition을 통과합니다. 이 과정에서 gradient vanishing/exploding과 장기 의존성 문제가 발생하기 쉽습니다.

LSTM과 GRU는 gate를 도입해 이 문제를 완화하지만, 순차 처리라는 구조적 제약 자체는 남습니다.

## 4. Transformer: 모든 token 사이를 attention으로 직접 연결한다

Transformer는 recurrent hidden state를 순서대로 넘기는 대신 **self-attention**으로 각 token이 다른 token을 직접 참고하게 합니다.

문장에 (n)개 token이 있다면 attention score는 개념적으로 (n 	imes n) 관계를 만듭니다.

예:

    "The animal did not cross the street because it was tired."

“it”이 무엇을 가리키는지 판단할 때 “animal”과 직접 높은 attention 관계를 만들 수 있습니다. 둘 사이에 여러 recurrent step을 거칠 필요가 없습니다.

## 5. 핵심 차이를 한 줄로 요약하면

- **RNN**: 한 단계씩 읽으며 이전 상태를 다음 단계로 전달합니다.
- **Transformer**: sequence 전체의 token 관계를 attention으로 직접 계산합니다.

이 차이가 학습 병렬성과 장거리 관계 처리의 차이로 이어집니다.

## 6. 계산 관점 비교

| 관점 | RNN | Transformer |
| --- | --- | --- |
| sequence 처리 | 순차적 | 학습 시 token 병렬 처리 가능 |
| 정보 전달 | hidden state를 단계적으로 전달 | attention으로 token 간 직접 연결 |
| 장거리 의존성 | 여러 recurrent step을 거침 | 두 위치가 attention으로 직접 상호작용 |
| 학습 병렬화 | 제한적 | 매우 유리 |
| 긴 sequence 비용 | step 수에 비례하는 순차 지연 | 일반 self-attention은 (O(n^2)) 메모리/연산 |
| 대표 활용 | 소규모 시계열, streaming recurrent 구조 | 현대 LLM, 번역, 비전 등 |

Transformer가 모든 면에서 공짜로 더 좋은 것은 아닙니다. 표준 self-attention은 sequence 길이가 (n)일 때 attention matrix가 (n^2)로 커집니다. 그래서 긴 문맥에서는 sliding-window attention, sparse attention, linear attention 같은 변형이 사용됩니다.

## 7. Transformer가 학습에서 빠른 이유

RNN은 같은 문장 안에서 다음 hidden state가 이전 hidden state를 기다립니다.

반면 Transformer 학습에서는 한 layer 안에서 여러 token의 Q/K/V projection을 행렬 연산으로 동시에 계산할 수 있습니다.

GPU/TPU는 큰 행렬 곱을 병렬 처리하는 데 매우 적합하므로, 대규모 데이터셋에서 이 차이가 중요합니다.

단, autoregressive LLM의 **추론(decode)**은 여전히 이전에 생성한 token이 있어야 다음 token을 생성할 수 있으므로 생성 단계 자체는 순차적입니다. Transformer의 “병렬 처리”를 학습과 생성 모두에 동일하게 적용되는 특징으로 오해하면 안 됩니다.

## 8. 언제 RNN이 여전히 유용한가

Transformer가 현대 언어 모델의 주류지만 RNN 계열이 항상 무의미한 것은 아닙니다.

다음 조건에서는 recurrent 구조가 고려될 수 있습니다.

- 매우 작은 모델이 필요한 경우
- 한 샘플씩 지속적으로 들어오는 streaming 시계열
- 메모리를 엄격하게 제한해야 하는 edge 환경
- task가 짧은 local dependency 중심이고 모델 단순성이 중요한 경우

반대로 대규모 텍스트, 긴 문맥, 대규모 병렬 학습에서는 Transformer 계열이 일반적으로 더 적합합니다.

## 9. 이 레슨이 다음 Transformer 레슨과 연결되는 방식

RNN과 Transformer의 차이를 이해하면 다음 질문이 자연스럽게 이어집니다.

1. recurrence가 없는데 token 순서는 어떻게 표현하는가? → positional encoding / RoPE
2. token끼리 무엇을 기준으로 참고하는가? → Q, K, V
3. 미래 token을 보면 안 되는 decoder에서는 어떻게 제한하는가? → causal mask
4. 서로 다른 관계를 동시에 어떻게 학습하는가? → multi-head attention
5. attention 뒤에서 각 token 표현을 어떻게 변환하는가? → FFN

## 핵심 정리

- RNN은 이전 hidden state를 다음 step에 넘기는 순차 구조입니다.
- 긴 sequence에서는 장거리 정보 전달과 병렬화에 제약이 있습니다.
- Transformer는 self-attention으로 token 간 직접 관계를 만듭니다.
- 학습 시 token 차원의 병렬화가 가능해 대규모 GPU 학습에 유리합니다.
- 표준 attention은 (O(n^2)) 비용이라는 별도 trade-off가 있습니다.
- autoregressive Transformer의 추론은 여전히 token-by-token입니다.

## 원문

- https://outcomeschool.com/blog/how-do-rnns-and-transformers-differ
