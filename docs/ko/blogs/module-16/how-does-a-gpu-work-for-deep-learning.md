# 딥러닝에서 GPU는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-a-gpu-work-for-deep-learning  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-07-03 공개 원문을 직접 확인해 CPU/GPU 구조, matrix multiplication 예제, VRAM·memory bandwidth, Tensor Core·precision, CUDA/cuDNN, training/inference, multi-GPU의 설명 순서를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. GPU가 딥러닝에 잘 맞는 이유

GPU는 원래 화면의 수백만 pixel을 동시에 계산하기 위해 만들어졌습니다. Pixel 계산은 서로 독립적인 경우가 많습니다.

딥러닝도 비슷합니다. Neural network의 핵심 연산은 수많은 multiply-add를 반복하는 matrix multiplication입니다.

따라서 복잡한 하나의 문제보다 단순한 계산을 매우 많이 병렬로 처리하는 GPU 구조가 잘 맞습니다.

## 2. CPU vs GPU

| 항목 | CPU | GPU |
| --- | --- | --- |
| Core 수 | 적음 | 매우 많음 |
| Core 성격 | 강력하고 복잡한 제어에 강함 | 단순 arithmetic에 최적 |
| 강점 | branch, OS, general-purpose work | parallel multiply-add |
| 작업 방식 | 적은 수의 일을 빠르게 | 많은 일을 동시에 |

원문 비유에서 CPU는 한 명의 뛰어난 수학 교수, GPU는 수천 명의 학생입니다.

백만 개의 간단한 산수 문제를 풀 때 교수 한 명은 하나씩 처리하지만, 학생 수천 명은 문제를 나눠 동시에 풀 수 있습니다.

## 3. Matrix Multiplication

원문 2×2 예:

    [1 2]   [5 6]
    [3 4] × [7 8]

왼쪽 위 원소:

    (1 × 5) + (2 × 7)
    = 5 + 14
    = 19

각 output 위치의 multiply-add 계산은 상당 부분 독립적입니다.

실제 neural network matrix는 수천×수천 크기이므로 millions of multiply-add가 생기고, 이것이 GPU 병렬 처리에 적합합니다.

## 4. Serial vs Parallel

CPU 직관:

    op1 → op2 → op3 → ...

GPU 직관:

    op1 ─┐
    op2 ─┤
    op3 ─┼→ 같은 시간대에 대량 처리
    ...  ┘

GPU 성능의 본질은 단순 clock speed가 아니라 massive parallelism입니다.

## 5. VRAM

GPU는 model weight, activation, input, KV Cache 등을 GPU 가까운 memory인 VRAM에 둡니다.

Model이 VRAM에 들어가지 않으면 CPU↔GPU offload 또는 multi-GPU partition이 필요합니다.

원문은 24GB, 40GB, 80GB 같은 large-VRAM GPU를 예로 듭니다.

## 6. Memory Bandwidth

Compute unit이 아무리 많아도 weight/data를 제때 공급하지 못하면 GPU가 기다립니다.

Memory bandwidth는 VRAM과 compute core 사이의 data 이동 속도입니다.

특히 LLM inference의 decode 단계에서는 bandwidth가 핵심 병목이 될 수 있습니다.

## 7. Tensor Core와 Lower Precision

Tensor Core는 matrix multiply-accumulate를 딥러닝에 맞게 매우 빠르게 수행하는 specialized hardware입니다.

원문이 설명하는 대표 precision:

- FP32: 32-bit
- FP16/BF16: 16-bit
- INT8: 8-bit

Precision을 낮추면 memory 사용과 bandwidth가 줄고 tensor-core throughput을 높일 수 있습니다.

원문은 FP16/BF16을 사용하면 메모리 사용을 대략 절반 수준으로 줄이고 더 빠르게 계산할 수 있다는 직관을 설명합니다. 실제 speedup은 GPU와 kernel에 따라 달라집니다.

## 8. CUDA와 cuDNN

Software stack:

    PyTorch / TensorFlow
      → cuDNN
      → CUDA
      → NVIDIA GPU

사용자는 보통 CUDA kernel을 직접 작성하지 않고 framework가 아래 stack을 사용합니다.

원문 PyTorch 예의 핵심은 tensor를 CUDA device로 옮긴 뒤 matrix multiplication을 수행하면 CUDA/cuDNN stack이 GPU를 사용한다는 것입니다.

## 9. Training vs Inference

### Training

- forward pass
- backward pass
- gradients
- optimizer state

가 필요해 compute와 memory 사용량이 큽니다.

### Inference

이미 학습된 weight로 주로 forward pass만 수행합니다.

Training보다 가볍지만 LLM에서는 KV Cache, long context, high concurrency 때문에 여전히 memory가 중요합니다.

## 10. Multi-GPU

### Data Parallelism

각 GPU에 full model copy를 두고 data batch를 나눕니다. 이후 gradient를 synchronize합니다.

### Model Parallelism

Model이 한 GPU에 들어가지 않으면 layer/tensor를 여러 GPU에 나눕니다.

GPU 간 communication이 많아지므로 NVLink 같은 high-speed interconnect가 중요합니다.

## 11. 왜 NVIDIA가 강한가

원문은 hardware만이 아니라 ecosystem을 강조합니다.

- GPU/Tensor Core
- VRAM/bandwidth
- CUDA
- cuDNN
- framework integration
- NVLink

이 조합이 현대 AI training/inference에서 강력한 진입 장벽이 됐습니다.

## 핵심 정리

- GPU는 수천 개의 단순 계산을 병렬 처리해 딥러닝 matrix multiplication에 적합합니다.
- 원문 2×2 matrix 예에서 한 output은 (1×5)+(2×7)=19입니다.
- VRAM 용량과 memory bandwidth는 compute 성능만큼 중요합니다.
- Tensor Core와 FP16/BF16/INT8 같은 lower precision이 modern AI throughput을 높입니다.
- Training은 forward+backward, inference는 주로 forward이며 memory profile도 다릅니다.
- Multi-GPU에서는 data parallelism과 model parallelism이 대표 전략입니다.

## 원문

- https://outcomeschool.com/blog/how-does-a-gpu-work-for-deep-learning
