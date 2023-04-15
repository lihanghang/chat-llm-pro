"""
文本向量化。如词，句子，段落等
TODO：引入词向量模型包实现本地化部署
"""
import os

import openai

from src.gpt import set_openai_key


def get_embedding(input_slice):
    """

    Args:
        input_slice: query, text_slice etc.

    Returns: List[Tuple]  [(text, embedding)], tokens_usage

    """
    # 先默认使用openai的embedding服务
    set_openai_key(os.getenv("OFFICE_OPENAI_API_KEY"))
    embedding = openai.Embedding.create(engine="text-embedding-ada-002", input=input_slice)
    return [(text, data.embedding) for text, data in zip(input_slice, embedding.data)], embedding.usage.total_tokens
