from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List 
from bson import ObjectId
from pydantic import field_serializer


# code review request/response, MongoDB collection model
# MongoDB files, code_reviews collection mapping

# MongoDB collection mappings
# PyObjectId: ObjectId (MongoDB's ID), so Pydantic check 
#             if ObjectId is valid and translate to ObjectId.
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if isinstance(v, ObjectId):
            return v
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
# CodeReviewModel and FileModel define structure of the 
# collection and rules of JSON transformation
# files collections
class FileModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )
    id: Optional[PyObjectId] = Field(None, alias="_id")
    filename: str
    content: str
    uploaded_at: str

# code review collections
class CodeReviewModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )
    id: Optional[PyObjectId] = Field(None, alias="_id")
    file_id: PyObjectId
    review_comments: List[str]
    summary: Optional[str]
    created_at: str

# API request/response models
class UploadResponse(BaseModel):
    file_id: str
    filename: str
    size: int

class AnalyzeRequest(BaseModel):
    file_id: str

class CodeReviewResponse(BaseModel):
    id: Optional[str] 
    file_id: str
    review_comments: List[str]
    summary: Optional[str]