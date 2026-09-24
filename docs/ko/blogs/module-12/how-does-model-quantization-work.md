# Model Quantization은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-model-quantization-work
> 원저자: Amit Shekhar / Outcome School
> 문서 성격: **원문 전체 번역본이 아닌 독립적인 한국어 상세 해설·학습 노트**

## 핵심 해설

모델 숫자를 더 적은 Bit로 표현해 Memory를 줄이고 추론을 빠르게 만드는 Quantization을 배웁니다.

## 핵심 학습 항목

- Model Quantization이란?
- FP32, INT8, INT4
- 적은 Bit가 Memory와 Speed에 미치는 영향
- Scale과 Zero-point
- Symmetric vs Asymmetric
- Per-tensor vs Per-channel
- PTQ vs QAT
- Weight-only vs Weight-and-activation
- LLM Outlier 문제
- GPTQ, AWQ, bitsandbytes, GGUF/llama.cpp
- Accuracy Trade-off와 Local LLM
- 정리

## 단계별 학습 가이드

### 1. Model Quantization이란?

**Model Quantization이란?**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 2. FP32, INT8, INT4

**FP32, INT8, INT4**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 3. 적은 Bit가 Memory와 Speed에 미치는 영향

**적은 Bit가 Memory와 Speed에 미치는 영향**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 4. Scale과 Zero-point

**Scale과 Zero-point**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 5. Symmetric vs Asymmetric

**Symmetric vs Asymmetric**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 6. Per-tensor vs Per-channel

**Per-tensor vs Per-channel**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 7. PTQ vs QAT

**PTQ vs QAT**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 8. Weight-only vs Weight-and-activation

**Weight-only vs Weight-and-activation**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 9. LLM Outlier 문제

**LLM Outlier 문제**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 10. GPTQ, AWQ, bitsandbytes, GGUF/llama.cpp

**GPTQ, AWQ, bitsandbytes, GGUF/llama.cpp**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 11. Accuracy Trade-off와 Local LLM

**Accuracy Trade-off와 Local LLM**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 12. 정리

**정리**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

## 실무 연결

- 정확도·안정성·속도·메모리에 미치는 영향을 확인합니다.
- training과 inference에서 동작이 달라지는지 구분합니다.
- 관련 hyperparameter와 실패 조건을 함께 확인합니다.
- 실제 프레임워크 구현과 연결해서 봅니다.

## 점검 질문

1. Model Quantization은 어떻게 동작하는가?을 한 문장으로 설명할 수 있는가?
2. 왜 필요한지 설명할 수 있는가?
3. 핵심 데이터 흐름을 순서대로 설명할 수 있는가?
4. 대표 장점과 한계를 말할 수 있는가?
5. 언제 이 방법을 선택할지 설명할 수 있는가?

## 원문

- https://outcomeschool.com/blog/how-does-model-quantization-work
