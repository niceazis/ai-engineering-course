# Medusa란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/decoding-medusa  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 현재 Outcome School 원문 본문은 웹 캐시에서 직접 열리지 않았습니다. 공식 Module 12 목차와 Medusa 원 논문/PMLR 공개 내용을 교차검증해 작성하며, 원문 고유 설명과 논문 수치를 구분합니다.

## 1. Draft Model 없는 Speculation

일반 speculative decoding:

    separate draft model
      → target model verification

Medusa:

    target backbone
      + extra decoding heads

하나의 backbone hidden state에서 여러 미래 위치의 token을 예측합니다.

## 2. Multiple Decoding Heads

기본 LM head는 next token을 예측합니다.

Medusa는 추가 head를 붙여:

    head 1 → t+1
    head 2 → t+2
    head 3 → t+3
    ...

처럼 미래 token 후보를 동시에 만듭니다.

실제 각 head는 여러 top candidate를 제안할 수 있습니다.

## 3. Candidate Tree

각 head의 후보를 조합하면 여러 continuation path가 생깁니다.

    token A
      ├─ B
      │  ├─ C
      │  └─ D
      └─ E ...

모든 조합을 독립 forward하면 비싸므로 Tree Attention으로 여러 branch를 한 번에 검증합니다.

## 4. Tree Attention

Candidate token들이 서로 다른 branch의 미래 정보를 보지 않도록 custom causal mask를 사용하면서 target backbone을 병렬 실행합니다.

그 뒤 가장 긴 acceptable prefix를 선택합니다.

## 5. Medusa-1

원 논문:

- backbone frozen
- extra Medusa heads만 학습
- 기존 model capability 유지에 유리
- 별도 draft model 불필요

PMLR 공개 결과는 **2.2× 이상 speedup**을 보고합니다.

## 6. Medusa-2

Backbone도 함께 fine-tune해 Medusa head의 future prediction 능력을 높입니다.

더 높은 speedup을 얻을 수 있지만 original capability 보존을 위한 training recipe가 필요합니다.

공개 논문은 약 2.3~2.8× 수준의 결과를 보고합니다(버전/평가표에 따라 수치 표기가 다를 수 있음).

## 7. Speculative Decoding과 비교

| 항목 | Draft Model | Medusa |
| --- | --- | --- |
| Drafter | 별도 model | extra heads |
| Memory | second model | head overhead |
| Training | matching draft 필요 | heads fine-tune |
| Verification | target | same backbone/tree |
| Distribution | exact scheme 가능 | acceptance scheme에 따라 |

## 8. 장점

- 별도 draft model 관리 없음
- parameter-efficient adaptation 가능
- single-model serving stack에 통합 쉬움
- batch=1/local serving에서도 유용

## 9. 한계

- extra head training 필요
- candidate tree size 증가 시 verify cost 증가
- sampling acceptance 설계
- 모든 model/runtime에서 자동 지원되는 것은 아님

## 핵심 정리

- Medusa는 target LLM에 여러 future-token head를 붙여 draft model을 대체합니다.
- Candidate continuation을 tree로 만들고 Tree Attention으로 한 번에 검증합니다.
- Medusa-1은 backbone freeze, Medusa-2는 backbone까지 함께 fine-tune합니다.
- 공개 원 논문은 2× 이상 inference speedup을 보고합니다.
- Outcome School 원문 본문은 직접 확인하지 못해 논문 기반 수치는 명시적으로 구분했습니다.

## 원문

- https://outcomeschool.com/blog/decoding-medusa
