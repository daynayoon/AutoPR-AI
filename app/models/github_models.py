from pydantic import BaseModel

# github request/response model
# so it doesnt need to be saved in MongoDB, data requesting to Github API directly

class PRRequest(BaseModel):
    repo: str       # ex. "username/repository"
    branch: str     # PR branch
    title: str      # PR title
    body: str       # PR body paragraph

class CommentRequest(BaseModel):
    repo: str
    pr_number: int
    comment: str

