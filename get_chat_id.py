#!/usr/bin/env python3
"""텔레그램 Chat ID 확인 스크립트"""
import requests
import json

BOT_TOKEN = "8083041139:AAGG_0xGmjWg1QEpWfrdtwLPJmvFkjlCnxA"

def get_chat_id():
    """Chat ID를 가져옵니다."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("ok"):
            print(f"❌ 오류: {data.get('description', 'Unknown error')}")
            return None
        
        updates = data.get("result", [])
        
        if not updates:
            print("⚠️  아직 봇과 대화를 시작하지 않았거나 메시지를 보내지 않았습니다.")
            print("\n다음 단계를 따라주세요:")
            print("1. 텔레그램에서 봇을 검색하세요")
            print("2. 봇과 대화를 시작하세요 (Start 버튼 클릭)")
            print("3. 봇에게 아무 메시지나 보내세요 (예: '안녕' 또는 '/start')")
            print("4. 그 다음 이 스크립트를 다시 실행하세요")
            return None
        
        # 가장 최근 메시지에서 Chat ID 추출
        latest_update = updates[-1]
        message = latest_update.get("message", {})
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        
        if chat_id:
            print(f"✅ Chat ID를 찾았습니다: {chat_id}")
            print(f"\n📝 .env 파일에 다음을 추가하세요:")
            print(f"TELEGRAM_CHAT_ID={chat_id}")
            return chat_id
        else:
            print("❌ Chat ID를 찾을 수 없습니다.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 요청 오류: {e}")
        return None
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None

if __name__ == "__main__":
    print("🔍 텔레그램 Chat ID 확인 중...\n")
    get_chat_id()

