import os
import secrets
from datetime import datetime, timedelta

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from app.auth.token_service import create_access_token
from app.core.db import get_db


router = APIRouter()

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
OAUTH_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/oauth/callback")
OAUTH_STATE_COOKIE = "oauth_state"
OAUTH_STATE_TTL_SECONDS = 600


def _require_github_oauth_creds():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GitHub OAuth credentials are not configured",
        )


@router.get("/login")
async def github_login():
    _require_github_oauth_creds()
    state = secrets.token_urlsafe(16)
    github_auth_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}&redirect_uri={OAUTH_REDIRECT_URI}&scope=repo&state={state}"
    )
    response = RedirectResponse(github_auth_url)
    response.set_cookie(
        OAUTH_STATE_COOKIE,
        state,
        httponly=True,
        max_age=OAUTH_STATE_TTL_SECONDS,
        secure=False,
        samesite="lax",
    )
    return response


@router.get("/callback")
async def github_callback(request: Request, code: str, state: str, db=Depends(get_db)):
    _require_github_oauth_creds()

    stored_state = request.cookies.get(OAUTH_STATE_COOKIE)
    if not stored_state or stored_state != state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OAuth state")

    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    data = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "code": code, "redirect_uri": OAUTH_REDIRECT_URI}

    async with httpx.AsyncClient(timeout=10) as client:
        token_resp = await client.post(token_url, headers=headers, data=data)
        token_resp.raise_for_status()
        access_token = token_resp.json().get("access_token")
        if not access_token:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to obtain access token")

        user_resp = await client.get("https://api.github.com/user", headers={"Authorization": f"token {access_token}"})
        user_resp.raise_for_status()
        user_data = user_resp.json()

    github_id = str(user_data.get("id"))
    username = user_data.get("login")
    if not github_id or not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to fetch user profile")

    await db.users.update_one(
        {"github_id": github_id},
        {
            "$set": {
                "username": username,
                "access_token": access_token,
                "created_at": datetime.utcnow().isoformat(),
                "token_acquired_at": datetime.utcnow().isoformat(),
            }
        },
        upsert=True,
    )

    token_data = {"sub": github_id, "username": username}
    jwt_token = create_access_token(token_data)

    redirect_url = os.getenv("POST_LOGIN_REDIRECT", "http://localhost:3000/github-login")
    response = RedirectResponse(f"{redirect_url}?token={jwt_token}")
    response.delete_cookie(OAUTH_STATE_COOKIE)
    return response
