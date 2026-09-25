# Transformer의 Encoder vs Decoder — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/encoder-vs-decoder-in-transformers  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 설명 순서와 예시를 보존해 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Transformer에서 Encoder와 Decoder가 하는 일

Transformer를 가장 단순하게 나누면:

- **Encoder**: 입력을 이해하고 문맥화된 표현을 만듭니다.
- **Decoder**: 지금까지의 출력과 조건 정보를 바탕으로 다음 token을 생성합니다.

둘 다 attention과 FFN을 사용하지만, **볼 수 있는 정보의 범위와 목적**이 다릅니다.

## 2. 먼저 token을 이해하기

문장:

    "I love AI"

은 tokenizer를 거쳐 여러 token으로 나뉘고 각 token이 embedding vector로 바뀝니다.

Transformer는 이 vector sequence를 처리합니다.

Encoder와 Decoder의 차이는 같은 token representation을 “어떤 attention 규칙으로 처리하느냐”에서 시작합니다.

## 3. Encoder: 입력 전체를 양방향으로 본다

Encoder self-attention에서는 일반적으로 한 token이 입력의 앞뒤 모든 token을 볼 수 있습니다.

예:

    "The bank of the river was muddy."

“bank”가 금융기관이 아니라 강둑이라는 의미를 결정하려면 뒤의 “river”가 중요합니다.

Encoder는 뒤 token도 참고할 수 있으므로 이런 **양방향 문맥 이해**에 적합합니다.

개념적 mask:

    token1  1 1 1 1
    token2  1 1 1 1
    token3  1 1 1 1
    token4  1 1 1 1

padding token 같은 특수 위치는 별도 mask로 제외할 수 있지만, 미래 방향을 막는 causal mask는 일반 encoder self-attention에는 필요하지 않습니다.

## 4. Decoder: 과거만 보고 다음 token을 만든다

Autoregressive decoder는 다음 token을 예측할 때 미래 token을 보면 안 됩니다.

예를 들어:

    "The sky is"

까지 주어졌을 때 “blue”를 예측해야 합니다.

학습 시 정답 문장 전체가 입력에 있어도 causal mask를 적용합니다.

    현재 위치  볼 수 있는 위치
    1          1
    2          1,2
    3          1,2,3
    4          1,2,3,4

따라서 decoder self-attention은 **left-to-right 생성 규칙**을 유지합니다.

## 5. 가장 중요한 차이

| 항목 | Encoder | Decoder |
| --- | --- | --- |
| 주 목적 | 입력 이해/표현 | 출력 생성 |
| attention 방향 | 보통 양방향 | causal, 과거 방향 |
| 미래 token | 볼 수 있음 | 볼 수 없음 |
| 대표 모델 | BERT | GPT 계열 |
| 대표 작업 | 분류, embedding, 추출 | 챗봇, 문서/코드 생성 |

“Encoder=이해, Decoder=생성”은 좋은 첫 직관이지만 절대적인 규칙으로 보면 안 됩니다. 실제 모델은 학습 목표와 architecture에 따라 다양한 작업을 할 수 있습니다.

## 6. Encoder-only Transformer

대표 예는 BERT입니다.

흐름:

    입력 token
      → encoder layer × N
      → 양방향 contextual representation
      → task head

주요 활용:

- 문장 분류
- named entity recognition
- 검색용 representation
- token-level prediction

입력 전체를 이미 알고 있는 문제에 적합합니다.

## 7. Decoder-only Transformer

GPT, ChatGPT의 기반이 되는 GPT 계열과 Claude, Gemini의 주요 언어 생성 구조는 decoder-only causal Transformer 계열로 이해할 수 있습니다.

흐름:

    prompt tokens
      → causal decoder layers
      → next-token logits
      → token 선택
      → prompt 뒤에 추가
      → 반복

장점은 하나의 next-token objective로 다양한 생성 작업을 통합하기 쉽다는 점입니다.

## 8. Encoder-Decoder Transformer

T5 같은 모델은 두 부분을 모두 사용합니다.

번역 예:

    Encoder input:
    "I love AI"
          ↓
      Encoder
          ↓
    contextual states
          ↓
      Decoder
          ↓
    "J'aime l'IA"

Decoder에는 두 attention이 있습니다.

1. masked self-attention: 지금까지 생성한 출력 token을 봅니다.
2. cross-attention: encoder가 만든 입력 representation을 봅니다.

이 구조는 입력 sequence와 출력 sequence의 역할이 명확히 다른 translation/summarization 계열 task에 자연스럽습니다.

## 9. Self-Attention과 Cross-Attention의 차이

Encoder self-attention:

    Q, K, V ← encoder 입력

Decoder masked self-attention:

    Q, K, V ← decoder 현재 sequence

Encoder-decoder cross-attention:

    Q ← decoder
    K, V ← encoder

즉 cross-attention은 “현재 무엇을 생성할지”를 나타내는 decoder query가 입력 문장의 어떤 부분을 참고할지 결정합니다.

## 10. 언제 무엇을 선택할까

Architecture 선택은 task의 데이터 흐름에서 시작하면 됩니다.

- 입력 전체를 읽고 label/representation이 필요 → encoder-only
- prompt 뒤에 계속 token을 생성 → decoder-only
- 명확한 source sequence를 읽고 별도 target sequence를 생성 → encoder-decoder

최근에는 대형 decoder-only LLM이 프롬프트만으로 많은 task를 수행하므로 응용 범위가 넓지만, 항상 계산 효율이나 정확도가 최적이라는 뜻은 아닙니다.

## 핵심 정리

- Encoder는 입력 전체를 양방향으로 볼 수 있습니다.
- Autoregressive Decoder는 causal mask로 미래 token을 차단합니다.
- Encoder-only는 BERT, decoder-only는 GPT 계열, encoder-decoder는 T5가 대표적입니다.
- Encoder-decoder의 decoder는 masked self-attention과 encoder cross-attention을 함께 사용합니다.
- 구조 선택은 “전체 입력을 이해하는가 / 순차 생성하는가 / source→target 변환인가”로 판단하면 쉽습니다.

## 원문

- https://outcomeschool.com/blog/encoder-vs-decoder-in-transformers
