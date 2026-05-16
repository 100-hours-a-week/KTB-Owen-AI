# 1주차 1번과제 제출 -> 1번과 2번 통합

- cli 프로그램 만들기
- (선택) 비동기 사용해보는 방향으로 리펙토링

### 설명
> 기상청 API과 텔레그램 봇연동을 통해 cli명령만으로 원하는 지역의 날씨와 가벼운 조언을 해주는 프로그램 
> todayW 판교 -> kanana로 브리핑 생성후 텔레그램 전송 

### 사용법
```txt

todayW 도시명(강남구) -> 날씨와 ai의 조언이 텔레그램에 전송
todayW where 지역명(서울시) -> 지역명(서울시 전체) 출력

```

- 가상환경 세팅 : uv환경을 사용하겠음
- 개인적으로 cpu에서 품질이 괜찮았던 모델인 kanana-nano를 사용하였음 
- instruct 모델이라 chat 형식의 프롬프트를 사용하였음 

### 봇 발급법
- CHAT_ID
    - @userinfobot 에 채팅보내면 알려줌
- Bot
    - 텔레그램에 봇파더에서 봇 토큰을 발급받기
    - 만든 봇에 메시지 보내기 

### 초기설정

```cmd
uv venv
source .venv/bin/activate
uv pip install huggingface-hub
hf download ch00n/kanana-nano-2.1b-instruct-Q4_K_M-GGUF
```
### 성능 테스트 
```txt
속도 측정, bench.py 만들어서 했음 -> 둘다 거의 실시간 
M4 Pro + Metal 가속 : 90.9 TPS 
CPU : 85.0 TPS
```

### 테스트 이미지 
- 이미지 1 -> 실제 cli 호출
    - 이미지 안뜨는 경우 "../01/IMG/CMD_IMG.png" 에 존재
<img src="../01/IMG/CMD_IMG.png" width="600">

- 이미지 2 -> 실제 텔레그램 전송
    - 이미지 안뜨는 경우 "../01/IMG/telegram_IMG.png" 에 존재 
<img src="../01/IMG/telegram_IMG.png" width="300">