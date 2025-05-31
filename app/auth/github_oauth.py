import os
import requests

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from app.core.db import get_db



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
        return {"error": "Failed to obtain access token"}
    
    # save user info and session
    user_response = requests.get(
        "https://api.github.com/user", # request user information
        headers={"Authorization": f"token {access_token}"}
    )
    user_data = user_response.json()
    github_id = str(user_data.get("id"))
    username = user_data.get("login")
    
    # DB save or update
    user_doc = {
        "_id": github_id,
        "github_id": github_id,
        "username": username,
        "access_token": access_token
    }
    await db.users.update_one({"_id": github_id}, {"$set": user_doc}, upsert=True)
    
    return {"message": "GitHub login success", "username": username}
