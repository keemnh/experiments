from openai import OpenAI
import requests
from datetime import datetime

# ✅ GPT 설정 (OpenAI API Key)
client = OpenAI(api_key=" ")     ###  <- 여기에 OpenAPI Key

# ✅ Notion 설정
NOTION_TOKEN = "  "    ## <- 여기에 노션 토큰
DATABASE_ID = "     "    ## <- 여기에 노션 db id
 
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# ✅ 질문 리스트
questions = [
    "What is RTOS?",
    "Explain BLE sniffing.",
    "What is prompt injection in LLMs?"
]

# ✅ 메인 루프
for q in questions:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": q}]
    )
    answer = response.choices[0].message.content

    # Notion에 보낼 데이터 구성
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {
                "title": [{"text": {"content": q}}]
            },
            "Response": {
                "rich_text": [{"text": {"content": answer}}]
            },
            "Timestamp": {
                "date": {"start": datetime.now().isoformat()}
            }
        }
    }

    # ✅ Notion API 호출
    res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
    print(f"[{res.status_code}] {q}")