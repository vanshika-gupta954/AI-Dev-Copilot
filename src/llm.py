"""
src/llm.py — OpenRouter API integration (Claude model)
"""

import os
import requests

from src.prompts import build_system_prompt, build_user_prompt

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-3.5-sonnet"


def get_copilot_response(code: str, error: str, level: str) -> str:
    """
    Send code + optional error to OpenRouter (Claude) and return raw response text.

    Args:
        code:  The user's code snippet.
        error: Optional error / traceback string.
        level: Explanation level — 'Beginner', 'Intermediate', or 'Expert'.

    Returns:
        Raw assistant message string from the model.

    Raises:
        ValueError: If the API key is missing.
        RuntimeError: If the API call fails.
    """
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY is not set. "
            "Add it to your .env file and restart the app."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-dev-copilot.local",
        "X-Title": "AI Dev Copilot",
    }

    payload = {
        "model": os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL),
        "messages": [
            {"role": "system", "content": build_system_prompt(level)},
            {"role": "user",   "content": build_user_prompt(code, error)},
        ],
        "temperature": 0.3,
        "max_tokens": 400,
    }

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError("Request timed out. Please try again.")
    except requests.exceptions.HTTPError as exc:
        detail = ""
        try:
            detail = response.json().get("error", {}).get("message", "")
        except Exception:
            pass
        raise RuntimeError(f"OpenRouter API error ({response.status_code}): {detail or exc}")
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Network error: {exc}")

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        raise RuntimeError(f"Unexpected API response format: {exc}\n\nFull response: {data}")
