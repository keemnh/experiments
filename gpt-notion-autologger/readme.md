# gpt-notion-autologger
  Automated pipeline for logging GPT responses directly into Notion databases.


### 🧠 Overview

This project implements an automated pipeline that:
- Sends prompts to OpenAI's GPT models
- Receives responses
- Stores prompt-response pairs in a structured Notion database with timestamps

It is part of the [keemlab](https://github.com/kimnahyun57/keemlab) experimental repository.




### ⚙️ Architecture

1. **User-defined Questions**  
   → `questions = [...]` 리스트에 직접 질문 입력

2. **GPT 응답 생성**  
   → `openai.ChatCompletion.create()` 호출을 통해 응답 획득

3. **JSON 페이로드 구성**  
   → 질문, 응답, 타임스탬프를 JSON으로 포맷팅

4. **Notion API 호출**  
   → POST 방식으로 `https://api.notion.com/v1/pages`에 전송

5. **자동 기록**  
   → Notion DB에 한 줄씩 자동 추가됨 (질문 & 응답 로그)




### 📁 Files

| File | Description |
|------|-------------|
| `gpt_logger.py` | Main automation script using OpenAI GPT and Notion API |
| `keemAPI.py` | Early standalone Notion DB integration script using pre-defined payload |
| `config.json` | Stores Notion token, database ID, and optional OpenAI key |
| `readme.md` | This documentation |
| `coretrace_logger_payload_template.json` | Template for POSTing a record to Notion DB manually |




### 🧪 Development Environment

- OS: macOS (Apple Silicon)
- Python: 3.12 via Homebrew
- Virtualenv: `coretrace-env`
- Editor: VS Code
- Git: GitHub + terminal + GitHub Web UI




### 🐛 All Errors (Chronological Log)

| Stage | Error Message / Symptom | Cause | Resolution |
|-------|--------------------------|-------|------------|
| Setup | `ModuleNotFoundError: No module named 'requests'` | System-level pip install blocked by macOS (PEP 668) | Used virtualenv: `python3 -m venv coretrace-env` → activated → reinstalled `requests` |
| Setup | `ModuleNotFoundError: No module named 'openai'` | Multiple Python versions; installed in wrong env | Installed with: `python3.12 -m pip install openai` inside correct venv |
| API Call | `openai.ChatCompletion.create` fails with `APIRemovedInV1` | Old API format deprecated in `openai>=1.0.0` | Rewrote using new client: `client = OpenAI(api_key=...)` |
| Notion API | `401 Unauthorized` | Wrong or missing Notion token / integration not shared | Used `secret_...` token and shared DB with the integration manually |
| Notion API | `400 Validation Error: Property does not exist` | Mismatch between Notion DB property name and payload | Matched Notion DB properties exactly: `Name`, `Response`, `Timestamp` |
| GitHub | “Sorry, a file exists where you're trying to create a subdirectory” | Created file `gpt-notion-autologger` instead of folder | Deleted file using terminal → committed → re-pushed to allow folder |
| GitHub | Password auth failed for push | GitHub deprecated password auth in 2021 | Created and used Personal Access Token (fine-grained, repo scope) |
| GitHub UI | Delete button not visible on web | File had no extension → UI didn’t show delete | Used local Git CLI to delete the file: `rm filename` + commit + push |
| Shell | `/bin/sh: coffee: command not found` | VS Code ran wrong interpreter (CoffeeScript?) | Changed interpreter to Python or used `python3 gpt_logger.py` directly |
| File Sync | Notion DB appears empty after `200 OK` response | Filter/view issue in Notion UI | Manually checked URL or updated view filters |
| JSON | `Prompt is not a property that exists.` | Payload used wrong field names | Matched keys to actual DB schema; removed `Prompt` and used `Name` |
| Execution | `No module named 'dotenv'` (later planned) | Optional config loading feature | Install with: `pip install python-dotenv` if needed |




### 💡 Future Improvements

- [ ] Add `summary` field auto-generation via GPT
- [ ] Add CLI interactive prompt mode with live logging
- [ ] Use `.env` to load API keys
- [ ] Categorization & automatic tag insertion
- [ ] Batch processing for prompt lists
