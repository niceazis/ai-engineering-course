# Sliding Window Attention은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-sliding-window-attention-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문 전체 번역이 아닌 독립적인 한국어 상세 해설입니다. 현재 Outcome School 원문 본문은 웹 캐시에서 직접 열리지 않았습니다. Outcome School 공식 Module 5 레슨 순서와 Sliding Window Attention의 공개 아키텍처 자료를 교차검증해 작성하며, 원문에서 직접 확인하지 못한 수치·문장을 원문 내용이라고 단정하지 않습니다.

## 1. Full Attention의 기본 비용

일반 causal self-attention에서 token i는 자신보다 앞선 모든 token을 볼 수 있습니다.

sequence length를 N이라고 하면 attention score matrix의 크기는 대략:

    N × N

입니다.

Causal mask 때문에 미래 절반은 실제 사용하지 않더라도, dense implementation의 비용은 sequence length에 대해 quadratic하게 증가합니다.

Long context에서는 이 비용이:

- training memory
- prefill compute
- attention kernel latency

를 크게 만듭니다.

## 2. Sliding Window Attention의 핵심

Sliding Window Attention(SWA)은 각 token이 전체 과거가 아니라 **가까운 W개 token만 보게** 합니다.

예:

    window size W = 4

현재 token t가 볼 수 있는 위치:

    t-3, t-2, t-1, t

과거가 더 길어도 window 밖 token에는 직접 attention을 하지 않습니다.

## 3. 작은 단계별 예

token sequence:

    [A B C D E F G H]

window size를 4로 두면:

    A → A
    B → A B
    C → A B C
    D → A B C D
    E → B C D E
    F → C D E F
    G → D E F G
    H → E F G H

window가 sequence를 따라 오른쪽으로 이동합니다.

그래서 Sliding Window라는 이름이 붙습니다.

## 4. 계산 복잡도

Full attention:

    O(N^2)

Window size W가 N보다 훨씬 작고 고정이라면:

    O(N × W)

수준으로 attention pair 수를 제한할 수 있습니다.

예를 들어:

    N = 100,000
    W = 4,096

이면 각 token이 최대 100,000개 과거를 보는 대신 약 4,096개 local token만 봅니다.

정확한 GPU 속도 향상은 kernel, sparsity representation, batch 구성에 따라 달라집니다.

## 5. KV Cache와의 관계

SWA를 decode 단계까지 local-only로 적용하면 오래된 K/V를 계속 유지할 필요가 줄어들 수 있습니다.

단순 local attention에서는 최근 W token의 K/V만 유지하는 ring buffer 방식도 가능합니다.

하지만 실제 모델은:

- 일부 layer는 full/global attention
- 일부 layer는 sliding attention
- sink/global token을 별도 유지

같은 hybrid design을 사용할 수 있으므로 모델별 cache 정책을 확인해야 합니다.

## 6. 먼 정보는 어떻게 전달되는가

한 layer에서 직접 볼 수 있는 범위가 W라도 layer를 여러 번 쌓으면 정보가 단계적으로 전파될 수 있습니다.

직관:

    Layer 1: 가까운 이웃 W개
    Layer 2: 이웃이 이미 받은 더 먼 정보 포함
    Layer 3: receptive field가 더 확장

따라서 local attention만으로도 깊은 network에서는 직접 window보다 더 먼 정보가 간접적으로 전달될 수 있습니다.

다만 이것은 모든 long-range fact가 full attention과 동일하게 보존된다는 뜻은 아닙니다.

## 7. Full Attention과 비교

| 항목 | Full Attention | Sliding Window Attention |
| --- | --- | --- |
| 직접 참조 범위 | 모든 과거 token | 최근 W token |
| attention pair 수 | O(N^2) | O(NW) |
| long-range 직접 연결 | 강함 | 제한적 |
| 긴 context 비용 | 큼 | 상대적으로 작음 |
| 구현 | dense kernel에 적합 | local/sparse kernel 필요 |

## 8. Locality가 잘 맞는 이유

언어에는 local dependency가 많습니다.

예:

- 바로 앞 명사와 동사
- 가까운 구두점
- 현재 문장의 문법 구조
- 최근 대화 turn

이런 관계는 작은 window에서도 충분히 잡힐 수 있습니다.

따라서 모든 layer에서 모든 token pair를 계산하는 것이 꼭 효율적인 것은 아닙니다.

## 9. Long-Range Dependency 문제

반대로 다음에는 local window만으로 부족할 수 있습니다.

- 문서 맨 앞 정의를 맨 끝에서 다시 사용
- 수만 token 이전의 identifier 참조
- 장기 agent trajectory의 초기 constraint
- 긴 codebase의 distant dependency

이 때문에 modern model은 SWA와 global attention을 섞거나 retrieval/context engineering을 함께 사용합니다.

## 10. Hybrid Attention

실용적인 설계 중 하나:

    Layer 1  → Sliding Window
    Layer 2  → Sliding Window
    Layer 3  → Full/Global
    Layer 4  → Sliding Window
    ...

Local layer가 대부분의 계산을 줄이고, 간헐적 global layer가 먼 위치를 직접 연결합니다.

정확한 주기와 window size는 model architecture에 따라 다릅니다.

## 11. Causal Mask와 같이 사용

Decoder LLM에서는 window 안에서도 미래 token을 보면 안 됩니다.

즉 mask 조건은 두 개입니다.

    j <= i              // causal
    j >= i - W + 1      // local window

두 조건을 모두 만족하는 위치만 attention 대상으로 남깁니다.

## 12. Streaming과 연결

Continuous streaming에서는 context가 계속 늘어납니다.

Full attention + full KV cache는 대화 길이에 따라 memory가 계속 증가할 수 있습니다.

SWA는 최근 window만 유지하는 구조와 잘 결합돼 **bounded memory**를 만들 수 있습니다.

그러나 초기 sink token을 무작정 제거하면 품질이 무너지는 현상이 있어 다음 Attention Sink 레슨과 연결됩니다.

## 13. 실무에서 볼 지표

SWA를 선택할 때 단순 benchmark score만 보면 부족합니다.

확인할 것:

- window size
- max context
- global layer 비율
- KV cache bytes/request
- TTFT
- decode tokens/s
- long-range retrieval accuracy
- Needle-in-a-Haystack 위치별 성능

## 14. 장점과 Trade-off

### 장점

- 긴 sequence attention compute 감소
- memory 사용 감소 가능
- local dependency 중심 task에서 효율적
- streaming/bounded-cache 설계와 결합 가능

### Trade-off

- 먼 정보에 대한 직접 attention 제한
- sparse/local kernel 구현 복잡성
- window size가 너무 작으면 품질 저하
- 실제 long-context 품질은 hybrid architecture와 training에 크게 의존

## 핵심 정리

- Sliding Window Attention은 각 token이 최근 W개 위치만 직접 봅니다.
- Dense full attention의 O(N^2)을 O(NW) 수준으로 줄일 수 있습니다.
- 여러 layer를 거치며 정보가 간접적으로 더 멀리 전파될 수 있지만 full attention과 동일하지 않습니다.
- Long-range 품질을 위해 global layer, sink token, retrieval 같은 기법과 결합될 수 있습니다.
- 원문 본문을 직접 열지 못했으므로 특정 Outcome School 수치라고 확인되지 않은 값은 설명용 예로만 사용했습니다.

## 원문

- https://outcomeschool.com/blog/how-does-sliding-window-attention-work
