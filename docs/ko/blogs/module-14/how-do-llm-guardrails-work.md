# LLM Guardrail은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-do-llm-guardrails-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-08-10 공개 원문을 직접 확인해 input/output guardrail, word-list/regex 예제, guard model과 limitation/best practice를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Guardrail이란?

LLM Guardrail은 main LLM 자체가 아니라 **LLM 앞뒤에 배치하는 별도 검사 layer**입니다.

    User
      → Input Guardrail
      → Main LLM
      → Output Guardrail
      → User

원문은 이를 문 앞의 security guard에 비유합니다.

## 2. 왜 필요한가

LLM은 다음 token을 예측하는 모델이므로:

- unsafe request
- off-topic request
- private data
- hallucinated answer
- brand/tone violation

을 application 정책대로 항상 처리한다는 보장이 없습니다.

따라서 policy enforcement를 model 내부 성향에만 맡기지 않고 외부 layer로 둡니다.

## 3. Input Guardrail

User message가 main LLM에 도달하기 전에 검사합니다.

예:

- harmful intent
- policy violation
- prompt injection signal
- PII
- unsupported topic

Fail이면 main LLM을 아예 호출하지 않고 refusal 또는 safe workflow로 route할 수 있습니다.

## 4. Output Guardrail

LLM response가 사용자에게 가기 전에 검사합니다.

예:

- PII leakage
- unsafe content
- schema violation
- unsupported claim
- restricted data

Input과 output 둘 다 사용하는 defense-in-depth가 좋습니다.

## 5. Guardrail 유형

원문 분류:

### Topic Guardrail

Domain 밖 질문 차단.

### Safety Guardrail

위험한 content/action 차단.

### Privacy Guardrail

전화번호·카드번호·개인정보 보호.

### Format Guardrail

JSON/table/list 등 required output shape 검증.

### Factual Guardrail

Source/evidence와 비교해 unsupported claim을 줄입니다.

## 6. 원문의 단순 Input 예

교육용 word-list:

    banned_words = ["hack", "bomb", "steal password"]

    message.lower()
      → banned word 포함?
         yes → blocked
         no  → allowed

이 방식은 쉽게 우회될 수 있습니다.

예:

- spacing
- spelling variation
- paraphrase

따라서 exact keyword rule은 첫 layer일 뿐입니다.

## 7. 원문의 Output Regex 예

10-digit number를 숨기는 예:

    re.sub(r"\d{10}", "[hidden]", answer)

원문 example:

    "You can call our agent at 9876543210"
      → "You can call our agent at [hidden]"

실전에서는 국가별 번호·email·identifier 등 훨씬 정교한 PII detector가 필요합니다.

## 8. Guard Model

작은 classifier/model이:

    safe / unsafe

처럼 semantic classification을 할 수 있습니다.

Flow:

    safety_check(input)
      → safe?
         no → refuse
         yes → main LLM

    safety_check(output)
      → safe?
         no → replace/refuse
         yes → return

## 9. Rule + Model + Deterministic Validation

가장 실용적인 구조:

- regex/schema: deterministic
- policy classifier: semantic safety
- retrieval/evidence checker: factuality
- permission system: actual action authorization

한 guard model에 모든 것을 맡기지 않습니다.

## 10. False Positive / False Negative

Guardrail은 완벽하지 않습니다.

False Positive:

    safe request를 막음

False Negative:

    unsafe request를 통과시킴

Risk가 큰 domain에서는 recall을 높이는 대신 user friction이 증가할 수 있습니다.

Threshold를 실제 traffic으로 calibration해야 합니다.

## 11. Latency와 Cost

Guard model을 input/output에 모두 호출하면:

- latency 증가
- cost 증가

가 생깁니다.

Rule-based fast path와 model-based slow path를 cascade로 구성할 수 있습니다.

## 12. Best Practice

원문 핵심:

- input + output 양쪽 사용
- layered defense
- blocked event logging
- good/bad sample test
- policy 지속 업데이트
- 한 guardrail만 신뢰하지 않기

추가로 production에서는 destructive tool action을 별도 permission layer로 막아야 합니다.

## 핵심 정리

- Guardrail은 main LLM 주변의 별도 safety/control layer입니다.
- Input과 Output 양쪽에 둘 수 있습니다.
- Rule, regex, classifier, evidence checker, permission을 조합하는 것이 좋습니다.
- Guardrail은 false positive/negative가 있으므로 평가와 지속 업데이트가 필요합니다.
- Safety policy와 actual tool authorization은 분리해야 합니다.

## 원문

- https://outcomeschool.com/blog/how-do-llm-guardrails-work
