# Github PR request code
# Github Comment code

import os
from typing import Optional

from github import Github, GithubException, BadCredentialsException


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


# rate limit: 5000 requests/hour
def get_github():
    try:
        g = Github(GITHUB_TOKEN)
        rate_limit = g.get_rate_limit()
        remaining = rate_limit.core.remaining
        reset_time = rate_limit.core.reset
        if remaining == 0:
            raise Exception(f"Github API rate limit exceeded. Reset at {reset_time}")
        return g
    except BadCredentialsException:
        raise Exception("Invalid Github credentials")
    except GithubException as e:
        raise Exception(f"Github API error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")


def create_pull_request(repo: str, branch: str, title: str, body: str):
    try: 
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(repo)
        base = "main"
        head = branch
        pr = repo.create_pull(title=title, body=body, head=head, base=base)
        return {"pr_numer": pr.number, "url": pr.html_url}
    except GithubException as e:
        raise Exception(f"Github API error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")
    

def add_pr_comment(repo: str, pr_number: int, comment: str):
    try:
        g = Github(GITHUB_TOKEN)
        repo = g.get_repo(repo)
        pr = repo.get_pull(pr_number)
        # pr doenst contain file_path and line_number because it positions review by diff hunk
        # edit: comment on the whole pr
        issue_comment = pr.create_issue_comment(comment)
        return {"review_id": issue_comment.id, "url": issue_comment.html_url}
    except GithubException as e:
        raise Exception(f"Github API error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")
