# environmental variables
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AutoPR-AI"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Python, FastAPI, Github AI, code review based on GPT-4"

    # 데이터베이스, OAuth, API 키 등도 나중에 추가 가능
    # e.g. MONGO_URI: str
    # e.g. GITHUB_CLIENT_ID: str

settings = Settings()