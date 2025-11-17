# LG 타임딜 크롤링 및 텔레그램 알림 시스템

LG 전자 타임딜 페이지에서 상품 정보를 크롤링하고, 매일 오전 9시에 텔레그램으로 상품 목록을 전송하는 자동화 시스템입니다.

## 주요 기능

- LG 타임딜 페이지에서 상품 정보 자동 크롤링
- 특정 우선 상품(42C5, 42C4, 48C5, 48C4) 자동 필터링 및 상단 표시
- 매일 오전 9시 자동 실행
- 텔레그램으로 상품 정보 전송

## 설치 방법

### 1. 저장소 클론 및 이동

```bash
cd LG
```

### 2. Python 가상환경 생성 및 활성화

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 입력하세요:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
LG_TIMEDEAL_URL=https://www.lge.co.kr/benefits/exhibitions/detail-PE00385001
PRIORITY_PRODUCTS=42C5,42C4,48C5,48C4
```

#### 텔레그램 봇 설정 방법

1. 텔레그램에서 [@BotFather](https://t.me/botfather)를 검색하고 대화 시작
2. `/newbot` 명령어로 새 봇 생성
3. 봇 이름과 사용자명 설정
4. 받은 토큰을 `TELEGRAM_BOT_TOKEN`에 입력

#### Chat ID 확인 방법

1. 생성한 봇과 대화 시작 (아무 메시지나 보내기)
2. 브라우저에서 다음 URL 접속 (TOKEN을 실제 토큰으로 교체):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
3. 응답에서 `"chat":{"id":123456789}` 부분의 숫자를 `TELEGRAM_CHAT_ID`에 입력

## 사용 방법

### 1. 수동 크롤링

```bash
python main.py --mode crawl
```

### 2. 수동 알림 전송

```bash
python main.py --mode send
```

### 3. 테스트 모드 (크롤링 + 전송)

```bash
python main.py --mode crawl --test
```

### 4. 스케줄러 실행 (매일 오전 9시 자동 실행)

```bash
python main.py --mode schedule
```

백그라운드에서 실행하려면:

```bash
nohup python main.py --mode schedule > crawler.log 2>&1 &
```

## 프로젝트 구조

```
LG/
├── crawler.py          # 크롤링 로직
├── telegram_sender.py   # 텔레그램 전송 로직
├── scheduler.py        # 스케줄링 로직
├── main.py            # 메인 실행 파일
├── config.py          # 설정 관리
├── requirements.txt   # Python 패키지 의존성
├── .env               # 환경 변수 (생성 필요)
└── data/              # 크롤링 데이터 저장 디렉토리
    └── products.json  # 상품 정보 JSON 파일
```

## 우선 상품 필터링

다음 상품 코드가 포함된 상품은 메시지 상단에 우선 표시됩니다:

- 42C5 (예: OLED42C5ENA에서 매칭)
- 42C4 (예: OLED42C4ENA에서 매칭)
- 48C5 (예: OLED48C5ENA에서 매칭)
- 48C4 (예: OLED48C4ENA에서 매칭)

상품명(모델명 포함)에서 부분 문자열 매칭 방식으로 검색하므로, 모델명의 일부만 일치해도 우선 상품으로 분류됩니다.

## 문제 해결

### Playwright 브라우저 설치 오류

```bash
playwright install chromium
```

### 텔레그램 메시지가 전송되지 않는 경우

1. `.env` 파일의 토큰과 Chat ID가 올바른지 확인
2. 봇과 대화를 시작했는지 확인
3. 로그 파일을 확인하여 에러 메시지 확인

### 크롤링이 실패하는 경우

1. 인터넷 연결 확인
2. LG 웹사이트 접근 가능 여부 확인
3. 페이지 구조가 변경되었을 수 있으므로 크롤러 코드 확인 필요

## 라이선스

이 프로젝트는 개인 사용 목적으로 제작되었습니다.

