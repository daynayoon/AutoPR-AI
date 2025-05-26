from pydantic import BaseModel

# github request/response model

class PRRequest(BaseModel):
    repo: str
    branch: str
    title: str
    body: str

class CommentRequest(BaseModel):
    repo: str
    pr_number: int
    comment: str

