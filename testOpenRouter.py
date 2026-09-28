import requests
import os

def call_openrouter(prompt, model="deepseek/deepseek-v4-flash-0731"):
    api_key = os.environ.get("OPENROUTER_API_KEY")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def extract_reply(response_json):
    return response_json["choices"][0]["message"]["content"]

if __name__ == "__main__":
    result = call_openrouter("Say hello in one short sentence.")
    print(extract_reply(result))
    print(result)  # full response, useful for debugging