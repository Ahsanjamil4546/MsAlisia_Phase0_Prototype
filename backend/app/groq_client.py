import httpx
from app.config import get_settings

settings = get_settings()


class GroqClientError(RuntimeError):
    pass


class LLMClientError(RuntimeError):
    pass


def split_system_messages(messages: list[dict[str, str]]) -> tuple[str, list[dict[str, str]]]:
    system_parts = [message["content"] for message in messages if message["role"] == "system"]
    chat_messages = [message for message in messages if message["role"] != "system"]
    return "\n\n".join(system_parts), chat_messages


def normalize_anthropic_messages(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    """Anthropic messages must alternate user/assistant roles."""
    normalized: list[dict[str, str]] = []

    for message in messages:
        role = message["role"]
        content = message["content"]
        if role not in {"user", "assistant"}:
            continue
        if normalized and normalized[-1]["role"] == role:
            normalized[-1]["content"] += f"\n\n{content}"
        else:
            normalized.append({"role": role, "content": content})

    if not normalized or normalized[0]["role"] != "user":
        normalized.insert(0, {"role": "user", "content": "Please help me learn."})

    return normalized


async def generate_with_anthropic(messages: list[dict[str, str]]) -> tuple[str, str, str]:
    """Call Anthropic's Messages API.

    Returns:
        reply text, provider name, and model name.
    """
    if not settings.anthropic_api_key:
        raise LLMClientError("Anthropic API key is not configured.")

    system_prompt, chat_messages = split_system_messages(messages)
    url = f"{settings.anthropic_base_url.rstrip('/')}/messages"
    headers = {
        "x-api-key": settings.anthropic_api_key,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.anthropic_model,
        "system": system_prompt,
        "messages": normalize_anthropic_messages(chat_messages),
        "temperature": settings.llm_temperature,
        "max_tokens": settings.llm_max_tokens,
    }

    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            content_blocks = data.get("content", [])
            text_parts = [
                block.get("text", "")
                for block in content_blocks
                if block.get("type") == "text" and block.get("text")
            ]
            content = "\n".join(text_parts).strip()
            if not content:
                raise LLMClientError("Anthropic returned an empty response.")
            return content, "anthropic", settings.anthropic_model
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text[:500]
        raise LLMClientError(f"Anthropic API returned {exc.response.status_code}: {detail}") from exc
    except Exception as exc:  # noqa: BLE001 - prototype-friendly error wrapping
        if isinstance(exc, LLMClientError):
            raise
        raise LLMClientError(f"Could not complete Anthropic request: {exc}") from exc


async def generate_with_groq(messages: list[dict[str, str]]) -> tuple[str, str, str]:
    """Call Groq's OpenAI-compatible Chat Completions API.

    Returns:
        reply text, provider name, and model name.
    """
    if not settings.groq_api_key:
        raise LLMClientError("Groq API key is not configured.")

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
            return content.strip(), "groq", settings.groq_model
    except httpx.HTTPStatusError as exc:
        detail = exc.response.text[:500]
        raise LLMClientError(f"Groq API returned {exc.response.status_code}: {detail}") from exc
    except Exception as exc:  # noqa: BLE001 - prototype-friendly error wrapping
        if isinstance(exc, LLMClientError):
            raise
        raise LLMClientError(f"Could not complete Groq request: {exc}") from exc


async def generate_with_llm(messages: list[dict[str, str]]) -> tuple[str, str, str]:
    """Prefer Claude/Anthropic when configured, then fall back to Groq, then demo."""
    errors: list[str] = []

    if settings.anthropic_api_key:
        try:
            return await generate_with_anthropic(messages)
        except LLMClientError as exc:
            errors.append(str(exc))

    if settings.groq_api_key:
        try:
            return await generate_with_groq(messages)
        except LLMClientError as exc:
            errors.append(str(exc))

    if settings.anthropic_api_key or settings.groq_api_key:
        raise GroqClientError("Could not complete provider request. " + " | ".join(errors))

    return demo_reply(messages), "demo", "demo"


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
