# Precision vs Recall — 매우 자세한 한국어 학습 노트

> 원문: https://outcomeschool.com/blog/precision-vs-recall
> 원저자: Amit Shekhar / Outcome School
> 문서 성격: **원문 전체 번역본이 아닌 독립적인 한국어 상세 해설·학습 노트**

## 핵심 정의

Precision은 Positive라고 예측한 것 중 실제 Positive 비율이고, Recall은 실제 Positive 중 찾아낸 비율이다.

---

## 1. Confusion Matrix

- TP: 실제 Positive를 Positive로 맞춤.
- FP: 실제 Negative를 Positive로 잘못 예측.
- FN: 실제 Positive를 놓침.
- TN: 실제 Negative를 Negative로 맞춤.

## 2. Precision

- Precision = TP/(TP+FP).
- Positive 예측의 신뢰도를 본다.
- False Positive 비용이 클 때 특히 중요하다.

## 3. Recall

- Recall = TP/(TP+FN).
- 실제 Positive를 놓치지 않는 능력을 본다.
- False Negative 비용이 클 때 특히 중요하다.

## 4. Threshold Trade-off

- threshold를 낮추면 보통 recall이 오르고 FP가 늘 수 있다.
- threshold를 높이면 precision이 오르고 FN이 늘 수 있다.
- 업무 비용 구조에 맞춰 threshold를 선택한다.

## 5. F1

- F1은 Precision과 Recall의 조화 평균이다.
- 한쪽이 매우 낮으면 F1도 강하게 낮아진다.

## 6. Class Imbalance

- Positive가 1%인 데이터에서 모두 Negative라 해도 Accuracy 99%가 나올 수 있다.
- 희귀 사건에서는 Accuracy만 보면 위험하다.

## 7. PR-AUC와 ROC-AUC

- ROC는 TPR/FPR 관계를 본다.
- PR curve는 Precision/Recall 관계를 본다.
- 희귀 Positive 문제에서는 PR-AUC가 더 직관적인 경우가 많다.

## 8. 실무 예

- 의료 선별은 FN 비용이 커 Recall을 중시할 수 있다.
- 정상 메일 오차가 치명적인 spam filter는 Precision을 더 중시할 수 있다.

## 학습 체크리스트

- 핵심 개념을 한 문장으로 설명할 수 있는가?
- 대표 수식이나 기준을 직접 설명할 수 있는가?
- 실무 예시를 하나 들 수 있는가?
- 실패하거나 오해하기 쉬운 조건을 설명할 수 있는가?

## 원문

- https://outcomeschool.com/blog/precision-vs-recall
