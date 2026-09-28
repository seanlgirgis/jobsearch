"""Minimal OpenRouter connectivity test; independent of the job-search pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

import httpx
from dotenv import dotenv_values


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "nvidia/nemotron-3.5-lightning:free"
DEFAULT_QUESTION = "Hello. What is the capital of France?"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--question", default=DEFAULT_QUESTION)
    args = parser.parse_args(argv)

    api_key = dotenv_values(ROOT / ".env").get("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY is missing from the project .env file.")
        return 2

    try:
        response = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": args.model,
                "messages": [{"role": "user", "content": args.question}],
                "max_tokens": 100,
            },
            timeout=20.0,
        )
        if response.is_error:
            print(f"OpenRouter test failed: HTTP {response.status_code}.")
            return 1
        answer = response.json()["choices"][0]["message"]["content"].strip()
    except httpx.TimeoutException:
        print("OpenRouter test failed: request timed out after 20 seconds.")
        return 1
    except httpx.HTTPError:
        print("OpenRouter test failed: connection error.")
        return 1
    except (KeyError, TypeError, ValueError):
        print("OpenRouter test failed: response was not a usable chat completion.")
        return 1

    print(f"Model: {args.model}")
    print(f"Question: {args.question}")
    print(f"Answer: {answer}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
