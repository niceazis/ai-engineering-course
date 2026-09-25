# Model Quantization은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-model-quantization-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 FP32/FP16/BF16/INT8/INT4, 7B memory 수치, scale·zero-point, symmetric/asymmetric, PTQ/QAT와 LLM-specific 방법을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Quantization이란?

Quantization은 model의 숫자를 더 적은 bit로 표현해 **memory, bandwidth, compute cost를 줄이는 방법**입니다.

예:

    FP32 → INT8 / INT4

Model architecture는 그대로 두고 weight/activation 표현 precision을 낮춥니다.

## 2. Bit 수와 표현력

원문 정리:

- FP32: 32-bit floating point
- FP16/BF16: 16-bit floating point
- INT8: 8-bit integer, 256 levels
- INT4: 4-bit integer, 16 levels

Bit가 줄수록 메모리는 작아지지만 원래 실수값을 더 거칠게 근사합니다.

## 3. 원문의 7B Model 수치

7 billion weights를 단순 계산하면:

    FP32: 4 bytes × 7B ≈ 28 GB
    INT8: 1 byte × 7B ≈ 7 GB
    INT4: 0.5 byte × 7B ≈ 3.5 GB

실제 파일/VRAM은 metadata, scales, KV cache, runtime buffer 때문에 더 필요할 수 있습니다.

## 4. Scale과 Zero-Point

Real value를 integer grid로 mapping합니다.

Asymmetric 예:

    q = round(x / scale) + zero_point
    x_hat = scale × (q - zero_point)

원문 예에서는 -1.0~1.0 범위를 0~255에 mapping하며 scale이 약 0.00784인 직관을 보여 줍니다.

## 5. Symmetric vs Asymmetric

### Symmetric

0을 중심으로 양수/음수 범위를 대칭 사용합니다.

    zero_point ≈ 0

구현이 단순하고 matrix kernel에 유리합니다.

### Asymmetric

데이터 min/max에 맞춰 zero-point를 둡니다.

비대칭 distribution을 더 잘 활용할 수 있지만 연산이 조금 복잡합니다.

## 6. Per-Tensor vs Per-Channel/Group

Per-tensor:

    tensor 전체에 하나의 scale

Per-channel/group:

    channel 또는 작은 group마다 scale

세밀한 scale은 outlier를 더 잘 처리하지만 metadata와 kernel 복잡도가 늘어납니다.

## 7. PTQ

Post-Training Quantization:

    pretrained model
      → calibration/quantize
      → deploy

재학습 없이 빠르게 적용합니다.

대표 LLM 방식:

- GPTQ
- AWQ
- bitsandbytes
- GGUF quantization

## 8. QAT

Quantization-Aware Training은 training 중 fake quantization effect를 넣어 model이 low precision에 적응하게 합니다.

장점:

- 낮은 bit에서 품질 보존 가능

단점:

- training cost
- pipeline 복잡

## 9. Weight-Only vs Weight+Activation

Weight-only:

- weight memory/bandwidth 절감
- activation은 FP16/BF16 등

Weight+activation:

- 더 큰 speed/memory 절감 가능
- activation outlier 때문에 품질/커널 난도 증가

## 10. LLM Outlier

Transformer activation/weight 일부는 범위가 매우 큽니다.

하나의 scale이 outlier에 맞춰지면 대부분 작은 값의 resolution이 손실됩니다.

대응:

- group-wise quantization
- outlier channel 별도 처리
- activation-aware scaling
- mixed precision

## 11. Accuracy Trade-off

Bit를 낮출수록 일반적으로:

    memory ↓
    bandwidth ↓
    quality risk ↑

하지만 model/data/task에 따라 Q4도 충분히 좋은 경우가 있습니다.

## 핵심 정리

- Quantization은 model 숫자의 bit precision을 줄여 memory/bandwidth를 낮춥니다.
- 원문 7B 예는 FP32 28GB, INT8 7GB, INT4 3.5GB입니다.
- Scale과 zero-point가 real↔integer mapping의 핵심입니다.
- Per-group/channel이 per-tensor보다 정밀하지만 metadata가 늘어납니다.
- PTQ는 간단, QAT는 더 비싸지만 low-bit 품질을 보존하기 쉽습니다.
- 실제 선택은 품질, VRAM, tokens/s를 함께 측정해야 합니다.

## 원문

- https://outcomeschool.com/blog/how-does-model-quantization-work
