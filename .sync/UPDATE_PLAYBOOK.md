# Continuous Korean Course Update Policy

이 저장소의 한국어판은 ChatGPT가 직접 유지한다.

## Source of truth

- Upstream: `amitshekhariitbhu/ai-engineering-course:main`
- 상태 파일: `.sync/upstream-state.json`
- 원본 구조 manifest: `docs/ko/course-manifest.json`

## 업데이트 규칙

1. 매일 upstream `main`의 최신 SHA와 manifest를 확인한다.
2. 변경이 없으면 저장소를 수정하지 않는다.
3. 변경이 있으면 신규/수정/삭제 레슨을 모듈별로 분류한다.
4. 신규·수정 Outcome School 블로그는 원문을 실제 확인한 뒤 독립적인 상세 한국어 학습 노트로 작성한다.
5. 원문 설명 순서, 예제, 수식, 수치, 비교, 단계적 논리를 가능한 한 보존하되 전체 번역·재배포 형태로 복제하지 않는다.
6. 직접 확인하지 못한 내용을 원문 내용이라고 단정하지 않는다. 원문을 열 수 없으면 문서에 그 한계를 명시하고 공식/1차 자료로만 보완한다.
7. YouTube 레슨은 영상 정체를 확인한다. 자막 전문을 직접 검증하지 못하면 그 사실을 상세 영상 노트에 명시한다.
8. `README.ko.md`, `docs/ko/module-XX.md`, 필요 시 `docs/ko/videos.md`를 함께 갱신한다.
9. Markdown code fence, zero-width 문자, tab, heading, 상대 링크를 검증한다.
10. 안전한 추가/수정은 PR을 만들고 squash merge한다.
11. 모듈 대규모 재편, 대량 삭제, 라이선스 변경, 검증 실패가 있으면 자동 병합하지 않고 사용자에게 알린다.
12. 모든 변경이 실제로 병합된 뒤에만 manifest와 `last_processed_commit`을 새 upstream SHA로 갱신한다.

## 품질 기준

- 짧은 번역이 아니라 독립적으로 학습 가능한 상세 노트여야 한다.
- 확인된 사실, 해설, 검증되지 않은 부분을 구분한다.
- 기존 상세 한국어 노트를 짧은 요약으로 퇴행시키지 않는다.
- 한 번의 업데이트에서 여러 모듈이 바뀌면 모듈별 PR을 우선한다.
