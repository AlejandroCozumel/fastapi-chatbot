from openai import OpenAI, OpenAIError

from app.core.config import get_settings
from app.core.errors import ProviderError


def get_assistant_response(message: str, context: str | None = None) -> str:
    settings = get_settings()
    if not settings.openai_api_key:
        return f"Mock assistant response: {message}"

    user_content = message if context is None else f"Context:\n{context}\n\nQuestion:\n{message}"
    try:
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.chat.completions.create(
            model=settings.openai_chat_model,
            messages=[
                {"role": "system", "content": "You are a helpful local assistant."},
                {"role": "user", "content": user_content},
            ],
        )
    except OpenAIError as exc:
        raise ProviderError("OpenAI request failed") from exc

    content = response.choices[0].message.content
    if not content:
        raise ProviderError("OpenAI returned an empty response")
    return content
