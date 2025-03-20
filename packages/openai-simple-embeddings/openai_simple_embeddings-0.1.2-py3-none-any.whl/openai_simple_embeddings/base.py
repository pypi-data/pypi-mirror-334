from typing import Optional
import logging

from openai import OpenAI

from .settings import OPENAI_EMBEDDINGS_BASE_URL
from .settings import OPENAI_EMBEDDINGS_API_KEY
from .settings import OPENAI_EMBEDDINGS_MODEL
from .settings import OPENAI_EMBEDDINGS_MAX_SIZE

__all__ = [
    "get_text_embeddings",
]
_logger = logging.getLogger(__name__)


def get_text_embeddings(
    text: str,
    llm: Optional[OpenAI] = None,
    model: Optional[str] = None,
    max_size: Optional[int] = None,
):
    """将文字转化为向量用于向量数据库检索。向量以浮点数数组表示。"""
    llm = llm or OpenAI(
        api_key=OPENAI_EMBEDDINGS_API_KEY,
        base_url=OPENAI_EMBEDDINGS_BASE_URL,
    )
    model = model or OPENAI_EMBEDDINGS_MODEL
    max_size = max_size or OPENAI_EMBEDDINGS_MAX_SIZE
    # fix text by max_size
    if len(text) > max_size:
        _logger.warning(
            "get_text_embeddings: the query text exceeds the limit, max_size=%s, text_size=%s",
            max_size,
            len(text),
        )
        text = text[:max_size]
    # doing embeddings
    try:
        _logger.debug(
            "get_text_embeddings start: model=%s, text=%s",
            model,
            text,
        )
        response = llm.embeddings.create(
            input=text,
            model=model,
        )
        _logger.debug(
            "get_text_embeddings done: model=%s, text=%s, response=%s",
            model,
            text,
            response,
        )
        result = response.data[0].embedding
    except Exception as error:
        _logger.error(
            "get_text_embeddings failed: model=%s, text=%s, error=%s",
            model,
            text,
            error,
        )
        raise RuntimeError(
            500,
            f"get_text_embeddings failed: model={model}, text={text}, error={error}",
        )
    return result
