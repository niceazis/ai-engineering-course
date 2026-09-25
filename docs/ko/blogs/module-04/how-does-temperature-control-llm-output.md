# Temperature는 LLM 출력을 어떻게 제어하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-temperature-control-llm-output  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 공식 인덱스와 과정 개요, 검색 가능한 원문 사본에서 확인한 설명 순서·수치 예제를 바탕으로 독립적으로 다시 쓴 한국어 해설입니다. 현재 원문 URL은 웹 캐시에서 직접 열리지 않아, 직접 확인하지 못한 세부 문장을 원문 내용이라고 단정하지 않습니다.

## 1. Temperature란?

Temperature는 LLM이 다음 token을 고를 때 **얼마나 보수적으로 또는 다양하게 sampling할지** 조절하는 값입니다.

- 낮은 Temperature: 확률이 높은 token에 더 집중
- 높은 Temperature: 낮은 확률 token에도 더 많은 기회
- Temperature = 1: 원래 logits의 상대적 차이를 그대로 사용
- Temperature = 0: 보통 최고 logit을 고르는 greedy decoding으로 특별 처리

Outcome School은 이를 안전하고 예측 가능한 답과 창의적이고 다양한 답 사이를 움직이는 knob로 설명합니다.

## 2. 다음 Token 선택

문맥이 다음이라고 합시다.

    The sky is ...

원문 예의 후보 score와 softmax 확률:

| Token | Score | Probability |
| --- | ---: | ---: |
| blue | 4.0 | 0.70 |
| clear | 3.0 | 0.26 |
| falling | 1.0 | 0.03 |
| banana | 0.0 | 0.01 |

모델은 이 probability distribution에서 다음 token 하나를 sampling합니다.

전체 흐름:

    logits → temperature scaling → softmax → sampling

## 3. Temperature가 들어가는 위치

핵심 계산:

    scaled_score = score / temperature

Temperature가 1이면 변화가 없습니다.

Temperature가 0.5면 score는 두 배가 되고, 2이면 score는 절반이 됩니다.

중요한 점은 **후보의 순서를 바꾸는 것이 아니라 score 사이 간격을 바꾼다**는 것입니다.

## 4. Temperature = 1

원래 score:

    [4.0, 3.0, 1.0, 0.0]

원문 확률:

    blue      0.70
    clear     0.26
    falling   0.03
    banana    0.01

모델의 기본 분포를 그대로 사용합니다.

## 5. Temperature = 0.5

scaled score:

    [8.0, 6.0, 2.0, 0.0]

원문 예의 확률:

    blue      0.88
    clear     0.12
    falling   0.00
    banana    0.00

상위 token에 probability가 더 집중됩니다.

## 6. Temperature = 2

scaled score:

    [2.0, 1.5, 0.5, 0.0]

원문 예의 확률:

    blue      0.51
    clear     0.31
    falling   0.11
    banana    0.07

분포가 더 평평해지고 낮은 확률 후보의 선택 가능성이 커집니다.

## 7. Softmax와의 관계

Softmax는 지수함수를 사용합니다.

    softmax(z_i) = exp(z_i) / sum(exp(z_j))

따라서 logit 차이가 커질수록 확률 분포가 빠르게 뾰족해집니다.

- T < 1: logit 차이를 확대 → sharper
- T > 1: logit 차이를 축소 → flatter

Temperature가 모델에 새 지식을 넣는 것은 아닙니다. 이미 계산된 후보의 **선택 분포만 바꿉니다.**

## 8. Temperature = 0

score / 0은 수학적으로 정의되지 않습니다.

따라서 serving engine은 Temperature 0을 보통 다음처럼 특별 취급합니다.

    next_token = argmax(logits)

즉 greedy decoding입니다.

원문은 Temperature 0이라도 하드웨어의 부동소수점 연산이나 병렬 계산의 작은 비결정성 때문에 모든 실행에서 bit-for-bit 동일 출력을 보장한다고 생각하면 안 된다고 설명합니다.

## 9. 낮은 Temperature의 용도

안정성이 중요한 작업:

- factual QA
- 코드 생성/수정
- 문서 요약
- 구조화 데이터 추출
- 형식 준수가 중요한 자동화

에 일반적으로 유리합니다.

그러나 정확성을 Temperature 하나가 보장하지는 않습니다. 검색 근거, schema validation, 테스트 등의 별도 검증이 필요합니다.

## 10. 높은 Temperature의 용도

다양성이 중요한 작업:

- brainstorming
- story
- marketing copy 초안
- 여러 대안 생성

에서 조금 높은 Temperature가 유용할 수 있습니다.

원문은 지나치게 높은 값이 엉뚱한 token을 고르게 하고, 그 token이 이후 autoregressive context에 들어가 전체 출력을 흔들 수 있다고 설명합니다.

예:

    The sky is banana

가 한번 선택되면 다음 token은 이미 이 이상한 prefix를 조건으로 생성됩니다.

## 11. Temperature와 Top-p

역할은 다릅니다.

- Temperature: probability distribution의 모양을 바꿈
- Top-p: sampling 가능한 후보 범위를 누적 확률 기준으로 자름

두 parameter를 동시에 바꾸면 어느 설정이 결과를 바꿨는지 알기 어렵습니다. 실험에서는 한 번에 하나씩 바꾸는 편이 좋습니다.

## 12. 실무 검증

같은 model/version/prompt를 고정하고 다음처럼 비교합니다.

    T = 0
    T = 0.2
    T = 0.7
    T = 1.0
    T = 1.5

확인할 지표:

- 정답률
- format 준수율
- invalid output 비율
- 반복성
- 다양성

## 핵심 정리

- Temperature는 logits를 softmax 전에 나누는 scale입니다.
- T < 1은 분포를 뾰족하게, T > 1은 평평하게 만듭니다.
- 원문 예에서 T=1의 0.70/0.26/0.03/0.01이 T=0.5에서는 0.88/0.12/0/0, T=2에서는 0.51/0.31/0.11/0.07로 변합니다.
- T=0은 보통 greedy decoding으로 특별 처리합니다.
- Temperature는 모델의 지식이나 추론 능력을 높이는 parameter가 아닙니다.

## 원문

- https://outcomeschool.com/blog/how-does-temperature-control-llm-output
