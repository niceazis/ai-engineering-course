# 지도학습 vs 비지도학습 — 매우 자세한 한국어 학습 노트

> 원문: https://outcomeschool.com/blog/supervised-vs-unsupervised-learning
> 원저자: Amit Shekhar / Outcome School
> 문서 성격: **원문 전체 번역본이 아닌 독립적인 한국어 상세 해설·학습 노트**

## 핵심 정의

지도학습은 입력과 정답(label)을 함께 사용해 예측 함수를 학습하고, 비지도학습은 명시적 정답 없이 데이터의 구조·군집·저차원 표현을 찾는다.

---

## 1. 핵심 구분

- 지도학습: (X, y) 형태의 labeled data를 사용한다.
- 비지도학습: X만 주어지고 y가 없다.
- 문제 이름보다 target의 존재 여부와 업무 목적이 더 중요하다.

## 2. 지도학습의 동작

- 입력 → 예측 → 정답과 비교 → loss 계산 → parameter update를 반복한다.
- Classification은 범주를, Regression은 연속값을 예측한다.
- Label 품질이 낮으면 모델이 잘못된 목표를 학습한다.

## 3. 비지도학습의 동작

- Clustering은 유사한 sample끼리 그룹을 만든다.
- Dimensionality Reduction은 중요한 구조를 보존하며 차원을 줄인다.
- Anomaly Detection은 정상 패턴에서 크게 벗어난 sample을 찾는 데 활용할 수 있다.

## 4. Self-Supervised Learning

- 사람이 label을 직접 붙이지 않고 데이터 자체에서 학습 target을 만든다.
- 다음 token 예측, masked token 복원 등이 대표적이다.
- 현대 LLM pretraining을 이해하는 데 매우 중요한 범주다.

## 5. 실무 선택

- 정답 target과 label이 있고 예측이 목표면 supervised를 우선 검토한다.
- label이 없고 데이터 구조 탐색이 목적이면 unsupervised가 적합하다.
- 일부 label만 있다면 semi-supervised 접근도 고려한다.

## 6. 평가

- 지도학습은 Accuracy, Precision, Recall, RMSE 등 metric을 정의하기 쉽다.
- 비지도학습은 내부 metric만으로 업무적 의미를 보장할 수 없다.
- cluster 결과는 사람이 실제 의미와 활용 가능성을 검증해야 한다.

## 7. 흔한 오해

- 비지도학습도 objective가 있다. label이 없을 뿐이다.
- Clustering 결과가 곧 현실의 정답 집단은 아니다.
- LLM pretraining은 보통 self-supervised learning으로 보는 편이 정확하다.

## 학습 체크리스트

- 이 개념을 한 문장으로 설명할 수 있는가?
- 실제 서비스 예시를 하나 들 수 있는가?
- 실패하거나 오해하기 쉬운 조건을 설명할 수 있는가?
- 이전/다음 레슨과의 연결을 설명할 수 있는가?

## 원문

- https://outcomeschool.com/blog/supervised-vs-unsupervised-learning
