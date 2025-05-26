from pydantic import BaseModel

# user data model (GitHub OAuth)

class User(BaseModel):
    github_id: str
    username: str
    access_token: str

# TODO: user_models.py is gonna be connected to OAuth (auth_service) and github router auth logic