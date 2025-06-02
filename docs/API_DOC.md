# API Documentation - AutoPR-AI

## /github/pr (POST)
- Create Github PR
- request:

{
    "repo": "username/repo",
    "branch": "feature-branch",
    "title": "New PR",
    "body": "PR details"
}
- reponse:

{
    "pr_number": 5,
    "url": "https://gitub.com/username/repo/pull/5"
}

## /github/comment (POST)
- Add comment to the Github PR
- request:

{
  "repo": "username/repo",
  "pr_number": 5,
  "comment": "Review comment"
}
- reponse:

{
  "review_id": 123456,
  "url": "https://github.com/username/repo/pull/5#issuecomment-123456"
}

## /github/secure-data (GET)
- Return the user information that is JWT authorized
- request:

Authorization: Bearer {JWT_TOKEN}

- reponse:

{
  "message": "Hello, username!"
}

## /review/upload (POST)
- Upload code file
- request:

file: upload_file.py

- reponse:

{
  "file_id": "abcdef123456",
  "filename": "upload_file.py",
  "size": 2048
}

## /review/analyze (POST)
- Return the reviewed analysis file of the code
- request:

{
  "file_id": "abcdef123456"
}


- reponse:

{
  "review_id": "abcdef654321",
  "review_comments": [
    "Consider adding type hints.",
    "Refactor nested loops to improve readability."
  ]
}
