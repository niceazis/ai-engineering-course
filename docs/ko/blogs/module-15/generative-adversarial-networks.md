# Generative Adversarial Network(GAN)이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/generative-adversarial-networks  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 Generator/Discriminator, 위조범-경찰 비유, minimax objective, alternating training, mode collapse와 대표 GAN 변형을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. GAN의 정의

GAN은 두 neural network가 서로 경쟁하며 data distribution을 학습하는 generative model입니다.

두 구성 요소:

### Generator G

Random noise z를 받아 fake sample을 생성합니다.

    z
      → G
      → fake image

### Discriminator D

Input sample이 real dataset에서 왔는지 Generator가 만든 fake인지 판별합니다.

    image
      → D
      → probability(real)

## 2. 원문의 위조범 vs 경찰 비유

원문은 GAN을 다음 경쟁으로 설명합니다.

- Generator = 더 정교한 위조지폐를 만드는 위조범
- Discriminator = 위조 여부를 감별하는 경찰

경찰이 강해질수록 위조범도 더 정교해지고, 위조범이 강해질수록 경찰도 더 세밀하게 구분하게 됩니다.

이 adversarial game을 반복하면서 Generator가 실제 data와 비슷한 sample을 만들도록 학습됩니다.

## 3. Minimax Objective

원 논문의 대표 objective:

    min_G max_D V(D,G)

    V(D,G)
      = E_x~pdata [log D(x)]
        + E_z~pz [log(1 - D(G(z)))]

Discriminator는:

    real → 1
    fake → 0

에 가깝게 만들려고 합니다.

Generator는 D(G(z))가 1에 가까워지도록 fake를 만듭니다.

## 4. Discriminator Training

한 step:

1. Real batch sample
2. Noise z sample
3. Generator로 fake batch 생성
4. D(real)의 loss
5. D(fake)의 loss
6. 두 loss를 합쳐 D update

Generator parameter는 이 단계에서 고정할 수 있습니다.

## 5. Generator Training

1. Noise z sample
2. Fake image G(z)
3. D(G(z)) 계산
4. Generator가 discriminator를 속이도록 G update

실전에서는 gradient가 약해지는 문제를 줄이기 위해 non-saturating loss를 흔히 사용합니다.

    L_G
      = - E_z [log D(G(z))]

## 6. Alternating Training

GAN은 일반적으로:

    update D
    update G
    update D
    update G
    ...

처럼 번갈아 학습합니다.

두 network의 balance가 매우 중요합니다.

D가 너무 강하면 G가 유용한 gradient를 받기 어렵고, G가 너무 강하면 D가 학습할 signal이 약해집니다.

## 7. Mode Collapse

원문에서 중요한 failure mode입니다.

Generator가 data distribution 전체를 배우지 않고 **몇 가지 sample type만 반복 생성**하는 현상입니다.

예:

실제 dataset:

    smiling faces
    serious faces
    side profiles
    multiple hairstyles

Generator:

    거의 비슷한 smiling face만 반복

Discriminator를 속이는 쉬운 mode 하나에 갇힌 것입니다.

## 8. Mode Collapse 대응

대표 접근:

- minibatch discrimination
- feature matching
- Wasserstein loss
- gradient penalty
- architecture/training balance 개선

완전히 사라지는 문제는 아니지만 modern GAN은 초기 GAN보다 훨씬 안정적입니다.

## 9. Training Instability

GAN은 하나의 고정 objective를 minimize하는 일반 supervised training과 달리 두 player가 동시에 바뀌는 game입니다.

그래서:

- oscillation
- non-convergence
- vanishing gradient
- discriminator dominance

가 발생할 수 있습니다.

## 10. DCGAN

Convolution 기반 GAN architecture.

대표 특징:

- strided convolution
- batch normalization
- ReLU/LeakyReLU
- fully connected layer 최소화

초기 image GAN의 표준 architecture로 큰 영향을 줬습니다.

## 11. Conditional GAN

Class label y 같은 condition을 Generator와 Discriminator에 함께 줍니다.

    z + class label
      → G
      → class-conditioned image

예:

    class = "cat"

을 주면 cat image를 만들도록 제어할 수 있습니다.

## 12. StyleGAN

고해상도 face generation으로 유명한 architecture입니다.

핵심 아이디어 중 하나는 latent를 intermediate style space로 바꾸고 layer별로 style을 주입하는 것입니다.

Pose, coarse structure, texture 같은 factor를 더 controllable하게 만들었습니다.

## 13. CycleGAN

Paired dataset 없이 domain A↔B translation을 학습합니다.

예:

    horse ↔ zebra

Cycle consistency:

    A → B → A

를 사용해 원래 content를 유지하도록 합니다.

## 14. GAN vs Diffusion

| 항목 | GAN | Diffusion |
| --- | --- | --- |
| Sampling | 한 번의 forward | 여러 denoising step |
| 속도 | 빠름 | 느린 편 |
| Training | adversarial, 불안정 | 상대적으로 안정 |
| Mode collapse | 가능 | 훨씬 적음 |
| Quality | 매우 높을 수 있음 | 현대 image generation의 주류 |

## 15. 실제 활용

- image synthesis
- face generation
- super-resolution
- image-to-image translation
- data augmentation
- style transfer
- domain adaptation

## 핵심 정리

- GAN은 Generator와 Discriminator의 adversarial game으로 data distribution을 학습합니다.
- Generator는 fake sample을 만들고 Discriminator는 real/fake를 구분합니다.
- Training은 두 network를 번갈아 update합니다.
- Mode Collapse와 instability가 대표적인 문제입니다.
- DCGAN, Conditional GAN, StyleGAN, CycleGAN이 주요 발전 방향입니다.

## 원문

- https://outcomeschool.com/blog/generative-adversarial-networks
