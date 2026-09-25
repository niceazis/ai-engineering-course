# OKF(Open Knowledge Format)란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/what-is-okf-open-knowledge-format  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 bundle, Markdown/YAML frontmatter, type 필수 field, cross-link graph와 MCP/Skill 관계를 독립적으로 정리했습니다.

## 1. OKF가 해결하는 문제

Agent가 data source에 접근할 수 있어도 다음을 모를 수 있습니다.

- table의 의미
- metric 정의
- 어떤 column이 canonical인지
- business term 관계
- data owner/freshness

Tool access와 domain knowledge는 다릅니다.

OKF는 이런 **data knowledge/semantics를 plain Markdown로 정리**하는 format입니다.

## 2. OKF의 핵심

원문의 요약:

    OKF = Open + Knowledge + Format

실제 row/data를 저장하는 format이 아니라:

> 데이터와 개념이 무엇을 의미하는지를 설명하는 knowledge layer.

## 3. Bundle

OKF file collection을 bundle이라고 부릅니다.

원문 예:

    sales/
      index.md
      datasets/
      tables/
        orders.md
        customers.md
      metrics/
        weekly_active_users.md

File path 자체가 concept identity 역할을 합니다.

## 4. 파일 구조

각 Markdown file:

    ---
    type: BigQuery Table
    title: Orders
    description: ...
    ---

    # Orders
    ...

처럼 YAML frontmatter + Markdown body로 구성됩니다.

원문 기준 required field:

    type

Optional agreed fields:

- title
- description
- resource
- tags
- timestamp

등입니다.

## 5. 왜 Plain Markdown인가

- 사람이 바로 읽을 수 있음
- Git diff/versioning
- 특별한 DB 없이 사용 가능
- LLM이 자연스럽게 읽음
- editor/CI ecosystem 활용

Format이 단순해 knowledge가 특정 vendor에 묶이지 않는 것이 목적입니다.

## 6. Cross-Link가 Graph를 만든다

Ordinary Markdown link:

    `[Orders](../tables/orders.md)`

를 사용하면 concept 간 relationship을 표현할 수 있습니다.

여러 file link가 모여 agent가 탐색할 수 있는 knowledge graph처럼 동작합니다.

## 7. Agent의 사용 방식

Task:

    "WAU 계산 SQL 작성"

Agent는:

1. OKF metric definition
2. 관련 table link
3. column semantics
4. source resource

를 읽고 실제 query/tool을 사용합니다.

단순 schema introspection보다 business meaning을 더 정확히 이해할 수 있습니다.

## 8. MCP / Skills / OKF

원문 한 줄 구분:

    MCP    = reach
    Skills = know-how
    OKF    = knowledge

예:

- MCP: BigQuery query 실행 capability
- OKF: orders table/metric 의미
- Skill: weekly report 작성 procedure

세 층을 조합하면 agent가 tool과 domain context를 함께 갖습니다.

## 9. 장점

- domain knowledge를 repository artifact로 관리
- 사람과 AI가 같은 source 사용
- code review 가능
- vendor-neutral
- cross-link navigation
- stale knowledge를 version control에서 추적

## 10. 한계

OKF file이 오래되면 agent도 잘못 판단합니다.

따라서:

- owner
- timestamp/version
- CI validation
- broken link check
- source-of-truth sync

가 필요합니다.

## 핵심 정리

- OKF는 actual data가 아니라 data의 의미와 관계를 Markdown으로 기록합니다.
- Bundle은 plain folder이며 file path가 concept identity입니다.
- YAML frontmatter에서 원문 기준 type이 유일한 필수 field입니다.
- Markdown link가 concept graph를 만듭니다.
- MCP=reach, Skills=know-how, OKF=knowledge라는 역할 구분이 핵심입니다.

## 원문

- https://outcomeschool.com/blog/what-is-okf-open-knowledge-format
