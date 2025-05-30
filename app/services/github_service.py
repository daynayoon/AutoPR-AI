# Github PR request code
# Github Comment code

from typing import Optional
import os
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def create_pull_request(repo: str, branch: str, title: str, body: str):
    # TODO: Github API connect (PyGithub)
    # return {"message": f"PR '{title}' requested for {repo}/{branch}"}
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(repo)
    base = "main"
    head = branch
    pr = repo.create_pull(title=title, body=body, head=head, base=base)
    return {"pr_numer": pr.number, "url": pr.html_url}


def add_comment(repo: str, pr_number: int, comment: str) -> dict:
    # TODO: Github API connect (PyGithub)
    return {"message": f"add the comment to the PR #{pr_number}"}