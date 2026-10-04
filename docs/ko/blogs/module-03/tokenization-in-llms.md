# LLM의 Tokenization — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/tokenization-in-llms  
> 원저자: Amit Shekhar / Outcome School  
> 게시일: 2026-10-03  
> 검증 상태: 2026-10-04 기준 정확한 원문 URL의 최신 검색 인덱스에서 본문·예제·수치·표를 확인했습니다. 원문 페이지 직접 열기는 cache miss로 실패했으므로, 아래는 확인 가능한 원문을 바탕으로 독립적으로 다시 쓴 학습 노트입니다.

## 1. Tokenization의 역할

LLM은 문자열이 아니라 정수 Token ID를 입력으로 받습니다.

원문의 첫 예제:

    I love learning
    -> "I" | " love" | " learning"
    -> 40 | 3021 | 6975

즉:

    Text -> Tokens -> Token IDs -> LLM

Token ID는 tokenizer마다 다릅니다.

## 2. 왜 필요한가

신경망은 숫자로 계산합니다. 따라서 텍스트를 숫자로 바꿔야 합니다. 동시에 token 크기를 정해야 합니다.

- 너무 큰 단위: vocabulary가 커지고 미등록 단어가 늘어남
- 너무 작은 단위: sequence가 길어져 context와 계산량 증가

Tokenization은 vocabulary 크기와 sequence 길이 사이의 균형입니다.

## 3. Token의 형태

Token은 단어, 단어 일부, 문자, 구두점, 앞쪽 공백을 포함한 문자열일 수 있습니다.

원문 예:

- cat -> 한 token
- unbelievable -> un | believ | able
- ! -> 한 token
- " love" -> 공백까지 포함한 token

영어 경험칙으로 원문은 1 token ≈ 4 characters ≈ 0.75 word, 100 tokens ≈ 75 words를 제시합니다. 이는 근사치입니다.

## 4. Character-level

    learning
    -> l | e | a | r | n | i | n | g

장점은 작은 vocabulary와 거의 없는 unknown word 문제입니다. 단점은 sequence가 너무 길고 각 token의 의미량이 작다는 점입니다. 원문은 100단어 문단이 약 500 token이 될 수 있다고 설명합니다.

## 5. Word-level

    I love learning
    -> I | love | learning

sequence는 짧지만 vocabulary가 매우 커집니다. 이름, 신조어, 코드, 다국어를 모두 단어별로 담기 어렵고, 없는 단어는 unknown token으로 대체될 수 있습니다. learn, learning, learned, learner도 서로 별도 token입니다.

## 6. Subword-level

현대 LLM의 일반적인 절충안입니다.

- the -> the
- learning -> learning
- tokenization -> token | ization
- unbelievable -> un | believ | able

자주 쓰는 표현은 크게, 드문 표현은 작은 재사용 조각으로 나눕니다. 원문은 일반적인 vocabulary 규모 예로 약 50,000~200,000을 제시합니다.

| 항목 | Character | Word | Subword |
| --- | --- | --- | --- |
| vocabulary | 매우 작음 | 매우 큼 | 중간 |
| token 수 | 매우 많음 | 적음 | 비교적 적음 |
| unknown word | 거의 없음 | 가능 | 거의 없음 |
| 현대 LLM | 드묾 | 드묾 | 널리 사용 |

## 7. BPE 원리

Byte Pair Encoding은 작은 단위에서 시작해 가장 자주 붙는 인접 pair를 반복 merge합니다.

1. 기본 단위로 시작
2. pair 빈도 계산
3. 최빈 pair merge
4. 다시 계산
5. 목표 vocabulary 크기까지 반복

## 8. 원문의 BPE 수치 예제

학습 corpus:

- hug 10회
- pug 5회
- hugs 5회

초기:

    h u g      x10
    p u g      x5
    h u g s    x5

첫 pair 빈도:

- h + u = 15
- u + g = 20
- p + u = 5
- g + s = 5

u + g를 ug로 합칩니다.

    h ug       x10
    p ug       x5
    h ug s     x5

다음에는 h + ug = 15이므로 hug로 합칩니다. 이후 p + ug와 hug + s가 5회로 동률이고 원문 예제는 p + ug를 pug로 합칩니다.

학습된 규칙:

    u + g  -> ug
    h + ug -> hug
    p + ug -> pug

새 입력 pugs에는 규칙을 같은 순서로 적용합니다.

    p, u, g, s
    -> p, ug, s
    -> pug, s

따라서 학습에 없던 pugs도 ["pug", "s"]로 표현할 수 있습니다.

## 9. Byte-level BPE와 tokenizer 고정

원문은 많은 현대 tokenizer가 문자 대신 256개 byte 값을 기본 단위로 쓰는 변형도 설명합니다. 여러 언어, emoji, 기호를 표현하기 유리합니다.

Tokenizer는 LLM보다 먼저 학습해 vocabulary와 merge rule을 고정한 뒤, 그 Token ID로 LLM을 학습합니다.

## 10. Vocabulary와 Token ID

원문의 작은 예:

| Token | ID |
| --- | ---: |
| h | 0 |
| u | 1 |
| g | 2 |
| p | 3 |
| s | 4 |
| ug | 5 |
| hug | 6 |
| pug | 7 |

    "pugs" -> ["pug", "s"] -> [7, 4]

Token ID는 embedding 자체가 아니라 embedding lookup의 index입니다.

## 11. Decoding

출력은 역방향입니다.

    [6, 4]
    -> ["hug", "s"]
    -> "hugs"

LLM은 ID를 생성하고 tokenizer가 text로 decode합니다.

원문의 cl100k_base 예:

    encode("I love learning")
    -> [40, 3021, 6975]

개별 decode 예:

    40 -> [I]
    3021 -> [ love]
    6975 -> [ learning]

공백도 token 문자열 일부가 될 수 있습니다.

## 12. Special Token

원문은 다음 제어 token을 설명합니다.

- sequence 종료 신호
- sequence 시작 신호
- padding
- chat message boundary

일반 텍스트 조각이 아니라 tokenizer나 주변 시스템이 특별한 의미를 부여한 vocabulary 항목입니다.

## 13. 실제 영향

### 문자 세기

strawberry의 r 개수처럼 문자 단위 접근이 필요한 작업은 subword 경계 때문에 어려울 수 있습니다.

### 숫자

12345가 "123" | "45"처럼 나뉠 수 있어 자리 단위 산술이 자연스럽지 않을 수 있습니다.

### Context와 비용

Context window와 API 사용량은 대개 token 수 기준입니다.

### 언어

원문은 영어 비중이 큰 tokenizer에서 Hindi, Tamil, Japanese 등이 더 잘게 나뉠 수 있다고 설명합니다. 같은 뜻도 token 수가 늘면 비용과 context 점유량이 커집니다.

### Code

공백과 indentation도 tokenization 대상이므로 코드 처리 효율에도 영향을 줍니다.

## 14. BPE 별도 레슨과의 관계

이 레슨은 문자/단어/subword 비교, BPE 개요, vocabulary, decoding, special token, 실무 영향을 설명합니다. 다음 BPE 레슨은 merge algorithm 자체를 더 깊게 다룹니다.

## 핵심 정리

- Tokenization은 text를 Token ID sequence로 바꾸는 첫 단계입니다.
- Character-level은 vocabulary가 작지만 sequence가 길고, Word-level은 반대 문제가 있습니다.
- Subword 방식은 두 극단 사이의 절충입니다.
- BPE는 빈번한 pair를 반복 merge합니다.
- 원문의 hug/pug/hugs 예제는 u+g -> ug, h+ug -> hug, p+ug -> pug 순입니다.
- Token ID는 embedding lookup의 index입니다.
- Tokenization은 context, 비용, 다국어 효율, 문자·숫자·코드 작업에 직접 영향을 줍니다.

## 원문 및 관련 자료

- https://outcomeschool.com/blog/tokenization-in-llms
- https://github.com/amitshekhariitbhu/ai-engineering-course
- https://www.youtube.com/watch?v=sK2s9I84EVI
