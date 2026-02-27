import base64
import os
from datetime import datetime
from typing import List, Tuple

from bson import ObjectId
from fastapi import HTTPException, UploadFile, status
from openai import AsyncOpenAI

from app.models.user_models import UserModel


MAX_FILE_SIZE_BYTES = 1_000_000  # 1 MB
ALLOWED_EXTENSIONS = {"py", "js", "ts", "tsx", "jsx", "java", "go", "rb", "rs", "cpp", "c", "cs", "php", "swift", "kt"}
OPENAI_MODEL = "gpt-4o"

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _require_openai_key():
    if not client.api_key:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="OPENAI_API_KEY is not configured")


def _validate_file(file: UploadFile, content: bytes) -> None:
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file")
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds limit",
        )
    extension = (file.filename.split(".")[-1] if "." in file.filename else "").lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"File type .{extension} is not allowed")


async def save_uploaded_file(file: UploadFile, db, user: UserModel | None = None) -> dict:
    content = await file.read()
    _validate_file(file, content)

    doc = {
        "filename": file.filename,
        "content": base64.b64encode(content).decode(),
        "uploaded_at": datetime.utcnow().isoformat(),
    }
    if user:
        doc["uploaded_by"] = user.github_id

    result = await db.files.insert_one(doc)
    return {"file_id": str(result.inserted_id), "filename": file.filename, "size": len(content)}


async def _fetch_file(db, file_id: str) -> Tuple[ObjectId, str]:
    try:
        object_id = ObjectId(file_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file_id")

    file_doc = await db.files.find_one({"_id": object_id})
    if not file_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    return object_id, base64.b64decode(file_doc["content"]).decode()


async def analyze_code(file_id: str, db, user: UserModel | None = None) -> dict:
    _require_openai_key()
    object_id, code = await _fetch_file(db, file_id)

    prompt = (
        "You are a rigorous code reviewer. Provide concise, actionable feedback. "
        "Respond with bullet lines, each describing an issue or suggestion."
    )

    response = await client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Review this code:\n{code}"},
        ],
        temperature=0.2,
        timeout=30,
    )
    review_text = response.choices[0].message.content.strip()
    review_comments: List[str] = [line.strip("- ").strip() for line in review_text.split("\n") if line.strip()]

    review_doc = {
        "file_id": object_id,
        "review_comments": review_comments,
        "summary": review_comments[0] if review_comments else "Automated code review",
        "created_at": datetime.utcnow().isoformat(),
    }
    if user:
        review_doc["created_by"] = user.github_id

    result = await db.code_reviews.insert_one(review_doc)
    return {"review_id": str(result.inserted_id), "review_comments": review_comments}


async def get_review_summary(review_id: str, db) -> dict:
    try:
        object_id = ObjectId(review_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid review_id")

    review_doc = await db.code_reviews.find_one({"_id": object_id})
    if not review_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    review_doc["_id"] = str(review_doc["_id"])
    review_doc["file_id"] = str(review_doc["file_id"])
    return review_doc
