import logging
from typing import Optional

import requests
from openai import OpenAI

from .settings import OPENAI_RERANK_BASE_URL
from .settings import OPENAI_RERANK_API_KEY
from .settings import OPENAI_RERANK_MODEL
from .settings import OPENAI_RERANK_MAX_SIZE
from .utils import get_openai_api_url
from .utils import safe_header_for_debug

__all__ = [
    "get_rerank_scores",
]
_logger = logging.getLogger(__name__)


def get_rerank_scores(
    query,
    documents,
    llm: Optional[OpenAI] = None,
    model: Optional[str] = None,
    max_size: Optional[int] = None,
):
    """返回文本相似度得分列表。"""
    if not documents:
        return []
    if query is None:
        raise RuntimeError(
            422,
            "get_rerank_scores failed: query can NOT be None value.",
        )
    for doc in documents:
        if doc is None:
            raise RuntimeError(
                422,
                "get_rerank_scores failed: documents can NOT have None value.",
            )
    llm = llm or OpenAI(api_key=OPENAI_RERANK_API_KEY, base_url=OPENAI_RERANK_BASE_URL)
    model = model or OPENAI_RERANK_MODEL
    max_size = max_size or OPENAI_RERANK_MAX_SIZE
    # 如果query, documents字符串超过最大长度，则截取最前面的字符串
    if len(query) > max_size:
        _logger.warning(
            "get_rerank_scores warning: the query string exceeds the limit, max_size=%s, query_size=%s",
            max_size,
            len(query),
        )
        query = query[:max_size]
    fixed_documents = []
    for document_index in range(len(documents)):
        document = documents[document_index]
        if len(document) > max_size:
            _logger.warning(
                "get_rerank_scores warning: the document string exceeds the limit, max_size=%s, document_size=%s, document_index=%s",
                max_size,
                len(document),
                document_index,
            )
            document = document[:max_size]
        fixed_documents.append(document)
    # 构建并请求
    url = get_openai_api_url("rerank", llm=llm)
    headers = {
        "Authorization": "Bearer " + llm.api_key,
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "query": query,
        "documents": fixed_documents,
    }
    _logger.debug(
        "get_rerank_scores request start: url=%s, headers=%s, data=%s",
        url,
        safe_header_for_debug(headers),
        data,
    )
    try:
        response = requests.post(
            url,
            json=data,
            headers=headers,
        )
    except Exception as error:
        _logger.error(
            "get_rerank_scores request failed: url=%s, headers=%s, data=%s, error=%s",
            url,
            headers,
            data,
            error,
        )
        raise RuntimeError(
            500,
            f"get_rerank_scores failed: http request failed...",
        )
    _logger.debug(
        "get_rerank_scores request done: url=%s, headers=%s, data=%s, response=%s",
        url,
        safe_header_for_debug(headers),
        data,
        response.text,
    )
    result = [
        x["relevance_score"]
        for x in sorted(response.json().get("results", []), key=lambda z: z["index"])
    ]
    if not result:
        _logger.error(
            "get_rerank_scores request failed: url=%s, headers=%s, data=%s, response=%s",
            url,
            headers,
            data,
            response.text,
        )
        raise RuntimeError(
            500,
            "get_rerank_scores failed: response parse error...",
        )
    return result
