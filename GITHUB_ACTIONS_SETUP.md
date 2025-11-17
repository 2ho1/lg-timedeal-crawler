# GitHub Actions로 자동 실행 설정하기

GitHub Actions를 사용하면 **완전 무료**로 매일 자동 실행할 수 있습니다!

## 장점
- ✅ 완전 무료
- ✅ 컴퓨터가 꺼져있어도 동작
- ✅ GitHub에 코드만 푸시하면 자동 실행
- ✅ 설정 간단

## 설정 방법

### 1. GitHub 저장소 생성
1. GitHub에 로그인
2. "New repository" 클릭
3. 저장소 이름 입력 (예: `lg-timedeal-crawler`)
4. "Create repository" 클릭

### 2. 코드 푸시
```bash
cd /Users/1004368/Desktop/cursor/LG
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/당신의사용자명/lg-timedeal-crawler.git
git push -u origin main
```

### 3. GitHub Secrets 설정
1. GitHub 저장소 페이지로 이동
2. "Settings" → "Secrets and variables" → "Actions" 클릭
3. "New repository secret" 클릭하여 다음 추가:

**필수:**
- `TELEGRAM_BOT_TOKEN`: `8083041139:AAGG_0xGmjWg1QEpWfrdtwLPJmvFkjlCnxA`
- `TELEGRAM_CHAT_ID`: `182163864`

**선택 (기본값 사용 가능):**
- `LG_TIMEDEAL_URL`: `https://www.lge.co.kr/benefits/exhibitions/detail-PE00385001`
- `PRIORITY_PRODUCTS`: `42C5,42C4,48C5,48C4`

### 4. 수동 테스트 실행
1. 저장소 페이지에서 "Actions" 탭 클릭
2. "LG Time Deal Daily Crawl" 워크플로우 선택
3. "Run workflow" 버튼 클릭
4. 실행 결과 확인

### 5. 자동 실행 확인
- 매일 오전 9시(한국 시간)에 자동 실행됩니다
- "Actions" 탭에서 실행 내역을 확인할 수 있습니다

## 실행 시간 변경
`.github/workflows/daily-crawl.yml` 파일에서 cron 시간을 변경할 수 있습니다:
- `0 0 * * *` = UTC 00:00 (한국 시간 09:00)
- `0 1 * * *` = UTC 01:00 (한국 시간 10:00)
- 등등...

## 문제 해결
- 실행이 실패하면 "Actions" 탭에서 로그 확인
- Secrets가 제대로 설정되었는지 확인
- Playwright 설치가 실패하면 로그 확인

