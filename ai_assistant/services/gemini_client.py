"""
Thin wrapper around the Gemini API.

Design goal: every other module in ai_assistant should be able to call
`generate(prompt)` and get a string back, WITHOUT caring whether a real
GEMINI_API_KEY is configured. If it isn't (e.g. no key yet, or the request
fails/times out), we fall back to a deterministic, rule-based response so
the rest of the app - and the demo - keeps working end to end.
"""
import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)
REQUEST_TIMEOUT_SECONDS = 30
GEMINI_URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)
REQUEST_TIMEOUT_SECONDS = 15


class GeminiUnavailableError(Exception):
    """Raised internally when the real API can't be used; callers should
    treat this as a signal to use a fallback, not surface it to the user."""


def is_configured() -> bool:
    return bool(getattr(settings, "GEMINI_API_KEY", ""))


def generate(prompt: str, system_instruction: str | None = None) -> str:
    """Return the model's text response, or raise GeminiUnavailableError."""
    if not is_configured():
        raise GeminiUnavailableError("GEMINI_API_KEY is not set")

    model = getattr(settings, "GEMINI_MODEL", "gemini-3.6-flash")
    url = GEMINI_URL_TEMPLATE.format(model=model)

    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    if system_instruction:
        payload["system_instruction"] = {"parts": [{"text": system_instruction}]}

    try:
        response = requests.post(
            url,
            params={"key": settings.GEMINI_API_KEY},
            json=payload,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

        if not response.ok:
            logger.warning(
                "Gemini API error %s: %s",
                response.status_code,
                response.text,
            )

        response.raise_for_status()

        data = response.json()
        candidates = data.get("candidates") or []

        if not candidates:
            raise GeminiUnavailableError("Gemini returned no candidates")

        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts).strip()

        if not text:
            raise GeminiUnavailableError("Gemini returned an empty response")

        return text

    except (requests.RequestException, ValueError, KeyError, IndexError) as exc:
        logger.warning("Gemini call failed, falling back: %s", exc)
        raise GeminiUnavailableError(str(exc)) from exc