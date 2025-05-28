from pydantic import BaseModel

# github request/response model
# so it doesnt need to be saved in MongoDB, data requesting to Github API directly

class PRRequest(BaseModel):
    repo: str
    branch: str
    title: str
    body: str

class CommentRequest(BaseModel):
    repo: str
    pr_number: int
    comment: str

