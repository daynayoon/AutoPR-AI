from motor.motor_asyncio import AsynIOMotorClient
from fastapi import Depends

# MongoDB connect dependencies

MONGO_URI = "my_mongoDB_uri"
client = AsynIOMotorClient(MONGO_URI)
db = client.get_database("code_review_db")

async def get_db():
    return db