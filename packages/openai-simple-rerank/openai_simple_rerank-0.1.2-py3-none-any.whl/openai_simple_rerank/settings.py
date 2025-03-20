import python_environment_settings

__all__ = [
    "OPENAI_RERANK_BASE_URL",
    "OPENAI_RERANK_API_KEY",
    "OPENAI_RERANK_MODEL",
    "OPENAI_RERANK_MAX_SIZE",
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
OPENAI_RERANK_BASE_URL = python_environment_settings.get(
    "OPENAI_RERANK_BASE_URL",
    OPENAI_BASE_URL,
    aliases=[
        "RERANK_BASE_URL",
    ],
)
OPENAI_RERANK_API_KEY = python_environment_settings.get(
    "OPENAI_RERANK_API_KEY",
    OPENAI_API_KEY,
    aliases=[
        "RERANK_API_KEY",
    ],
)
OPENAI_RERANK_MODEL = python_environment_settings.get(
    "OPENAI_RERANK_MODEL",
    "bge-m3",
    aliases=[
        "OPENAI_RERANK_MODEL_NAME",
        "RERANK_MODEL",
        "RERANK_MODEL_NAME",
    ],
)
OPENAI_RERANK_MAX_SIZE = python_environment_settings.get(
    "OPENAI_RERANK_MAX_SIZE",
    1024,
    aliases=[
        "RERANK_MAX_SIZE",
    ],
)
