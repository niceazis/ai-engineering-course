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

- **Feature Engineering**은 원시 데이터를 모델이 학습하기 좋은 입력 특성으로 바꾸는 과정입니다.
- 어떤 특성을 선택하고, 변환하고, 조합하느냐에 따라 같은 알고리즘도 성능이 크게 달라질 수 있습니다.
- 숫자 스케일링, 범주형 변수 인코딩, 불필요한 특성 제거, 도메인 지식을 이용한 새 특성 생성 등이 대표적인 작업입니다.
- 핵심은 “더 복잡한 모델”보다 “문제를 잘 표현하는 입력”이 성능에 큰 영향을 줄 수 있다는 점입니다.

## 3. One-hot Encoding in Machine Learning
원본: https://www.youtube.com/watch?v=6AmedU5i9go

- 범주형 값을 모델이 사용할 수 있는 숫자 형태로 바꾸는 대표 방법인 **One-hot Encoding**을 설명합니다.
- 예를 들어 색상 값이 red/green/blue라면 각 범주를 별도 0/1 열로 변환합니다.
- 범주 사이에 존재하지 않는 순서 관계를 숫자 1,2,3처럼 잘못 부여하는 문제를 피할 수 있습니다.
- 범주 수가 매우 많으면 차원이 크게 늘어나는 단점이 있어 다른 인코딩이나 임베딩을 고려해야 합니다.

## 4. Epoch, Batch, Batch Size, Iteration
원본: https://www.youtube.com/watch?v=NFLlXE-6vno

- 신경망 학습에서 자주 혼동하는 **Epoch, Batch, Batch Size, Iteration**의 관계를 정리합니다.
- Epoch는 전체 학습 데이터를 한 번 모두 사용한 상태를 의미합니다.
- Batch는 한 번의 계산에 넣는 데이터 묶음이고, Batch Size는 그 묶음의 샘플 수입니다.
- Iteration은 한 Batch를 이용해 forward/backward pass와 파라미터 업데이트를 한 횟수입니다.
- 데이터가 N개이고 Batch Size가 B라면 보통 한 Epoch당 약 N/B번의 Iteration이 발생합니다.

## 5. Softmax Activation Function in Machine Learning
원본: https://www.youtube.com/watch?v=2Zx6x01WwWM

- **Softmax**는 여러 클래스에 대한 raw score(logit)를 합이 1인 확률 분포로 변환합니다.
- 다중 분류 모델의 출력층에서 각 클래스의 상대적 가능성을 표현할 때 흔히 사용됩니다.
- 큰 logit 차이를 더 뚜렷한 확률 차이로 바꾸며, Cross-Entropy Loss와 자주 함께 사용됩니다.
- Attention에서도 score를 가중치로 정규화할 때 같은 원리가 사용됩니다.

## 6. Tokenization in Large Language Models (LLMs)
원본: https://www.youtube.com/watch?v=sK2s9I84EVI

- LLM이 문자열을 그대로 읽지 않고 **Token**이라는 작은 단위로 분해해 처리하는 이유와 방식을 설명합니다.
- Token은 단어 전체일 수도 있고, 단어 일부나 문자·기호 조각일 수도 있습니다.
- BPE 같은 Subword 방식은 어휘 크기와 미등록 단어 문제 사이의 균형을 잡습니다.
- Token 수는 Context Window 사용량, API 비용, 추론 속도와 직접 연결되므로 실무적으로도 중요합니다.

## 7. Embeddings in Machine Learning
원본: https://www.youtube.com/watch?v=LedXW6xl21s

- **Embedding**은 단어·문장·이미지 같은 대상을 의미를 반영하는 숫자 벡터로 표현하는 방법입니다.
- 의미가 비슷한 항목은 벡터 공간에서 가까워지도록 학습됩니다.
- Cosine Similarity 같은 지표로 벡터 간 의미 유사도를 계산할 수 있습니다.
- Semantic Search, 추천, RAG, 클러스터링 등 현대 AI 시스템의 핵심 기반 기술입니다.

## 8. Why is the context window limited in LLMs?
원본: https://www.youtube.com/watch?v=CGIhxIaOg3M

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
