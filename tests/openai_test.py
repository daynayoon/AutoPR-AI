from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

response = client.chat.completions.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

print(response.choices[0].message.content)
