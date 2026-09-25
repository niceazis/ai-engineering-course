# Voice/Video Call은 어떻게 동작하는가? — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/voice-and-video-call  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: Outcome School 원문을 직접 확인해 WebRTC, Signaling, STUN, TURN, NAT, peer-to-peer media flow를 보존하면서 현대적인 ICE 관점을 보완한 독립적인 한국어 상세 해설입니다.

## 1. 전체 문제

Voice/video call은 두 client 사이에 low-latency media를 실시간으로 전달해야 합니다.

핵심 구성:

- Signaling
- WebRTC media connection
- STUN
- TURN

원문은 이 네 요소를 중심으로 설명합니다.

## 2. WebRTC

WebRTC는 browser/mobile application에 real-time audio/video/data communication capability를 제공합니다.

하지만 WebRTC 자체가 모든 call setup을 해결하는 것은 아닙니다.

특히 signaling protocol은 application이 별도로 구현합니다.

## 3. Signaling

Call을 시작하기 전에 두 peer는 다음 정보를 교환해야 합니다.

- session description
- media capability
- network candidate
- call accept/reject
- metadata

원문은 signaling transport의 예로 WebSocket을 언급합니다.

Signaling은 **media transport 자체가 아니라 연결을 협상하는 control plane**입니다.

## 4. Peer-to-Peer 목표

가능하면 media는:

    Client A
      ⇄
    Client B

로 직접 전달하는 것이 latency와 server bandwidth 측면에서 유리합니다.

하지만 NAT/firewall 때문에 직접 연결이 항상 가능한 것은 아닙니다.

## 5. NAT 문제

대부분 device는 private IP를 사용합니다.

Router/NAT가 public internet과 private network 사이 address/port mapping을 만듭니다.

Peer는 단순히 상대 private IP를 알아도 internet에서 직접 접근할 수 없습니다.

## 6. STUN

원문은 STUN server를 client가 외부에서 보이는 public-facing address를 알아내는 데 사용하는 component로 설명합니다.

Client는 STUN request를 보내 자신의 NAT mapping 정보를 확인합니다.

현대 WebRTC에서는 ICE candidate gathering 과정의 일부로 이해하는 것이 정확합니다.

## 7. ICE

실제 WebRTC connection은 여러 candidate를 수집하고 connectivity check를 수행합니다.

Candidate 예:

- host candidate
- server-reflexive candidate via STUN
- relay candidate via TURN

그중 연결 가능한 최적 path를 선택합니다.

원문의 STUN→P2P 설명을 현대적으로 확장하면 ICE가 전체 orchestration을 담당한다고 볼 수 있습니다.

## 8. TURN

P2P가 실패하면 TURN server가 media relay 역할을 합니다.

    Client A
      → TURN
      → Client B

원문 표현대로 TURN은 한 client의 data를 받아 다른 client에 전달하는 mediator입니다.

## 9. TURN의 비용

TURN을 사용하면 media traffic이 server를 통과합니다.

따라서:

- server bandwidth 비용
- 추가 latency
- relay capacity planning

이 필요합니다.

그래서 가능한 경우 direct P2P를 선호합니다.

## 10. Signaling과 Media 분리

원문은 call 종료, setting 변경 같은 small control data가 signaling channel로 갈 수 있다고 설명합니다.

반면 audio/video RTP media는 WebRTC media path를 사용합니다.

즉:

    signaling = control
    WebRTC media = real-time payload

입니다.

## 11. Call Setup Step-by-Step

1. Caller가 signaling server에 call 요청
2. Callee가 accept
3. SDP/candidate 교환
4. STUN을 통해 NAT mapping 확인
5. ICE connectivity check
6. direct path 성공 시 P2P
7. 실패하면 TURN relay
8. audio/video stream
9. hangup/control event는 signaling으로 전달

## 12. 보안

WebRTC media는 일반적으로 encrypted transport를 사용합니다.

Production에서는:

- identity/authentication
- signaling authorization
- TURN credential
- abuse/rate limit
- recording consent

도 별도로 관리해야 합니다.

## 13. Voice AI Agent와 연결

사람↔AI voice call에서도 WebRTC는 client audio transport로 사용할 수 있습니다.

차이는 peer가 다른 사람이 아니라:

    browser/mobile
      ⇄
    Voice AI media backend

일 수 있다는 점입니다.

VAD/STT/LLM/TTS layer가 WebRTC 위에 추가됩니다.

## 핵심 정리

- WebRTC는 real-time media를 담당하지만 signaling은 별도입니다.
- STUN은 NAT 환경에서 외부 address/candidate 발견을 돕습니다.
- ICE가 candidate를 비교해 실제 연결 path를 선택합니다.
- Direct P2P가 안 되면 TURN이 media를 relay합니다.
- TURN은 안정성을 높이지만 server bandwidth와 latency 비용이 큽니다.

## 원문

- https://outcomeschool.com/blog/voice-and-video-call
