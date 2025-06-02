from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.services.github_service import create_pull_request, add_pr_comment
from app.models.github_models import PRRequest, CommentRequest
from app.models.user_models import UserModel
from app.auth.dependencies import get_current_user


#github router
router = APIRouter()

# pr: request PR (POST)
# comment: add comment on the PR (POST)


@router.post("/pr")
async def create_pr(pr: PRRequest, user: UserModel = Depends(get_current_user)):
    # TODO: Github API call logic
    result = create_pull_request(pr.repo, pr.branch, pr.title, pr.body)
    return result

@router.post("/comment")
async def add_comment(req: CommentRequest, user: UserModel = Depends(get_current_user)):
    result = add_pr_comment(req.repo, req.pr_number, req.comment)
    return result

# get current user
@router.get("/secure-data")
async def secure_data(user: UserModel = Depends(get_current_user)):
    return {"message": f"Hello, {user.username}!"}

# @router.get("/test")
# async def test_github():
#     return {"message": "GitHub router working"}
