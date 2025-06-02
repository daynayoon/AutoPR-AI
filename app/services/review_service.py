# file upload (save in MongoDB) code
# GPT-4 code analyze code
# request summary of the analysis code

import base64
import os
from datetime import datetime

from bson import ObjectId
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



async def analyze_code(file_id: str,  db):
    # TODO: GPT-4 API, request the analysis
    try:
        file_doc = await db.files.find_one({"_id": ObjectId(file_id)})
        if not file_doc:
            return {"error": "File not found"}
        
        content_b64 = file_doc["content"]
        code = base64.b64decode(content_b64).decode()

        # GPT-4 analyze (e.g., OpenAI ChatCompletion)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a code reviewer."},
                {"role": "user", "content": f"Review this code:\n{code}"}
            ]
        )
        review_comments = response.choices[0].message.content.strip().split("\n")

        # save review_comments
        review_doc = {
            "file_id": ObjectId(file_id),
            "review_comments": review_comments,
            "summary": "Automated code review",
            "created_at": datetime.utcnow().isoformat()
        }
        result = await db.code_reviews.insert_one(review_doc)
        return {"review_id": str(result.inserted_id), "review_comments": review_comments}
    except Exception as e:
        return {"error": str(e)}
    

def save_uploaded_file(file_connect: bytes, filename: str) -> dict:
    # TODO: save the file in MongoDB
    return {"message": f"saved file {filename}"}

def summarize_review() -> dict:
    # TODO: request the result of analysis logic
    return {"message": "returned the result of the analysis"}