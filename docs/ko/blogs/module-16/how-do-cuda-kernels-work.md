# CUDA Kernel은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-do-cuda-kernels-work  
> 원저자: Amit Shekhar / Outcome School  
> 원문 확인: 2026-09-30에 Outcome School 원문을 직접 확인했습니다.  
> 교차검증: NVIDIA CUDA Programming Guide와 CUDA Best Practices Guide의 thread hierarchy, warp, block limit, host/device memory 설명을 확인했습니다.

## 1. 왜 GPU가 필요한가?

CPU는 비교적 적은 수의 강력한 core로 복잡한 제어 흐름과 순차 작업을 잘 처리합니다. GPU는 많은 실행 자원을 이용해 같은 종류의 연산을 대량의 데이터에 병렬로 적용하는 데 유리합니다.

원문은 많은 감자를 처리하는 주방을 예로 듭니다. CPU는 숙련된 소수의 작업자가 순서대로 처리하는 방식에 가깝고, GPU는 많은 작업자가 독립적인 항목을 동시에 처리하는 방식에 가깝습니다.

AI 학습과 추론에는 큰 matrix multiplication과 vector operation이 반복됩니다. 서로 독립적인 계산을 많이 수행할 수 있기 때문에 GPU의 병렬 실행 모델과 잘 맞습니다.

핵심은 단순히 core 수가 아니라 **같은 연산을 많은 데이터 요소에 동시에 적용할 수 있는가**입니다.

## 2. CUDA란?

CUDA(Compute Unified Device Architecture)는 NVIDIA GPU에서 일반 목적 병렬 연산을 수행하기 위한 platform과 programming model입니다.

일반적인 CUDA program은 다음 흐름을 가집니다.

1. Host에서 input을 준비합니다.
2. Device memory를 확보합니다.
3. Input을 Host에서 Device로 복사합니다.
4. GPU에서 kernel을 실행합니다.
5. 결과를 Device에서 Host로 가져옵니다.
6. Device memory를 해제합니다.

CUDA는 C/C++ 계열 syntax와 runtime API를 이용해 GPU가 수행할 연산을 직접 기술할 수 있게 합니다.

## 3. CUDA Kernel이란?

CUDA Kernel은 **GPU에서 실행되며 많은 thread가 같은 kernel code를 동시에 수행하는 함수**입니다.

중요한 사고방식은 다음과 같습니다.

- Kernel code는 한 번 작성합니다.
- GPU는 같은 kernel을 많은 thread에서 실행합니다.
- 각 thread는 자신의 index를 이용해 서로 다른 data element를 처리합니다.

CUDA C++에서는 보통 `__global__` qualifier가 붙은 함수가 host에서 호출되어 device에서 실행되는 kernel입니다.

## 4. Thread, Block, Grid

CUDA는 실행 단위를 계층적으로 구성합니다.

- **Thread**: kernel code를 한 번 수행하는 worker
- **Block**: 여러 thread의 묶음
- **Grid**: 한 번의 kernel launch에 포함되는 여러 block의 묶음

```text
Grid
├── Block 0
│   ├── Thread 0
│   ├── Thread 1
│   └── ...
├── Block 1
│   └── ...
└── ...
```

같은 block의 thread는 shared memory를 이용해 협력할 수 있습니다.

원문은 block당 256 thread를 예로 사용합니다. NVIDIA 공식 문서에서 block당 최대 thread 수는 1024로 제시되며, 실제 최적 block size는 kernel의 register/shared-memory 사용량과 GPU architecture에 따라 달라집니다.

## 5. Host와 Device

CUDA 문맥에서 Host는 CPU와 host memory, Device는 GPU와 device memory를 뜻합니다.

Discrete GPU에서는 host와 device memory가 분리되어 있으므로 data 이동이 필요합니다. 이 이동에는 비용이 있으므로 workload가 너무 작으면 GPU 계산의 이득보다 transfer와 launch overhead가 더 클 수 있습니다.

## 6. 첫 예제: 1,000,000개 원소의 Vector Addition

원문은 길이 1,000,000인 배열 `a`, `b`를 더해 `c`를 만드는 예제를 사용합니다.

CPU에서는 한 loop가 모든 원소를 순서대로 처리합니다.

```cpp
void add_cpu(int n, const float* a, const float* b, float* c) {
    for (int i = 0; i < n; ++i) {
        c[i] = a[i] + b[i];
    }
}
```

GPU kernel에서는 각 thread가 하나의 index를 맡도록 바꿉니다.

```cpp
__global__ void add_gpu(int n, const float* a, const float* b, float* c) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}
```

CPU version에서는 loop가 `i`를 바꿔가며 진행하지만, GPU version에서는 각 thread가 자기 `i` 하나를 계산합니다.

## 7. Block 수 계산

원문의 조건은 다음과 같습니다.

- `n = 1,000,000`
- `threadsPerBlock = 256`

필요한 block 수는 ceiling division으로 구합니다.

```text
blocks = ceil(1,000,000 / 256)
       = 3,907
```

Integer arithmetic에서는 다음 식을 사용할 수 있습니다.

```cpp
int blocks = (n + threadsPerBlock - 1) / threadsPerBlock;
```

실제로 launch되는 thread 수는 다음과 같습니다.

```text
3,907 × 256 = 1,000,192
```

필요한 원소보다 192개 thread가 더 만들어지므로 `if (i < n)` 조건이 배열 범위를 보호합니다.

Kernel launch는 다음 형태입니다.

```cpp
add_gpu<<<blocks, threadsPerBlock>>>(n, d_a, d_b, d_c);
```

## 8. Memory 할당과 전송

전체 흐름은 다음과 같이 정리할 수 있습니다.

```cpp
float *d_a, *d_b, *d_c;

cudaMalloc(&d_a, n * sizeof(float));
cudaMalloc(&d_b, n * sizeof(float));
cudaMalloc(&d_c, n * sizeof(float));

cudaMemcpy(d_a, a, n * sizeof(float), cudaMemcpyHostToDevice);
cudaMemcpy(d_b, b, n * sizeof(float), cudaMemcpyHostToDevice);

add_gpu<<<blocks, threadsPerBlock>>>(n, d_a, d_b, d_c);

cudaMemcpy(c, d_c, n * sizeof(float), cudaMemcpyDeviceToHost);

cudaFree(d_a);
cudaFree(d_b);
cudaFree(d_c);
```

| 단계 | API | 역할 |
| --- | --- | --- |
| Device memory 확보 | `cudaMalloc` | GPU memory allocation |
| Host → Device | `cudaMemcpy` | input 전송 |
| 계산 | kernel launch | GPU 병렬 실행 |
| Device → Host | `cudaMemcpy` | 결과 회수 |
| 정리 | `cudaFree` | GPU memory 해제 |

CUDA source는 일반적으로 `.cu` 파일로 작성하고 NVIDIA `nvcc` toolchain으로 compile할 수 있습니다.

## 9. Thread가 자기 Data를 찾는 식

핵심 식은 다음과 같습니다.

```cpp
int i = blockIdx.x * blockDim.x + threadIdx.x;
```

- `threadIdx.x`: 현재 block 안에서 thread의 index
- `blockIdx.x`: grid 안에서 block의 index
- `blockDim.x`: block당 thread 수

따라서:

```text
global_index
= block_index × threads_per_block + thread_index_in_block
```

Block size가 256일 때:

| Block | Thread | 계산 | Global index |
| ---: | ---: | --- | ---: |
| 0 | 0 | `0 × 256 + 0` | 0 |
| 0 | 5 | `0 × 256 + 5` | 5 |
| 1 | 0 | `1 × 256 + 0` | 256 |
| 2 | 10 | `2 × 256 + 10` | 522 |

모든 thread가 같은 code를 실행하지만 서로 다른 global index를 얻기 때문에 서로 다른 data를 처리합니다.

## 10. 1D, 2D, 3D Index

앞 예제는 1차원 배열이므로 `.x`만 사용합니다. CUDA의 thread와 block은 1D뿐 아니라 2D, 3D로 구성할 수 있습니다.

Image나 matrix에서는 `.x`, `.y`를 이용해 row와 column을 mapping하는 방식이 자연스럽습니다. 핵심 원리는 각 thread가 자신의 좌표를 계산해 해당 data만 처리하는 것입니다.

## 11. Kernel이 GPU에서 실행되는 과정

GPU는 여러 Streaming Multiprocessor(SM)로 구성됩니다.

많은 block을 launch해도 모든 block이 한 순간에 동시에 실행되는 것은 아닙니다. GPU가 실행 가능한 block을 SM에 배치하고, resource가 비면 다음 block을 배치합니다.

Block 하나가 소비하는 thread, register, shared memory 양에 따라 한 SM에 동시에 resident할 수 있는 block 수가 달라집니다.

## 12. Warp와 Warp Divergence

NVIDIA CUDA programming model에서 thread는 **32개씩 warp**로 묶여 실행됩니다.

Block당 256 thread라면:

```text
256 / 32 = 8 warps
```

Warp 안의 thread가 서로 다른 branch를 선택하면 여러 execution path를 처리해야 하므로 효율이 떨어질 수 있습니다. 이를 warp divergence라고 합니다.

```cpp
if (condition) {
    path_a();
} else {
    path_b();
}
```

앞의 `if (i < n)`은 마지막 block 일부에만 영향을 주므로 전체 workload에서는 일반적으로 영향이 제한적입니다.

## 13. CUDA Memory 계층

원문은 세 가지 memory를 중심으로 설명합니다.

### Global Memory

- 큰 device memory 영역
- 모든 thread가 접근 가능
- capacity가 크지만 on-chip memory보다 access cost가 큼
- 앞 예제의 `d_a`, `d_b`, `d_c`가 위치

### Shared Memory

- 같은 block의 thread가 공유
- on-chip에 위치
- capacity가 제한적
- 같은 data를 여러 thread가 반복 사용할 때 효과적

### Registers

- 각 thread가 사용하는 빠른 storage
- index와 local scalar 등에 사용
- 수가 제한되어 있어 register 사용량은 occupancy에도 영향을 줄 수 있음

원문은 global memory가 shared memory보다 약 100배 느리다는 직관적 표현을 사용합니다. 이 비율은 모든 GPU와 access pattern에 적용되는 고정 수치가 아닙니다. 실제 차이는 architecture, cache, coalescing, access pattern 등에 따라 달라지므로 **shared memory가 data reuse에서 훨씬 유리할 수 있다는 방향성**으로 이해하는 것이 안전합니다.

## 14. Shared Memory를 이용한 Data Reuse

Matrix multiplication처럼 같은 input tile을 반복 사용하는 연산에서는 다음 방식이 효과적일 수 있습니다.

1. Global memory에서 tile을 읽습니다.
2. Shared memory에 저장합니다.
3. 같은 block의 여러 thread가 이를 재사용합니다.
4. 최종 결과를 global memory에 기록합니다.

NVIDIA Best Practices Guide도 shared memory가 redundant global memory access를 줄이고 access pattern을 개선하는 데 유용하다고 설명합니다.

단순 vector addition은 원소를 한 번씩만 사용하므로 shared memory의 이점이 크지 않을 수 있습니다.

## 15. CUDA Kernel과 AI

Deep learning과 LLM workload에는 다음 연산이 반복됩니다.

- matrix multiplication
- normalization
- activation
- attention 관련 tensor operation
- sampling 전후 연산

Framework 사용자는 직접 kernel을 작성하지 않아도 됩니다.

```python
y = torch.matmul(a, b)
```

같은 높은 수준의 API 아래에서 framework와 backend가 GPU implementation을 선택합니다. Operation과 환경에 따라 CUDA kernel, cuBLAS/cuBLASLt 같은 NVIDIA library 등이 사용될 수 있습니다.

즉 LLM이 token을 생성하는 과정 아래에는 많은 GPU kernel 실행이 연속적으로 존재합니다.

## 16. CUDA Kernel이 잘 맞는 경우

- 같은 operation을 많은 data에 적용할 때
- data element 사이의 dependency가 적을 때
- workload가 충분히 커서 transfer와 launch overhead를 상쇄할 때
- memory access pattern을 효율적으로 구성할 수 있을 때

대표적인 workload는 matrix multiplication, image processing, deep learning tensor operation, scientific simulation입니다.

## 17. 잘 맞지 않는 경우

### 작업이 너무 작을 때

소량의 data를 위해 GPU transfer와 kernel launch를 수행하면 CPU가 직접 처리하는 것보다 느릴 수 있습니다.

### 순차 dependency가 강할 때

앞 단계 결과가 반드시 있어야 다음 단계를 계산할 수 있으면 대규모 병렬화를 적용하기 어렵습니다.

### Branch가 지나치게 많을 때

같은 warp 안에서 thread가 자주 다른 path를 선택하면 divergence가 성능을 떨어뜨릴 수 있습니다.

### Device memory가 부족할 때

Data를 계속 host와 device 사이에서 옮겨야 하면 transfer가 bottleneck이 될 수 있습니다.

## 18. CPU와 GPU 비교

| 항목 | CPU | GPU |
| --- | --- | --- |
| 실행 자원 | 상대적으로 적은 수의 강력한 core | 대량 병렬 처리를 위한 많은 실행 자원 |
| 강점 | 복잡한 logic, branch, sequential task | 같은 계산을 많은 data에 적용 |
| AI에서 역할 | orchestration, preprocessing, control | matrix/tensor 연산 |
| Memory | host RAM 중심 | device memory와 transfer 고려 |
| 병렬화 | 제한된 thread 병렬성 | 대규모 data parallelism |

GPU가 항상 CPU보다 빠른 것은 아닙니다. **문제가 충분히 크고 병렬화 가능하며 memory movement 비용을 감당할 수 있을 때** GPU의 장점이 커집니다.

## 19. 전체 흐름

```text
Host data 준비
→ Device memory 할당
→ Host-to-Device copy
→ Grid/Block 크기 결정
→ Kernel launch
→ Thread별 index 계산
→ SM/warp에서 병렬 실행
→ Device-to-Host copy
→ Device memory 해제
```

## 20. 핵심 정리

- CUDA Kernel은 GPU에서 실행되는 함수이며 많은 thread가 같은 code를 병렬 수행합니다.
- Thread는 block으로, block은 grid로 구성됩니다.
- 각 thread는 `blockIdx`, `blockDim`, `threadIdx`를 이용해 자기 data index를 계산합니다.
- 원문의 1,000,000-element 예제에서 block당 256 thread를 쓰면 3,907 block, 총 1,000,192 thread가 launch됩니다.
- NVIDIA CUDA의 warp size는 32입니다.
- NVIDIA 문서에서 block당 최대 thread 수는 1024입니다.
- 성능은 arithmetic뿐 아니라 memory hierarchy, transfer, access pattern, divergence에 크게 영향을 받습니다.
- GPU는 모든 문제의 정답이 아니라 충분히 크고 병렬화 가능한 workload에서 강합니다.

## 참고 자료

- 원문: https://outcomeschool.com/blog/how-do-cuda-kernels-work
- NVIDIA CUDA Programming Guide: https://docs.nvidia.com/cuda/cuda-programming-guide/
- NVIDIA CUDA Best Practices Guide: https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/
