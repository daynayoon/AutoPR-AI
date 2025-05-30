from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.github_service import create_pull_request, add_pr_comment
from app.models.github_models import PRRequest, CommentRequest

from app.auth.dependencies import get_current_user
from app.models.user_models import User

#github router
router = APIRouter()

# pr: request PR (POST)
# comment: add comment on the PR (POST)


@router.post("/pr")
async def create_pr(pr: PRRequest):
    # TODO: Github API call logic
    result = create_pull_request(pr.repo, pr.branch, pr.title, pr.body)
    return result

@router.post("/comment")
async def add_comment(req: CommentRequest):
    result = add_pr_comment(req.repo, req.pr_number, req.comment)
    return result

# get current user
@router.get("/secure-data")
async def secure_data(user: User = Depends(get_current_user)):
    return {"message": f"Hello, {user.username}!"}

# @router.get("/test")
# async def test_github():
#     return {"message": "GitHub router working"}
