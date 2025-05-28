# from pymongo import MongoClient
# import os

# # MongoDB Atlas connection string
# uri = os.getenv("MONGODB_URI")

# # create Client
# client = MongoClient(uri)

# # print DB List 
# print(client.list_database_names())

from fastapi import APIRouter, Depends, HTTPException
from app.core.db import get_db
import base64

from app.models.review_models import FileModel
from app.models.user_models import UserModel
from bson import ObjectId, errors

router = APIRouter()

@router.post("/insert-file")
async def insert_file(db=Depends(get_db)):
    content_b64 = base64.b64encode(b"print('Hello')").decode()
    doc = {"filename": "example.py", "content": content_b64, "uploaded_at": "2025-05-28"}
    res = await db.files.insert_one(doc)
    return {"inserted_id": str(res.inserted_id)}

@router.get("/get-file/{file_id}", response_model=FileModel)
async def get_file(file_id: str, db=Depends(get_db)):
    try:
        oid = ObjectId(file_id)
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid file_id format")
    doc = await db.files.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="File not found")
    doc["content"] = base64.b64decode(doc["content"]).decode()
    return doc

@router.post("/insert-user")
async def insert_user(db=Depends(get_db)):
    user_doc = {"github_id": "123", "username": "testuser", "access_token": "token123", "created_at": "2025-05-28"}
    res = await db.users.insert_one(user_doc)
    return {"inserted_id": str(res.inserted_id)}

@router.get("/get-user/{user_id}", response_model=UserModel)
async def get_user(user_id: str, db=Depends(get_db)):
    try:
        oid = ObjectId(user_id)
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user_id format")
    doc = await db.users.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="User not found")
    return doc


# @router.get("/test-db")
# async def test_db(db = Depends(get_db)):
#     try:
#         collections = await db.list_collection_names()
#         return {"collections": collections}
#     except Exception as e:
#         return {"error": str(e)}

# post request needs to be called by curl
# Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:8000/db-test/insert-file"
