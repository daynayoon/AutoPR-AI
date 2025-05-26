from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# code review request/response, MongoDB collection model
# MongoDB files, code_reviews collection mapping

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    size: int

class AnalyzeRequest(BaseModel):
    file_id: str

class CodeReview(BaseModel):
    id: Optional[str] = Field(default_factory=str, alias="_id")
    file_id: str
    review_comments: list[str]
    summary: Optional[str]