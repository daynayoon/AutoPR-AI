from fastapi import Depends, HTTPException, Header, status
from bson import ObjectId

from app.core.db import get_db
from app.auth.token_service import verify_access_token
from app.models.user_models import UserModel

# Token dependencies for JWT authentication

async def get_current_user(authorization: str = Header(...), db = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code = 401, detail="Invalid Authorization header")
    token = authorization.split(" ")[1]
    payload = verify_access_token(token)
    github_id = payload.get("sub")
    username = payload.get("username")

    if not github_id:
        raise HTTPException(status_code=401, detail= "Invalid token payload")
    
    user_doc = await db.users.find_one({"github_id": github_id})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    return UserModel(**user_doc)