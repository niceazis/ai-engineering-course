# Ollama는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-ollama-work
> 원저자: Amit Shekhar / Outcome School
> 검증 상태: 2026-10-06 기준 Outcome School 본문 전체는 직접 확인하지 못했습니다. 대신 upstream 저장소의 commit `b4022e72277423ff5e646f3b1a2c6383fe5cda1c`에서 이 레슨의 제목, URL, 설명 순서와 학습 항목 11개를 직접 확인했습니다. 아래 세부 내용은 그 순서를 유지하되 Ollama 공식 문서와 공식 GitHub 자료로만 보완했습니다. 원문에 실제로 포함되었는지 확인할 수 없는 예시와 수치는 원문 내용으로 단정하지 않습니다.

## 1. 로컬에서 LLM을 실행한다는 의미

로컬 추론은 모델의 Weight를 자신의 컴퓨터에 내려받고, 자신의 CPU/GPU와 메모리를 사용해 Prompt를 처리하고 Token을 생성하는 방식입니다.

```text
외부 API: 앱 -> 인터넷 -> 외부 모델 서버 -> 응답
로컬 실행: 앱 -> localhost의 Ollama server -> 로컬 모델 -> 응답
```

장점은 로컬 데이터 경계를 유지하기 쉽고, 이미 내려받은 모델은 외부 모델 API 없이 실행할 수 있으며, 모델과 실행 설정을 직접 관리할 수 있다는 점입니다. 반면 성능과 실행 가능한 모델 크기는 로컬 RAM/VRAM과 연산 성능에 직접 제한됩니다.

## 2. Ollama란?

Ollama는 Open Model을 다운로드하고 실행·관리하며 애플리케이션에서 API로 사용할 수 있게 하는 오픈소스 도구입니다. 공식 GitHub 저장소는 지원 추론 Backend 중 하나로 llama.cpp를 명시합니다.

사용자 관점에서는 모델 선택, 필요한 모델 데이터 확보, 모델 로드, CPU/GPU 추론, CLI 또는 API 요청, 생성 결과 반환을 하나의 흐름으로 묶어 줍니다. 따라서 Ollama는 단순한 모델 파일 저장소가 아니라 모델 관리와 로컬 Serving을 쉽게 사용할 수 있도록 만든 계층으로 이해하는 것이 적절합니다.

## 3. 큰 모델이 만드는 메모리 문제

LLM Weight가 차지하는 이론적 메모리는 다음처럼 근사할 수 있습니다.

```text
Weight memory ≈ parameter count × bits per weight / 8
```

예를 들어 7B 모델이라면 Weight만 계산했을 때 FP16은 약 14 GB, 4-bit 표현은 약 3.5 GB입니다. 이 수치는 개념 설명을 위한 계산 예시이며 Outcome School 원문의 수치라고 주장하지 않습니다.

실행 시에는 Weight 외에도 KV Cache, Runtime Buffer, Metadata, 긴 Context를 위한 추가 메모리가 필요합니다.

## 4. Quantization과 GGUF

Quantization은 Weight를 더 낮은 Precision으로 표현해 메모리 사용량과 Memory Bandwidth 부담을 줄이는 기법입니다. 낮은 Bit 수는 Local Hardware에서 더 큰 모델을 실행할 가능성을 높이지만, 방식에 따라 정확도 손실이 생길 수 있습니다.

GGUF는 llama.cpp 생태계에서 모델 Weight와 Metadata를 담는 형식입니다. Ollama의 공식 Modelfile 문서는 로컬 GGUF 파일을 Base Model로 가져오는 방식을 지원합니다.

- Quantization: 숫자의 표현 정밀도를 줄이는 방법
- GGUF: 모델 데이터와 Metadata를 담는 형식
- Ollama: 모델을 관리하고 실행하며 API로 제공하는 도구

## 5. Client와 Server 구조

Ollama는 Client가 로컬 Server에 요청하는 구조로 이해할 수 있습니다.

```text
CLI / Python / JavaScript / 사용자 앱
                |
                v
        Ollama local server
                |
                v
        inference backend
                |
                v
           CPU / GPU
```

공식 API 문서 기준 로컬 API Base URL은 `http://localhost:11434/api`이고 OpenAI-compatible Endpoint도 제공합니다. 이 구조 덕분에 Terminal에서 시험한 모델을 같은 로컬 Server를 통해 애플리케이션에서도 호출할 수 있습니다.

## 6. 모델 실행의 단계

upstream에서 공개한 설명 순서를 기준으로 한 요청의 흐름을 정리하면 다음과 같습니다.

1. Client가 모델과 Prompt를 지정합니다.
2. Server가 요청한 모델의 Local 상태를 확인합니다.
3. 필요한 모델이 없으면 먼저 모델 데이터를 확보합니다.
4. Model Metadata와 Runtime Option을 읽습니다.
5. 가능한 CPU/GPU 자원에 모델을 로드합니다.
6. Prompt를 Token으로 변환합니다.
7. Prefill 단계에서 입력을 처리하고 KV Cache를 만듭니다.
8. Decode 단계에서 다음 Token을 반복 생성합니다.
9. 생성 결과를 Client에 반환합니다.
10. 연속 요청을 위해 모델을 일정 시간 Memory에 유지할 수 있습니다.

Ollama 공식 FAQ는 기본적으로 Idle 상태의 모델을 일정 시간 Memory에 유지하며, API 옵션으로 이 시간을 조정할 수 있다고 설명합니다.

## 7. 모델 다운로드와 저장

Ollama는 내려받은 모델을 Local Model Store에 보관하고 다음 실행에서 재사용합니다. 공식 FAQ에는 운영체제별 기본 저장 위치와 별도 저장 위치를 지정하는 환경 설정이 문서화되어 있습니다.

```text
모델 이름
  -> 모델 정보 확인
  -> 필요한 데이터 다운로드
  -> local model store 저장
  -> 이후 실행에서 재사용
```

즉 동일 모델을 실행할 때마다 전체 모델을 다시 다운로드하는 구조는 아닙니다.

## 8. CPU와 GPU에서의 실행

Local LLM 성능은 모델 크기와 Quantization, RAM/VRAM 용량, Memory Bandwidth, Context 길이, 동시 요청 수의 영향을 받습니다.

Ollama 공식 FAQ는 현재 모델의 Processor 배치를 확인하는 기능을 제공하며, 모델이 GPU 전체, CPU 전체 또는 CPU/GPU에 나뉘어 로드될 수 있음을 설명합니다.

여러 GPU가 있는 환경에서는 한 GPU에 모델이 완전히 들어가면 한 GPU에 배치하는 것을 우선하고, 그렇지 않으면 여러 GPU에 나눌 수 있습니다.

Weight가 메모리에 들어가는 것과 긴 Context 및 높은 동시성을 안정적으로 처리할 수 있는 것은 별개의 문제입니다. Context가 길어지면 KV Cache도 커집니다.

## 9. Modelfile

Ollama 공식 문서는 Modelfile을 Customized Model을 만들고 공유하기 위한 Blueprint로 설명합니다.

| 항목 | 역할 |
| --- | --- |
| `FROM` | Base Model 지정 |
| `PARAMETER` | Runtime Parameter 설정 |
| `TEMPLATE` | Prompt Template 지정 |
| `SYSTEM` | System Message 지정 |
| `LICENSE` | License 정보 |
| `MESSAGE` | 예시 대화 |
| `REQUIRES` | 최소 Ollama Version |
| `CAPABILITY` | 추가 Capability |

GGUF 파일을 Base Model로 지정하는 방식도 공식 지원됩니다. 이 구조는 Weight를 다시 학습하지 않고도 Base Model과 실행 설정을 하나의 재현 가능한 정의로 묶을 수 있게 합니다.

## 10. API를 통한 Code 사용

Ollama는 Local HTTP API와 공식 Python/JavaScript Library를 제공합니다.

```python
from ollama import chat

response = chat(
    model="gemma4",
    messages=[{"role": "user", "content": "KV Cache를 설명해줘."}],
)

print(response.message.content)
```

애플리케이션은 Model Process를 직접 제어하기보다 Local Ollama Server에 요청하고 결과를 받습니다. 이 때문에 개발자는 모델 Runtime의 세부 설정보다 애플리케이션 로직에 더 집중할 수 있습니다.

## 11. 잘 맞는 환경과 한계

Ollama는 개인 PC나 Workstation에서 Open Model을 빠르게 시험할 때, Local Prototype을 만들 때, 외부 모델 API를 거치지 않고 데이터를 처리하고 싶을 때, Python/JavaScript 앱에 간단한 Local LLM API가 필요할 때 유용합니다.

반대로 모델이 RAM/VRAM보다 지나치게 크거나, 긴 Context와 많은 동시 요청이 필요하거나, 높은 Throughput과 엄격한 Production SLA가 필요한 대규모 Serving에서는 한계가 커질 수 있습니다. Quantization에 따른 품질 저하를 허용하기 어려운 Task도 별도 검토가 필요합니다.

## 12. Ollama, llama.cpp, vLLM 비교

| 도구 | 중심 역할 | 대표적인 적합 환경 |
| --- | --- | --- |
| llama.cpp | 저수준 Local Inference Runtime | Local Model 실행과 Hardware 최적화 |
| Ollama | 모델 관리 + Local Server + CLI/API | Local 개발과 애플리케이션 연결 |
| vLLM | 높은 Throughput의 Serving Engine | GPU Server의 다중 사용자 Serving |

Ollama가 llama.cpp Backend를 활용한다고 해서 두 프로젝트가 같은 것은 아닙니다. llama.cpp가 Runtime Engine에 가깝다면 Ollama는 그 위에서 모델 Lifecycle과 사용 인터페이스를 단순화하는 역할에 가깝습니다.

## 13. 핵심 정리

- 로컬 LLM은 자신의 Hardware에서 모델 Weight를 사용해 추론합니다.
- Quantization과 GGUF는 Local 실행 가능성을 높이는 핵심 요소입니다.
- Ollama는 Client-Server 구조로 모델 관리와 추론을 단순화합니다.
- 실행 과정은 모델 확인, 로드, Tokenization, Prefill, Decode, Response 순으로 이해할 수 있습니다.
- Modelfile은 Base Model과 실행 설정을 재현 가능한 형태로 묶습니다.
- Local API와 공식 Client Library를 이용해 애플리케이션에 연결할 수 있습니다.
- 대규모 동시 Serving에서는 전용 Serving Engine이 더 적합할 수 있습니다.

## 14. 직접 검증한 원문 범위

Outcome School 본문 전체는 직접 검증하지 못했습니다. upstream course commit에서 직접 확인한 학습 항목은 다음 11개입니다.

1. What does running an LLM locally mean
2. What is Ollama
3. The big problem: models are huge
4. Quantization and the GGUF file format
5. The architecture: client and server
6. What happens when we run a model
7. How models are downloaded and stored
8. How the model runs on CPU and GPU
9. What is a Modelfile
10. Using Ollama from code through its API
11. Where it works well and where it fails

따라서 위 순서는 보존했지만, 직접 확인하지 못한 원문의 비유·예시·수치·문장을 이 문서의 내용과 동일하다고 단정하지 않습니다.

## 출처

- Outcome School 원문: https://outcomeschool.com/blog/how-does-ollama-work
- Upstream commit: https://github.com/amitshekhariitbhu/ai-engineering-course/commit/b4022e72277423ff5e646f3b1a2c6383fe5cda1c
- Ollama 공식 GitHub: https://github.com/ollama/ollama
- Ollama API 공식 문서: https://docs.ollama.com/api/introduction
- Ollama Modelfile 공식 문서: https://docs.ollama.com/modelfile
- Ollama FAQ 공식 문서: https://docs.ollama.com/faq
