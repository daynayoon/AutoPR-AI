from github import Github
import os

# GitHub Token
token = os.getenv("GITHUB_TOKEN")


g = Github(token)
user = g.get_user()
print(user.login)  

for repo in user.get_repos():
    print(f"- {repo.full_name}")