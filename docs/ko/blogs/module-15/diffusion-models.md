# Diffusion Model이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/diffusion-models  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 Forward/Reverse Process, 약 1,000-step noise schedule, noise-prediction training objective와 text-conditioned generation의 흐름을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Diffusion Model의 핵심 아이디어

Diffusion Model은 깨끗한 데이터에 점차 noise를 추가해 완전한 noise에 가깝게 만든 뒤, 반대로 **noise를 조금씩 제거하는 방법을 학습**해 새로운 데이터를 생성합니다.

전체 구조:

    clean image
      → Forward Process
      → noisy image
      → almost pure noise

    pure/random noise
      → Reverse Process
      → denoised image
      → generated image

Forward Process는 고정된 확률 과정이고, 실제로 model이 학습하는 핵심은 Reverse Process입니다.

## 2. 왜 바로 이미지를 생성하지 않는가

고차원 image distribution에서 한 번에 완성 이미지를 직접 생성하는 것은 어렵습니다.

Diffusion은 문제를 수백~수천 개의 작은 denoising step으로 나눕니다.

    hard global generation
      → many easier local denoising predictions

이 decomposition이 안정적인 training의 핵심입니다.

## 3. Forward Diffusion

시간 step t마다 Gaussian noise를 조금씩 추가합니다.

대표 식:

    q(x_t | x_{t-1})
      = N(
          sqrt(1 - beta_t) x_{t-1},
          beta_t I
        )

여기서:

- x_0: 원본 이미지
- x_t: t번째 noisy image
- beta_t: noise schedule

입니다.

## 4. Closed-Form Sampling

매 step을 실제로 순차 실행하지 않고 임의의 t에서 바로 noisy sample을 만들 수 있습니다.

    x_t
      = sqrt(alpha_bar_t) x_0
        + sqrt(1 - alpha_bar_t) epsilon

    epsilon ~ N(0, I)

Training 때 임의의 t를 뽑아 한 번에 x_t를 만들 수 있어 효율적입니다.

## 5. 원문의 약 1,000-Step 예

원문은 대표적인 diffusion process를 설명하면서 **약 1,000개의 noise step**을 예로 듭니다.

직관:

    t=0       → 깨끗한 이미지
    t=100     → 약간 noisy
    t=500     → 구조가 많이 흐려짐
    t=1000    → 거의 pure noise

정확한 step 수는 model/sampler마다 다릅니다.

## 6. Reverse Process

생성 시에는 noise에서 시작합니다.

    x_T ~ N(0, I)

각 step에서 model이 현재 x_t를 보고 noise 또는 denoised direction을 예측해:

    x_t
      → x_{t-1}

로 조금씩 이동합니다.

반복하면 최종적으로 x_0에 가까운 sample을 얻습니다.

## 7. Noise Prediction Model

대표 DDPM training에서는 neural network epsilon_theta가 input x_t와 timestep t를 받아 **추가된 noise epsilon을 예측**합니다.

    epsilon_hat
      = epsilon_theta(x_t, t)

Loss:

    L
      = || epsilon - epsilon_hat ||^2

즉 원본 이미지를 직접 예측하기보다 noise를 맞히는 문제로 바꿉니다.

## 8. Training Step-by-Step

1. Dataset에서 clean image x_0 sample
2. Random timestep t 선택
3. Random Gaussian noise epsilon 생성
4. Closed-form으로 x_t 생성
5. Model이 epsilon_hat 예측
6. MSE loss 계산
7. Backpropagation으로 model update
8. 반복

이 과정에서 model은 다양한 noise level의 denoising pattern을 배웁니다.

## 9. Timestep Embedding

같은 noisy image라도 현재 noise level이 다르면 해야 할 denoising 정도가 다릅니다.

그래서 timestep t를 embedding해 network에 함께 제공합니다.

    image features
      + time embedding
      → noise prediction

## 10. U-Net

전통적인 image diffusion에서는 U-Net 구조가 널리 쓰였습니다.

특징:

- downsampling path
- bottleneck
- upsampling path
- skip connection

High-level semantic 정보와 low-level spatial detail을 동시에 유지하기 좋습니다.

최근에는 Transformer-based diffusion backbone도 많이 사용됩니다.

## 11. Conditional Diffusion

Text-to-image에서는 text prompt를 condition으로 사용합니다.

    text prompt
      → text encoder
      → text embeddings

    noisy image + timestep + text embeddings
      → denoiser
      → predicted noise

Cross-attention으로 image representation이 text token을 참고합니다.

## 12. Classifier-Free Guidance

Conditional generation에서 흔한 기법입니다.

Training 시 일부 sample에서 condition을 비우고:

    conditional prediction
    unconditional prediction

둘 다 학습합니다.

Inference에서는 두 예측을 조합해 prompt를 더 강하게 따르게 합니다.

개념:

    eps_guided
      = eps_uncond
        + w (eps_cond - eps_uncond)

w가 너무 크면 prompt adherence는 높아지지만 artifacts나 diversity 감소가 생길 수 있습니다.

## 13. Sampling Step을 줄일 수 있는 이유

Training은 수백~수천 step schedule을 사용해도 inference에서는 DDIM, DPM-Solver 같은 sampler로 더 적은 step을 사용할 수 있습니다.

Trade-off:

    fewer steps
      → faster
      → quality risk

Sampler와 model에 따라 최적점이 다릅니다.

## 14. Latent Diffusion

Pixel space에서 직접 diffusion하면 해상도가 커질수록 계산량이 매우 큽니다.

Latent Diffusion은 먼저 VAE encoder로 image를 압축합니다.

    image
      → VAE encoder
      → latent z

Diffusion은 latent 공간에서 수행됩니다.

    noise latent
      → denoise
      → latent
      → VAE decoder
      → image

Stable Diffusion 계열의 핵심 구조입니다.

## 15. GAN과 비교

Diffusion 장점:

- training 안정성
- 높은 sample quality
- mode collapse가 상대적으로 적음

단점:

- iterative sampling 때문에 느림
- inference compute 큼

GAN은 한 번의 generator forward로 빠르게 만들 수 있지만 adversarial training이 불안정할 수 있습니다.

## 16. 대표 활용

- text-to-image
- image editing
- inpainting
- super-resolution
- image-to-image
- audio/video generation
- 3D/medical generation

## 핵심 정리

- Diffusion은 Forward에서 noise를 추가하고 Reverse에서 noise를 제거하는 생성 모델입니다.
- 원문은 대표적으로 약 1,000-step noise process를 설명합니다.
- Training에서는 임의 timestep의 noisy image에서 추가된 noise를 예측하도록 학습합니다.
- Text-to-image는 text embedding을 denoising network의 condition으로 사용합니다.
- Latent Diffusion은 pixel 대신 compressed latent에서 diffusion을 수행해 비용을 크게 줄입니다.

## 원문

- https://outcomeschool.com/blog/diffusion-models
