from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.auth.dependencies import get_current_user
from app.core.db import get_db
from app.models.review_models import AnalyzeRequest, CodeReviewModel, FileModel, UploadResponse
from app.models.user_models import User, UserModel
from app.services.review_service import (
    analyze_code,
    get_review_summary,
    save_uploaded_file,
)


router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_code(
    file: UploadFile = File(...),
    db=Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    return await save_uploaded_file(file, db, user)


@router.post("/analyze")
async def review_code(req: AnalyzeRequest, db=Depends(get_db), user: UserModel = Depends(get_current_user)):
    return await analyze_code(req.file_id, db, user)


@router.get("/summary/{review_id}")
async def review_summary(review_id: str, db=Depends(get_db), user: UserModel = Depends(get_current_user)):
    return await get_review_summary(review_id, db)


@router.get("/review-secure")
async def review_secure(user: User = Depends(get_current_user), db=Depends(get_db)):
    return {"message": f"User {user.username} connected to DB!"}
