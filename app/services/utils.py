from typing import Optional

# common logic (e.g., token, responses)

def get_github_token() -> str:
    # TODO: GitHub OAuth token load
    return "your_github_token_here"

def format_response(success: bool, data: Optional[dict] = None, error: Optional[str] = None) -> dict:
    return {
        "success": success,
        "data": data,
        "error": error
    }

# TODO: utils.py: common functions are going to be called for github_service.py, review_service.py, router