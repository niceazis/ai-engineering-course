# Android TensorFlow Lite 머신러닝 예제 — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/android-tensorflow-lite-machine-learning-example  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2019-08-02 공개 원문을 직접 확인해 TensorFlow Lite의 목적, low-latency on-device inference, quantized kernel, .tflite 변환과 Android loading 흐름을 보존하면서 현재 관점의 주의사항을 덧붙인 독립적인 한국어 상세 해설입니다.

## 1. TensorFlow Lite의 목적

원문은 TensorFlow Lite를 mobile/embedded device에서 machine learning inference를 실행하기 위한 lightweight solution으로 설명합니다.

핵심 장점:

- on-device inference
- low latency
- small binary size
- Android Neural Networks API를 통한 hardware acceleration 지원
- mobile optimized kernel

## 2. 왜 On-device인가

Mobile app에서 cloud round trip 없이 바로 inference하면:

- latency 감소
- offline 동작 가능
- raw data를 device 안에 둘 수 있음

장점이 있습니다.

Module 16의 Cloud vs On-device 선택과 직접 연결됩니다.

## 3. TensorFlow Model과 .tflite Model

원문이 가장 중요하게 강조하는 부분은 일반 TensorFlow model을 그대로 Android에서 쓰는 것이 아니라 **TensorFlow Lite가 읽는 .tflite format으로 변환**해야 한다는 점입니다.

개념:

    trained TensorFlow model
      → TensorFlow Lite Converter
      → model.tflite
      → Android app

## 4. Label File

Object classification/detection 예제에서는 model output index를 사람이 읽는 class 이름으로 바꾸기 위해 label file을 같이 사용합니다.

예:

    output index 0 → cat
    output index 1 → dog
    output index 2 → car

Model file과 label mapping version이 어긋나면 잘못된 결과가 표시될 수 있습니다.

## 5. Low-Latency 최적화

원문은 TensorFlow Lite가 mobile latency를 줄이기 위해 다음을 사용한다고 설명합니다.

- mobile-optimized kernels
- pre-fused activations
- quantized kernels
- fixed-point math

Quantization은 model size와 memory bandwidth를 줄여 mobile inference에 특히 유리합니다.

## 6. Android 실행 흐름

일반적인 흐름:

1. .tflite model을 app asset에 포함
2. model file load
3. Interpreter 생성
4. input tensor shape/format에 맞게 preprocessing
5. inference 실행
6. output tensor 읽기
7. label mapping/postprocessing
8. UI에 결과 표시

## 7. Object Detection이라면 추가로 필요한 것

Classification과 달리 object detection은 보통:

- bounding box
- class ID
- confidence score
- detection count

를 해석해야 합니다.

또 input image를 model이 기대하는 resolution과 normalization 방식으로 변환해야 합니다.

## 8. Hardware Acceleration

원문은 Android Neural Networks API 지원을 언급합니다.

현대 Android에서는 hardware/device에 따라:

- CPU
- GPU delegate
- NNAPI
- vendor accelerator

등을 사용할 수 있습니다.

지원 operator와 실제 speedup은 device별로 다르므로 benchmark가 필요합니다.

## 9. Quantization

Mobile deployment에서 대표적으로:

- float16
- int8
- dynamic-range quantization

등을 고려할 수 있습니다.

낮은 precision은 model size와 latency를 줄이지만 accuracy regression을 확인해야 합니다.

## 10. Production 주의점

- model version
- input/output tensor contract
- preprocessing code
- label file
- delegate compatibility

를 같이 versioning해야 합니다.

Model만 교체하고 preprocessing이 그대로면 inference가 조용히 틀릴 수 있습니다.

## 11. 현재 생태계 주의

이 원문은 2019년에 작성됐습니다.

TensorFlow Lite의 branding/API와 Android ML deployment ecosystem은 이후 변화가 있었으므로 실제 신규 구현에서는 현재 TensorFlow Lite/LiteRT 및 Android 공식 문서를 기준으로 API를 확인해야 합니다.

원문의 핵심 학습 포인트는 특정 API 문법이 아니라:

> mobile용 model artifact를 준비하고, device runtime에서 효율적으로 inference한다

는 구조입니다.

## 핵심 정리

- TensorFlow Lite는 mobile/embedded on-device inference를 위한 lightweight runtime입니다.
- 일반 TensorFlow model을 .tflite format으로 변환해 Android app에서 load합니다.
- 원문은 optimized kernel, pre-fused activation, quantized kernel과 NNAPI acceleration을 강조합니다.
- Model, label, preprocessing, output postprocessing을 하나의 contract로 관리해야 합니다.
- 원문이 오래된 만큼 실제 API는 현재 공식 문서로 재검증해야 합니다.

## 원문

- https://outcomeschool.com/blog/android-tensorflow-lite-machine-learning-example
