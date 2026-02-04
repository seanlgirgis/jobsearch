# scripts/test_xai_api.py
#python -m scripts.test_xai_api
# scripts/test_xai_api.py
# Updated for official xai-sdk (v1.6.1 as per your pip output)
# scripts/test_xai_api.py
# Fixed for official xai-sdk (uses typed message builders: system, user, etc.)
# scripts/test_xai_openai.py



import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("XAI_API_KEY")
if not api_key:
    print("XAI_API_KEY missing")
    exit(1)

client = OpenAI(
    api_key=api_key,
    base_url="https://api.x.ai/v1",
)

try:
    completion = client.chat.completions.create(
        model="grok-3",  # or "grok-4-1-fast-reasoning", "grok-4-fast-reasoning"
        messages=[
            {"role": "system", "content": "You are Grok from xAI."},
            {"role": "user", "content": "Hello! This should work via OpenAI-compatible endpoint. Confirm model and say hi."}
        ],
        temperature=0.7,
        max_tokens=120,
    )
    print("Success via OpenAI client:")
    print(completion.choices[0].message.content.strip())
except Exception as e:
    print("Error:")
    print(str(e))