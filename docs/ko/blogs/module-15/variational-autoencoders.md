# Variational Autoencoder(VAE)란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/variational-autoencoders  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 Autoencoder의 한계, μ·σ latent distribution, Reparameterization Trick, Reconstruction+KL Loss와 μ=1.5, σ=0.2 → z=1.6 예제를 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. Autoencoder 복습

일반 Autoencoder:

    input x
      → Encoder
      → latent vector z
      → Decoder
      → reconstruction x_hat

목표는 input을 작은 latent representation으로 압축하고 다시 복원하는 것입니다.

Loss 예:

    L_recon
      = ||x - x_hat||^2

## 2. 일반 Autoencoder의 생성 문제

Autoencoder는 training sample을 잘 reconstruct할 수 있지만 latent space가 **매끄럽고 연속적이라는 보장**이 없습니다.

예:

    z_A = [1.2, -0.8]
    z_B = [4.9, 3.1]

사이에 아무 의미 없는 빈 공간이 생길 수 있습니다.

Random z를 뽑아 decoder에 넣으면 realistic sample이 나오지 않을 수 있습니다.

## 3. VAE의 핵심

VAE는 Encoder가 하나의 point z를 직접 출력하지 않습니다.

대신 latent distribution의 parameter를 출력합니다.

대표적으로:

    mean = mu
    log variance = log sigma^2

그 뒤 그 distribution에서 z를 sample합니다.

    q_phi(z|x)
      = N(mu, sigma^2)

## 4. 왜 Distribution으로 표현하는가

각 sample을 고정 점이 아니라 확률 분포로 표현하면 neighboring sample들의 latent distribution이 겹치고 latent space가 더 smooth해집니다.

그 결과:

- interpolation
- random sampling
- generation

이 더 자연스러워집니다.

## 5. Reparameterization Trick

문제:

    z ~ N(mu, sigma^2)

처럼 직접 sampling하면 random operation을 통해 gradient를 backpropagate하기 어렵습니다.

해결:

    epsilon ~ N(0, 1)

    z
      = mu + sigma * epsilon

Randomness를 epsilon으로 분리하면 mu와 sigma는 differentiable path 안에 남습니다.

이것이 Reparameterization Trick입니다.

## 6. 원문의 수치 예

원문 예:

    mu = 1.5
    sigma = 0.2
    epsilon = 0.5

그러면:

    z
      = 1.5 + 0.2 × 0.5
      = 1.6

Encoder는 1.6이라는 값을 직접 출력한 것이 아니라 distribution parameter를 출력했고, random epsilon으로 latent sample을 만든 것입니다.

## 7. Decoder

Sampled z를 Decoder에 넣어 input을 reconstruct합니다.

    z
      → Decoder
      → x_hat

Generation 시에는 Encoder 없이 prior에서 z를 직접 sample할 수 있습니다.

    z ~ N(0, I)
      → Decoder
      → new sample

## 8. VAE Loss

두 부분을 합칩니다.

    L
      = L_reconstruction
        + beta * L_KL

기본 VAE에서는 beta=1인 형태가 대표적입니다.

## 9. Reconstruction Loss

Input과 output을 비슷하게 만듭니다.

Image:

- MSE
- BCE

등을 사용할 수 있습니다.

이 term만 있으면 일반 Autoencoder와 유사하게 latent point가 제멋대로 흩어질 수 있습니다.

## 10. KL Divergence

Approximate posterior:

    q(z|x)
      = N(mu, sigma^2)

가 standard normal prior:

    p(z)
      = N(0, I)

와 너무 멀어지지 않도록 합니다.

Gaussian VAE의 KL term은 closed form으로 계산할 수 있습니다.

대표 형태:

    KL
      = -1/2 Σ(
          1 + log sigma^2
          - mu^2
          - sigma^2
        )

## 11. 두 Loss의 Trade-off

Reconstruction term이 너무 강하면:

- input은 잘 복원
- latent space가 irregular

KL이 너무 강하면:

- latent는 잘 정돈
- reconstruction이 흐려질 수 있음

beta-VAE는 KL weight를 조절해 disentanglement/quality trade-off를 바꿉니다.

## 12. Latent Space Interpolation

두 sample latent:

    z_A
    z_B

사이를:

    z(t)
      = (1-t)z_A + t z_B

로 이동하며 decode하면 두 sample 사이의 smooth transition을 만들 수 있습니다.

VAE latent space가 generative representation으로 유용한 이유입니다.

## 13. VAE가 Diffusion에 쓰이는 이유

Latent Diffusion에서 VAE는 image를 더 작은 latent tensor로 압축합니다.

    image
      → VAE Encoder
      → latent

Diffusion은 이 latent에서 수행되고 마지막에:

    latent
      → VAE Decoder
      → image

로 복원합니다.

따라서 VAE는 현대 image generation에서도 핵심 구성 요소입니다.

## 14. VAE의 장점

- smooth latent space
- principled probabilistic model
- sampling/interpolation 가능
- representation learning
- latent compression

## 15. 한계

- reconstruction/generated image가 blurrier할 수 있음
- posterior collapse
- likelihood objective와 perceptual quality의 불일치
- decoder capacity에 따른 문제

## 16. 대표 활용

- image generation
- anomaly detection
- representation learning
- compression
- latent diffusion encoder/decoder
- molecule/data generation

## 핵심 정리

- VAE는 Encoder가 latent point가 아니라 mean과 variance를 출력합니다.
- Reparameterization Trick은 z = mu + sigma × epsilon으로 randomness와 differentiable path를 분리합니다.
- 원문 예에서 mu=1.5, sigma=0.2, epsilon=0.5이면 z=1.6입니다.
- Loss는 Reconstruction + KL Divergence로 구성됩니다.
- KL term이 latent distribution을 standard normal에 가깝게 만들어 random sampling 가능한 smooth latent space를 만듭니다.

## 원문

- https://outcomeschool.com/blog/variational-autoencoders
