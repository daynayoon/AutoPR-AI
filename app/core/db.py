from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends
from pathlib import Path
import os
from dotenv import load_dotenv

# MongoDB connect dependencies

env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# everytime you got uri, add db name to uri
print("Mongodb uri:", os.getenv("MONGODB_URI"))
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
print(f"DATABASE_NAME: {DATABASE_NAME}")
print(f"env_path: {env_path.resolve()}")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DATABASE_NAME]

# try:
#     client = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
#     db = client[DATABASE_NAME]
#     print("MongoDB connected")
# except Exception as e:
#     print(f"MongoDB failed: {e}")

def get_motor_client():
    return client

async def get_db():
    return db