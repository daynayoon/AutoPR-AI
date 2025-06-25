# AutoPR-AI Backend – Setup & Usage Guide

This document provides everything you need to run and use the AutoPR-AI backend locally, including environment variable configuration, API usage examples, and local development instructions.

---

## 1. Environment Configuration

Create a `.env` file in your project root with the following variables:

```env
=== OpenAI GPT-4 API ===
OPENAI_API_KEY=your_openai_api_key_here

Get it from: https://platform.openai.com/account/api-keys

=== GitHub OAuth & API ===
GITHUB_CLIENT_ID=your_github_oauth_app_client_id
GITHUB_CLIENT_SECRET=your_github_oauth_app_client_secret
GITHUB_TOKEN=your_personal_access_token_for_github

Register an app at: https://github.com/settings/developers

=== MongoDB Atlas ===
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=your_database_name

Example: mongodb+srv://user:pass@cluster.mongodb.net

=== JWT Configuration ===
SECRET_KEY=your_jwt_secret_key
```

## 2. Example API Usage

🔐 GitHub OAuth Login

```
GET http://localhost:8000/oauth/login
→ Redirects to GitHub login, issues JWT upon success.
```

📄 Upload a Code File

```
curl -X POST http://localhost:8000/review/upload \
  -F "file=@example.py"
```

Response:

```
{
  "file_id": "abc123...",
  "filename": "example.py"
}
```

🧠 Run GPT-4 Code Review

```
curl -X POST http://localhost:8000/review/analyze \
  -H "Content-Type: application/json" \
  -d '{"file_id": "abc123..."}'
```

Response:

```
{
  "review_id": "xyz456...",
  "review_comments": ["Consider adding type hints.", "..."]
}
```

🔀 Create Pull Request

```
curl -X POST http://localhost:8000/github/pr \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "repo": "your-username/repo-name",
    "branch": "feature-branch",
    "title": "AI-generated review PR",
    "body": "Suggested changes from AutoPR-AI"
  }'
```

## 3. Local Development

Backend Setup

```
# 1. Clone the repo and navigate in
git clone https://github.com/yourname/AutoPR-AI.git
cd AutoPR-AI

# 2. Create virtual environment and activate
python -m venv venv
source venv/bin/activate     # or .\venv\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp docs/setup-guide.md .env  # or copy manually

# 5. Run FastAPI server
uvicorn app.main:app --reload
```

Server runs at: http://localhost:8000/docs

✅ Tip: All APIs are documented in the Swagger UI automatically provided by FastAPI.

For any questions or contributions, please open an issue or PR on GitHub.
