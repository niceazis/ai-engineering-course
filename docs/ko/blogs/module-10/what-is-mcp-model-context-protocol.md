# MCP(Model Context Protocol)란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/what-is-mcp-model-context-protocol  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인하고 MCP의 client/server 표준화 역할을 독립적으로 설명합니다. 프로토콜의 현재 세부 사양은 MCP 공식 문서를 우선해야 합니다.

## 1. MCP 이전의 문제

AI app마다 외부 system integration을 따로 만들면:

    Agent A × GitHub
    Agent A × DB
    Agent B × GitHub
    Agent B × DB

처럼 N×M connector 문제가 생깁니다.

MCP는 tool/data provider가 표준 server interface를 제공하고 AI host/client가 이를 공통 방식으로 사용하도록 합니다.

## 2. 이름 분해

### Model

LLM/AI application.

### Context

Model이 작업에 사용할 external data, resources, tools.

### Protocol

서로 다른 software가 통신하는 공통 규칙.

## 3. USB-C 비유의 의미

Outcome School은 MCP를 USB-C처럼 설명합니다.

핵심은 "모든 기능을 MCP가 실행한다"가 아니라 **서로 다른 host와 provider 사이의 연결 contract를 표준화**한다는 것입니다.

## 4. 구성 요소

실용적으로:

### MCP Host

AI application/IDE/agent runtime.

### MCP Client

Host 안에서 server와 protocol session을 관리.

### MCP Server

외부 capability를 MCP interface로 노출.

Server는 local process일 수도 remote service일 수도 있습니다.

## 5. 제공 Capability

MCP server는 사양에 따라 tools/resources/prompts 등의 capability를 노출할 수 있습니다.

Agent는 server가 제공하는 metadata를 보고 사용할 수 있는 기능을 발견합니다.

## 6. Request Flow

    AI host
      → MCP client
      → server capability discovery
      → model sees tool/resource metadata
      → model selects action
      → host/client sends protocol request
      → server executes
      → structured result
      → model context

## 7. 일반 REST API와 차이

REST API는 service-specific endpoint contract입니다.

MCP는 AI client가 다양한 server를 **공통 discovery/call pattern**으로 사용할 수 있게 하는 protocol layer입니다.

MCP server 내부에서 실제 REST/DB/file API를 호출할 수 있습니다.

## 8. Security Boundary

MCP가 표준이라고 자동으로 안전해지는 것은 아닙니다.

확인:

- server trust
- authentication
- allowed tools
- filesystem scope
- network access
- secrets
- destructive action confirmation

Tool description 또한 prompt injection surface가 될 수 있습니다.

## 9. Local Server

예:

    filesystem server
      → 특정 workspace 파일만 read/write

Host는 전체 disk가 아니라 허용된 root를 server permission으로 제한할 수 있습니다.

## 10. Remote Server

Remote MCP는 네트워크 authentication/authorization, transport security, tenant isolation이 추가로 중요합니다.

## 11. MCP와 Agent Skills

MCP:

    외부 capability/data 연결 protocol

Agent Skill:

    특정 작업의 instructions/procedure/code package

Skill이 MCP tool을 사용하는 workflow를 가르칠 수 있습니다. 둘은 대체재가 아닙니다.

## 핵심 정리

- MCP는 AI host와 tool/data provider 사이 연결을 표준화합니다.
- Host/Client/Server 구조와 capability discovery가 핵심입니다.
- MCP는 외부 API를 대체하기보다 AI-facing integration layer를 표준화합니다.
- 실제 tool 실행과 permission은 server/runtime에 남습니다.
- Agent Skills는 procedure, MCP는 capability connection이라는 역할 차이가 있습니다.

## 원문

- https://outcomeschool.com/blog/what-is-mcp-model-context-protocol
