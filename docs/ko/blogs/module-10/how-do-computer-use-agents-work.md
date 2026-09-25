# Computer-Use Agent는 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/how-do-computer-use-agents-work  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 Perceive→Think→Act loop, screenshot perception, mouse/keyboard action과 safety를 독립적으로 정리했습니다.

## 1. 정의

Computer-Use Agent는 API가 아니라 **사람처럼 화면을 보고 GUI를 조작**해 작업을 수행하는 agent입니다.

가능한 action:

- click
- type
- scroll
- drag
- key press
- screenshot

Legacy desktop/web app처럼 전용 API가 없는 환경에서도 사용할 수 있습니다.

## 2. Perceive-Think-Act

원문의 기본 loop:

    Perceive
      → Think
      → Act
      → screen changes
      → Perceive again

### Perceive

현재 screenshot/UI state를 읽음.

### Think

목표와 화면을 비교해 next single action 결정.

### Act

mouse/keyboard action 실행.

## 3. Screen Perception

두 방식이 있습니다.

### Vision/Screenshot

Pixel 이미지를 multimodal model이 해석.

장점: 어떤 GUI에도 적용 가능.

단점: 작은 text/좌표 오류.

### Structured Accessibility/DOM

가능한 환경에서는 accessibility tree/DOM을 사용해 element metadata를 얻을 수 있습니다.

더 정확하지만 모든 app에서 사용할 수 있는 것은 아닙니다.

Hybrid가 강합니다.

## 4. Coordinate Action

Vision agent는:

    click(x, y)

같은 coordinate를 출력할 수 있습니다.

화면 resolution, scaling, scroll 변화로 target이 움직일 수 있어 action 후 반드시 다시 screenshot을 봐야 합니다.

## 5. Example

목표:

    웹사이트에서 invoice PDF 다운로드

Loop:

1. screenshot
2. login button click
3. screenshot
4. credentials type
5. dashboard 확인
6. invoices 메뉴 click
7. 원하는 row 선택
8. download
9. file existence 검증

각 action 뒤 state가 실제로 바뀌었는지 확인합니다.

## 6. Why API보다 느린가

API:

    one structured request

Computer use:

    perceive/action round trip 여러 번

따라서 가능한 경우 안정적인 API/tool이 GUI automation보다 우선입니다.

GUI는 API가 없거나 인간 UI 자체를 사용해야 할 때 fallback로 적합합니다.

## 7. Safety

GUI agent는 실제 side effect가 큽니다.

특히:

- purchase
- delete
- send
- publish
- permission change

전에는 confirmation/approval boundary가 필요합니다.

## 8. Guardrail

- domain allowlist
- credential isolation
- action allowlist
- max steps
- transaction limit
- destructive-action confirmation
- screenshot/log audit
- prompt-injection defense

화면 안의 악성 instruction을 system instruction보다 높은 권한으로 해석하면 안 됩니다.

## 9. 실패 Mode

- wrong element click
- stale screenshot
- popup/modal
- scrolling miss
- dynamic layout
- CAPTCHA
- unexpected login/MFA
- download not completed

Action success를 visual/DOM/file state로 검증해야 합니다.

## 10. Human-in-the-Loop

High-risk step에서:

    agent proposes action
      → user approves
      → execute

pattern을 사용합니다.

Autonomy level을 task risk에 맞게 조절해야 합니다.

## 핵심 정리

- Computer-use agent는 화면을 인식하고 mouse/keyboard action을 반복합니다.
- 원문 핵심 loop는 Perceive→Think→Act입니다.
- Screenshot vision과 structured DOM/accessibility를 조합할 수 있습니다.
- API보다 느리고 brittle하므로 API가 있으면 API가 우선입니다.
- 실제 side effect 때문에 confirmation, permission, action verification이 필수입니다.

## 원문

- https://outcomeschool.com/blog/how-do-computer-use-agents-work
