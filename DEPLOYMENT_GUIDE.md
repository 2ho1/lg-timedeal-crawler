# 클라우드 배포 가이드

컴퓨터가 꺼져있어도 동작하도록 클라우드 서버에 배포하는 방법입니다.

## 추천 무료 서비스

### 1. Railway (추천) ⭐
- **무료 티어**: $5 크레딧/월 (충분함)
- **장점**: 설정 간단, 자동 배포
- **단점**: 크레딧 소진 시 중단

### 2. Render
- **무료 티어**: 있음 (15분 비활성 시 슬립)
- **장점**: 무료, 안정적
- **단점**: 슬립 모드 때문에 첫 실행이 느릴 수 있음

### 3. Fly.io
- **무료 티어**: 있음
- **장점**: 빠름, 안정적
- **단점**: 설정이 조금 복잡

### 4. PythonAnywhere
- **무료 티어**: 있음
- **장점**: Python 전용, 간단
- **단점**: 무료는 외부 URL 접근 제한

## Railway 배포 방법 (가장 추천)

### 1. Railway 계정 생성
1. https://railway.app 접속
2. GitHub로 로그인
3. "New Project" 클릭

### 2. 프로젝트 준비
GitHub에 코드를 푸시해야 합니다.

### 3. Railway에 배포
1. Railway 대시보드에서 "New Project" → "Deploy from GitHub repo"
2. 저장소 선택
3. 자동으로 배포 시작

### 4. 환경 변수 설정
Railway 대시보드에서:
- `TELEGRAM_BOT_TOKEN` 추가
- `TELEGRAM_CHAT_ID` 추가
- `LG_TIMEDEAL_URL` 추가 (선택)
- `PRIORITY_PRODUCTS` 추가 (선택)

### 5. 필요한 파일 추가
Railway 배포를 위해 다음 파일들이 필요합니다.

