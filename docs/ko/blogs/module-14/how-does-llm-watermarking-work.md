# LLM Watermarking은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-llm-watermarking-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 Outcome School 원문 본문은 웹 캐시에서 직접 열리지 않았습니다. 공식 Module 14 목차가 제시하는 Secret Key·Preferred Token Set·probability bias·statistical detection 흐름과 공개 LLM watermarking 연구의 일반 원리를 기준으로 독립적으로 설명하며, 원문 고유 수치는 단정하지 않습니다.

## 1. Watermarking의 목표

LLM 생성 text에 사람이 읽기에는 거의 차이가 없지만 **통계적으로 검출 가능한 signal**을 넣습니다.

목적:

- model-generated text detection
- provenance
- platform abuse investigation

일반 AI-text classifier와 달리 생성 model이 watermark를 의도적으로 삽입합니다.

## 2. Next-Token Sampling의 여유

LLM은 다음 token 후보에 확률을 줍니다.

예:

    good      0.25
    useful    0.20
    clear     0.15
    ...

여러 자연스러운 후보가 있을 때 특정 subset을 아주 조금 더 선호해도 text quality가 크게 변하지 않을 수 있습니다.

Watermark는 이 확률적 여유를 이용합니다.

## 3. Secret Key

Secret key와 이전 token/context를 hash해 vocabulary를 매 step 두 집합으로 나눌 수 있습니다.

예:

    preferred / green list
    other / red list

어떤 token이 preferred인지 외부에서는 key 없이는 예측하기 어렵습니다.

## 4. Probability Bias

생성 시 preferred token의 logit에 작은 bias를 더합니다.

    z'_i =
      z_i + delta   if preferred
      z_i           otherwise

그 뒤 softmax/sampling합니다.

Preferred token이 **반드시** 선택되는 것이 아니라 probability가 조금 올라갑니다.

## 5. Preferred Set이 계속 바뀌는 이유

같은 token만 계속 선호하면 pattern이 쉽게 드러나고 문장 품질이 나빠집니다.

Context/key 기반으로 매 position의 preferred set을 바꿔 자연스러운 distribution을 유지합니다.

## 6. 한 Token으로는 판별 못 한다

Watermark는 개별 token이 아니라 긴 sequence의 통계적 편향을 봅니다.

    expected preferred count
      vs
    observed preferred count

관찰된 preferred-token 비율이 우연으로 보기 어려울 정도로 높으면 watermark signal로 판단합니다.

## 7. Detection

Detector는 같은 secret key를 사용해 text 각 위치의 preferred set을 재구성합니다.

그 뒤 z-score 같은 통계량을 계산할 수 있습니다.

개념:

    z =
      (observed_green - expected_green)
      / standard_deviation

Threshold를 넘으면 watermark 가능성이 높다고 판단합니다.

## 8. 품질 Trade-off

Bias delta가 너무 작으면:

- detection 약함

너무 크면:

- text distribution 왜곡
- quality 저하

즉 detectability와 generation quality 사이 trade-off가 있습니다.

## 9. Editing Robustness

다음 편집은 signal을 약화시킬 수 있습니다.

- paraphrase
- translation
- heavy rewrite
- token deletion/insertion

부분 편집에는 signal이 일부 남을 수 있지만 강한 transformation은 watermark를 제거할 수 있습니다.

따라서 watermark는 cryptographic proof가 아닙니다.

## 10. AI Text Detector와 차이

AI classifier:

    text style/statistics를 보고 추정

Watermark detector:

    generator가 넣은 secret-key-controlled signal을 확인

Watermark는 생성 단계 control이 필요하지만 provenance signal이 더 명시적일 수 있습니다.

## 11. False Positive / False Negative

Statistical detector이므로 threshold에 따라:

- false positive
- false negative

가 존재합니다.

짧은 text일수록 sample 수가 적어 신뢰도가 낮습니다.

## 12. 실제 활용 시 고려

- key management
- multiple model/version keys
- language/tokenizer
- text length
- adversarial editing
- legal/policy interpretation

Detector 결과만으로 중요한 제재 결정을 자동화하는 것은 위험할 수 있습니다.

## 핵심 정리

- LLM watermark는 next-token probability를 secret-key 기반 preferred set 쪽으로 약하게 bias합니다.
- 긴 text에서 preferred-token 빈도가 비정상적으로 높다는 통계 signal을 검출합니다.
- 개별 token은 watermark를 드러내지 않습니다.
- Detectability와 quality 사이 trade-off가 있습니다.
- Paraphrase/translation 같은 변환으로 signal이 약해질 수 있어 절대적 증명 수단은 아닙니다.
- Outcome School 원문 본문을 직접 확인하지 못해 특정 수치를 원문 내용으로 단정하지 않았습니다.

## 원문

- https://outcomeschool.com/blog/how-does-llm-watermarking-work
