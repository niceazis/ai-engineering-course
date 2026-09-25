# LLM Evaluation이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/llm-evaluation  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-05-24 공개 원문을 직접 확인해 Automatic Metric, Benchmark, Human Evaluation, LLM-as-a-Judge, Task-Specific·Safety Evaluation의 순서와 예시를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. LLM Evaluation의 목적

LLM Evaluation은 모델이나 LLM 애플리케이션이 실제로 기대한 일을 얼마나 잘하는지 측정하는 과정입니다.

확인해야 할 질문:

- 정답인가?
- 도움이 되는가?
- 안전한가?
- 이전 버전보다 나아졌는가?
- latency/cost를 감안해 배포할 가치가 있는가?

평가 없이 배포하면 prompt/model 변경이 좋아졌는지 나빠졌는지 알 수 없습니다.

## 2. 네 가지 핵심 평가 방법

원문은 네 가지로 정리합니다.

1. Automatic Metrics
2. Benchmarks
3. Human Evaluation
4. LLM as a Judge

Task-Specific Evaluation과 Safety Evaluation은 이 네 방법을 실제 use case에 맞게 조합하는 상위 설계라고 설명합니다.

## 3. Automatic Metrics

### BLEU

주로 번역에서 n-gram precision을 봅니다.

단점:

    reference: The cat sat on the mat
    output:    A feline rested on the rug

의미가 비슷해도 lexical overlap이 낮아 score가 낮을 수 있습니다.

### ROUGE

주로 summarization에서 reference n-gram coverage를 봅니다.

### BERTScore

Contextual embedding으로 semantic similarity를 평가해 paraphrase에 더 강합니다.

### METEOR

Synonym, stemming, word order를 일부 고려합니다.

### Perplexity

Next-token prediction quality를 측정합니다. 낮을수록 test data를 더 높은 확률로 예측합니다.

### Exact Match

정답 문자열이 정확히 같으면 1, 아니면 0.

Math, short factual answer처럼 objective answer가 있는 task에 좋습니다.

## 4. Benchmark

원문이 분류한 대표 benchmark:

### General Knowledge

- MMLU
- MMLU-Pro

### Common Sense

- HellaSwag

### Coding

- HumanEval
- SWE-bench Verified
- LiveCodeBench

### Math

- GSM8K
- MATH
- AIME

### Frontier Reasoning

- GPQA-Diamond
- Humanity's Last Exam

### Instruction Following

- IFEval

### Tool Use

- BFCL

### Long Context

- RULER

### Truthfulness

- TruthfulQA

### Conversation Preference

- Chatbot Arena / LMArena

## 5. Benchmark를 그대로 믿으면 안 되는 이유

원문은 세 가지를 강조합니다.

### Saturation

Top models가 ceiling에 가까워지면 구분력이 떨어집니다.

### Data Contamination

Training에서 test item을 이미 봤을 수 있습니다.

### Qualification Bar

낡은 benchmark라도 minimum capability gate로 사용할 수 있습니다.

## 6. Human Evaluation

원문 방식:

- Likert scale 1~5
- Pairwise comparison
- Error annotation

장점:

- tone, usefulness, creativity 등 open-ended quality 판단 가능

단점:

- 느림
- 비쌈
- annotator disagreement

중요한 최종 check에 적합합니다.

## 7. LLM as a Judge

Strong LLM에게:

    input
    candidate output
    rubric

을 주고 score/verdict를 받습니다.

원문은 position bias, verbosity bias, self-preference bias를 경고합니다.

따라서 human sample과 judge agreement를 검증해야 합니다.

## 8. RAG Evaluation

원문은 RAGAS 계열의 네 패턴을 소개합니다.

### Context Precision

가져온 chunk 중 실제 관련 chunk의 비율.

### Context Recall

필요한 evidence 중 얼마나 retrieve했는가.

### Faithfulness / Groundedness

최종 answer가 retrieved context에 의해 뒷받침되는가.

### Answer Relevance

질문에 실제로 답했는가.

Retrieval과 generation을 따로 평가해야 root cause를 알 수 있습니다.

## 9. Agent Evaluation

원문은 agent에서 다음을 추가로 봅니다.

- 올바른 tool 선택
- 올바른 arguments
- task completion
- step count

대표 benchmark로 τ-bench, SWE-bench Verified, GAIA, WebArena, BFCL 등을 언급합니다.

## 10. Code Generation

Code는 text similarity보다 **실행 가능한 verifier**가 훨씬 좋습니다.

    generated code
      → unit tests
      → pass/fail

정답이 기계적으로 검증 가능하면 LLM judge보다 deterministic checker를 우선합니다.

## 11. Safety / Red Team

평가 대상:

- jailbreak
- prompt injection
- harmful request
- privacy leak
- bias

원문은 HarmBench, AdvBench, TrustLLM을 예로 듭니다.

Safety는 launch 전 1회가 아니라 production traffic에서 지속 모니터링해야 합니다.

## 12. Best Practice

원문 핵심:

- public benchmark만 쓰지 말고 custom eval set 작성
- automatic + judge + human 조합
- judge를 human label로 검증
- prompt/model 변경마다 regression eval
- rare but important edge case 포함
- latency/cost도 함께 측정

## 13. 평가 Dataset 설계

좋은 custom eval set은 평균적인 case뿐 아니라:

    common cases
    hard cases
    known failures
    adversarial cases
    high-business-risk cases

를 포함합니다.

실제 production failure가 나오면 eval set에 추가해 재발 방지 test로 만듭니다.

## 핵심 정리

- LLM Evaluation은 correctness뿐 아니라 helpfulness, safety, cost, latency까지 포함합니다.
- Automatic Metric, Benchmark, Human, LLM Judge를 task에 맞게 조합합니다.
- RAG는 retrieval과 grounded generation을 분리 평가해야 합니다.
- Objective verifier가 있으면 judge보다 test/rule을 우선합니다.
- 가장 중요한 것은 public benchmark보다 실제 use case를 반영한 regression eval set입니다.

## 원문

- https://outcomeschool.com/blog/llm-evaluation
