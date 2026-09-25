# 모듈 14 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 14: AI 안전과 보안

이 모듈에서는 LLM 애플리케이션을 안전하게 유지하는 방법, 공격자가 시스템을 깨뜨리는 방식, AI 생성 텍스트를 식별하는 방법을 배웁니다.

**이 모듈의 레슨:**

1. [LLM Guardrail은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-do-llm-guardrails-work)
   ↳ [한국어 상세 학습 노트](blogs/module-14/how-do-llm-guardrails-work.md)

2. [LLM의 Prompt Injection이란 무엇이며 어떻게 방어하는가?](https://outcomeschool.com/blog/prompt-injection-in-llms)
   ↳ [한국어 상세 학습 노트](blogs/module-14/prompt-injection-in-llms.md)

3. [LLM Watermarking은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-llm-watermarking-work)
   ↳ [한국어 상세 학습 노트](blogs/module-14/how-does-llm-watermarking-work.md)


---

### 14.1 LLM Guardrail은 어떻게 동작하는가?

모델 입력과 출력 주변에서 안전 정책을 검사하는 Guardrail을 배웁니다.

- LLM이란?
- LLM Guardrail이란?
- 필요한 이유
- Input과 Output에서의 위치
- Guardrail 유형
- 코드로 보는 간단한 Input Guardrail
- Output Guardrail
- 다른 Model을 Guardrail로 사용
- 요청 하나의 단계별 흐름
- 한계
- Best Practice

시작하기: [LLM Guardrail](https://outcomeschool.com/blog/how-do-llm-guardrails-work)

→ [한국어 상세 학습 노트](blogs/module-14/how-do-llm-guardrails-work.md)


### 14.2 Prompt Injection이란?

외부 데이터나 사용자 입력에 악성 지시를 넣어 모델이 개발자의 의도보다 공격자의 지시를 따르게 만드는 Prompt Injection을 배웁니다.

- LLM과 Prompt
- System Prompt와 User Prompt
- Prompt Injection이란?
- 근본 원인
- 간단한 예제
- Direct Prompt Injection
- Indirect Prompt Injection
- 실제 공격 흐름
- 코드 예제
- Prompt Injection vs Jailbreaking
- SQL Injection과 다른 이유
- 공격자가 얻을 수 있는 것
- 방어 방법
- Defense Checklist
- 자체 테스트
- 아직 완전히 해결되지 않은 이유

시작하기: [Prompt Injection](https://outcomeschool.com/blog/prompt-injection-in-llms)

→ [한국어 상세 학습 노트](blogs/module-14/prompt-injection-in-llms.md)


### 14.3 LLM Watermarking은 어떻게 동작하는가?

모델이 생성한 텍스트에 의미를 크게 훼손하지 않고 통계적 신호를 남겨 나중에 검출하는 Watermarking을 배웁니다.

- Watermark란?
- 필요한 이유
- LLM 텍스트 생성
- 다음 Token 선택
- Watermarking이 가능한 확률적 여유
- Secret Key
- Preferred Token과 기타 Token
- 확률을 미세하게 조정하는 방법
- Preferred Set이 계속 바뀌는 이유
- 한 Token vs 수천 Token
- Detection
- AI Text Detector와의 차이
- 품질을 유지하는 이유
- 편집된 텍스트
- 실제 활용
- 장단점

시작하기: [LLM Watermarking](https://outcomeschool.com/blog/how-does-llm-watermarking-work)

→ [한국어 상세 학습 노트](blogs/module-14/how-does-llm-watermarking-work.md)


---
