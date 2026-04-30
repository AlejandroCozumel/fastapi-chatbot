import hashlib
import json
import math

from openai import OpenAI, OpenAIError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.errors import ProviderError
from app.db.models import DocumentChunk, User
from app.services.chat import get_assistant_response


def _mock_embedding(text: str, dimensions: int = 16) -> list[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return [byte / 255 for byte in digest[:dimensions]]


def create_embedding(text: str) -> list[float]:
    settings = get_settings()
    if not settings.openai_api_key:
        return _mock_embedding(text)
    try:
        client = OpenAI(api_key=settings.openai_api_key)
        response = client.embeddings.create(
            model=settings.openai_embedding_model,
            input=text,
        )
    except OpenAIError as exc:
        raise ProviderError("OpenAI embedding request failed") from exc
    return list(response.data[0].embedding)


def serialize_embedding(embedding: list[float]) -> str:
    return json.dumps(embedding)


def deserialize_embedding(value: str | None) -> list[float]:
    if value is None:
        return []
    return [float(item) for item in json.loads(value)]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right:
        return 0.0
    limit = min(len(left), len(right))
    left = left[:limit]
    right = right[:limit]
    numerator = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


def answer_from_documents(db: Session, user: User, question: str) -> tuple[str, list[int], str]:
    chunks = list(
        db.scalars(select(DocumentChunk).where(DocumentChunk.user_id == user.id))
    )
    if not chunks:
        raise ProviderError("No usable document context is available")

    query_embedding = create_embedding(question)
    ranked = sorted(
        (
            (
                cosine_similarity(query_embedding, deserialize_embedding(chunk.embedding_json)),
                chunk,
            )
            for chunk in chunks
        ),
        key=lambda item: item[0],
        reverse=True,
    )
    selected = [chunk for score, chunk in ranked[:3] if score > 0]
    if not selected:
        raise ProviderError("No relevant document context is available")

    context = "\n\n".join(chunk.content for chunk in selected)
    answer = get_assistant_response(question, context=context)
    return answer, sorted({chunk.document_id for chunk in selected}), context


def user_has_document_chunks(db: Session, user: User) -> bool:
    return (
        db.scalar(
            select(DocumentChunk.id)
            .where(DocumentChunk.user_id == user.id)
            .limit(1)
        )
        is not None
    )
