# from pymongo import MongoClient
# import os

# # MongoDB Atlas connection string
# uri = os.getenv("MONGODB_URI")

# # create Client
# client = MongoClient(uri)

# # print DB List 
# print(client.list_database_names())

from fastapi import APIRouter, Depends
from app.core.db import get_db

router = APIRouter()

@router.get("/test-db")
async def test_db(db = Depends(get_db)):
    try:
        collections = await db.list_collection_names()
        return {"collections": collections}
    except Exception as e:
        return {"error": str(e)}