# Github PR request code
# Github Comment code

from typing import Optional

def create_pull_request(repo: str, branch: str, title: str, body: str) -> dict:
    # TODO: Github API connect (PyGithub)
    return {"message": f"PR '{title}' requested for {repo}/{branch}"}

def add_comment(repo: str, pr_number: int, comment: str) -> dict:
    # TODO: Github API connect (PyGithub)
    return {"message": f"add the comment to the PR #{pr_number}"}