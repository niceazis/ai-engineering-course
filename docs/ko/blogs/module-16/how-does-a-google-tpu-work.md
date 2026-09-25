# Google TPU는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-a-google-tpu-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-06-28 공개 원문을 직접 확인해 TPU의 목적, matrix multiply, (2×5)+(3×6)+(4×7)=56 예제, MXU와 Systolic Array의 data flow를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. TPU란?

TPU는 Google이 machine learning 연산을 위해 설계한 Tensor Processing Unit입니다.

CPU처럼 범용 작업을 잘하기보다 tensor와 matrix math를 매우 효율적으로 처리하도록 특화됐습니다.

## 2. Google이 TPU를 만든 이유

원문은 2013년 무렵 Google이 voice search, photo search, translation 등 ML workload 증가로 data-center compute demand가 급격히 늘어날 것을 우려했다고 설명합니다.

범용 CPU/GPU를 계속 늘리는 대신 ML에 가장 많이 쓰는 연산을 훨씬 빠르고 전력 효율적으로 실행하는 전용 chip을 설계한 것입니다.

## 3. CPU, GPU, TPU

### CPU

- flexible
- strong control flow
- 적은 수의 강한 core

### GPU

- many parallel cores
- 범용 parallel compute
- ML에도 매우 강함

### TPU

- flexibility를 더 줄이고
- matrix multiply와 MAC에 더 특화

전용 hardware일수록 특정 workload에는 효율이 높지만 범용성은 낮아집니다.

## 4. 가장 중요한 연산

원문 예:

    inputs  = [2, 3, 4]
    weights = [5, 6, 7]

계산:

    (2 × 5)
    + (3 × 6)
    + (4 × 7)

    = 10 + 18 + 28
    = 56

이 pattern을 MAC, Multiply-and-Accumulate라고 볼 수 있습니다.

Neural network는 이런 연산을 billions of times 반복합니다.

## 5. MXU

TPU의 핵심 matrix engine은 MXU, Matrix Multiply Unit입니다.

MXU 안에는 많은 작은 MAC unit이 grid로 배치된 Systolic Array가 있습니다.

## 6. Systolic Array

원문 핵심 data flow:

- weight는 calculator에 배치
- input은 왼쪽에서 오른쪽으로 이동
- running total은 위에서 아래로 이동

각 cell은:

    new_total
      = input × weight
        + incoming_total

을 수행합니다.

## 7. Data Reuse가 핵심

보통 processor가 매 계산마다 memory에서 operand를 다시 가져오면 energy와 시간이 많이 듭니다.

Systolic Array에서는 data가 neighbor cell로 흘러가며 여러 번 재사용됩니다.

즉 compute 가까이 data를 유지해 memory traffic을 줄입니다.

## 8. 원문의 전체 계산 흐름

1. Host computer가 model/data 준비
2. Weight/input을 TPU memory로 전송
3. Weight를 MXU/Systolic Array에 공급
4. Input이 array를 따라 흐름
5. 각 cell이 MAC 수행
6. Accumulated result가 아래쪽으로 출력
7. 다음 neural-network operation으로 전달

## 9. 왜 빠르고 전력 효율적인가

- matrix multiply 전용 구조
- control overhead 감소
- 높은 data reuse
- predictable data flow
- specialized numeric formats

때문입니다.

## 10. TPU Pod

큰 model 학습에서는 여러 TPU를 고속 network로 연결해 하나의 cluster처럼 사용합니다.

GPU cluster와 마찬가지로 model partition, data parallel, collective communication이 중요합니다.

## 11. 한계

- Google ecosystem/cloud 의존성
- 범용 GPU보다 flexible하지 않음
- workload/operator compatibility 중요
- tooling/debugging 차이

모든 ML workload에서 TPU가 GPU보다 빠르다고 일반화하면 안 됩니다.

## 핵심 정리

- TPU는 ML matrix math에 특화된 Google accelerator입니다.
- 원문 예의 MAC 계산은 (2×5)+(3×6)+(4×7)=56입니다.
- TPU 핵심은 MXU 안의 Systolic Array입니다.
- Input은 가로, accumulated result는 세로 방향으로 흐르며 data를 재사용합니다.
- 범용성 일부를 포기하고 speed와 power efficiency를 얻는 구조입니다.

## 원문

- https://outcomeschool.com/blog/how-does-a-google-tpu-work
