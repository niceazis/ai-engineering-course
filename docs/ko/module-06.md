# 모듈 6 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 6: 언어 모델의 종류

모든 언어 모델이 거대한 텍스트 생성 LLM인 것은 아닙니다. 더 작은 모델, 추론 특화 모델, 재귀형 모델, diffusion 기반 모델, 의사결정 전용 모델을 살펴보고 언제 무엇을 선택할지 배웁니다.

**이 모듈의 레슨:**

1. [Small Language Model(SLM)이란 무엇이며 언제 사용해야 하는가?](https://outcomeschool.com/blog/small-language-models-slms)
2. [Large Reasoning Model(LRM)이란 무엇이며 LLM과 어떻게 다른가?](https://outcomeschool.com/blog/large-reasoning-models)
3. [Recursive Language Model(RLM)이란 무엇이며 어떻게 동작하는가?](https://outcomeschool.com/blog/recursive-language-models)
4. [Diffusion Language Model(DLM)은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-do-diffusion-language-models-dlms-work)
5. [Jev와 System One Model](https://outcomeschool.com/blog/jev-and-system-one-models-explained)

---

### 6.1 Small Language Model(SLM)이란?

작은 언어 모델의 기준, 중요성, 강점과 trade-off를 배웁니다.

- SLM = Small + Language Model
- Language Model이란?
- 어느 정도가 “Small”인가?
- 대표적인 SLM
- 작은 크기에서도 성능을 유지하는 방법
- SLM이 중요한 이유
- SLM vs LLM
- 모델 크기의 스펙트럼
- SLM이 강한 사용 사례
- Trade-off
- SLM을 선택해야 할 때
- 빠른 요약

시작하기: [Small Language Model(SLM)](https://outcomeschool.com/blog/small-language-models-slms)

### 6.2 Large Reasoning Model(LRM)이란?

표준 LLM과 달리 답변 전에 더 많은 추론을 수행하는 LRM의 동작 방식과 학습, 사용 시점을 배웁니다.

- 큰 그림
- LRM이란?
- LLM vs LRM
- LRM이 “생각”하는 방식
- Test-time Compute
- LRM 학습 방식
- 학습 단계와 예측 단계의 입출력
- LRM과 일반 LLM의 선택 기준
- 대표적인 LRM
- 흔한 실수
- 빠른 요약

시작하기: [Large Reasoning Model(LRM)](https://outcomeschool.com/blog/large-reasoning-models)

### 6.3 Recursive Language Model(RLM)이란?

모델의 컨텍스트 윈도우를 넘는 매우 큰 입력을 처리하기 위한 Recursive Language Model을 배웁니다.

- RLM이란?
- RLM이 필요한 이유
- 동작 방식
- 모델이 코드를 작성하고 실행하는 방식
- RLM이 더 잘 동작하는 이유
- RLM 내부의 Recursion
- 단순 Chunking과의 차이
- 장점
- 한계
- 사용 시점
- RLM vs RAG
- 실제 사례

시작하기: [Recursive Language Model(RLM)](https://outcomeschool.com/blog/recursive-language-models)

### 6.4 Diffusion Language Model(DLM)은 어떻게 동작하는가?

기존 autoregressive LLM과 다른 방식으로 텍스트를 생성하는 Diffusion Language Model을 배웁니다.

- DLM이란?
- 오늘날 언어 모델의 텍스트 생성 방식
- 기존 접근의 문제
- Diffusion 아이디어의 출발점
- 텍스트에서 “Noise”란?
- Forward와 Reverse 두 단계
- 단계별 텍스트 생성 과정
- 작은 end-to-end 예제
- 코드 형태의 설명
- DLM vs 일반 언어 모델
- 장점
- 한계
- 현재 기술 수준

시작하기: [Diffusion Language Model(DLM)](https://outcomeschool.com/blog/how-do-diffusion-language-models-dlms-work)

### 6.5 Jev와 System One Model

텍스트를 생성하지 않고 소프트웨어가 바로 사용할 수 있는 빠른 판단만 수행하는 모델을 살펴봅니다.

- System One Model이란?
- System One vs System Two 사고
- 작은 판단에 일반 LLM을 사용할 때의 문제
- Jev란?
- Jev 동작 방식
- Typed Answer: Choice, Score, Yes/No
- Calibration과 RLCD
- Jev가 hallucination을 만들 수 없는 이유
- Jev vs LLM
- 강점과 실패 영역
- 어떤 모델을 언제 사용할까?

시작하기: [Jev와 System One Model](https://outcomeschool.com/blog/jev-and-system-one-models-explained)

---
