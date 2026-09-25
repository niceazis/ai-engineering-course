# LLM의 Byte Pair Encoding(BPE)이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/bpe-in-llms  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문의 설명 순서와 BPE 학습 예제를 보존한 독립적 한국어 해설입니다.

## 1. Tokenization부터 시작하기

모델은 문자열 자체가 아니라 숫자 ID를 처리합니다. 따라서 텍스트를 작은 조각인 token으로 나누고 각 token을 ID로 바꾸는 과정이 필요합니다. 이것이 tokenization입니다.

“I love teaching AI”를 예로 들면 먼저 텍스트를 적절한 단위로 자른 뒤 각 조각을 vocabulary의 ID로 매핑합니다.

문제는 **어디를 기준으로 얼마나 크게 자를 것인가**입니다.

## 2. 단어 단위와 문자 단위의 한계

### Word-level

“I love teaching”을 세 단어로 나누는 방식은 직관적이지만 vocabulary가 너무 커집니다.

- 이름, 신조어, 기술 용어, 오타, 다국어 표현을 모두 별도 단어로 다루기 어렵습니다.
- 학습에 없던 단어는 unknown token으로 뭉개질 수 있습니다.

### Character-level

“I love”를 I, 공백, l, o, v, e처럼 문자 단위로 나누면 unknown 문제는 줄어듭니다.

하지만 원문의 예처럼 10단어 문장이 50개 이상의 작은 token이 될 수 있습니다. sequence가 길어지고 각 token이 담는 의미도 지나치게 작아집니다.

BPE는 이 두 극단 사이의 **subword 단위**를 학습합니다.

## 3. BPE의 핵심 아이디어

BPE(Byte Pair Encoding)는 처음에는 작은 단위에서 시작하고, 데이터에서 **가장 자주 붙어 등장하는 인접 token pair를 반복적으로 합칩니다.**

그 결과 vocabulary에는 다음이 섞입니다.

- 매우 자주 등장하는 완전한 단어
- ing, tion, est 같은 흔한 subword
- 희귀 패턴을 처리하기 위한 작은 단위

즉 자주 등장하는 패턴은 큰 token으로 압축하고, 드문 표현은 더 작은 token 조합으로 표현합니다.

## 4. 원문의 학습 corpus

원문은 다음 빈도를 사용합니다.

    low      × 5
    lower    × 2
    newest   × 6
    widest   × 3

처음에는 각 단어를 문자로 나누고 end-of-word 표시를 붙입니다.

    l o w _        × 5
    l o w e r _    × 2
    n e w e s t _  × 6
    w i d e s t _  × 3

초기 vocabulary는 문자 집합입니다.

    {l, o, w, e, r, n, s, t, i, d, _}

## 5. 가장 빈번한 pair 찾기

인접 pair 빈도를 세면 원문의 일부 결과는 다음과 같습니다.

- e s: newest 6회 + widest 3회 = 9
- s t: 9
- t _: 9
- l o: low 5회 + lower 2회 = 7
- o w: 7

예제에서는 e s를 먼저 합쳐 es라는 새 token을 만듭니다.

    n e w es t _
    w i d es t _

vocabulary에 es가 추가됩니다.

## 6. Merge를 반복하기

다음에는 es t가 9회 나타나므로 est로 합칩니다.

    n e w est _
    w i d est _

이후 est _, l o → lo, lo w → low 같은 merge가 이어질 수 있습니다.

매 merge마다:

1. vocabulary에 새 token이 하나 생기고
2. corpus 표현은 더 적은 수의 token으로 압축됩니다.

## 7. 언제 멈추는가

목표 vocabulary size에 도달하면 merge 학습을 멈춥니다.

원문은 현대 LLM의 예시 범위로 대략 32,000~256,000 token을 언급하고, 구체적으로:

- LLaMA 3: 약 128K
- Gemma: 약 256K

를 예로 듭니다.

이 값은 모델/토크나이저 버전에 따라 달라질 수 있으므로 특정 모델을 구현할 때는 실제 tokenizer 설정을 확인해야 합니다.

## 8. 새 텍스트를 tokenize하는 방법

BPE 학습 결과는 단순한 vocabulary만이 아닙니다. **merge rule의 순서**도 중요합니다.

원문의 “lowest” 예:

    시작: l o w e s t
    e s → es: l o w es t
    es t → est: l o w est
    l o → lo: lo w est
    lo w → low: low est

결과:

    ["low", "est"]

“newer”도 학습된 merge rule을 순서대로 적용해 ["new", "er"]처럼 분해할 수 있습니다.

핵심은 “현재 vocabulary에서 가장 긴 문자열을 무조건 greedy하게 찾는다”가 아니라, **학습 때 정해진 merge 우선순위를 재현한다**는 것입니다.

## 9. 희귀 단어를 처리하는 방식

“widestness”처럼 학습 corpus에 없던 단어도 이미 배운 subword merge가 적용되는 부분은 합쳐지고, 나머지는 더 작은 단위로 남습니다.

따라서 완전히 새로운 단어라도 이미 알고 있는 subword나 더 작은 기본 단위로 표현할 수 있습니다. 이것이 word-level tokenizer의 OOV(Out-Of-Vocabulary) 문제를 크게 줄이는 이유입니다.

실제 GPT 계열의 byte-level BPE처럼 byte를 기본 단위로 쓰는 변형에서는 임의의 UTF-8 텍스트에 대한 fallback 성질이 더 강해집니다. 다만 원문의 교육용 예제는 문자 단위와 end-of-word 표기를 사용해 알고리즘을 설명합니다.

## 10. 왜 LLM에서 유용한가

BPE의 trade-off는 다음과 같습니다.

- word-level보다 vocabulary를 통제하기 쉽습니다.
- character-level보다 sequence를 짧게 만들 수 있습니다.
- 흔한 단어와 접사는 큰 token으로 효율적으로 표현합니다.
- 드문 단어도 작은 subword 조합으로 처리할 수 있습니다.

그러나 token 경계가 인간의 “단어” 경계와 같지는 않습니다. 같은 문자열도 공백, 대소문자, 언어, tokenizer 규칙에 따라 다른 token sequence가 됩니다.

## 11. LLM 실무에서 반드시 연결해서 볼 것

tokenization은 모델 바깥의 전처리가 아니라 모델 동작과 비용에 직접 연결됩니다.

- context window는 보통 “문자 수”가 아니라 token 수 기준입니다.
- API 비용도 token 기준인 경우가 많습니다.
- 같은 문장이라도 tokenizer에 따라 token 수가 달라집니다.
- tokenizer vocabulary와 모델 embedding matrix는 맞물려 있습니다.
- tokenizer를 바꾸면 기존 모델 weight와 호환되지 않을 수 있습니다.

## 핵심 정리

- BPE는 빈번한 인접 pair를 반복해서 merge하는 subword tokenizer입니다.
- 학습 결과는 vocabulary와 ordered merge rules입니다.
- 원문의 low/lower/newest/widest 예제에서 e+s→es, es+t→est처럼 빈도가 높은 pair를 합칩니다.
- 새 문장은 학습한 merge rule을 같은 순서로 적용해 tokenize합니다.
- word-level의 OOV 문제와 character-level의 지나친 sequence 길이 사이에서 균형을 잡습니다.

## 원문

- https://outcomeschool.com/blog/bpe-in-llms
