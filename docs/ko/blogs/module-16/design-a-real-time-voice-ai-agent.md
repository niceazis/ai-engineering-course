# 실시간 Voice AI Agent 설계 — 한국어 상세 학습 노트

> 원문: https://outcomeschool.com/blog/design-a-real-time-voice-ai-agent  
> 원저자: Amit Shekhar / Outcome School  
> 문서 성격: 원문 URL은 현재 직접 열리지 않았습니다. Outcome School 공식 홈페이지의 2026-09-16 게시 설명, 공식 AI Agents tutorial index, 공개 원문 캐시에서 확인 가능한 transport/AEC 세부사항을 교차검증해 독립적으로 재구성했습니다. 자막/원문 전체를 확인하지 못한 세부 수치는 원문 내용으로 단정하지 않습니다.

## 1. Voice AI Agent란?

실시간 voice agent는:

    listen
      → understand
      → reason/tool use
      → speak

를 사람이 대화한다고 느낄 정도로 짧은 latency 안에 반복하는 system입니다.

Text chatbot보다 훨씬 어렵습니다.

이유:

- continuous audio
- turn detection
- interruption
- acoustic noise
- STT/TTS latency
- tool latency
- telephony/network jitter

가 동시에 존재하기 때문입니다.

## 2. 요구사항

대표적인 success criteria:

- 자연스러운 turn-taking
- 낮은 first-response latency
- interruption 즉시 반응
- tool call 가능
- session context 유지
- thousands of concurrent sessions
- privacy/security
- observable and evaluable

## 3. High-Level Architecture

Cascaded architecture:

    microphone
      → audio transport
      → VAD / turn detection
      → STT
      → LLM + tools
      → TTS
      → audio stream

Speech-to-speech architecture:

    audio
      → multimodal speech model
      → audio

Hybrid는 두 방식을 상황에 따라 조합합니다.

## 4. Audio Transport

Browser/mobile에서 real-time media transport에는 WebRTC가 잘 맞습니다.

공개 원문 캐시는 audio가 약 20ms chunk 단위로 server에 stream되는 예를 설명합니다.

WebRTC 장점:

- low-latency media
- jitter handling
- NAT traversal ecosystem
- encryption
- AEC support

## 5. Acoustic Echo Cancellation

Agent speaker output이 사용자의 microphone에 다시 들어가면 system이 자기 목소리를 user speech로 오인할 수 있습니다.

AEC는:

    microphone signal
      - known speaker output
      → user voice

를 얻는 방향으로 echo를 줄입니다.

Barge-in이 제대로 동작하려면 매우 중요합니다.

## 6. Voice Activity Detection

VAD는 현재 audio에 speech가 있는지 판단합니다.

Device에서 작은 VAD를 돌리면:

- silent audio 전송 감소
- privacy/traffic 개선
- 빠른 interruption detection

에 도움이 됩니다.

## 7. Turn Detection

VAD만으로는 사용자가 잠깐 쉬는 것인지 발화를 끝낸 것인지 구분하기 어렵습니다.

Turn detection은:

- silence duration
- prosody
- semantic completeness
- model prediction

을 조합할 수 있습니다.

너무 빨리 끊으면 user를 interrupt하고, 너무 늦으면 대화가 답답해집니다.

## 8. Speech-to-Text

Cascaded pipeline에서는 streaming STT가 partial transcript를 지속적으로 냅니다.

예:

    "I want to book..."
      → partial transcript
      → final transcript

LLM을 final transcript까지 무조건 기다리지 않고 partial context를 활용하는 최적화도 가능합니다.

## 9. LLM + Tools

LLM은 단순 답변뿐 아니라 tool call을 결정합니다.

예:

    "내일 오후 3시에 예약해줘"
      → calendar availability
      → booking tool
      → confirmation

Tool latency가 voice UX 전체에 직접 영향을 줍니다.

## 10. Text-to-Speech

TTS는 전체 문장이 완성될 때까지 기다리지 않고 streaming synthesis를 할 수 있습니다.

    LLM token stream
      → phrase chunk
      → TTS
      → audio

이렇게 하면 perceived latency를 줄일 수 있습니다.

## 11. Cascaded Pipeline

    STT → LLM → TTS

장점:

- 각 component 교체 쉬움
- text transcript와 tool integration 쉬움
- observability 좋음

단점:

- 각 stage latency가 누적
- prosody/emotion 정보 손실 가능

## 12. Speech-to-Speech

Audio를 직접 이해하고 audio로 응답합니다.

장점:

- 낮은 latency 가능
- emotion/prosody 보존
- 자연스러운 interruption

단점:

- tool/control integration이 더 복잡할 수 있음
- debugging과 audit가 어려울 수 있음

## 13. Hybrid

예:

- normal conversation → speech-to-speech
- transaction/tool call → text reasoning/tool pipeline

처럼 역할을 나눌 수 있습니다.

## 14. Latency Budget

Total response latency:

    network
    + turn detection
    + STT
    + LLM first token
    + tool call
    + TTS first audio

의 합입니다.

한 stage만 빠르게 해서는 충분하지 않습니다.

p50뿐 아니라 p95/p99를 봐야 합니다.

## 15. Barge-in

사용자가 agent가 말하는 중간에 말을 시작하면:

1. user speech 감지
2. current TTS playback 중지
3. queued audio 폐기
4. new user turn 시작
5. context에 interrupted state 반영

해야 합니다.

## 16. Telephony

일반 전화망은:

- PSTN
- SIP: call setup/control
- RTP: audio transport

를 사용해 provider가 voice stream을 software backend로 전달할 수 있습니다.

## 17. Scaling

Session마다:

- audio stream
- STT state
- LLM context
- TTS stream
- tool state

가 필요합니다.

Stateless HTTP request보다 connection/session resource 관리가 어렵습니다.

## 18. Edge Cases

- background noise
- overlapping speech
- echo
- silence
- user changes mind
- network packet loss
- STT misrecognition
- tool timeout
- TTS failure

을 별도 test case로 만들어야 합니다.

## 19. Observability

Trace에 최소:

- audio connection
- VAD/turn timing
- STT partial/final
- LLM latency
- tool calls
- TTS first-byte/first-audio
- interruption event
- total turn latency

를 기록합니다.

## 20. Safety와 Privacy

Voice data는 민감할 수 있습니다.

필수 고려:

- encryption
- retention
- PII redaction
- tool authorization
- call recording consent
- prompt injection from audio/transcript

## 핵심 정리

- Real-time voice agent는 audio transport, VAD/turn detection, STT, LLM+tools, TTS를 하나의 low-latency loop로 묶습니다.
- Cascaded, speech-to-speech, hybrid 세 architecture를 비교해야 합니다.
- Barge-in과 AEC가 자연스러운 대화의 핵심입니다.
- Total latency는 한 model이 아니라 모든 stage의 합입니다.
- 원문 URL 전체를 직접 열지 못한 부분은 Outcome School 공식 게시 설명과 공개된 기술 자료로만 보완했습니다.

## 원문

- https://outcomeschool.com/blog/design-a-real-time-voice-ai-agent
