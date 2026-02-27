import os
from typing import Optional

from dotenv import find_dotenv, load_dotenv
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient


load_dotenv(find_dotenv())

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client: Optional[AsyncIOMotorClient] = None
db = None


async def connect_to_mongo():
    global client, db
    if client:
        return
    if not MONGODB_URI or not DATABASE_NAME:
        raise RuntimeError("MONGODB_URI or DATABASE_NAME is not configured")
    client = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
    db = client[DATABASE_NAME]
    # warmup ping
    await db.command("ping")


async def close_mongo_connection():
    global client
    if client:
        client.close()
        client = None


def get_motor_client():
    return client


async def get_db():
    if not db:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database not initialized")
    return db
