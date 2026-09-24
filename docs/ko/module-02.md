# 모듈 2 한국어 학습 요약

> 이 문서는 연결된 제3자 블로그 원문 전체를 번역해 재게시한 것이 아니라, 학습을 위해 핵심 내용을 한국어로 정리한 상세 요약입니다. 각 레슨의 원문 링크는 그대로 함께 제공합니다.

## 모듈 2: 딥러닝과 신경망

이 모듈에서는 신경망이 실제로 어떻게 학습하는지 배웁니다. 경사하강법과 역전파의 수학을 단계별로 이해하고, 학습을 안정적으로 만드는 기법도 살펴봅니다.

모듈을 마치면 forward pass에서 가중치 업데이트까지 신경망 학습 과정을 설명할 수 있고, normalization과 dropout이 왜 중요한지도 이해하게 됩니다.

**이 모듈의 레슨:**

1. [인공신경망의 Bias란?](https://outcomeschool.com/blog/bias-in-artificial-neural-network)
2. [경사하강법은 어떻게 동작하는가?](https://outcomeschool.com/blog/math-behind-gradient-descent)
3. [역전파는 어떻게 동작하는가? 수학으로 단계별 설명](https://outcomeschool.com/blog/math-behind-backpropagation)
4. [Cross-Entropy Loss란?](https://outcomeschool.com/blog/math-behind-cross-entropy-loss)
5. [신경망의 Dropout이란 무엇이며 어떻게 동작하는가?](https://outcomeschool.com/blog/dropout-in-neural-networks)
6. [Batch Normalization vs Layer Normalization](https://outcomeschool.com/blog/batch-normalization-vs-layer-normalization)
7. [RMSNorm이란? Root Mean Square Layer Normalization 설명](https://outcomeschool.com/blog/rmsnorm-root-mean-square-layer-normalization)
8. [순환 신경망(RNN)이란?](https://outcomeschool.com/blog/recurrent-neural-network)
9. [PyTorch는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-pytorch-work)
10. [머신러닝 라이브러리 TensorFlow는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-the-machine-learning-library-tensorflow-work)

---

### 2.1 인공신경망의 Bias란?

이 글에서는 인공신경망의 Bias가 무엇인지 배웁니다.

시작하기: [인공신경망의 Bias란?](https://outcomeschool.com/blog/bias-in-artificial-neural-network)

### 2.2 경사하강법은 어떻게 동작하는가?

단계별 수치 예제를 통해 경사하강법의 수학을 배웁니다.

다음 내용을 다룹니다.

- 큰 그림
- Loss Function이란?
- Gradient Descent란?
- 경사하강법의 직관
- 경사하강법의 수학
- 단계별 수치 예제
- 여러 파라미터를 가진 경사하강법
- Learning Rate의 역할
- 경사하강법의 종류
- Python에서의 경사하강법
- 전체 흐름 연결하기

시작하기: [경사하강법은 어떻게 동작하는가?](https://outcomeschool.com/blog/math-behind-gradient-descent)

영상 보기: [Epoch, Batch, Batch Size, Iteration](https://www.youtube.com/watch?v=NFLlXE-6vno)

### 2.3 역전파는 어떻게 동작하는가? 수학으로 단계별 설명

신경망 역전파의 수학을 배웁니다.

다음 내용을 다룹니다.

- 역전파란?
- 미적분의 Chain Rule
- Forward Pass
- Loss 계산
- Backward Pass(역전파)
- 단계별 수치 예제
- 경사하강법을 이용한 가중치 업데이트
- Python에서의 역전파

시작하기: [역전파는 어떻게 동작하는가? 수학으로 단계별 설명](https://outcomeschool.com/blog/math-behind-backpropagation)

### 2.4 Cross-Entropy Loss란?

단계별 수치 예제를 이용해 Cross-Entropy Loss의 수학을 배웁니다.

다음 내용을 다룹니다.

- 큰 그림
- Cross-Entropy란?
- Cross-Entropy Loss 공식
- 음의 로그를 취하는 이유
- Binary Cross-Entropy Loss
- Categorical Cross-Entropy Loss
- 단계별 수치 예제
- 언어 모델의 Cross-Entropy Loss
- Cross-Entropy Loss의 Gradient
- 빠른 요약

시작하기: [Cross-Entropy Loss란?](https://outcomeschool.com/blog/math-behind-cross-entropy-loss)

영상 보기: [Softmax Activation Function in Machine Learning](https://www.youtube.com/watch?v=2Zx6x01WwWM)

### 2.5 신경망의 Dropout이란 무엇이며 어떻게 동작하는가?

신경망의 Dropout이 무엇인지, 어떤 문제를 해결하는지, 간단한 예제로 단계별 동작 방식을 이해하고 어디에 사용되는지 살펴봅니다.

다음 내용을 다룹니다.

- Dropout이란?
- 과적합 문제
- Dropout이 필요한 이유
- Dropout의 동작 방식
- 단계별 예제
- 학습 시점 vs 테스트 시점의 Dropout
- 코드에서의 Dropout
- Dropout 변형
- Dropout의 장점
- Dropout의 사용처

시작하기: [신경망의 Dropout이란 무엇이며 어떻게 동작하는가?](https://outcomeschool.com/blog/dropout-in-neural-networks)

### 2.6 Batch Normalization vs Layer Normalization

Batch Normalization과 Layer Normalization을 배우고, 둘의 차이와 각각 언제 사용하는지 살펴봅니다.

다음 내용을 다룹니다.

- Normalization이란?
- Normalization이 필요한 이유
- Batch Normalization이란?
- Layer Normalization이란?
- Batch Normalization vs Layer Normalization
- 언제 무엇을 사용할까?

시작하기: [Batch Normalization vs Layer Normalization](https://outcomeschool.com/blog/batch-normalization-vs-layer-normalization)

### 2.7 RMSNorm이란? Root Mean Square Layer Normalization 설명

[L​​ayer Normalization](https://outcomeschool.com/blog/batch-normalization-vs-layer-normalization)보다 빠르고 단순한 대안이며 Llama, Mistral, Gemma, Qwen, PaLM, DeepSeek 등 많은 현대 LLM에서 사용하는 RMSNorm을 배웁니다.

다음 내용을 다룹니다.

- 깊은 신경망에서 normalization이 필요한 이유
- Layer Normalization(LayerNorm) 빠른 복습
- RMSNorm이 무엇이고 어떻게 동작하는가
- 구체적인 수치 예제로 보는 RMSNorm의 수학
- LayerNorm vs RMSNorm의 핵심 차이
- 현대 LLM이 RMSNorm을 선호하는 이유
- 코드 예제
- Transformer에서 RMSNorm의 위치
- 빠른 요약

시작하기: [RMSNorm이란? Root Mean Square Layer Normalization 설명](https://outcomeschool.com/blog/rmsnorm-root-mean-square-layer-normalization)

### 2.8 순환 신경망(RNN)이란?

순환 신경망(Recurrent Neural Network)을 배웁니다.

시작하기: [순환 신경망(RNN)이란?](https://outcomeschool.com/blog/recurrent-neural-network)

### 2.9 PyTorch는 어떻게 동작하는가?

PyTorch의 동작 원리를 배웁니다. Tensor가 무엇인지, computation graph와 autograd가 함께 모델을 학습하는 방식, GPU를 사용하는 이유와 PyTorch가 실무에서 널리 쓰이는 이유도 살펴봅니다.

다음 내용을 다룹니다.

- PyTorch란?
- Tensor란?
- PyTorch가 해결하는 문제
- Computation Graph란?
- Autograd란?
- 완전한 학습 예제
- GPU란 무엇이며 PyTorch는 왜 GPU를 사용하는가?
- PyTorch가 인기 있는 이유

시작하기: [PyTorch는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-pytorch-work)

### 2.10 머신러닝 라이브러리 TensorFlow는 어떻게 동작하는가?

머신러닝 라이브러리 TensorFlow의 동작 방식을 배웁니다.

시작하기: [머신러닝 라이브러리 TensorFlow는 어떻게 동작하는가?](https://outcomeschool.com/blog/how-does-the-machine-learning-library-tensorflow-work)

**모듈 2 영상 및 추가 자료:**

- [Epoch, Batch, Batch Size, Iteration](https://www.youtube.com/watch?v=NFLlXE-6vno) (영상)

---
