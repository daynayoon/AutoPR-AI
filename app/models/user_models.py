from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId
from pydantic import field_serializer


# user data model (GitHub OAuth)

class User(BaseModel):
    github_id: str
    username: str
    access_token: str

# TODO: user_models.py is gonna be connected to OAuth (auth_service) and github router auth logic

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
    
class UserModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )
    id: Optional[PyObjectId] = Field(None, alias="_id")
    github_id: str
    username: str
    access_token: str
    created_at: str