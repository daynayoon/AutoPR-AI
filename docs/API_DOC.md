# AutoPR-AI API Documentation

This document provides a full reference for all API endpoints offered by the AutoPR-AI backend.

All endpoints follow RESTful conventions and are protected where necessary using JWT authentication.

## Authentication

### GitHub OAuth Login

**GET** `/oauth/login`

- Redirects user to GitHub OAuth flow

### GitHub OAuth Callback

**GET** `/oauth/callback?code=...`

- Exchanges GitHub code for access token

- Returns: `{ message, username, jwt_token }`

### JWT-Protected Test Endpoint

**GET** `/github/secure-data`

- Requires Header: `Authorization: Bearer <jwt_token>`

- Returns: `{ message: Hello, <username>! }`

## Review Workflow

### Upload a Code File

**POST** `/review/upload`

- Form Data: `file (Python code file)`

- Response:

```
{
  "file_id": "<file_id>",
  "filename": "example.py",
  "size": 123
}
```

### Analyze Uploaded File (GPT-4)

**POST** `/review/analyze`

- JSON Body:

```
{
  "file_id": "<file_id>"
}
```

- Response:

```
{
  "review_id": "<review_id>",
  "review_comments": [
    "Consider adding type hints.",
    "Refactor nested loops to improve readability."
  ]
}
```

## GitHub Integration

### Create Pull Request

**POST** `/github/pr`

- Headers: `Authorization: Bearer <jwt_token>`

- JSON Body:

```
{
  "repo": "username/repo",
  "branch": "feature-branch",
  "title": "AI Code Review PR",
  "body": "Suggested improvements from AutoPR-AI"
}
```

- Response:

```
{
  "pr_numer": 7,
  "url": "https://github.com/username/repo/pull/7"
}
```

### Add Comment to Pull Request

**POST** `/github/comment`

- Headers: `Authorization: Bearer <jwt_token>`

- JSON Body:

```
{
  "repo": "username/repo",
  "pr_number": 7,
  "comment": "Looks good! Please add unit tests."
}
```

- Response:

```
{
  "review_id": 12345678,
  "url": "https://github.com/username/repo/pull/7#issuecomment-12345678"
}
```

## Error Handling

All endpoints return structured error responses like:

```
{
  "detail": "Error message"
}
```

Common Status Codes:

- `400` – Bad request / Missing input

- `401` – Unauthorized / Invalid JWT

- `500` – Internal server error / GPT or GitHub issues

## Notes

- You must upload a file and run a review before calling the `/github/pr` endpoint to attach meaningful comments.

- JWT tokens expire in 24 hours by default.

- Only public GitHub repositories are currently supported.
