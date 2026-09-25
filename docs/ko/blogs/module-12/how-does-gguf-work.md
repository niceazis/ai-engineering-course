# GGUF는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-gguf-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 file structure, metadata, quantized tensors, Q4_K_M 이름과 mmap 활용을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. GGUF란?

GGUF는 llama.cpp ecosystem에서 local inference에 필요한 model tensors, quantization, tokenizer, architecture/config metadata를 하나의 portable binary file에 담는 format입니다.

## 2. 파일 안의 구성

개념적으로:

    header
    metadata key/value
    tensor descriptors
    tensor data

Runtime은 metadata를 읽어 architecture/tokenizer/context 정보와 tensor 위치를 파악합니다.

## 3. 왜 Local Inference에 유용한가

- single file 배포
- CPU/GPU mixed inference
- multiple quantization variants
- memory mapping
- cross-platform loader

에 적합합니다.

## 4. Quantized Weight

GGUF는 Q4/Q5/Q8 등 quantized tensor representation을 직접 저장할 수 있습니다.

따라서 다운로드한 파일 자체가 이미 특정 precision variant입니다.

## 5. Q4_K_M 해석

원문 설명:

    Q4_K_M
    | | |
    | | +-- M: size/quality variant
    | +---- K: modern K-quant family
    +------ 4: roughly 4 bits/weight

원문 비교:

| Variant | 대략 bit | 특성 |
| --- | ---: | --- |
| Q4_K_M | 약 4 | 작은 size, 좋은 균형 |
| Q5_K_M | 약 5 | 더 큰 memory, 품질 상승 |
| Q8_0 | 약 8 | 가장 큼, 높은 품질 |

원문은 일반 laptop에서 Q4_K_M을 좋은 시작점으로 설명합니다.

## 6. Memory Mapping

GGUF는 tensor offset이 명확해 runtime이 file을 mmap하고 필요한 page를 OS에 맡길 수 있습니다.

장점:

- startup 시 full copy 불필요
- OS page cache 활용
- process 간 read-only page 공유 가능

## 7. Metadata Extensibility

새 architecture/field가 필요하면 metadata key를 추가할 수 있습니다.

Format version과 runtime support가 맞아야 하므로 최신 llama.cpp/loader compatibility를 확인해야 합니다.

## 8. GGUF vs Safetensors

GGUF:

- local inference metadata와 quantization에 강함
- llama.cpp 계열 중심

Safetensors:

- framework-neutral safe tensor storage
- training/fine-tuning ecosystem에서 널리 사용

목적이 다릅니다.

## 핵심 정리

- GGUF는 model tensor와 tokenizer/config metadata를 한 file에 담는 local-inference format입니다.
- Quantized weight를 직접 저장해 여러 Q4/Q5/Q8 variant를 배포합니다.
- 원문 Q4_K_M은 약 4-bit K-quant medium variant로 설명됩니다.
- mmap-friendly layout이 local startup/memory 효율에 유리합니다.
- Format과 runtime compatibility를 함께 확인해야 합니다.

## 원문

- https://outcomeschool.com/blog/how-does-gguf-work
