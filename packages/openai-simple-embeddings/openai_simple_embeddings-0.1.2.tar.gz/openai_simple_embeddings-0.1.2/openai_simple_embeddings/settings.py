import python_environment_settings

__all__ = [
    "OPENAI_EMBEDDINGS_BASE_URL",
    "OPENAI_EMBEDDINGS_API_KEY",
    "OPENAI_EMBEDDINGS_MODEL",
    "OPENAI_EMBEDDINGS_MAX_SIZE",
]

OPENAI_BASE_URL = python_environment_settings.get(
    "OPENAI_BASE_URL",
    "http://localhost/v1",
    aliases=[
        "LLM_BASE_URL",
        "BASE_URL",
    ],
)
OPENAI_API_KEY = python_environment_settings.get(
    "OPENAI_API_KEY",
    None,
    aliases=[
        "LLM_API_KEY",
        "API_KEY",
    ],
)
OPENAI_EMBEDDINGS_BASE_URL = python_environment_settings.get(
    "OPENAI_EMBEDDINGS_BASE_URL",
    OPENAI_BASE_URL,
    aliases=[
        "EMBEDDINGS_BASE_URL",
    ],
)
OPENAI_EMBEDDINGS_API_KEY = python_environment_settings.get(
    "OPENAI_EMBEDDINGS_API_KEY",
    OPENAI_API_KEY,
    aliases=[
        "EMBEDDINGS_API_KEY",
    ],
)
OPENAI_EMBEDDINGS_MODEL = python_environment_settings.get(
    "OPENAI_EMBEDDINGS_MODEL",
    "bge-m3",
    aliases=[
        "OPENAI_EMBEDDINGS_MODEL_NAME",
        "EMBEDDINGS_MODEL",
        "EMBEDDINGS_MODEL_NAME",
    ],
)
OPENAI_EMBEDDINGS_MAX_SIZE = python_environment_settings.get(
    "OPENAI_EMBEDDINGS_MAX_SIZE",
    1024,
    aliases=[
        "EMBEDDINGS_MAX_SIZE",
    ],
)
