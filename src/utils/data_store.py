import pickle

import faiss
import numpy as np
from .doc import *


def doc2embedding(parser_file_path):
    """
       文本转化为词向量
       Args:
           parser_file_path: 解析后的文件路径

       Returns: dict

       """

    emb_data = create_embedding(parser_file_path)
    emb = np.array([emm[1] for emm in emb_data])  # 获取向量值
    data = [emm[0] for emm in emb_data]  # 获取向量对应的文本数据

    d = emb.shape[1]
    logging.info(f'd={d}')
    index = faiss.IndexFlatL2(d)
    index.add(emb)
    return {"index": index, "embedding": data}


def save_embedding(embedding_with_index: dict, save_path: str):
    """
    存储词向量至本地文件夹
    Args:
        embedding_with_index:
        save_path: 存储文件路径

    Returns: .pickle file
    """

    # 存储到本地
    with open(save_path, 'wb') as f:
        pickle.dump(embedding_with_index, f)
    logging.info(f'Success save {save_path}')
