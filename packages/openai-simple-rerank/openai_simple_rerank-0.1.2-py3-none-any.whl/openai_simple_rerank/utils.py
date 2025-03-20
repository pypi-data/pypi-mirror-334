from typing import Optional
from openai import OpenAI

from .settings import OPENAI_API_KEY
from .settings import OPENAI_BASE_URL

__all__ = [
    "get_openai_base_url",
    "get_openai_api_url",
    "safe_header_for_debug",
]


def get_openai_base_url(llm: Optional[OpenAI] = None):
    """返回规范化的OPEN AI BASE_URL。

    规范化的URL格式为：http://host/v1/。
    """
    llm = llm or OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
    url = str(llm.base_url)
    if not url.endswith("/"):
        url += "/"
    if not url.endswith("v1/"):
        url += "v1/"
    return url


def get_openai_api_url(name, llm: Optional[OpenAI] = None):
    """获取OPENAI接口指定服务的URL地址。"""
    url = get_openai_base_url(llm=llm)
    return url + name


def safe_header_for_debug(header: dict):
    """隐藏请求头中的敏感信息。"""
    result = {}
    for key, value in header.items():
        if key in ["Authorization", "x-api-key", "apikey", "token"]:
            if isinstance(value, str):
                length = len(value)
                pos = int(length / 3)
                result[key] = value[:pos] + "***" + value[-pos:]
    return result
