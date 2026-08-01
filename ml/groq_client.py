import logging
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GROQ_API_URL = os.getenv(
    "GROQ_API_URL",
    "https://api.groq.com/openai/v1/chat/completions",
)
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def create_chat_completion(
    messages,
    temperature=0.2,
    max_tokens=400,
    response_format=None,
):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured")

    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    if response_format:
        payload["response_format"] = response_format

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    last_error = None
    for attempt in range(3):
        try:
            response = requests.post(
                GROQ_API_URL,
                headers=headers,
                json=payload,
                timeout=35,
            )
            if response.status_code >= 400:
                logger.error(
                    "Groq API returned %s: %s",
                    response.status_code,
                    response.text[:500],
                )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except requests.RequestException as exc:
            last_error = exc
            logger.warning(
                "Groq API connection attempt %s failed: %s",
                attempt + 1,
                exc,
            )
            time.sleep(1 + attempt)

    raise RuntimeError("Groq API request failed after retries") from last_error
