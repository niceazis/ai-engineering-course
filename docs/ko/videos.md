# YouTube 영상 한국어 요약

> 아래 내용은 각 영상의 핵심 주제를 한국어로 정리한 학습용 요약입니다. 영상 원문은 각 항목의 링크에서 확인할 수 있습니다.

## 1. AI Engineering Explained: LLM, RAG, MCP, Agent, Fine-Tuning, Quantization
원본: https://www.youtube.com/watch?v=lnfWvX66FUk

- AI 엔지니어링에서 반복해서 등장하는 여섯 핵심 개념인 **LLM, RAG, MCP, Agent, Fine-tuning, Quantization**을 한 번에 훑는 개요 영상입니다.
- LLM은 언어 이해·생성을 담당하는 기반 모델, RAG는 외부 지식을 검색해 답변에 결합하는 패턴, MCP는 AI 애플리케이션과 도구·데이터를 연결하는 표준 인터페이스로 설명할 수 있습니다.
- Agent는 모델이 단순 응답을 넘어 도구를 사용하고 반복적으로 목표를 수행하게 하는 구조입니다.
- Fine-tuning은 특정 작업·도메인에 맞게 모델을 추가 학습하는 방법이고, Quantization은 모델의 수치 정밀도를 낮춰 메모리와 추론 비용을 줄이는 방법입니다.
- 전체 코스를 시작하기 전에 AI 엔지니어링의 큰 지도를 잡는 용도로 적합합니다.

## 2. Feature Engineering in Machine Learning
원본: https://www.youtube.com/watch?v=QLlywrWuXag

→ [한국어 상세 영상 학습 노트](videos/module-01/feature-engineering-in-machine-learning.md)

Date-Time→Hour 추출, 위치 feature 결합, bucketization, feature 제거 등 실제 예제를 따라가며 Feature Engineering이 모델 입력 표현을 어떻게 개선하는지 상세히 설명합니다.

## 3. One-hot Encoding in Machine Learning
원본: https://www.youtube.com/watch?v=6AmedU5i9go

→ [한국어 상세 영상 학습 노트](videos/module-01/one-hot-encoding-in-machine-learning.md)

범주형 값을 1,2,3으로 단순 치환할 때 생기는 가짜 순서 문제부터 one-hot vector, high cardinality, unknown category, ordinal encoding·embedding과의 차이까지 단계별로 설명합니다.

## 4. Epoch, Batch, Batch Size, Iteration
원본: https://www.youtube.com/watch?v=NFLlXE-6vno

→ [한국어 상세 영상 학습 노트](videos/module-02/epoch-batch-batch-size-iteration.md)

Epoch·Batch·Batch Size·Iteration의 정확한 관계를 수치 예제로 연결하고, batch size가 memory·gradient noise·iteration 수에 미치는 영향까지 설명합니다.

## 5. Softmax Activation Function in Machine Learning
원본: https://www.youtube.com/watch?v=2Zx6x01WwWM

→ [한국어 상세 영상 학습 노트](videos/module-02/softmax-activation-function-in-machine-learning.md)

→ [모듈 3용 상세 영상 학습 노트](videos/module-03/softmax-activation-function-in-machine-learning.md)

Logit을 확률 분포로 바꾸는 수식, Outcome School의 [2,3,1] 예제, Cross-Entropy와의 연결, numerical stability까지 단계별로 설명합니다.

## 6. Tokenization in Large Language Models (LLMs)
원본: https://www.youtube.com/watch?v=sK2s9I84EVI

→ [한국어 상세 영상 학습 노트](videos/module-03/tokenization-in-large-language-models.md)

- LLM이 문자열을 그대로 읽지 않고 **Token**이라는 작은 단위로 분해해 처리하는 이유와 방식을 설명합니다.
- Token은 단어 전체일 수도 있고, 단어 일부나 문자·기호 조각일 수도 있습니다.
- BPE 같은 Subword 방식은 어휘 크기와 미등록 단어 문제 사이의 균형을 잡습니다.
- Token 수는 Context Window 사용량, API 비용, 추론 속도와 직접 연결되므로 실무적으로도 중요합니다.

## 7. Embeddings in Machine Learning
원본: https://www.youtube.com/watch?v=LedXW6xl21s

→ [한국어 상세 영상 학습 노트](videos/module-03/embeddings-in-machine-learning.md)

- **Embedding**은 단어·문장·이미지 같은 대상을 의미를 반영하는 숫자 벡터로 표현하는 방법입니다.
- 의미가 비슷한 항목은 벡터 공간에서 가까워지도록 학습됩니다.
- Cosine Similarity 같은 지표로 벡터 간 의미 유사도를 계산할 수 있습니다.
- Semantic Search, 추천, RAG, 클러스터링 등 현대 AI 시스템의 핵심 기반 기술입니다.

## 8. Why is the context window limited in LLMs?
원본: https://www.youtube.com/watch?v=CGIhxIaOg3M

→ [한국어 상세 영상 학습 노트](videos/module-04/why-context-window-limited-in-llms.md)

- **Context Window**는 한 번의 추론에서 모델이 참고할 수 있는 Token 범위입니다.
- 입력 길이가 늘수록 Attention 계산량과 KV Cache 메모리 사용량이 증가해 비용과 Latency가 커집니다.
- 단순히 최대 길이를 늘리는 것만으로는 모든 위치의 정보를 동일하게 잘 활용한다는 보장이 없습니다.
- 긴 Context에서는 중요한 내용을 선택·요약하거나 RAG, Context Compaction 같은 기법을 함께 사용하는 것이 중요합니다.

## 9. Agentic RAG Explained
원본: https://www.youtube.com/watch?v=6nSegpuWJVw

- 일반 RAG가 정해진 검색 파이프라인을 한 번 실행한다면 **Agentic RAG**는 Agent가 검색 자체를 판단하고 반복합니다.
- Agent는 질문을 분석하고, 어떤 검색을 할지 결정하고, 결과가 부족하면 Query를 수정하거나 다른 Source를 찾을 수 있습니다.
- 복잡한 질문이나 여러 단계의 조사에는 강하지만 Tool Call 증가로 비용·Latency·실패 가능성이 높아질 수 있습니다.
- 따라서 단순 질의에는 Standard RAG, 계획·검증이 필요한 복잡한 질의에는 Agentic RAG가 더 적합합니다.

## 10. LLM Inference Optimization
원본: https://www.youtube.com/watch?v=jV2sCj4lHYk

- LLM Serving에서 속도와 비용을 좌우하는 주요 병목을 정리하는 영상입니다.
- Prefill과 Decode의 특성이 다르며, KV Cache는 이전 Token의 Key/Value 계산을 재사용해 생성 속도를 높입니다.
- Quantization, Paged Attention, Continuous Batching, Speculative Decoding 같은 기법은 각각 Memory, Throughput, Latency 병목을 줄이는 데 사용됩니다.
- 최적화는 하나의 기법으로 끝나는 것이 아니라 Model Size, Hardware, 동시 사용자 수, TTFT/TPOT 목표에 맞춰 조합해야 합니다.

## 11. The First-Token Latency Problem in LLMs
원본: https://www.youtube.com/watch?v=XD8DD4cEHu0

- 사용자가 요청한 뒤 **첫 Token이 나오기까지의 시간(TTFT)**이 왜 길어질 수 있는지를 설명하는 주제입니다.
- 긴 Prompt를 한 번에 처리하는 Prefill 단계는 계산 집약적이어서 TTFT에 큰 영향을 줍니다.
- Prompt 길이, Batch 상태, Model Size, GPU 계산 성능, Cache 재사용 여부가 첫 응답 지연을 좌우합니다.
- Prefix/Prompt Cache, Prefill 최적화, 적절한 Scheduling, Prefill-Decode 분리 같은 접근으로 TTFT를 줄일 수 있습니다.
