# RAG 문서를 어떻게 Chunking할까? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/chunking-strategies-for-rag
> 원저자: Amit Shekhar / Outcome School
> 문서 성격: **원문 전체 번역본이 아닌 독립적인 한국어 상세 해설·학습 노트**

## 핵심 해설

큰 문서를 적절한 작은 조각으로 나눠 필요한 내용을 정확히 검색하는 Chunking 전략을 배웁니다.

## 핵심 학습 항목

- RAG란?
- Chunk란?
- Chunking이 필요한 이유
- Retrieval 동작 방식
- 잘못된 Chunking의 문제
- Fixed-size Chunking
- Sentence-based Chunking
- Recursive Chunking
- Document Structure 기반 Chunking
- Semantic Chunking
- Contextual Chunking
- Small-to-big Chunking
- Agentic Chunking
- Chunk Overlap
- Chunk Size 선택
- 전략 비교
- 흔한 실수
- 결론

## 단계별 학습 가이드

### 1. RAG란?

**RAG란?**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 2. Chunk란?

**Chunk란?**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 3. Chunking이 필요한 이유

**Chunking이 필요한 이유**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 4. Retrieval 동작 방식

**Retrieval 동작 방식**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 5. 잘못된 Chunking의 문제

**잘못된 Chunking의 문제**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 6. Fixed-size Chunking

**Fixed-size Chunking**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 7. Sentence-based Chunking

**Sentence-based Chunking**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 8. Recursive Chunking

**Recursive Chunking**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 9. Document Structure 기반 Chunking

**Document Structure 기반 Chunking**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 10. Semantic Chunking

**Semantic Chunking**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 11. Contextual Chunking

**Contextual Chunking**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 12. Small-to-big Chunking

**Small-to-big Chunking**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 13. Agentic Chunking

**Agentic Chunking**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 14. Chunk Overlap

**Chunk Overlap**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 15. Chunk Size 선택

**Chunk Size 선택**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 16. 전략 비교

**전략 비교**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 17. 흔한 실수

**흔한 실수**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

### 18. 결론

**결론**의 정의, 필요한 이유, 입력과 출력, 전체 시스템에서의 위치를 연결해서 이해합니다. 작은 예제나 코드 흐름으로 직접 확인하고, 비슷한 대안과의 차이 및 trade-off까지 설명할 수 있어야 합니다.

## 실무 연결

- 정확도·안정성·속도·메모리에 미치는 영향을 확인합니다.
- training과 inference에서 동작이 달라지는지 구분합니다.
- 관련 hyperparameter와 실패 조건을 함께 확인합니다.
- 실제 프레임워크 구현과 연결해서 봅니다.

## 점검 질문

1. RAG 문서를 어떻게 Chunking할까?을 한 문장으로 설명할 수 있는가?
2. 왜 필요한지 설명할 수 있는가?
3. 핵심 데이터 흐름을 순서대로 설명할 수 있는가?
4. 대표 장점과 한계를 말할 수 있는가?
5. 언제 이 방법을 선택할지 설명할 수 있는가?

## 원문

- https://outcomeschool.com/blog/chunking-strategies-for-rag
