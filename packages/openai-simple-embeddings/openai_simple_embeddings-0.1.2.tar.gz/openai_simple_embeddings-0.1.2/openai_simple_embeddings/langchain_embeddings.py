from typing import Optional
from typing import List
import logging

from openai import OpenAI
from langchain_core.embeddings import Embeddings
from langchain_core.runnables.config import run_in_executor

from .settings import OPENAI_EMBEDDINGS_BASE_URL
from .settings import OPENAI_EMBEDDINGS_API_KEY
from .settings import OPENAI_EMBEDDINGS_MODEL
from .settings import OPENAI_EMBEDDINGS_MAX_SIZE

__all__ = [
    "OpenAISimpleEmbeddings",
]
_logger = logging.getLogger(__name__)


class OpenAISimpleEmbeddings(Embeddings):
    """由于`langchain_openai.embeddings.OpenAIEmbeddings`无法兼容bge-m3等模型，需要重新实现简易的embeddings服务对象用于向量数据库检索。"""

    def __init__(
        self,
        llm: Optional[OpenAI] = None,
        model: Optional[str] = None,
        max_size: Optional[int] = None,
    ):
        self.llm = llm or OpenAI(
            api_key=OPENAI_EMBEDDINGS_API_KEY,
            base_url=OPENAI_EMBEDDINGS_BASE_URL,
        )
        self.model = model or OPENAI_EMBEDDINGS_MODEL
        self.max_size = max_size or OPENAI_EMBEDDINGS_MAX_SIZE

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs."""
        # fix texts by max_size
        fixed_texts = []
        for text_index in range(len(texts)):
            text = texts[text_index]
            if len(text) > self.max_size:
                _logger.warning(
                    "embed_documents: the query text exceeds the limit, text_index=%s, max_size=%s, text_size=%s",
                    text_index,
                    self.max_size,
                    len(text),
                )
                fixed_texts.append(text[: self.max_size])
            else:
                fixed_texts.append(text)
        texts = fixed_texts
        # do embeddings
        _logger.debug(
            "embed_documents start: model=%s, texts=%s",
            self.model,
            texts,
        )
        response = self.llm.embeddings.create(
            input=texts,
            model=self.model,
        )
        result = [x.embedding for x in response.data]
        _logger.debug(
            "embed_documents finished: model=%s, texts=%s, response=%s",
            self.model,
            texts,
            response,
        )
        return result

    def embed_query(self, text: str) -> List[float]:
        """Embed query text."""
        # fix text by max_size
        if len(text) > self.max_size:
            _logger.warning(
                "embed_query: the query text exceeds the limit, max_size=%s, text_size=%s",
                self.max_size,
                len(text),
            )
            text = text[: self.max_size]
        # do embeddings
        _logger.debug(
            "embed_query start: model=%s, text=%s",
            self.model,
            text,
        )
        response = self.llm.embeddings.create(
            input=text,
            model=self.model,
        )
        result = response.data[0].embedding
        _logger.debug(
            "embed_query finished: model=%s, text=%s, response=%s",
            self.model,
            text,
            response,
        )
        return result

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """Asynchronous Embed search docs."""
        return await run_in_executor(None, self.embed_documents, texts)

    async def aembed_query(self, text: str) -> List[float]:
        """Asynchronous Embed query text."""
        return await run_in_executor(None, self.embed_query, text)
