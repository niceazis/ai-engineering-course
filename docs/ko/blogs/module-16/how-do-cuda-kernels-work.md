# CUDA Kernel은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-do-cuda-kernels-work  
> 원저자: Amit Shekhar / Outcome School  
> 검증 한계: 2026-09-29 동기화 시점에 Outcome School 원문 URL의 본문 전문을 직접 열어 검증하지 못했습니다. 따라서 원문 전문을 확인했다고 단정하지 않습니다. upstream `README.md`에 공개된 레슨 소개와 목차의 순서를 보존하고, 기술 세부 사항은 NVIDIA의 공식 CUDA Programming Guide와 공식 NVIDIA 자료만으로 보완했습니다. 원문 전문을 다시 직접 확인할 수 있게 되면 예제·수치·표현 순서를 재대조해야 합니다.

## 1. 왜 GPU가 필요한가?

CPU는 복잡한 제어 흐름과 소수의 작업을 빠르게 처리하는 데 강합니다. GPU는 같은 종류의 계산을 많은 데이터에 반복 적용하는 대규모 병렬 작업에 강합니다.

AI에서 자주 등장하는 vector addition, matrix multiplication, convolution, activation, normalization, attention의 tensor 연산은 작은 독립 계산으로 나누기 쉽습니다.

```text
A = [a0, a1, a2, a3, ...]
B = [b0, b1, b2, b3, ...]

C[0] = A[0] + B[0]
C[1] = A[1] + B[1]
C[2] = A[2] + B[2]
...
```

각 원소의 덧셈은 다른 원소의 결과를 기다릴 필요가 없습니다. GPU는 이런 작업을 매우 많은 Thread에 나눠 동시에 처리합니다.

따라서 핵심은 "GPU가 항상 CPU보다 빠르다"가 아니라 **대량의 독립적이고 규칙적인 병렬 계산을 GPU가 효율적으로 처리할 수 있다**는 것입니다.

## 2. CUDA란?

CUDA는 NVIDIA GPU를 범용 병렬 계산에 사용할 수 있게 하는 NVIDIA의 parallel computing platform과 programming model입니다.

CUDA 프로그램은 크게 Host와 Device로 나눠 생각할 수 있습니다.

```text
CPU
└─ Host code
   ├─ GPU memory 준비
   ├─ input 전송
   ├─ Kernel 실행 요청
   └─ 결과 회수

GPU
└─ Device code
   └─ 많은 Thread가 Kernel 실행
```

NVIDIA 문서에서 CPU 쪽은 **Host**, GPU 쪽은 **Device**입니다.

실무의 소프트웨어 계층은 보통 다음처럼 이어집니다.

```text
PyTorch / TensorFlow / JAX
        ↓
cuBLAS / cuDNN / custom kernels
        ↓
CUDA runtime / driver
        ↓
NVIDIA GPU
```

고수준 Framework를 사용하면 직접 CUDA C++를 작성하지 않아도 많은 Tensor 연산이 내부적으로 GPU Kernel로 실행됩니다.

## 3. CUDA Kernel이란?

CUDA Kernel은 **GPU에서 많은 Thread가 병렬로 실행하는 함수**입니다.

CUDA C++에서는 GPU에서 실행할 함수를 `__global__`로 선언합니다.

```cpp
__global__ void add(const float* a, const float* b, float* c) {
    // GPU에서 실행
}
```

일반 CPU 함수 호출과 달리 Kernel을 실행할 때 Grid와 Block 크기를 함께 지정합니다.

```cpp
add<<<numBlocks, threadsPerBlock>>>(a, b, c);
```

같은 Kernel code를 많은 GPU Thread가 실행하되, 각 Thread가 자신의 Index를 이용해 서로 다른 데이터를 맡습니다.

즉 Kernel의 핵심 질문은 다음과 같습니다.

> 각 GPU Thread가 맡은 데이터 한 조각에 어떤 계산을 수행할 것인가?

## 4. Thread, Block, Grid

CUDA의 기본 실행 계층은 다음과 같습니다.

```text
Grid
├─ Block 0
│  ├─ Thread 0
│  ├─ Thread 1
│  └─ ...
├─ Block 1
│  ├─ Thread 0
│  ├─ Thread 1
│  └─ ...
└─ ...
```

### Thread

실제 계산을 수행하는 가장 작은 논리적 실행 단위입니다. 각 Thread는 `threadIdx`로 Block 내부의 자신의 위치를 알 수 있습니다.

### Block

여러 Thread의 묶음입니다. 같은 Block의 Thread는 Shared Memory를 공유하고 `__syncthreads()` 같은 Barrier로 협력할 수 있습니다.

```cpp
dim3 block(256);
```

NVIDIA CUDA Programming Guide는 Thread Block 하나가 가질 수 있는 Thread 수에 하드웨어 상한이 있으며 일반적인 현재 CUDA Device에서는 최대 1024개라고 설명합니다. 최적 Block 크기는 Workload와 GPU Architecture에 따라 달라집니다.

### Grid

여러 Block의 묶음입니다. Input이 Block 하나보다 크면 여러 Block이 전체 Data를 나눕니다.

보조 예제로 원소 1,000개를 Thread 256개짜리 Block으로 처리한다면 필요한 Block은 4개입니다.

```text
ceil(1000 / 256) = 4
```

정수 계산에서는 흔히 다음 패턴을 씁니다.

```cpp
int numBlocks = (N + threadsPerBlock - 1) / threadsPerBlock;
```

이 1,000/256 예시는 CUDA 모델 설명을 위한 보조 예제이며 Outcome School 원문의 수치라고 단정할 수 없습니다.

## 5. Host와 Device

전형적인 CUDA 실행 흐름은 다음과 같습니다.

```text
1. Host에서 Input 준비
2. Device Memory 확보
3. Host → Device Data 복사
4. Kernel Launch
5. GPU 계산
6. Device → Host 결과 복사
7. Device Memory 해제
```

기본 CUDA Runtime API 흐름은 다음 형태입니다.

```cpp
float* d_a;
float* d_b;
float* d_c;

cudaMalloc(&d_a, bytes);
cudaMalloc(&d_b, bytes);
cudaMalloc(&d_c, bytes);

cudaMemcpy(d_a, h_a, bytes, cudaMemcpyHostToDevice);
cudaMemcpy(d_b, h_b, bytes, cudaMemcpyHostToDevice);

add<<<blocks, threads>>>(d_a, d_b, d_c);

cudaMemcpy(h_c, d_c, bytes, cudaMemcpyDeviceToHost);

cudaFree(d_a);
cudaFree(d_b);
cudaFree(d_c);
```

현대 CUDA에는 Unified Memory 등 다른 방식도 있지만 Host와 Device의 기본 역할을 이해하기에는 이 구조가 가장 명확합니다.

Kernel Launch는 Host 관점에서 비동기적으로 진행될 수 있으므로 결과를 반드시 기다려야 하는 지점에서는 적절한 Synchronization이 필요합니다.

## 6. 첫 CUDA Kernel 작성

Vector Addition에서는 Thread 하나가 원소 하나를 담당하게 만들 수 있습니다.

```cpp
__global__ void vectorAdd(
    const float* a,
    const float* b,
    float* c,
    int n
) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;

    if (i < n) {
        c[i] = a[i] + b[i];
    }
}
```

Launch는 다음 형태입니다.

```cpp
int threadsPerBlock = 256;
int numBlocks = (n + threadsPerBlock - 1) / threadsPerBlock;

vectorAdd<<<numBlocks, threadsPerBlock>>>(d_a, d_b, d_c, n);
```

중요한 것은 Kernel 자체보다 각 Thread가 자기 몫의 Data Index를 찾는 방식입니다.

## 7. 각 Thread는 자기 일을 어떻게 찾는가?

1차원 Data의 대표적인 Global Index 식은 다음과 같습니다.

```text
global_index
= blockIdx.x × blockDim.x + threadIdx.x
```

- `threadIdx.x`: 현재 Block 안의 Thread 번호
- `blockDim.x`: Block 하나의 Thread 수
- `blockIdx.x`: 현재 Block 번호
- `gridDim.x`: 전체 Grid의 Block 수

Block당 256 Thread라면 다음과 같이 이어집니다.

```text
block 0, thread 0   → 0 × 256 + 0   = 0
block 0, thread 255 → 0 × 256 + 255 = 255
block 1, thread 0   → 1 × 256 + 0   = 256
block 1, thread 1   → 1 × 256 + 1   = 257
```

2차원 Image나 Matrix는 `.x`, `.y`를 함께 사용할 수 있습니다.

```cpp
int x = blockIdx.x * blockDim.x + threadIdx.x;
int y = blockIdx.y * blockDim.y + threadIdx.y;
```

NVIDIA 공식 문서의 핵심은 Grid와 Block이 1D, 2D, 3D로 구성될 수 있고 `threadIdx`, `blockIdx`, `blockDim`, `gridDim`을 이용해 각 Thread가 자신의 작업 위치를 계산한다는 점입니다.

## 8. Kernel이 실행될 때 GPU 내부에서는 무슨 일이 일어나는가?

CUDA Programming Model에서 Block은 서로 독립적으로 실행 가능해야 합니다. GPU Scheduler는 Block을 사용 가능한 Streaming Multiprocessor(SM)에 배치합니다.

```text
Kernel Launch
    ↓
Grid 생성
    ↓
여러 Block
    ↓
SM에 Block 배치
    ↓
Thread를 Warp 단위로 실행
    ↓
각 Thread가 자기 Data 계산
```

NVIDIA GPU에서는 Thread가 Hardware 실행 시 Warp라는 묶음으로 처리되며 Warp는 32개 Thread로 구성됩니다.

같은 Warp의 Thread가 비슷한 Instruction Path를 실행하면 효율적입니다. 조건문 때문에 Thread가 서로 다른 Path로 갈라지면 Warp Divergence가 생겨 Throughput이 떨어질 수 있습니다.

Block은 서로의 실행 순서에 의존해서는 안 됩니다. 이 독립성이 있어야 같은 Kernel이 작은 GPU부터 많은 SM을 가진 GPU까지 확장될 수 있습니다.

## 9. CUDA Memory

GPU 성능은 계산량뿐 아니라 **Data를 어디에 두고 어떤 Pattern으로 읽는가**에 크게 좌우됩니다.

| Memory | Scope | 핵심 특징 |
| --- | --- | --- |
| Register | Thread | 매우 빠르고 Thread Private |
| Local Memory | Thread | Thread Private, Device Memory에 위치할 수 있음 |
| Shared Memory | Block | 같은 Block의 Thread가 공유 |
| Global Memory | Grid 전체 | 용량이 크지만 상대적으로 높은 Latency |
| Constant Memory | Grid 전체 | Read-only Pattern에 특화 |
| Texture Memory | Grid 전체 | 특정 Access Pattern에 특화 |

### Global Memory

모든 Thread가 접근할 수 있는 큰 Device Memory입니다. AI Tensor와 Model Weight의 상당 부분이 여기에 놓입니다. Compute Unit이 Data를 기다리면 성능이 낮아질 수 있습니다.

### Shared Memory

한 Block의 Thread들이 공유하는 On-chip Memory입니다. Global Memory보다 낮은 Latency와 높은 Bandwidth를 제공할 수 있어 같은 Data를 여러 번 사용할 때 유용합니다.

```text
Global Memory에서 Tile 읽기
        ↓
Shared Memory에 저장
        ↓
Block 내부 Thread가 재사용
        ↓
계산
```

Matrix Multiplication 같은 연산에서 Tile을 Shared Memory에 올려 재사용하면 Global Memory Traffic을 줄일 수 있습니다.

### Access Pattern

인접한 Thread가 인접한 Memory Address를 읽으면 Hardware가 요청을 효율적으로 묶을 수 있습니다. 이런 Coalesced Access가 가능한 Layout은 GPU Kernel 성능에 매우 중요합니다.

따라서 Kernel 최적화는 단순히 연산 수를 줄이는 문제가 아니라 Memory Layout, Tiling, Cache, Shared Memory, Synchronization을 함께 설계하는 문제입니다.

## 10. CUDA Kernel이 AI에서 중요한 이유

PyTorch에서 다음 한 줄을 작성해도 실제 아래 계층에서는 GPU Library나 Compiler가 적절한 Kernel을 선택하거나 생성합니다.

```python
y = x @ w
```

AI Workload는 다음과 같은 Kernel들로 구성됩니다.

- Matrix Multiplication
- Attention
- Normalization
- Activation
- Element-wise Operation
- Reduction
- Quantization / Dequantization

작은 Operation을 각각 별도 Kernel로 실행하면 Kernel Launch Overhead와 Intermediate Memory Traffic이 누적될 수 있습니다. 여러 Operation을 하나로 합치는 **Kernel Fusion**은 이 비용을 줄이는 대표적인 최적화입니다.

FlashAttention, Fused MLP, Fused Normalization, Quantized GEMM 같은 기술도 계산과 Memory 이동을 더 효율적으로 구성하는 Kernel Engineering과 연결됩니다.

CUDA Kernel을 이해하면 다음을 더 정확하게 분석할 수 있습니다.

- GPU Utilization이 낮은 이유
- 작은 Batch에서 Latency가 커지는 이유
- Memory Bandwidth가 병목이 되는 이유
- Kernel Fusion이 성능을 높이는 이유
- FlashAttention 같은 Custom Kernel이 필요한 이유
- 이론상 FLOPS와 실제 AI Throughput이 다른 이유

## 11. CUDA Kernel이 잘 맞는 곳과 잘 맞지 않는 곳

### 잘 맞는 작업

- 같은 계산을 많은 Data에 반복
- 높은 Data Parallelism
- Matrix/Tensor 연산
- Image Processing
- Scientific Computing
- Deep Learning Training
- LLM Inference
- Simulation

### 잘 맞지 않는 작업

- Data가 너무 작아 Kernel Launch Overhead가 더 큰 경우
- Branch가 많고 Thread마다 실행 경로가 크게 다른 경우
- 순차 의존성이 강해 병렬화가 어려운 경우
- CPU↔GPU Data Transfer가 계산보다 비싼 경우
- Irregular Memory Access가 심한 경우

따라서 GPU 사용 자체가 성능 향상을 보장하지 않습니다.

```text
실제 이득
= 병렬 계산으로 얻는 이득
- Kernel Launch Overhead
- Data Transfer 비용
- Synchronization 비용
- 비효율적 Memory Access 비용
- Divergence 비용
```

이 식은 정량 성능 공식이 아니라 GPU Offload의 Trade-off를 정리하기 위한 개념식입니다.

## 핵심 정리

- CUDA는 NVIDIA GPU를 범용 병렬 계산에 사용하는 Platform/Programming Model입니다.
- CUDA Kernel은 GPU의 많은 Thread가 동시에 실행하는 Device 함수입니다.
- 기본 실행 구조는 `Grid → Block → Thread`입니다.
- `blockIdx`, `blockDim`, `threadIdx`로 각 Thread의 작업 위치를 계산합니다.
- CPU는 Host, GPU는 Device이며 Memory Allocation, Data Transfer, Kernel Launch가 함께 동작합니다.
- Block은 SM에 배치되고 Thread는 Warp 단위로 실행됩니다.
- CUDA 성능은 Compute뿐 아니라 Global/Shared Memory, Access Pattern, Synchronization에 크게 좌우됩니다.
- AI Framework의 고수준 Tensor 연산도 아래에서는 하나 이상의 GPU Kernel로 실행되는 경우가 많습니다.
- Kernel Fusion과 Custom Attention Kernel은 AI Training/Inference 최적화의 핵심 도구입니다.
- GPU는 대규모 규칙적 병렬 계산에 강하지만 작은 작업, 강한 순차 의존성, 불규칙한 Branch/Memory Access에는 항상 유리하지 않습니다.

## 검증에 사용한 1차 자료

- Outcome School 원문 URL — 본문 직접 검증 실패: https://outcomeschool.com/blog/how-do-cuda-kernels-work
- NVIDIA CUDA Programming Guide — Intro to CUDA C++: https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/intro-to-cuda-cpp.html
- NVIDIA CUDA Programming Guide — Writing CUDA SIMT Kernels: https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/writing-cuda-kernels.html
- NVIDIA CUDA Programming Guide — Memory Hierarchy / Heterogeneous Programming: https://docs.nvidia.com/cuda/cuda-programming-guide/
