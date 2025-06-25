# AutoPR-AI: Intelligent Code Review API
![status](https://img.shields.io/badge/status-beta-purple)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-blue)
![license](https://img.shields.io/badge/license-MIT-brightgreen)
![GitHub last commit](https://img.shields.io/github/last-commit/daynayoon/AutoPR-AI)
![GitHub issues](https://img.shields.io/github/issues/daynayoon/AutoPR-AI)
![GitHub forks](https://img.shields.io/github/forks/daynayoon/AutoPR-AI)
![GitHub stars](https://img.shields.io/github/stars/daynayoon/AutoPR-AI)

**AutoPR-AI** is a backend REST API that enables automated code review for files. It leverages **Github OAuth, OpenAI GPT-4, and MongoDB Atlas** to analyze code and leave intelligent review comments directly on pull requests.
> - GitHub OAuth Login
> - GPT-4 Powered Code Review
> - MongoDB Atlas for Data Persistence
> - JWT Authentication
> - RESTful API Design using FastAPI

## Features
- 📁 **Upload a file** via `/review/upload`
- 🤖 **Generate a GPT-based review** via `/review/analyze`
- 🔀 **Create GitHub Pull Requests** via `/github/pr`
- 💬 **Add automated review comments** via `/github/comment`
- 🔐 **Authenticate users via GitHub OAuth** via `/oauth/login`
- 👉 **Issue JWT tokens** and manage user sessions

## Tech Stack
- **FastAPI** – High-performance Python API framework
- **MongoDB Atlas + Motor** – Asynchronous database access
- **GitHub OAuth + PyGithub** – GitHub authentication & PR actions
- **OpenAI GPT-4 API** – AI-powered code analysis and comment generation
- **JWT (pyjwt)** – Secure user session management
- **Swagger (OpenAPI)** – Auto-generated documentation at /docs

## Authentication Flow
- Visit `/oauth/login` to authenticate via GitHub
- Receive a `jwt_token` on successful login
- Pass the token in headers for protected endpoints: `Authorization: Bearer <jwt_token>`

## Configuration
Environment variables are required. See [`docs/api-usage.md`](./docs/api-usage.md) for full setup.

## Getting Started
1. **Clone the repository**
```
   git clone https://github.com/yourusername/AutoPR-AI.git
   cd AutoPR-AI
```
2. **Set up the virtual environment**
```
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```
3. **Install dependencies**
```
    pip install -r requirements.txt
```
4. **Configure environment variables**
   - Create a `.env` file with the following keys:
```
GITHUB_TOKEN=your_github_pat
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
OPENAI_API_KEY=your_openai_api_key
```
5. **Run the server**
```
uvicorn app.main:app --reload
```
## API Reference
Detailed endpoint descriptions and request/response examples are available in [API_DOC.md](docs/API_DOC.md).
> (or) Auto-generated Swagger UI is available at: <http://localhost:8000/docs>

## Future Improvements
- Optional cloud deployment via GCP or Azure
- Smarter GPT-4 prompt engineering
- GitHub webhook support for automatic reviews
- Frontend dashboard (React/Next.js) as a future extension
  
## License
This project is licensed under the MIT License.
