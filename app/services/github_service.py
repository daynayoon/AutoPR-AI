import asyncio
import os
from typing import Optional

from fastapi import HTTPException, status
from github import BadCredentialsException, Github, GithubException


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def _require_token() -> str:
    if not GITHUB_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GITHUB_TOKEN is not configured",
        )
    return GITHUB_TOKEN


def get_github() -> Github:
    token = _require_token()
    try:
        client = Github(token)
        rate_limit = client.get_rate_limit()
        remaining = rate_limit.core.remaining
        reset_time = rate_limit.core.reset
        if remaining == 0:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Github API rate limit exceeded. Reset at {reset_time}",
            )
        return client
    except BadCredentialsException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Github credentials")
    except GithubException as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Github API error: {exc}")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error: {exc}")


def _create_pull_request_sync(repo: str, branch: str, title: str, body: str) -> dict:
    client = get_github()
    repository = client.get_repo(repo)
    base = "main"
    pr = repository.create_pull(title=title, body=body, head=branch, base=base)
    return {"pr_number": pr.number, "url": pr.html_url}


def _add_pr_comment_sync(repo: str, pr_number: int, comment: str) -> dict:
    client = get_github()
    repository = client.get_repo(repo)
    pull = repository.get_pull(pr_number)
    issue_comment = pull.create_issue_comment(comment)
    return {"review_id": issue_comment.id, "url": issue_comment.html_url}


async def create_pull_request(repo: str, branch: str, title: str, body: str) -> dict:
    return await asyncio.to_thread(_create_pull_request_sync, repo, branch, title, body)


async def add_pr_comment(repo: str, pr_number: int, comment: str) -> dict:
    return await asyncio.to_thread(_add_pr_comment_sync, repo, pr_number, comment)
