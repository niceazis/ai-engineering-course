# TensorFlow는 어떻게 동작하는가? — 원문 기반 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-does-the-machine-learning-library-tensorflow-work  
> Amit Shekhar / Outcome School · 2019-08-02  
> 원문은 TensorFlow 1.x의 graph/session 중심 API를 설명합니다. 아래 노트는 그 원문의 구조를 충실히 정리하되, 현재 TensorFlow 2.x와 API가 다르다는 점을 명확히 구분합니다.

## 원문의 핵심 관점

원문은 TensorFlow를 **data-flow graph를 만들고 그 graph를 실행하는 framework**로 설명합니다.

graph의 구성:

- node: operation
- edge: operation 사이를 이동하는 tensor
- constant: 고정 값
- placeholder: 실행 시 공급하는 입력
- operation: add, multiply 같은 계산
- session: graph를 실제 실행

## 간단한 graph

```text
a ----       add ----> result
b ----/
```

한 operation의 output tensor가 다음 operation의 input이 되면서 더 큰 계산 graph를 만듭니다.

## 원문의 TF1 스타일 예제

원문은 constant 2와 3을 만들고 Session에서 addition과 multiplication을 실행하는 예제를 먼저 보여줍니다.

그 다음 placeholder 두 개를 graph input으로 두고:

```text
add(a,b)
multiply(a,b)
```

를 정의한 뒤, Session 실행 시 실제 값을 feed하는 구조를 설명합니다.

핵심은 **graph 정의와 graph 실행이 분리되어 있다**는 점입니다.

## Mini TensorFlow를 직접 만드는 흐름

원문은 내부 구조를 이해하기 위해 아주 작은 graph engine을 직접 설계합니다.

### 1. Operation

공통 Operation 객체는 자신의 input node들과 output 연결 관계를 기억합니다.

그 위에:

- add
- multiply

같은 구체적 operation을 만듭니다.

### 2. Placeholder와 Constant

Placeholder는 실행할 때 외부에서 값을 받습니다.

Constant는 graph 안에 고정된 값을 보관합니다.

### 3. Graph

Graph 객체는:

- operations
- placeholders
- variables/constants

같은 구성 요소를 모아 관리합니다.

### 4. 실행 순서 계산

최종 operation을 계산하려면 먼저 dependency가 되는 input node부터 처리해야 합니다.

원문은 post-order traversal을 사용해 필요한 node를 dependency 순서로 나열합니다.

### 5. Session

Session은 정렬된 node를 순서대로 평가합니다.

- placeholder면 feed 값 사용
- constant면 저장된 값 사용
- operation이면 input 결과를 받아 compute 실행

최종 target operation의 output을 반환합니다.

## 원문의 y = mx + c 예제

원문은 mini framework의 마지막 확인으로:

```text
y = m*x + c
m = 10
c = 1
```

을 graph로 만듭니다.

`x=10`을 feed하면:

```text
multiply(10,10) -> 100
add(100,1) -> 101
```

이 dependency 순서로 실행됩니다.

이 예제의 목적은 TensorFlow가 단순히 함수를 즉시 호출하는 것이 아니라 **계산 관계를 graph로 표현하고 dependency에 맞게 실행할 수 있다**는 내부 아이디어를 보여주는 것입니다.

## 현재 TensorFlow와의 차이

이 원문은 2019년에 작성되었고 `tf.Session`, `tf.placeholder` 같은 TensorFlow 1.x API를 사용합니다.

현재 TensorFlow 2.x는 eager execution이 기본이라 일반 코드는 Python 문장처럼 즉시 실행됩니다. 필요할 때 `tf.function` 등을 사용해 graph로 변환·최적화할 수 있습니다.

따라서:

```text
원문의 핵심 개념: computation graph와 dependency execution
원문의 API 예시: TF1 시대
현재 실무 API: TF2 eager-first
```

로 구분해서 이해해야 합니다.

## PyTorch와 연결

현대 PyTorch도 computation graph를 사용하지만 일반적으로 실행 중 동적으로 graph를 구성하는 방식으로 설명됩니다.

TensorFlow 2.x 역시 eager-first가 되면서 사용자 경험은 과거 TF1보다 훨씬 동적이고 Python 친화적으로 바뀌었습니다.

## 이해 확인

1. graph에서 node와 edge는 각각 무엇을 나타내나요?
2. 원문의 Session이 dependency 순서를 알아야 하는 이유는 무엇인가요?
3. 원문의 TF1 코드와 현재 TF2 코드가 다르다는 점을 왜 명시해야 하나요?

## 연결 학습

- 원문: https://outcomeschool.com/blog/how-does-the-machine-learning-library-tensorflow-work
- 이전: [PyTorch](how-does-pytorch-work.md)
- [모듈 2](../../module-02.md)
