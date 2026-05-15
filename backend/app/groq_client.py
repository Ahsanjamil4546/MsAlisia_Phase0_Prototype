import httpx
from app.config import get_settings

settings = get_settings()


class GroqClientError(RuntimeError):
    pass


async def generate_with_groq(messages: list[dict[str, str]]) -> tuple[str, str]:
    """Call Groq's OpenAI-compatible Chat Completions API.

    Returns:
        reply text and provider name.
    """
    if not settings.groq_api_key:
        return demo_reply(messages), "demo"

    url = f"{settings.groq_base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.groq_model,
        "messages": messages,
        "temperature": settings.llm_temperature,
        "max_tokens": settings.llm_max_tokens,
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return content.strip(), "groq"
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text[:500]
        raise GroqClientError(f"Groq API returned {exc.response.status_code}: {detail}") from exc
    except Exception as exc:  # noqa: BLE001 - prototype-friendly error wrapping
        raise GroqClientError(f"Could not complete Groq request: {exc}") from exc


def demo_reply(messages: list[dict[str, str]]) -> str:
    user_message = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
    text = user_message.lower()

    if any(term in text for term in ["lcm", "least common multiple"]):
        return (
            "Great question. LCM means the smallest number that two numbers can both divide into evenly. "
            "Let’s try one small step: list the first few multiples of 4: 4, 8, 12, 16. "
            "Now, what are the first four multiples of 6?"
        )
    if any(term in text for term in ["fraction", "fractions"]):
        return (
            "Nice start. A fraction shows parts of a whole. The top number tells how many parts we have, "
            "and the bottom number tells how many equal parts are in the whole. Quick check: in 3/5, "
            "which number tells the total equal parts?"
        )
    if any(term in text for term in ["multiply", "multiplication", "times"]):
        return (
            "You’re thinking about multiplication. Multiplication is repeated groups. For example, 3 × 4 means "
            "3 groups of 4. Quick check: what is 2 groups of 5?"
        )
    return (
        "Good effort. Let’s work on one small step at a time. Tell me the exact math problem you want help with, "
        "and I’ll guide you with a short hint first."
    )
