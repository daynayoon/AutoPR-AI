from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from app.services.review_service import save_uploaded_file, analyze_code, summarize_review
from app.models.review_models import UploadResponse, CodeReviewModel, AnalyzeRequest

from app.auth.dependencies import get_current_user
from app.core.db import get_db
from app.models.user_models import User

# code review router
router = APIRouter()

# uplaod: code file uplaod (POST)
# analyze: request to analyze the code uploaded (POST)
# summary: check the result of analysis

@router.post("/upload")
async def upload_code(file: UploadFile = File(...)):
    # TODO: file save and MongoDB
    content = await file.read()
    result = save_uploaded_file(content, file.filename)
    return result

@router.post("/analyze")
async def analyze_code(req: AnalyzeRequest):
    #TODO: GPT-4 connection -- code review logic
    result = analyze_code(req.file_id)
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
