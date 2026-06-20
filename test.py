import os

import requests
from dotenv import load_dotenv


API_URL = "https://api.studio.nebius.com/v1/chat/completions"
MODEL = "meta-llama/Llama-3.3-70B-Instruct"


def main():
    load_dotenv()

    api_key = os.getenv("NEBIUS_API_KEY")
    if not api_key:
        raise RuntimeError("NEBIUS_API_KEY is not set in .env")

    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": "Say hello in one sentence",
                }
            ],
        },
        timeout=60,
    )
    response.raise_for_status()

    data = response.json()
    print(data["choices"][0]["message"]["content"])


if __name__ == "__main__":
    main()
