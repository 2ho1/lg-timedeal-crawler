# 텔레그램 봇 설정 가이드

## 1단계: 텔레그램 봇 생성

### 1. BotFather 찾기
1. 텔레그램 앱을 엽니다
2. 검색창에 `@BotFather`를 입력하고 검색합니다
3. **@BotFather** (공식 텔레그램 봇)을 선택합니다
4. "시작" 또는 "Start" 버튼을 클릭합니다

### 2. 새 봇 생성
1. BotFather와의 채팅창에서 `/newbot` 명령어를 입력합니다
2. BotFather가 봇 이름을 물어봅니다 (예: "LG 타임딜 알림봇")
3. 원하는 이름을 입력합니다
4. 다음으로 봇 사용자명을 물어봅니다 (예: "lg_timedeal_bot")
   - 사용자명은 반드시 `bot`으로 끝나야 합니다
   - 이미 사용 중인 이름이면 다른 이름을 시도해야 합니다
5. 성공하면 BotFather가 **봇 토큰**을 제공합니다
   - 예: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
   - 이 토큰을 복사해두세요!

### 3. 봇 토큰 확인 (나중에 필요할 때)
- `/token` 명령어를 입력하면 현재 봇의 토큰을 다시 볼 수 있습니다

## 2단계: Chat ID 확인

### 방법 1: 봇과 대화 후 API로 확인 (권장)

1. **봇과 대화 시작**
   - 텔레그램 검색창에서 방금 만든 봇의 사용자명을 검색합니다 (예: `@lg_timedeal_bot`)
   - 봇을 선택하고 "시작" 또는 "Start" 버튼을 클릭합니다
   - 아무 메시지나 보냅니다 (예: "안녕")

2. **Chat ID 확인**
   - 브라우저를 엽니다
   - 주소창에 다음 URL을 입력합니다 (YOUR_BOT_TOKEN을 실제 토큰으로 교체):
     ```
     https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
     ```
   - 예시:
     ```
     https://api.telegram.org/bot1234567890:ABCdefGHIjklMNOpqrsTUVwxyz/getUpdates
     ```
   - 페이지가 열리면 JSON 형식의 데이터가 보입니다
   - 다음 부분을 찾습니다:
     ```json
     "chat":{"id":123456789,"first_name":"Your","type":"private"}
     ```
   - `"id":` 뒤의 숫자 (예: `123456789`)가 **Chat ID**입니다

### 방법 2: @userinfobot 사용

1. 텔레그램에서 `@userinfobot`을 검색합니다
2. 봇을 시작하고 `/start` 명령어를 보냅니다
3. 봇이 당신의 Chat ID를 알려줍니다

## 3단계: .env 파일 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 입력합니다:

```env
TELEGRAM_BOT_TOKEN=여기에_봇_토큰_입력
TELEGRAM_CHAT_ID=여기에_Chat_ID_입력
LG_TIMEDEAL_URL=https://www.lge.co.kr/benefits/exhibitions/detail-PE00385001
PRIORITY_PRODUCTS=42C5,42C4,48C5,48C4
```

### 예시:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
LG_TIMEDEAL_URL=https://www.lge.co.kr/benefits/exhibitions/detail-PE00385001
PRIORITY_PRODUCTS=42C5,42C4,48C5,48C4
```

## 4단계: 테스트

설정이 완료되면 다음 명령어로 테스트합니다:

```bash
source venv/bin/activate
python main.py --mode crawl --test
```

## 문제 해결

### 봇 토큰을 잃어버렸어요
- BotFather와의 채팅에서 `/token` 명령어를 입력하세요

### Chat ID를 찾을 수 없어요
- 봇과 대화를 시작했는지 확인하세요
- `getUpdates` URL에서 토큰이 올바른지 확인하세요
- 봇에게 메시지를 보낸 후 다시 시도하세요

### 메시지가 전송되지 않아요
- `.env` 파일의 토큰과 Chat ID가 올바른지 확인하세요
- 봇과 대화를 시작했는지 확인하세요
- 봇 토큰에 공백이나 따옴표가 없는지 확인하세요

