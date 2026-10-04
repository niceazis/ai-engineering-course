# LLM Stop Tokens — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/stop-tokens-in-llms  
> 검증 상태: 2026-10-04 현재 Outcome School upstream README에서 레슨 제목·순서·목차는 직접 확인했습니다. 원문 블로그 본문은 아직 직접 가져오지 못해 상세 예제와 수치는 검증되지 않았습니다. 아래 세부 동작은 공식 upstream 목차를 기준으로 Hugging Face Transformers와 OpenAI의 1차 문서로 보완했으며, 보완 내용을 Outcome School 원문이라고 단정하지 않습니다.

## 1. Token이란?

LLM은 vocabulary의 token을 하나씩 선택해 응답을 만듭니다. 선택된 token은 다시 문맥 뒤에 붙고 다음 token 예측에 사용됩니다.

    현재 sequence -> next-token score -> token 선택 -> append -> 반복

## 2. LLM은 텍스트를 어떻게 생성하는가?

Autoregressive LLM은 지금까지의 token을 조건으로 다음 token 분포를 만들고 한 token씩 생성합니다. 사람이 보기에 문장이 완성됐더라도 generation loop에는 별도의 종료 조건이 필요합니다.

## 3. 왜 LLM에는 종료 신호가 필요한가?

대표적인 종료 조건은 EOS token, 외부 stopping criteria, 최대 생성 길이, 사용자 중단입니다. Hugging Face 공식 문서는 EosTokenCriteria가 end-of-sequence token이 생성되면 generation을 중단하며 기본적으로 model generation config의 eos_token_id를 사용한다고 설명합니다.

정상적인 EOS 종료와 최대 길이에 걸린 강제 종료는 구분해야 합니다.

## 4. Stop Token이란?

Stop Token 또는 EOS token은 vocabulary 안의 특별한 token ID로 생성 종료를 표현합니다.

    다음 token 선택
      -> eos_token_id 인가?
      -> yes: 종료
      -> no: sequence에 추가 후 계속

Stop Token은 모델이 실제로 다음 token 후보로 선택할 수 있는 ID입니다. 사람이 읽는 일반 문자열과 동일할 필요는 없습니다.

## 5. 모델은 Stop Token을 어떻게 배우는가?

이 절의 상세 설명은 Outcome School 원문 본문을 직접 검증하지 못했으므로 일반적인 언어 모델 학습 원리로 보완합니다. 학습 데이터에서 sequence나 message 경계가 종료 token으로 표현되면 모델은 해당 문맥 뒤에 그 token이 올 확률을 학습할 수 있습니다. 실제 token과 chat boundary는 모델과 tokenizer마다 다릅니다.

## 6. Stop Token vs Stop Sequence

| 항목 | Stop Token / EOS | Stop Sequence |
| --- | --- | --- |
| 형태 | vocabulary의 특별한 token ID | 사용자가 지정한 문자열 또는 sequence |
| 설정 위치 | 모델/tokenizer | API 또는 inference layer |
| 종료 | EOS ID가 생성될 때 | 지정 sequence가 감지될 때 |

OpenAI 공식 문서에 따르면 Chat Completions API의 stop parameter에는 최대 4개의 stop sequence를 지정할 수 있고, 감지된 stop sequence 자체는 반환 결과에 포함되지 않습니다. 문자열 하나가 tokenizer에서 반드시 token 하나인 것은 아닙니다.

## 7. 모델이 Stop Token을 만들지 않으면?

Production system은 EOS가 나오지 않는 경우를 대비해 최대 길이 제한 같은 별도 안전장치를 둡니다. Hugging Face는 MaxLengthCriteria처럼 길이로 generation을 중단하는 stopping criteria도 제공합니다.

- EOS 종료: 모델이 종료 token을 선택
- 길이 제한: 외부 시스템이 강제로 중단

길이 제한 종료는 문장이나 코드가 중간에서 잘릴 수 있으므로 종료 이유를 구분하는 것이 중요합니다.

## 8. Chat Model의 Stop Token

Chat model은 문서 끝뿐 아니라 message 또는 turn 경계를 표현해야 합니다. 실제 end-of-turn token, EOS, chat template은 모델마다 다를 수 있으므로 다른 모델의 ID나 문자열을 그대로 복사하지 말고 해당 tokenizer와 generation config를 확인해야 합니다.

## 9. 흔한 실수

- 마침표를 EOS와 같은 것으로 보는 것
- Stop Token과 외부 Stop Sequence를 같은 개념으로 보는 것
- 최대 token 수 도달을 정상 종료로 해석하는 것
- 다른 모델의 eos_token_id를 그대로 사용하는 것
- 너무 흔한 문자열을 stop sequence로 지정해 출력을 조기에 자르는 것

## 10. 전체 생성 흐름

    prompt -> tokenize -> model -> next token -> EOS 검사
                                      |
                                      +-- EOS: 종료
                                      +-- 아니면 append 후 반복

외부 stop sequence와 최대 길이는 이 loop 주변의 추가 stopping criteria입니다.

## 핵심 정리

- LLM은 token을 반복 생성하므로 종료 조건이 필요합니다.
- EOS/Stop Token은 vocabulary의 특별한 token ID입니다.
- Hugging Face EosTokenCriteria는 EOS 생성 시 generation을 중단합니다.
- Stop Sequence는 API/inference layer의 별도 종료 조건입니다.
- OpenAI stop parameter는 최대 4개 sequence를 받을 수 있고 감지된 sequence를 결과에 포함하지 않습니다.
- EOS가 나오지 않을 경우를 대비해 최대 길이 제한이 필요합니다.
- 모델별 tokenizer, eos_token_id, chat template을 실제로 확인해야 합니다.
- Outcome School 원문 본문을 직접 검증하지 못한 부분은 공식 1차 문서로만 보완했습니다.

## 확인 자료

- https://outcomeschool.com/blog/stop-tokens-in-llms
- https://github.com/amitshekhariitbhu/ai-engineering-course
- https://huggingface.co/docs/transformers/main/internal/generation_utils
- https://help.openai.com/en/articles/5072263-how-do-i-use-stop-sequences-in-the-openai-api
