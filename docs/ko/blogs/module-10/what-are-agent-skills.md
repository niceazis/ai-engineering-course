# Agent Skills란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/what-are-agent-skills  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 2026-07-30 공개 원문을 직접 확인해 SKILL.md, description trigger, 3단계 Progressive Disclosure와 MCP 비교를 반영한 독립적인 한국어 상세 해설입니다.

## 1. 왜 Skill이 필요한가

Agent에게 조직별 procedure를 매번 긴 system prompt로 넣으면 context를 낭비합니다.

Skill은 특정 작업의:

- instructions
- reference
- template
- script/code

를 하나의 folder로 패키징하고 **필요할 때만 로드**합니다.

## 2. 기본 구조

원문 예의 핵심:

    skill-name/
      SKILL.md
      reference.md   (optional)
      template...    (optional)
      script...      (optional)

SKILL.md에는 metadata와 실제 절차가 들어갑니다.

## 3. Description이 Trigger

Agent는 skill의 name/description을 보고 현재 request와 관련 있는지 판단합니다.

따라서 description은 단순 소개문이 아니라 **routing interface**입니다.

좋은 description은:

- 언제 사용
- 어떤 입력/task
- 주요 scope

가 분명해야 합니다.

## 4. Progressive Disclosure

원문은 세 level로 설명합니다.

### Level 1

항상 name + description만 로드.

### Level 2

Task와 match하면 full SKILL.md body를 읽음.

### Level 3

본문이 reference/template/script를 가리키면 실제 필요할 때만 추가 file을 읽음.

즉 deep knowledge가 context를 차지하는 시점을 늦춥니다.

## 5. Context Engineering 관점

50개의 skill이 있어도 full instruction 50개를 동시에 넣지 않습니다.

    catalog metadata
      → semantic match
      → one/few skill load
      → extra file on demand

Agent toolset이 커질수록 이 pattern이 중요합니다.

## 6. Skill에 Code를 넣는 이유

자연어 instruction만으로 exact/repeatable 작업이 어려운 경우 script를 포함할 수 있습니다.

예:

- file converter
- validator
- formatter
- deterministic report generator

AI가 판단하고 code가 정확한 계산/변환을 담당하는 구조가 좋습니다.

## 7. Project Skill과 Personal Skill

원문은 project 안에 skill을 두면 repository/team과 함께 공유되고, personal location의 skill은 개인 workflow에 사용할 수 있는 형태를 설명합니다.

정확한 path와 지원 범위는 사용하는 agent 제품의 현재 문서를 확인해야 합니다.

## 8. Skill vs MCP

원문의 핵심 구분:

    MCP = reach
    Skill = know-how

MCP:

- DB/API/file 같은 capability 연결

Skill:

- 그 capability를 **언제 어떻게 써야 하는지 procedure** 제공

Skill이 MCP tool을 호출하는 workflow를 담을 수 있습니다.

## 9. 좋은 Skill 작성법

새로운 capable teammate에게 인수인계한다고 생각합니다.

포함:

- organization-specific rule
- exact workflow
- edge case
- validation
- reusable script

제외:

- model이 이미 아는 일반 상식
- 불필요한 긴 설명
- 매번 달라지는 transient data

## 10. 실패 Mode

- 너무 넓은 description → 잘못 trigger
- too narrow → 필요한데 trigger 안 됨
- huge SKILL.md → progressive disclosure 이점 감소
- stale procedure
- unsafe script/tool permission

Skill도 versioning/test가 필요합니다.

## 핵심 정리

- Agent Skill은 특정 task의 instructions·references·scripts를 folder로 묶은 reusable package입니다.
- SKILL.md의 description이 routing trigger 역할을 합니다.
- 원문은 name/description → full SKILL.md → extra files의 3단계 progressive disclosure를 설명합니다.
- Skill은 know-how, MCP는 external reach라는 차이가 핵심입니다.
- Skill이 많아질수록 context loading과 versioning discipline이 중요합니다.

## 원문

- https://outcomeschool.com/blog/what-are-agent-skills
