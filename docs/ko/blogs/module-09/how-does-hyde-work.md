# HyDE는 RAG에서 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-hyde-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인하고 HyDE(Hypothetical Document Embeddings)의 query→hypothetical document→embedding→retrieval 흐름을 독립적으로 설명합니다.

## 1. 기본 RAG의 Retrieval Gap

질문은 짧고 실제 정답 문서는 설명문 형태인 경우가 많습니다.

Query:

    "왜 배터리가 빨리 닳나요?"

Relevant document:

    "High background activity and display brightness increase battery consumption..."

두 text의 형태가 다르므로 query embedding이 document embedding space에서 최적의 위치에 있지 않을 수 있습니다.

## 2. HyDE의 아이디어

질문 자체를 embedding하지 않고 먼저 LLM에게 **그럴듯한 가상의 답변/문서**를 생성하게 합니다.

    query
      → LLM
      → hypothetical document
      → embedding
      → vector search

실제 corpus의 정답과 가상 문서가 document-like 표현을 공유하므로 retrieval이 개선될 수 있습니다.

## 3. Hypothetical은 사실일 필요가 없다

HyDE의 생성 문서는 최종 답이 아닙니다.

그 목적은:

    좋은 검색 vector 만들기

입니다.

일부 내용이 사실과 달라도 semantic direction이 적절하면 관련 문서를 찾을 수 있습니다.

최종 answer는 **실제 retrieved evidence**에 기반해야 합니다.

## 4. 예시

Question:

    "기업용 SSO 설정 방법은?"

LLM hypothetical:

    "관리자는 identity provider의 SAML metadata를 등록하고 ACS URL과 entity ID를 설정한다..."

이 문서를 embedding하면 실제 SSO 설정 가이드와 query 자체보다 가까워질 수 있습니다.

## 5. End-to-End

1. User query
2. Generator LLM이 hypothetical answer 생성
3. Hypothetical text embedding
4. Vector DB top-k 검색
5. 실제 document/chunks 반환
6. 필요하면 rerank
7. Retrieved evidence + original query를 final LLM에 전달
8. Final answer

## 6. Query Expansion과 차이

Keyword query expansion:

    synonym / alternative terms 추가

HyDE:

    완성된 document-like text를 생성

따라서 더 풍부한 semantic context를 embedding에 넣습니다.

## 7. Multiple HyDE

한 가상 문서만 만들지 않고 여러 answer를 생성해 vector를 평균하거나 결과를 합칠 수 있습니다.

장점:

- 다양한 관점

단점:

- LLM call/embedding cost 증가

## 8. 장점

- 짧거나 모호한 query 보완
- query/document 표현 형식 차이 축소
- 별도 fine-tuning 없이 적용 가능

## 9. 단점

- query당 LLM generation 추가 → latency/cost
- hypothetical direction이 틀리면 retrieval drift
- exact ID/keyword query에는 불필요
- final generation이 hypothetical 내용을 evidence로 오인하지 않도록 분리 필요

## 10. 언제 쓰나

유용:

- natural-language research question
- zero-shot domain retrieval
- query가 매우 짧고 document가 설명형

덜 유용:

- exact code/ID lookup
- latency가 매우 민감
- hybrid/reranker만으로 이미 retrieval이 충분

## 11. Evaluation

Baseline:

    query embedding search

HyDE:

    hypothetical embedding search

같은 labeled query set에서:

- Recall@k
- MRR/nDCG
- end-to-end answer accuracy
- latency/cost

를 비교해야 합니다.

## 핵심 정리

- HyDE는 질문 대신 LLM이 만든 hypothetical document를 embedding해 검색합니다.
- 가상 문서는 최종 사실 근거가 아니라 retrieval query representation입니다.
- Query와 corpus document의 표현 gap을 줄이는 것이 목적입니다.
- Final answer는 반드시 실제 retrieved sources를 사용해야 합니다.
- 추가 LLM call이 있으므로 retrieval gain이 cost/latency를 정당화하는지 측정해야 합니다.

## 원문

- https://outcomeschool.com/blog/how-does-hyde-work
