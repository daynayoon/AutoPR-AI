from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from app.services.review_service import save_uploaded_file, analyze_code, summarize_review
from app.models.review_models import FileModel, UploadResponse, CodeReviewModel, AnalyzeRequest
from app.models.user_models import User
from app.services.review_service import analyze_code
from app.auth.dependencies import get_current_user
from app.core.db import get_db
import base64
from datetime import datetime

# code review router
router = APIRouter()

# uplaod: code file uplaod (POST)
# analyze: request to analyze the code uploaded (POST)
# summary: check the result of analysis

# file upload -> save in MongoDB -> parsing the uploaded file -> GPT4 analyze
@router.post("/upload")
async def upload_code(file: UploadFile = File(...), db=Depends(get_db)):
    # TODO: file save and MongoDB
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")
    content_b64 = base64.b64encode(content).decode()
    doc = {
        "filename": file.filename,
        "content": content_b64,
        "uploaded_at": datetime.utcnow().isoformat()
    }
    result = await db.files.insert_one(doc)
    return {"file_id":str(result.inserted_id), "filename":file.filename, "size": len(content)}


@router.post("/analyze")
async def review_code(req: AnalyzeRequest, db=Depends(get_db)):
    #TODO: GPT-4 connection -- code review logic
    result = await analyze_code(req.file_id, db)
    return result





@router.get("/summary")
async def review_summary():
    # TODO: return the result of the code analysis
    result = summarize_review()
    return result

@router.get("/review-secure")
async def review_secure(user: User = Depends(get_current_user), db=Depends(get_db)):
    # db = MongoDB
    return {"message": f"User {user.username} connected to DB!"}


# @router.get("/test")
# async def test_review():
#     return {"message": "Review router working"}
