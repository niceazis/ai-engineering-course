# System Design이란? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/system-design  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 functional/non-functional requirements, trade-off, scalability·availability·latency·consistency, API·DB·cache·load balancing의 큰 흐름을 보존하면서 독립적으로 다시 쓴 한국어 상세 해설입니다.

## 1. System Design의 정의

원문 정의:

> System Design은 특정 functional / non-functional requirements를 만족하도록 component, API, database table 등을 설계하는 과정입니다.

즉 단일 algorithm이 아니라 **전체 시스템의 구성 요소와 관계를 설계하는 작업**입니다.

## 2. System + Design

원문은 다음처럼 분해합니다.

### System

요구사항을 만족하기 위해 여러 component를 조합한 것.

### Design

그 component를 얼마나 효율적으로 조합하는가.

따라서 system design은 "어떤 기술을 아는가"보다 **어떤 trade-off를 선택하는가**가 중요합니다.

## 3. Functional Requirement

사용자가 시스템에서 실제로 할 수 있어야 하는 기능입니다.

원문 Instagram 예:

- image upload
- like
- share
- comment

YouTube 예:

- upload video
- view
- like
- comment
- search
- subscribe

이런 요구사항이 API와 data model의 출발점이 됩니다.

## 4. Non-Functional Requirement

원문 Instagram 예:

- image가 유실되지 않아야 함
- downtime이 없어야 함
- 쉽게 scale해야 함

또 일반적으로:

- low latency
- availability
- durability
- consistency
- security
- throughput

같은 성질을 정의합니다.

## 5. Trade-off

원문은 "모든 것을 동시에 완벽하게" 만들 수 없다는 점을 강조합니다.

예:

Instagram에서:

- image rendering latency는 매우 중요
- comment count가 여러 server에서 잠시 다르게 보이는 것은 허용 가능

즉 일부 data는 eventual consistency를 허용하고 user-facing media path는 latency를 우선할 수 있습니다.

## 6. 왜 System Design이 필요한가

원문 목표:

- 쉽게 scale
- no downtime
- low latency
- server redundancy
- data consistency
- load distribution
- component reuse
- system-wide efficiency

사용자 수가 늘어도 기존 architecture가 무너지지 않아야 합니다.

## 7. Scaling

### Vertical Scaling

한 machine의 CPU/RAM을 키웁니다.

장점:

- 단순

단점:

- hardware 한계
- single-machine risk

### Horizontal Scaling

Server instance를 여러 개 추가합니다.

장점:

- large-scale traffic에 유리
- redundancy

단점:

- distributed state
- synchronization
- load balancing 필요

## 8. Availability

한 server가 죽어도 서비스가 계속 동작하려면:

    multiple replicas
      + health check
      + failover
      + load balancer

가 필요합니다.

"No downtime"은 실제로는 명확한 availability SLO로 정의해야 합니다.

## 9. Latency

API latency는:

- network
- database
- cache miss
- downstream service
- computation

의 합입니다.

평균뿐 아니라 p95/p99 tail latency를 보는 것이 중요합니다.

## 10. Consistency

여러 replica에 같은 data가 있을 때 즉시 같은 값이 보여야 하는지 결정해야 합니다.

강한 consistency:

- correctness 우선
- latency/availability 비용 가능

Eventual consistency:

- replica가 나중에 동기화
- scale/availability에 유리

Use case별 판단이 필요합니다.

## 11. Capacity Estimation

원문은 system design에서 estimation이 필요하다고 설명합니다.

대표 추정:

- DAU/MAU
- requests/sec
- read/write ratio
- object size
- storage growth
- network bandwidth

이 숫자가 DB/shard/cache architecture를 결정합니다.

## 12. Database Design

질문:

- relational vs NoSQL
- partition key
- index
- replication
- transaction boundary

를 요구사항에 맞춰 결정합니다.

Database 선택은 유행이 아니라 access pattern에서 시작해야 합니다.

## 13. API Design

Functional requirement를 interface로 바꿉니다.

예:

    POST /images
    GET /feed
    POST /comments

실제 design에서는:

- idempotency
- pagination
- authentication
- rate limit
- versioning

까지 봅니다.

## 14. Storage

Image/video 같은 large object는 relational DB row에 그대로 넣기보다 object storage + metadata DB 구조가 일반적입니다.

Data type에 맞는 storage를 선택합니다.

## 15. Caching

Hot data를 cache해:

- latency 감소
- DB load 감소

를 노립니다.

하지만 stale data, invalidation, cache stampede를 고려해야 합니다.

## 16. Load Balancing

Traffic을 여러 server에 분산합니다.

    clients
      → load balancer
      → server A/B/C

Health check와 routing policy가 중요합니다.

## 17. AI System Design과 연결

AI system은 전통적 component에 다음이 추가됩니다.

- model gateway
- vector DB
- GPU serving
- prompt cache
- agent/tool runtime
- evaluation/observability

하지만 기본 원칙은 같습니다.

> requirement → estimate → component → trade-off → failure handling

## 핵심 정리

- System Design은 functional/non-functional requirements를 만족하도록 전체 component와 관계를 설계하는 과정입니다.
- 원문은 scalability, no downtime, low latency, consistency, load distribution을 핵심 목표로 봅니다.
- 모든 목표는 trade-off가 있으며 use case에 따라 우선순위를 정해야 합니다.
- estimation, database, API, storage, cache, load balancer가 기본 building block입니다.
- AI system design도 결국 같은 distributed-system 원칙 위에 model-specific component가 추가된 형태입니다.

## 원문

- https://outcomeschool.com/blog/system-design
