# 모듈 15 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 15: 멀티모달 AI와 생성 모델

이 모듈에서는 AI가 이미지와 다른 형태의 데이터를 처리하는 방법, Noise에서 이미지를 생성하는 다양한 생성 모델을 배웁니다.

**이 모듈의 레슨:**

1. [Multimodal AI란?](https://outcomeschool.com/blog/multimodal-ai)
   ↳ [한국어 상세 학습 노트](blogs/module-15/multimodal-ai.md)

2. [Vision Transformer(ViT)란?](https://outcomeschool.com/blog/decoding-vision-transformer-vit)
   ↳ [한국어 상세 학습 노트](blogs/module-15/decoding-vision-transformer-vit.md)

3. [Image Embedding은 어떻게 동작하는가?](https://outcomeschool.com/blog/how-do-image-embeddings-work)
   ↳ [한국어 상세 학습 노트](blogs/module-15/how-do-image-embeddings-work.md)

4. [Diffusion Model이란?](https://outcomeschool.com/blog/diffusion-models)
   ↳ [한국어 상세 학습 노트](blogs/module-15/diffusion-models.md)

5. [Generative Adversarial Network(GAN)이란?](https://outcomeschool.com/blog/generative-adversarial-networks)
   ↳ [한국어 상세 학습 노트](blogs/module-15/generative-adversarial-networks.md)

6. [Variational Autoencoder(VAE)란?](https://outcomeschool.com/blog/variational-autoencoders)
   ↳ [한국어 상세 학습 노트](blogs/module-15/variational-autoencoders.md)


---

### 15.1 Multimodal AI란?

텍스트, 이미지, 음성 등 여러 Modality를 함께 다루는 AI를 배웁니다.

- 큰 그림
- Modality란?
- Unimodal vs Multimodal AI
- Multimodal AI가 필요한 이유
- 동작 방식
- 세 가지 대표 유형
- 실제 사례
- 사용 사례
- 흔한 실수
- 빠른 요약

시작하기: [Multimodal AI](https://outcomeschool.com/blog/multimodal-ai)

→ [한국어 상세 학습 노트](blogs/module-15/multimodal-ai.md)


### 15.2 Vision Transformer(ViT)란?

이미지를 Patch로 나누고 Token처럼 처리해 Transformer로 분류하는 ViT를 배웁니다.

- 큰 그림
- Image를 Patch로 분할
- Patch Embedding
- CLS Token
- Position Embedding
- Transformer Encoder
- Classification Head
- 전체 과정
- ViT vs CNN
- 빠른 요약

시작하기: [Vision Transformer](https://outcomeschool.com/blog/decoding-vision-transformer-vit)

→ [한국어 상세 학습 노트](blogs/module-15/decoding-vision-transformer-vit.md)


### 15.3 Image Embedding은 어떻게 동작하는가?

이미지를 Vector로 표현해 Similarity Search와 Recommendation 등에 사용하는 Image Embedding을 배웁니다.

- Embedding이란?
- Image Embedding이란?
- 필요한 이유
- 컴퓨터가 이미지를 보는 방식
- 생성 방식
- 수치 예제
- Embedding 간 Similarity
- 코드 예제
- 실제 활용
- 요약

시작하기: [Image Embedding](https://outcomeschool.com/blog/how-do-image-embeddings-work)

→ [한국어 상세 학습 노트](blogs/module-15/how-do-image-embeddings-work.md)


### 15.4 Diffusion Model이란?

Noise를 점차 제거해 이미지를 생성하는 Diffusion Model을 배웁니다.

- Diffusion Model이란?
- 필요한 이유
- Forward와 Reverse Process
- Forward: Noise 추가
- Reverse: Noise 제거
- 단계별 예제
- 학습 방식
- 간단한 코드 예제
- Conditional Diffusion(Text-to-Image)
- 장점
- 사용처

시작하기: [Diffusion Model](https://outcomeschool.com/blog/diffusion-models)

→ [한국어 상세 학습 노트](blogs/module-15/diffusion-models.md)


### 15.5 Generative Adversarial Network(GAN)이란?

Generator와 Discriminator가 경쟁하며 새로운 이미지를 생성하는 GAN을 배웁니다.

- GAN이란?
- Generator vs Discriminator
- 위조범 vs 경찰 비유
- Adversarial Training Loop
- Loss와 Minimax Game
- PyTorch 스타일 코드
- Mode Collapse
- 학습 안정성
- DCGAN, Conditional GAN, StyleGAN, CycleGAN
- 실제 활용

시작하기: [GAN](https://outcomeschool.com/blog/generative-adversarial-networks)

→ [한국어 상세 학습 노트](blogs/module-15/generative-adversarial-networks.md)


### 15.6 Variational Autoencoder(VAE)란?

매끄럽고 구조화된 Latent Space를 학습해 새로운 데이터를 생성할 수 있는 VAE를 배웁니다.

- Autoencoder란?
- 일반 Autoencoder의 문제
- VAE란?
- Encoder, Latent Space, Decoder
- Reparameterization Trick
- VAE Loss
- 간단한 예제
- 코드 예제
- 장점
- 사용처

시작하기: [VAE](https://outcomeschool.com/blog/variational-autoencoders)

→ [한국어 상세 학습 노트](blogs/module-15/variational-autoencoders.md)


---
