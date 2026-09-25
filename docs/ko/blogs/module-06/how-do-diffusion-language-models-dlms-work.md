# Diffusion Language Model(DLM)은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-do-diffusion-language-models-dlms-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문을 직접 확인해 masking noise, forward/reverse phase, confidence remasking, France 4-slot 예, autoregressive 비교를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. DLM의 핵심 아이디어

Diffusion Language Model은 일반적인 autoregressive LM처럼 왼쪽에서 오른쪽으로 token 하나씩 생성하지 않습니다.

원문의 직관:

> 전체 문장을 거칠고 불완전한 상태에서 시작해 여러 round 동안 동시에 고쳐 나간다.

즉:

    Autoregressive:
    token1 → token2 → token3 → ...

    Diffusion:
    [mask][mask][mask][mask]
      → 일부 채우기
      → 다시 추론/수정
      → 완성

## 2. 기존 Autoregressive 방식

일반 LLM:

1. next token 예측
2. token 확정
3. 그 token을 prefix에 추가
4. 다음 token 예측

문제:

- step t+1은 t가 끝나야 시작
- output 길이가 길수록 sequential decode step 증가
- 이미 확정한 앞 token을 자연스럽게 되돌리기 어려움

DLM은 이 sequential bottleneck을 다른 방식으로 풀려 합니다.

## 3. Diffusion 아이디어의 출발점

Image diffusion:

    clean image
      → noise 추가
      → 더 많은 noise
      → pure static

Training은 반대로:

    pure/noisy input
      → denoise
      → cleaner
      → clean image

Text는 pixel처럼 연속 noise를 단순 더할 수 없으므로 discrete noise 정의가 필요합니다.

## 4. Text에서 Noise란?

원문은 masking을 noise로 사용합니다.

Clean:

    The cat sat on the mat

조금 noise:

    The cat [?] on the mat

더 많이:

    The [?] [?] on [?] mat

Pure noise:

    [?] [?] [?] [?] [?] [?]

즉 hidden/masked token이 많을수록 noisy한 sentence입니다.

## 5. Forward Phase

Forward process는 training에서 clean sentence를 점점 mask합니다.

    clean x_0
      → partially masked x_t
      → fully masked x_T

이 단계 자체는 learned intelligence가 아니라 training example을 만드는 corruption process입니다.

Model이 배워야 할 것은 reverse입니다.

## 6. Reverse Phase

Model은 masked sentence의 여러 위치를 동시에 예측합니다.

    [?] [?] [?] [?]
      → predictions + confidence
      → confident token 유지
      → uncertain token 다시 mask
      → repeat

각 round에서 확실한 위치가 anchor가 되고 다음 round가 더 쉬워집니다.

## 7. 원문의 5-slot 예

원문은 다음 refinement 예를 사용합니다.

    Round 1:
    [?] [?] [?] [?] [?]

    Round 2:
    The [?] [?] is [?]

    Round 3:
    The food [?] is good

    Round 4:
    The food here is good

쉬운/high-confidence token을 먼저 lock하고 애매한 위치를 다시 추론합니다.

## 8. France 예 — 전체 흐름

질문:

    What is the capital of France?

4개의 answer slots:

    [?] [?] [?] [?]

### Round 1

모든 slot을 동시에 guess:

    The is capital Paris

Confidence가 높은 The와 Paris만 유지:

    The [?] [?] Paris

### Round 2

남은 두 위치를 다시 추론:

    The capital is Paris

두 round 만에 완료됩니다.

원문의 핵심은 **4개 word를 4번 sequentially 생성하는 대신 각 round에서 모든 position을 병렬 추론**한다는 점입니다.

## 9. Confidence Threshold

원문의 simplified algorithm:

    sentence = all masks

    for each round:
        guesses, confidence = model.predict_all(sentence)

        for each position:
            if confidence > threshold:
                keep guess
            else:
                mask again

        if no masks:
            stop

원문은 threshold 예로 90%처럼 “충분히 확실한 token만 lock”하는 직관을 설명합니다.

## 10. Earlier Token을 수정할 수 있다

Autoregressive generation은 이미 생성한 token이 다음 prefix가 되므로 자연스럽게 rollback하기 어렵습니다.

DLM은 어떤 위치를 다시 mask해 다음 round에 재예측할 수 있습니다.

따라서 global consistency를 반복 개선할 수 있습니다.

## 11. Parallelism

Autoregressive:

    number of decode steps ≈ output token count

DLM:

    number of denoising rounds

이론적으로 한 round에서 여러 token을 동시에 결정할 수 있어 output length와 strictly 1:1인 sequential dependency를 줄입니다.

실제 wall-clock advantage는 model size, number of rounds, hardware utilization에 따라 달라집니다.

## 12. Whole-Sentence View

각 round에서 전체 partially-completed sequence를 보기 때문에:

- 뒤쪽 token이 앞쪽 예측에 영향
- 앞 token도 다시 수정 가능
- infilling과 constrained editing에 자연스러움

이라는 특성이 있습니다.

## 13. Autoregressive vs DLM

원문 비교:

| Feature | Autoregressive | DLM |
| --- | --- | --- |
| Writing order | left-to-right | whole sequence refinement |
| Parallel work | 제한적 | multiple positions |
| Steps | token 수에 비례 | denoising rounds |
| Earlier token revision | 직접적으론 어려움 | re-mask 가능 |
| Length | EOS까지 자연 생성 | 일부 방식은 length 사전 설정 필요 |

## 14. DLM도 Transformer를 쓸 수 있다

DLM의 차이는 “Transformer냐 아니냐”가 아닙니다.

원문은 DLM도 Transformer-based architecture를 사용할 수 있다고 설명합니다.

차이는 generation/training objective:

- AR: next-token causal prediction
- DLM: masked/noisy sequence denoising

입니다.

## 15. 장점

원문:

### Parallel Speed Potential

한 round에 여러 token을 결정할 수 있습니다.

### Self-Correction

낮은 confidence 위치를 다시 mask해 수정합니다.

### Global View

전체 sequence를 각 round에서 함께 봅니다.

### Natural Infilling

부분 sentence/code의 빈칸 completion에 잘 맞습니다.

## 16. 한계

### Round 수 선택

너무 적으면 incomplete/incorrect, 너무 많으면 speed advantage가 줄어듭니다.

### Length

일부 DLM은 output slot length를 미리 정해야 해 open-ended generation이 awkward할 수 있습니다.

### Confidence/Remasking Policy

어떤 token을 lock하고 다시 mask할지 policy가 품질과 latency를 좌우합니다.

### Ecosystem Maturity

Autoregressive LLM serving stack만큼 표준화되지 않았습니다.

## 17. 현재 기술을 볼 때의 질문

새 DLM을 평가할 때:

- discrete diffusion objective가 무엇인가?
- mask schedule은?
- number of rounds는?
- adaptive early stop 가능한가?
- output length를 어떻게 정하는가?
- KV cache와 유사한 reuse가 가능한가?
- quality per wall-clock latency는?
- coding/math/long-form에서 AR 대비 어떠한가?

를 확인해야 합니다.

## 핵심 정리

- DLM은 full/partial masked text에서 시작해 여러 round로 denoise합니다.
- Text noise는 원문에서 token masking으로 설명됩니다.
- Forward는 training corruption, reverse가 learned denoising입니다.
- Confidence가 높은 token을 유지하고 낮은 token은 다시 mask합니다.
- 여러 position을 병렬로 고칠 수 있어 autoregressive sequential decode와 다른 latency trade-off를 만듭니다.
- Transformer를 써도 generation objective가 diffusion이면 DLM입니다.

## 원문

- https://outcomeschool.com/blog/how-do-diffusion-language-models-dlms-work
