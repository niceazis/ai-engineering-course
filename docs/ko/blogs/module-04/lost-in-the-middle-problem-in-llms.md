# Lost in the Middle 문제와 해결 방법 — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/lost-in-the-middle-problem-in-llms  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 공식 뉴스레터와 검색 가능한 원문 사본에서 확인한 20문서 예제, U-shaped curve, Needle-in-a-Haystack test, 여섯 해결 접근을 보존해 독립적으로 다시 쓴 한국어 상세 해설입니다. 현재 블로그 원문 URL 자체는 웹 캐시에서 직접 열리지 않아 이 한계를 명시합니다.

## 1. Context Window는 수용량이지 균일한 이해 보장이 아니다

Context window는 한 request에서 모델이 받아들일 수 있는 token 범위입니다.

원문은 100,000-token context를 예로 들어 대략 75,000 words 수준으로 설명합니다.

중요한 전제:

> 입력이 context window 안에 들어간다고 해서 모든 위치의 정보를 똑같이 잘 활용한다는 보장은 없습니다.

Lost in the Middle은 바로 이 차이를 다룹니다.

## 2. Lost in the Middle이란?

긴 prompt에서 중요한 정보가:

- 시작에 있으면 잘 사용되고
- 끝에 있어도 잘 사용되지만
- **중간에 있으면 활용 정확도가 떨어지는 현상**

입니다.

Context truncation과는 다릅니다.

- truncation: token이 모델 입력에 아예 들어가지 않음
- lost in the middle: token은 입력 안에 있지만 모델이 제대로 활용하지 못함

후자는 error 없이 그럴듯한 오답이 나올 수 있어 더 찾기 어렵습니다.

## 3. 원문의 20문서 Refund Policy 예

회사 QA 시스템에 20개 문서를 넣습니다.

질문:

    What is our refund policy?

### Document 2에 답이 있을 때

시작에 가까우므로 모델이 잘 찾습니다.

### Document 10에 같은 답을 옮겼을 때

모델이 중간 정보를 놓쳐 다음과 같이 실패할 수 있습니다.

    I could not find the refund policy ...

### Document 19로 옮겼을 때

끝에 가까워지면 다시 잘 답합니다.

바뀐 것은 content가 아니라 **position**뿐입니다.

## 4. U-shaped Performance Curve

하나의 fact를 시작부터 끝까지 위치만 바꿔 accuracy를 재면:

- beginning: 높음
- middle: 낮음
- end: 높음

이 되어 U자형 curve가 나타날 수 있습니다.

    Accuracy
    high   *                         *
           *                       *
             *                   *
                *     *     *
    low   -----------------------------
          start      middle       end

원문은 사람 기억의 primacy/recency bias를 직관으로 연결하지만 모델 메커니즘이 인간 기억과 동일하다는 뜻은 아닙니다.

## 5. 긴 Input에서 더 잘 드러나는 이유

짧은 prompt에서는 middle이 작아 문제가 눈에 띄지 않을 수 있습니다.

Input이 길어지면:

- attention 후보 token 수가 늘어남
- position handling 영향이 커짐
- 학습에서 충분히 보지 못한 극단적 길이를 사용할 수 있음

따라서 최대 128K 지원과 128K 전체에서 균일한 retrieval accuracy는 전혀 다른 주장입니다.

## 6. 원문이 설명하는 원인 1 — Attention 분산

긴 sequence에서는 중요하지 않은 token도 attention 후보가 됩니다.

관련 token에 충분한 weight를 집중하기 어려워질 수 있습니다.

## 7. 원인 2 — Position 효과와 Attention Sink

답을 생성하는 지점과 가까운 마지막 구간은 직접적인 recency advantage가 있을 수 있습니다.

첫 token들은 일부 model/head에서 attention sink처럼 불필요한 attention mass를 흡수하는 현상이 알려져 있습니다.

원문은 이 positional effect가 middle을 상대적으로 약하게 만드는 요인 중 하나라고 설명합니다.

## 8. 원인 3 — 인간 문서 구조

많은 글은:

- 시작: 핵심 주제/요약
- 중간: 세부 근거
- 끝: 결론

형태입니다.

이런 training distribution이 시작과 끝을 중요하게 보는 경향에 영향을 줄 수 있습니다.

## 9. 원인 4 — Full-Length Training 부족

모델이 128K context를 지원하더라도 대부분의 training sample이 훨씬 짧았다면 최대 길이 전 구간을 균일하게 활용하는 능력이 부족할 수 있습니다.

Context 지원 길이는 architecture/runtime capacity와 학습된 활용 능력을 구분해서 봐야 합니다.

## 10. RAG에서의 실패

Retriever가 정답 chunk를 가져왔는데도 prompt 가운데 깊이 배치하면 generation이 이를 놓칠 수 있습니다.

예:

    retrieved chunks = 30
    correct chunk rank = 12

Retrieval recall은 성공인데 final answer는 실패할 수 있습니다.

따라서 RAG는 retrieval metric과 generation answer metric을 분리해서 평가해야 합니다.

## 11. Long Chat과 Agent

### Long Chat

대화 중간에 준 중요한 rule이나 사실이 context가 길어지면서 약해질 수 있습니다.

### Long-running Agent

Agent가 30 step 이상 tool result를 context에 누적하면 중간 단계에서 발견한 사실이 묻힐 수 있습니다.

이 때문에 context compaction, structured state, external memory가 중요합니다.

## 12. Long Document 분석

200-page contract나 긴 log를 한 번에 넣고 모든 문제를 찾아 달라고 하면 시작/끝 issue에 비해 중간 issue가 누락될 가능성이 있습니다.

모델이 스스로 놓친 구간을 경고하지 않을 수 있어 중요한 검토를 단일 long-context call 하나에만 의존하는 것은 위험합니다.

## 13. Needle in a Haystack Test

원문은 직접 측정하는 방법을 제시합니다.

### Step 1

긴 irrelevant filler text를 준비합니다. 이것이 haystack입니다.

### Step 2

고유한 fact를 만듭니다.

    The secret code for the Mumbai office is BLUE-4471.

### Step 3

fact를 10% depth에 삽입합니다.

### Step 4

질문합니다.

    What is the secret code for the Mumbai office?

### Step 5

정답 여부를 기록합니다.

이 과정을:

    0%, 10%, 20%, ... 100%

depth와 여러 context length에서 반복합니다.

Heatmap으로 보면 어떤 길이/위치에서 성능이 무너지는지 확인할 수 있습니다.

원문은 model version, prompt format, content에 따라 weak zone이 달라지므로 자기 production 조건에서 직접 테스트해야 한다고 강조합니다.

## 14. 해결책 1 — 모두 넣기

큰 context window가 있으니 모든 chunk를 넣는 방식입니다.

문제:

- middle weakness는 남음
- input token 비용 증가
- prefill latency 증가

Context capacity는 quality guarantee가 아닙니다.

## 15. 해결책 2 — 더 적게, 더 좋은 Context

예:

    50 chunks
      → reranker
      → top 5 chunks

짧은 context는 weak middle을 줄입니다.

원문은 reranking으로 실제 질문에 중요한 chunk만 남기는 접근을 가장 단순하고 효과적인 방법 중 하나로 설명합니다.

## 16. 해결책 3 — Chunk를 바깥쪽부터 배치

많은 chunk를 꼭 넣어야 한다면 강한 시작/끝 위치를 활용합니다.

rank:

    1 2 3 4 5 6 7

원문의 재배치 예:

    1 3 5 7 6 4 2

가장 중요한 chunk를 시작, 두 번째를 끝, 세 번째를 시작 다음, 네 번째를 끝 직전처럼 배치합니다.

또 질문은 prompt 끝에 두고, 매우 중요한 instruction은 시작과 끝에 반복하는 전략을 설명합니다.

## 17. 해결책 4 — 큰 일을 작은 일로 분해

30개 문서를 한 request로 처리하는 대신:

1. 각 document에 같은 질문 수행
2. 각 document의 짧은 결과 수집
3. 짧은 결과들만 마지막 request에서 통합

하는 Map-Reduce 스타일입니다.

장점:

- 각 문서가 짧은 context에서 처리됨

단점:

- call 수, cost, latency 증가

## 18. 해결책 5 — 근거를 먼저 추출

원문의 prompt-chain 아이디어:

1. 질문과 관련된 문장과 document number를 먼저 추출
2. 아직 최종 답을 만들지 않음
3. 추출한 근거만으로 최종 답 작성

Buried evidence를 짧고 새로운 context로 끌어올린 뒤 reasoning하는 방식입니다.

## 19. 해결책 6 — Model을 직접 Benchmark

광고된 context length만 보고 모델을 고르지 않습니다.

Needle test로 실제:

- input length
- content type
- prompt format
- model version

을 재현해 비교해야 합니다.

1M context 지원은 1M token 모든 위치를 같은 품질로 이해한다는 보장이 아닙니다.

## 핵심 정리

- Lost in the Middle은 입력에 존재하는 정보가 위치 때문에 덜 활용되는 현상입니다.
- 전형적으로 시작/끝이 높고 중간이 낮은 U-shaped 성능이 나타날 수 있습니다.
- RAG, long chat, long document, long-running agent에서 silent failure를 만듭니다.
- Needle-in-a-Haystack test로 자기 시스템의 위치 민감도를 측정해야 합니다.
- 첫 해결은 context를 줄이고 relevance를 높이는 것입니다.
- 많은 context가 필요하면 중요 chunk를 시작/끝에 배치하거나 map-reduce/prompt chaining으로 분해합니다.

## 원문

- https://outcomeschool.com/blog/lost-in-the-middle-problem-in-llms
