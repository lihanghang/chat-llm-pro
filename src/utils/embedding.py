"""
文本向量化。如词，句子，段落等
TODO：引入词向量模型包实现本地化部署。text2vec-large-chinese
"""
import logging
import os

import openai
from langchain.embeddings import HuggingFaceEmbeddings

from src.gpt import set_openai_key

embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec": "GanymedeNil/text2vec-large-chinese",
}


def get_embedding(input_slice):
    """

    Args:
        input_slice: query, text_slice etc.


    Returns: List[Tuple]  [(text, embedding)], tokens_usage

    """
    local = os.getenv('is_local').lower() in ('true', '1', 't')
    if not local:
        # 先默认使用openai的embedding服务
        set_openai_key(os.getenv("OFFICE_OPENAI_API_KEY"))
        embedding = openai.Embedding.create(engine="text-embedding-ada-002", input=input_slice)
        return [(text, data.embedding) for text, data in zip(input_slice, embedding.data)], embedding.usage.total_tokens
    else:
        logging.info("Load local text2Vector.")
        embedding_obj = HuggingFaceEmbeddings(model_name=embedding_model_dict['text2vec'],)
        embedding = embedding_obj.embed_documents(input_slice)
        return [(text, data) for text, data in zip(input_slice, embedding)], len(input_slice)
