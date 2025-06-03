import os
import requests

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from datetime import datetime

from app.core.db import get_db
from app.auth.token_service import create_access_token
from app.models.user_models import UserModel



router = APIRouter()

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

# github login route
@router.get("/login")
async def github_login():
    redirect_uri = "http://localhost:8000/oauth/callback"
    github_auth_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={redirect_uri}&scope=repo"
    return RedirectResponse(github_auth_url)

# github OAuth callback route
@router.get("/callback")
async def github_callback(code: str, db=Depends(get_db)):
    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code
    }
    response = requests.post(token_url, headers=headers, data=data)
    access_token = response.json().get("access_token")
    if not access_token:
        return HTTPException(status_code=400, detail="Failed to obtain access token")
    
    # save user info and session
    user_response = requests.get("https://api.github.com/user", headers={"Authorization": f"token {access_token}"})
    user_data = user_response.json()
    github_id = str(user_data.get("id"))
    username = user_data.get("login")
    
    # DB save or update
    # user_doc = {
    #     "_id": github_id,
    #     "github_id": github_id,
    #     "username": username,
    #     "access_token": access_token
    # }
    # await db.users.update_one({"_id": github_id}, {"$set": user_doc}, upsert=True)
    await db.users.update_one(
        {"github_id": github_id},
        {"$set": {
            "username": username,
            "access_token": access_token,
            "created_at": datetime.utcnow().isoformat()
        }},
        upsert=True
    )

    # JWT token
    token_data = {"sub": github_id, "username": username}
    jwt_token = create_access_token(token_data)
    
    # return {"message": "GitHub login success", "username": username, "jwt_token": jwt_token}
    redirect_url = f"http://localhost:3000/github-login?token={jwt_token}"
    return RedirectResponse(redirect_url)
