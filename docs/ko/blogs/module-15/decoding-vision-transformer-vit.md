# Vision Transformer(ViT)란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/decoding-vision-transformer-vit  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-04-15 공개 원문을 직접 확인해 224×224 이미지, 16×16 patch, 196 token, 768-dimensional patch vector, CLS token과 position embedding의 흐름을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. 큰 그림

Vision Transformer(ViT)는 이미지를 CNN의 convolution hierarchy 대신 **작은 patch로 나누고 각 patch를 token처럼 Transformer에 넣는 방식**입니다.

전체 흐름:

    image
      → patches
      → patch embeddings
      → + CLS token
      → + positional embeddings
      → Transformer encoder
      → CLS representation
      → classification head

## 2. Step 1 — Image를 Patch로 나누기

원문 예:

    image = 224 × 224 pixels
    patch = 16 × 16 pixels

가로 patch 수:

    224 / 16 = 14

세로도 14이므로 총 patch:

    14 × 14 = 196

즉 하나의 이미지를 **196개의 visual token**으로 바꿉니다.

## 3. Patch 하나의 크기

RGB 이미지라면 한 patch에는:

    16 × 16 × 3
    = 768 values

가 있습니다.

Patch를 flatten하면 768-dimensional vector가 됩니다.

## 4. Step 2 — Patch Embedding

Flattened patch를 learnable linear projection에 통과시켜 Transformer hidden dimension으로 바꿉니다.

ViT-Base 예에서는 input patch vector도 768, hidden dimension도 768이라 shape가 같을 수 있지만 projection weight는 여전히 학습됩니다.

## 5. Convolution으로도 구현 가능

원문은 patch extraction + projection을 한 번의 convolution으로 구현할 수 있다고 설명합니다.

    kernel_size = 16
    stride = 16

이면 서로 겹치지 않는 16×16 영역마다 output embedding을 만들 수 있습니다.

## 6. Step 3 — CLS Token

196 patch token 앞에 하나의 learnable CLS token을 추가합니다.

    [CLS], P1, P2, ..., P196

총 sequence length:

    197

마지막 Transformer layer의 CLS representation을 image 전체의 summary vector처럼 사용해 classification head에 넣습니다.

## 7. Step 4 — Position Embedding

Transformer는 token 순서를 본질적으로 알지 못합니다.

이미지에서는 patch 위치가 중요하므로 positional embedding을 patch embedding에 더합니다.

## 8. Step 5 — Transformer Encoder

한 block의 기본 흐름:

1. LayerNorm
2. Multi-Head Self-Attention
3. Residual
4. LayerNorm
5. MLP/Feed-Forward
6. Residual

Self-Attention을 통해 한 patch가 이미지 내 다른 patch와 관계를 학습할 수 있습니다.

## 9. Global Interaction

고양이 이미지에서 귀 patch, 눈 patch, 몸 patch가 멀리 떨어져 있어도 attention으로 직접 연결될 수 있습니다.

CNN은 local kernel을 여러 layer 쌓아 receptive field를 넓히지만 ViT는 attention에서 global interaction을 직접 만들 수 있습니다.

## 10. Step 6 — Classification Head

마지막 CLS vector를 Linear/MLP head에 넣어 class logits을 계산합니다.

    logits = W h_CLS + b

Softmax를 적용하면 class probability를 얻을 수 있습니다.

## 11. Patch Size Trade-off

### 8×8 Patch

224×224 기준:

    28 × 28 = 784 tokens

더 세밀하지만 attention cost가 크게 증가합니다.

### 16×16 Patch

    14 × 14 = 196 tokens

대표적인 균형점입니다.

### 32×32 Patch

    7 × 7 = 49 tokens

빠르지만 작은 detail을 잃을 수 있습니다.

## 12. ViT vs CNN

| 항목 | CNN | ViT |
| --- | --- | --- |
| 기본 단위 | local convolution | patch token |
| Inductive bias | locality가 강함 | 상대적으로 약함 |
| Global relation | 깊은 layer 필요 | attention으로 직접 |
| Data 요구 | 비교적 효율적 | 큰 pretraining에서 강함 |
| Scaling | architecture별 제약 | Transformer scaling과 잘 맞음 |

## 핵심 정리

- ViT는 이미지를 patch token sequence로 바꿔 Transformer encoder에 넣습니다.
- 원문 예는 224×224, 16×16 patch → 14×14 = 196 patches입니다.
- RGB patch 하나는 16×16×3 = 768 values입니다.
- CLS token이 image-level representation 역할을 하고 positional embedding이 patch 위치를 알려 줍니다.
- Patch를 작게 하면 detail은 늘지만 token 수와 attention cost가 크게 증가합니다.

## 원문

- https://outcomeschool.com/blog/decoding-vision-transformer-vit
