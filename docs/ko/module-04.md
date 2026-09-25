# 모듈 4 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 4: LLM이 텍스트를 생성하는 방식

이 모듈에서는 LLM이 다음 토큰을 선택하는 방식, 창의성을 조절하는 방법, 출력이 토큰 단위로 사용자에게 전달되는 과정, 그리고 컨텍스트 윈도우가 실패하는 지점을 배웁니다.

모듈을 마치면 프롬프트 입력부터 최종 응답까지 무슨 일이 일어나는지, 어떤 설정이 출력에 영향을 주는지 이해할 수 있습니다.

**이 모듈의 레슨:**

1. [Temperature는 LLM 출력을 어떻게 제어하는가?](https://outcomeschool.com/blog/how-does-temperature-control-llm-output)
   ↳ [한국어 상세 학습 노트](blogs/module-04/how-does-temperature-control-llm-output.md)

2. [Top-k와 Top-p Sampling은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-do-top-k-and-top-p-sampling-work)
   ↳ [한국어 상세 학습 노트](blogs/module-04/how-do-top-k-and-top-p-sampling-work.md)

3. [Token Streaming은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-token-streaming-work)
   ↳ [한국어 상세 학습 노트](blogs/module-04/how-does-token-streaming-work.md)

4. [LLM의 Lost in the Middle 문제와 해결 방법](https://outcomeschool.com/blog/lost-in-the-middle-problem-in-llms)
   ↳ [한국어 상세 학습 노트](blogs/module-04/lost-in-the-middle-problem-in-llms.md)


---

### 4.1 Temperature는 LLM 출력을 어떻게 제어하는가?

Temperature가 예측 가능하고 안정적인 답변과 창의적이고 다양한 답변 사이를 어떻게 조절하는지 배웁니다. LLM이 다음 토큰을 하나씩 고르는 과정과 점수가 확률로 바뀌는 과정, Temperature가 확률을 어떻게 바꾸는지 살펴봅니다.

- LLM에서 Temperature란?
- LLM이 다음 토큰을 고르는 방식
- Score에서 Probability로
- Temperature가 개입하는 지점
- 수치 예제
- 낮은 Temperature
- 높은 Temperature
- Temperature = 1과 0
- 왜 Temperature라고 부르는가?
- 사용 사례별 적절한 값
- 흔한 실수

시작하기: [Temperature는 LLM 출력을 어떻게 제어하는가?](https://outcomeschool.com/blog/how-does-temperature-control-llm-output)

→ [한국어 상세 학습 노트](blogs/module-04/how-does-temperature-control-llm-output.md)


### 4.2 Top-k와 Top-p Sampling은 어떻게 동작하는가?

LLM이 다음 토큰을 선택할 때 사용하는 대표적인 두 샘플링 방식인 Top-k와 Top-p를 배웁니다.

- 다음 토큰 선택 과정
- 항상 최고 확률 토큰만 고를 때의 문제
- 모든 토큰에서 무작위 선택할 때의 문제
- Top-k Sampling이란?
- 단계별 Top-k 예제
- Top-k의 한계
- Top-p Sampling이란?
- 단계별 Top-p 예제
- Top-k vs Top-p
- Temperature와 함께 사용하는 방법
- 언제 무엇을 사용할까?

시작하기: [Top-k와 Top-p Sampling](https://outcomeschool.com/blog/how-do-top-k-and-top-p-sampling-work)

→ [한국어 상세 학습 노트](blogs/module-04/how-do-top-k-and-top-p-sampling-work.md)


### 4.3 Token Streaming은 어떻게 동작하는가?

Token Streaming이 왜 필요한지, 서버와 브라우저가 어떻게 통신하는지, ChatGPT와 Claude 같은 실제 시스템에서 어떻게 사용되는지 배웁니다.

- Token Streaming이란?
- LLM 텍스트 생성 복습
- Streaming이 필요한 이유
- SSE란?
- HTTP 연결을 열어두는 방식
- Streaming 메시지 형식
- 서버에서 화면까지 전체 흐름
- 스트림을 끝내는 [DONE] 마커
- SSE vs WebSocket
- 실제 Token Streaming

시작하기: [Token Streaming은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-token-streaming-work)

→ [한국어 상세 학습 노트](blogs/module-04/how-does-token-streaming-work.md)


### 4.4 LLM의 Lost in the Middle 문제와 해결 방법

긴 입력에서 모델이 시작과 끝은 잘 활용하지만 중간 정보를 놓치는 Lost in the Middle 문제를 배웁니다.

- Context Window란?
- Lost in the Middle 문제
- 예제로 이해하기
- U자형 성능 곡선
- 발생 원인
- 실제 시스템에 미치는 영향
- 직접 테스트하는 방법
- 해결 방법
- 기억할 핵심 포인트

시작하기: [Lost in the Middle 문제와 해결 방법](https://outcomeschool.com/blog/lost-in-the-middle-problem-in-llms)

→ [한국어 상세 학습 노트](blogs/module-04/lost-in-the-middle-problem-in-llms.md)


영상 보기: [Why is the context window limited in LLMs?](https://www.youtube.com/watch?v=CGIhxIaOg3M)

**모듈 4 영상 및 추가 자료:**

- [Why is the context window limited in LLMs?](https://www.youtube.com/watch?v=CGIhxIaOg3M) (영상)

---
