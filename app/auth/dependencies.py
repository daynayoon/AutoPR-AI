from fastapi import Depends, HTTPException, Header, status

from app.models.user_models import User

# Token dependencies for JWT authentication

def get_current_user(authorization: str = Header(...)) -> User:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    token = authorization[len("Bearer "):]

    # TODO: real JWT auth and get user info
    return User(github_id="123", username="dawon020411", access_token=token)