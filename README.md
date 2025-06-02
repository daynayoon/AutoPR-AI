# AutoPR-AI
AI-Powered Code Review & Pull Request Automation for GitHub

## Overview
AutoPR-AI is a full-stack web application designed to automate code reviews and enhance collaboration on GitHub repositories. 
Built with **Python (FastAPI)** and **MongoDB**, it **integrates OpenAI's GPT models** to provide code quality suggestions and generate pull requests with automated comments.

## Features
- GitHub OAuth authentication and JWT-based user session management
- Secure code upload and asynchronous review analysis
- GPT-powered code review comment generation
- Automated pull request creation with inline review comments
- Fully tested MongoDB CRUD operations for users, files, and reviews
- API documentation via Swagger UI and ReDoc

## Tech Stack
- **Backend**: Python (FastAPI), PyGithub, OpenAI API, JWT, OAuth
- **Database**: MongoDB (motor)
- **Authentication**: GitHub OAuth, JWT
- **Dev Tools**: Docker (optional), Swagger UI, ReDoc
  
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

## Future Improvements
- Integration with CI/CD pipelines
- Enhanced review analysis with custom GPT models
- Frontend dashboard for code review management (React)
  
## License
This project is licensed under the MIT License.
