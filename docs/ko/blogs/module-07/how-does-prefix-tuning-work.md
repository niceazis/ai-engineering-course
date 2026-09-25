# Prefix Tuning은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-prefix-tuning-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 2026-08-24 글의 공개 사본과 공식 뉴스레터를 확인해 prefix가 실제 text가 아니라 layer별 learnable K/V라는 점, reparameterization, Prompt Tuning·LoRA 비교를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Prefix Tuning의 정의

Prefix Tuning은 base LLM을 전부 freeze한 채, 각 Transformer layer가 참고할 **작은 learnable prefix vectors**만 학습하는 parameter-efficient fine-tuning 방법입니다.

핵심:

> Prefix는 사용자에게 보이는 실제 단어가 아니라 모델 내부 attention에 들어가는 학습 가능한 숫자입니다.

## 2. 왜 필요한가

Task가 10개이고 full fine-tuning을 사용하면:

    task 1 → full model copy
    task 2 → full model copy
    ...
    task 10 → full model copy

가 될 수 있습니다.

Prefix Tuning:

    one frozen base model
      + prefix_task1
      + prefix_task2
      + ...
      + prefix_task10

으로 바꿉니다.

Task별 추가 parameter는 보통 base model의 매우 작은 비율입니다.

## 3. Prefix는 실제 Text가 아니다

Prompt engineering:

    "다음 문서를 요약하세요:"

처럼 tokenized text를 입력 앞에 붙입니다.

Prefix Tuning:

    [learned vectors P1 P2 ... Pm]

를 attention 내부에 넣습니다.

Tokenizer vocabulary에 존재하는 word/token일 필요가 없습니다.

## 4. Attention 관점

일반 self-attention:

    Q = XWq
    K = XWk
    V = XWv

Prefix Tuning에서는 layer마다 추가 K/V를 붙입니다.

    K' = [K_prefix ; K_input]
    V' = [V_prefix ; V_input]

Query는 실제 input token에서 옵니다.

    Q = Q_input

따라서 실제 token이 attention할 때 learned prefix K/V도 함께 볼 수 있습니다.

## 5. Layer마다 Prefix가 들어간다

Prompt Tuning은 주로 input embedding layer 앞에 learnable virtual token을 붙입니다.

Prefix Tuning은 **각 Transformer layer의 attention K/V space**에 prefix state를 제공합니다.

이 차이가 중요한 이유는 task signal이 모든 layer에 직접 주입되기 때문입니다.

## 6. Training 흐름

1. Pretrained model freeze
2. Prefix parameter 초기화
3. Input을 frozen model에 전달
4. 각 layer에서 prefix K/V 추가
5. Target response loss 계산
6. Gradient는 prefix에만 전달
7. 반복

도식:

    learned prefix K/V
          ↓
    frozen Transformer layer
          ↓
    output
          ↓
    loss
          ↓
    update prefix only

## 7. Reparameterization

원문은 prefix vector를 직접 학습하면 optimization이 불안정할 수 있어 original paper가 작은 network를 통한 reparameterization을 사용했다고 설명합니다.

개념:

    small learned embedding
      → small MLP
      → actual prefix K/V

Training 후에는 MLP를 버리고 생성된 final prefix만 저장할 수 있습니다.

PEFT library의 prefix_projection 옵션이 이 개념과 연결됩니다.

## 8. Prefix Size

Base model이 수십억 parameter여도 prefix는 훨씬 작습니다.

Prefix length m, layers L, K/V dimension d라면 대략 parameter scale은:

    O(L × m × d × 2)

입니다.

Full model parameter와 비교하면 1% 미만이 될 수 있습니다.

## 9. Prefix Length Trade-off

짧은 prefix:

- 저장/학습 cost 작음
- task capacity 낮을 수 있음

긴 prefix:

- 더 많은 task information
- attention input 길이 증가
- parameter 증가

Task별 validation으로 결정해야 합니다.

## 10. Prefix Tuning vs Full Fine-Tuning

| 항목 | Full FT | Prefix Tuning |
| --- | --- | --- |
| Base weight | update | frozen |
| Task별 저장 | full checkpoint | small prefix |
| Training memory | 높음 | 낮음 |
| Capacity | 큼 | prefix에 제한 |
| Multi-task switching | 무거움 | prefix 교체 |

## 11. Prefix Tuning vs Prompt Tuning

### Prompt Tuning

- input embedding 앞에 learnable virtual token
- 주로 첫 layer input에서 시작

### Prefix Tuning

- 모든/여러 Transformer layer의 K/V에 prefix
- deeper control

따라서 Prefix Tuning이 parameter는 조금 더 쓰지만 더 강한 adaptation을 제공할 수 있습니다.

## 12. Prefix Tuning vs LoRA

LoRA:

    weight update ΔW = BA

즉 linear weight path를 수정합니다.

Prefix Tuning:

    attention context에 learned K/V 추가

즉 weight 자체는 건드리지 않고 attention에서 참고하는 memory-like vectors를 추가합니다.

어느 것이 더 좋은지는 model/task에 따라 다릅니다.

## 13. 장점

- Base model immutable
- Task별 adapter 작음
- 여러 task 공유 serving에 적합
- catastrophic forgetting이 적음
- full fine-tuning보다 적은 GPU memory

## 14. 한계

- Full FT보다 adaptation capacity 제한
- Prefix가 attention context 일부를 차지
- 일부 task/model에서 LoRA보다 성능이 낮을 수 있음
- task마다 prefix artifact 관리 필요

## 15. 실제 활용 Pattern

한 base model에:

    prefix_legal
    prefix_support
    prefix_summary
    prefix_sql

을 저장합니다.

Request routing 결과에 따라 적절한 prefix를 선택합니다.

이렇게 하면 여러 specialized behavior를 하나의 frozen model 위에 운영할 수 있습니다.

## 핵심 정리

- Prefix Tuning은 model weight를 freeze하고 learnable prefix만 학습합니다.
- Prefix는 text가 아니라 attention에 들어가는 numeric K/V vectors입니다.
- Query는 실제 token에서 오고, K/V에 prefix가 추가됩니다.
- Original method는 안정성을 위해 reparameterization MLP를 사용합니다.
- Prompt Tuning은 input embedding 중심, Prefix Tuning은 layer별 attention K/V 중심입니다.
- LoRA는 weight update, Prefix Tuning은 attention context adaptation이라는 차이가 핵심입니다.

## 원문

- https://outcomeschool.com/blog/how-does-prefix-tuning-work
