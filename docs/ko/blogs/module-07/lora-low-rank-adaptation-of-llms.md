# LoRA(Low-Rank Adaptation)란 무엇이며 LLM을 어떻게 파인튜닝하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/lora-low-rank-adaptation-of-llms  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-04-24 공개 원문을 직접 확인해 ΔW=BA, 초기화, scaling, rank, Transformer 적용 위치와 merge 과정을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. LoRA가 해결하는 문제

Full fine-tuning은 weight matrix W 전체를 업데이트합니다.

큰 LLM에서는:

- gradient
- optimizer state
- updated weight
- activation

을 저장해야 하므로 GPU memory와 checkpoint storage가 큽니다.

LoRA는 다음 가정에서 출발합니다.

> 특정 task에 맞게 필요한 weight 변화 ΔW는 full matrix보다 훨씬 낮은 rank로 근사할 수 있다.

## 2. 핵심 수식

원래 linear layer:

    h = W x

Fine-tuning 후:

    h = (W + ΔW) x

LoRA는:

    ΔW = B A

로 둡니다.

따라서:

    h = W x + (B A) x

Base W는 freeze하고 A, B만 학습합니다.

## 3. 왜 Low-Rank인가

W shape이:

    d_out × d_in

일 때 full ΔW parameter 수:

    d_out × d_in

LoRA:

    A: r × d_in
    B: d_out × r

parameter 수:

    r(d_in + d_out)

r이 d보다 훨씬 작으면 매우 큰 절감이 생깁니다.

## 4. 수치 예

W가 4096×4096이라고 합시다.

Full update:

    4096 × 4096
    = 16,777,216 parameters

LoRA rank r=8:

    A = 8 × 4096
    B = 4096 × 8

합계:

    65,536 parameters

Full update 대비 약 256배 작습니다.

정확한 전체 절감률은 LoRA를 어느 layer에 적용하는지에 따라 달라집니다.

## 5. 초기화

원문:

- A: 작은 random Gaussian
- B: 0

따라서 시작 시:

    B A = 0

이고 model output은 원래 base model과 정확히 같습니다.

Training이 진행되면서 B가 변해 adapter effect가 생깁니다.

## 6. Scaling

원문 forward:

    h = W x + (alpha / r) * (B A) x

alpha는 adapter 영향의 scale입니다.

원문은 흔한 선택 예로:

    alpha = 2r

을 언급합니다.

하지만 실제 optimal alpha/rank는 task와 implementation에 따라 튜닝합니다.

## 7. Rank r

Rank는 LoRA의 가장 중요한 hyperparameter 중 하나입니다.

원문 권장 예:

    r = 8 ~ 64

작은 r:

- trainable parameters 적음
- memory/compute 적음
- adaptation capacity 낮음

큰 r:

- 더 복잡한 update 표현
- cost 증가

무조건 rank를 키운다고 성능이 계속 증가하지는 않습니다.

## 8. Transformer에서 어디에 붙이는가

대표적으로 attention projection에 적용합니다.

- Wq
- Wk
- Wv
- Wo

또 FFN projection에도 적용할 수 있습니다.

실전에서는 Q/V만 적용하거나 모든 linear layer에 적용하는 등 설정이 다양합니다.

Parameter budget과 task 성능을 함께 실험해야 합니다.

## 9. Training 흐름

1. Pretrained model load
2. Base parameters freeze
3. Target modules에 LoRA A/B 삽입
4. Forward:
   - base path Wx
   - adapter path BAx
5. 두 path 합산
6. Loss 계산
7. Backprop은 A/B만 update
8. Adapter checkpoint 저장

## 10. Memory가 줄어드는 이유

Full FT는 모든 parameter에 gradient/optimizer state가 필요합니다.

LoRA에서는 trainable parameter가 극히 적으므로:

- gradient memory
- optimizer state
- checkpoint size

가 크게 줄어듭니다.

Base weight forward는 여전히 필요하므로 inference/training 중 base model memory 자체가 사라지는 것은 아닙니다.

## 11. Merge

Training 후:

    W_merged = W + (alpha/r) BA

로 합칠 수 있습니다.

Merge하면 inference에서는 adapter branch를 따로 계산하지 않아도 됩니다.

장점:

- 추가 runtime latency 없음

단점:

- 여러 adapter를 runtime에서 쉽게 swap하려면 unmerged가 편리
- merged checkpoint마다 full model copy가 생길 수 있음

## 12. Adapter Swapping

Base model 하나:

    W

Task별:

    A_customer, B_customer
    A_code, B_code
    A_summary, B_summary

만 저장하면 됩니다.

같은 base model을 유지하면서 작은 adapter만 교체합니다.

Multi-tenant serving에서 특히 유용합니다.

## 13. LoRA vs Full Fine-Tuning

| 항목 | Full FT | LoRA |
| --- | --- | --- |
| Update | 모든 weight | A/B adapter |
| GPU memory | 매우 큼 | 훨씬 작음 |
| Checkpoint | full model | small adapter |
| Capacity | 최대 | rank에 제한 |
| Forgetting | 상대적으로 큼 | base 보존에 유리 |
| Serving | full checkpoint | merge 또는 adapter swap |

## 14. QLoRA와 연결

QLoRA는 base model을 4-bit 등으로 quantize해 memory를 더 줄이고 LoRA adapter를 학습하는 방식입니다.

개념:

    quantized frozen base
      + trainable LoRA

LoRA와 quantization의 장점을 결합합니다.

## 15. 흔한 실패

### Rank 너무 작음

Task 변화가 복잡하면 underfit할 수 있습니다.

### Target module 선택이 부적절

Q/V만으로 충분한 task가 있는 반면 FFN까지 필요한 task도 있습니다.

### Learning rate 과다

Trainable parameter가 적어도 overfit/instability가 가능합니다.

### Base mismatch

Task에 기본 capability가 없는 model에 LoRA만 붙인다고 모든 새 능력이 생기지는 않습니다.

## 핵심 정리

- LoRA는 ΔW를 low-rank product BA로 표현합니다.
- Base W는 freeze하고 A/B만 학습합니다.
- 원문은 A random, B zero 초기화와 alpha/r scaling을 설명합니다.
- rank 8~64가 흔한 실용 범위 예입니다.
- Trainable parameters를 100~1000배 이상 줄일 수 있습니다.
- Training 후 merge하거나 adapter swapping 방식으로 유지할 수 있습니다.
- LoRA는 Full FT보다 훨씬 저렴하지만 adaptation capacity가 rank와 target modules에 제한됩니다.

## 원문

- https://outcomeschool.com/blog/lora-low-rank-adaptation-of-llms
