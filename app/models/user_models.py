from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field, ConfigDict, GetCoreSchemaHandler
from pydantic_core import core_schema

# user data model (GitHub OAuth)

class User(BaseModel):
    github_id: str
    username: str
    access_token: str

# TODO: user_models.py is gonna be connected to OAuth 
#       (auth_service) and github router auth logic

# PyObjectId: ObjectId (MongoDB's ID), so Pydantic check if 
#             ObjectId is valid and translate to ObjectId.
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
    
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: core_schema.CoreSchema, handler: GetCoreSchemaHandler):
        return {'type': 'string'}

# UserModels defines that schema of the user document
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