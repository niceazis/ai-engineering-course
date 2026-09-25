# Tokenization in Large Language Models (LLMs) — 한국어 상세 영상 학습 노트

> 영상: https://www.youtube.com/watch?v=sK2s9I84EVI  
> 제공: Outcome School  
> 검증 범위: 영상 URL과 제목은 Outcome School 공식 과정/공식 GitHub 자료에서 확인했습니다. **YouTube 자막 전문은 직접 확보·검증하지 못했습니다.** 따라서 아래 내용은 자막의 문장별 번역이 아니라 공식 영상 주제와 같은 과정의 BPE 원문을 근거로 만든 상세 학습 노트입니다.

## 1. LLM이 문자열을 바로 읽지 못하는 이유

신경망은 텍스트 문자열이 아니라 숫자 tensor를 처리합니다.

따라서:

    "I love AI"
       ↓
    tokens
       ↓
    token IDs
       ↓
    embedding vectors

의 변환이 필요합니다.

Tokenization은 문자열을 모델 vocabulary에 존재하는 단위로 나누고 각 단위를 integer ID로 바꾸는 과정입니다.

## 2. Token은 반드시 단어가 아니다

가능한 token 단위:

- word
- character
- byte
- subword

현대 LLM에서는 subword/byte 기반 tokenizer가 널리 사용됩니다.

이유는 word-level과 character-level의 trade-off 때문입니다.

### Word-level 문제

- vocabulary가 지나치게 커짐
- 새로운 이름/오타/신조어 처리 어려움
- OOV 문제

### Character-level 문제

- vocabulary는 작지만 sequence가 길어짐
- token 하나의 의미 단위가 너무 작음

Subword는 흔한 패턴은 크게, 희귀한 패턴은 작게 나누는 절충안입니다.

## 3. BPE의 핵심

Byte Pair Encoding 계열의 기본 직관:

1. 작은 단위에서 시작
2. corpus에서 자주 붙는 adjacent pair를 셈
3. 가장 빈번한 pair를 하나의 token으로 merge
4. 목표 vocabulary size까지 반복

공식 Outcome School BPE 레슨의 예:

    low      × 5
    lower    × 2
    newest   × 6
    widest   × 3

초기 문자 단위에서:

- e+s: 9회
- s+t: 9회
- t+_: 9회
- l+o: 7회
- o+w: 7회

처럼 빈도를 세고 merge합니다.

    e + s → es
    es + t → est
    l + o → lo
    lo + w → low

## 4. Tokenizer 학습과 Tokenization 실행은 다르다

### Tokenizer 학습

corpus에서 vocabulary와 merge rule을 만듭니다.

### 실제 tokenization

이미 정해진 vocabulary/merge rule을 새 텍스트에 적용합니다.

공식 레슨의 단순 예:

    lowest
    → l o w e s t
    → l o w es t
    → l o w est
    → lo w est
    → low est

결과:

    ["low", "est"]

즉 모델 inference 시 매번 pair 빈도를 새로 학습하는 것이 아닙니다.

## 5. Token ID와 Embedding의 관계

Tokenizer 결과:

    ["low", "est"]
       ↓
    [421, 983]

같은 token ID는 embedding table의 row를 가리킵니다.

    token id 421
       ↓
    embedding[421]
       ↓
    d_model 차원 vector

따라서 tokenizer vocabulary와 모델의 input embedding/output vocabulary weight는 강하게 결합되어 있습니다.

학습된 모델에서 tokenizer만 임의로 교체하면 token ID 의미가 달라져 모델이 정상 동작하지 않습니다.

## 6. Context Window와 비용

LLM의 context length는 보통 “글자 수”가 아니라 **token 수**로 제한됩니다.

같은 의미라도:

- 언어
- 공백
- 특수문자
- 코드
- tokenizer 종류

에 따라 token 수가 달라집니다.

따라서 API 비용, latency, KV cache 메모리도 tokenization과 직접 연결됩니다.

## 7. Special Token

실제 tokenizer에는 일반 텍스트 이외의 special token이 있을 수 있습니다.

예:

- BOS: sequence 시작
- EOS: sequence 종료
- PAD: batch padding
- role/control token: system/user/assistant 구분

정확한 token 이름과 ID는 모델마다 다릅니다.

## 8. 직접 확인할 때의 실습

모델별 tokenizer로 같은 문자열을 tokenize해 비교해 보십시오.

확인 항목:

1. token 문자열
2. token IDs
3. 총 token 수
4. decode해서 원문이 복원되는지
5. 영어/한국어/코드의 token 수 차이

## 핵심 정리

- Tokenization은 텍스트를 모델이 처리할 integer IDs로 바꾸는 첫 단계입니다.
- token은 단어와 같지 않으며 subword/byte 단위가 흔합니다.
- BPE는 빈번한 pair를 반복 merge해 vocabulary를 학습합니다.
- tokenizer 학습과 실제 tokenization 실행을 구분해야 합니다.
- token 수는 context window, API 비용, latency, KV cache와 직접 연결됩니다.
- 이 노트는 영상 자막 직역이 아니라 공식 영상 주제와 Outcome School BPE 자료를 바탕으로 한 학습 보조 자료입니다.
