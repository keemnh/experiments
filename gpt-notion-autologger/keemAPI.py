import requests, json

// notion token 입력
// notion db id 입력
NOTION_TOKEN = " "
DATABASE_ID = "  "

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

with open("coretrace_logger_payload_template.json") as f:
    data = json.load(f)

data["parent"]["database_id"] = DATABASE_ID

res = requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)
print(res.status_code, res.json())
