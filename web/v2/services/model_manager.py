"""
模型管理器类
"""
import logging
import pickle
from typing import Optional, Dict, Any

import numpy as np
import openai

from src.gpt import GPT, set_openai_key
from src.utils.embedding import get_embedding
from web import (
    api_base,
    api_type,
    api_version,
    azure_model_name,
    azure_openai_key,
    office_model_name,
    office_openai_key,
)


class ModelManager:
    """模型管理器类"""
    
    def __init__(self):
        self.gpt: Optional[GPT] = None
        self.current_model_type: Optional[str] = None
    
    def load_model(self, model_type: str) -> GPT:
        """
        根据模型类型加载不同参数
        Args:
            model_type: 模型类型
        Returns:
            GPT 模型实例
        """
        # 如果已加载相同类型的模型，直接返回
        if self.gpt is not None and self.current_model_type == model_type:
            logging.info(f"使用已加载的模型: {model_type}")
            return self.gpt
        
        try:
            if model_type == "azure":
                set_openai_key(azure_openai_key, api_version, api_base, api_type)
                self.gpt = GPT(engine=azure_model_name, temperature=0.6, max_tokens=1024)
                self.current_model_type = model_type
                logging.info(f"成功加载 Azure 模型: {azure_model_name}")
                
            elif model_type == "open_ai":
                set_openai_key(office_openai_key)
                self.gpt = GPT(engine=office_model_name, temperature=0.6, max_tokens=1024)
                self.current_model_type = model_type
                logging.info(f"成功加载 OpenAI 模型: {office_model_name}")
                
            else:
                logging.warning(f"未知的模型类型: {model_type}")
                return None
            
            return self.gpt
            
        except Exception as e:
            error_msg = f"模型加载失败: {str(e)}"
            logging.error(error_msg)
            raise RuntimeError(error_msg)
    
    def get_current_gpt(self) -> Optional[GPT]:
        """
        获取当前 GPT 实例
        Returns:
            当前 GPT 实例
        """
        return self.gpt
    
    def get_current_store_dir(self) -> Optional[str]:
        """
        获取当前存储目录（从文件服务获取）
        Returns:
            当前存储目录路径
        """
        # 这个方法需要从文件服务获取，暂时返回 None
        # 实际使用时需要通过依赖注入获取
        return None
    
    def load_document_embedding(self, store_dir: str) -> Optional[Dict[str, Any]]:
        """
        加载文档向量数据
        Args:
            store_dir: 存储目录
        Returns:
            向量数据字典
        """
        try:
            embedding_file = f"{store_dir}/embedding.pickle"
            with open(embedding_file, "rb") as file:
                emb_data = pickle.load(file)
            
            logging.info("成功加载文档向量文件")
            return emb_data
            
        except Exception as e:
            error_msg = f"加载文档向量失败: {str(e)}"
            logging.error(error_msg)
            return None
    
    def search_context(self, query: str, embedding_data: Dict[str, Any]) -> Optional[str]:
        """
        搜索相关内容
        Args:
            query: 查询文本
            embedding_data: 向量数据
        Returns:
            相关内容文本
        """
        try:
            index, data = embedding_data["index"], embedding_data["embedding"]
            
            # 计算查询向量
            emb, query_token_num = get_embedding(query)
            logging.info(f"查询 token 数量: {query_token_num}")
            
            # 搜索相关内容
            _, text_index = index.search(np.array([emb[0][1]]), k=15)
            
            # 构建上下文
            context = []
            for i in list(text_index[0]):
                context.extend(data[i : i + 6])
            
            # 控制上下文长度
            lens = [len(text) for text in context]
            maximum = 3000
            for idx, l in enumerate(lens):
                maximum -= l
                if maximum < 0:
                    context = context[: idx + 1]
                    logging.warning(f"超过最大长度，截断到前 {idx + 1} 个片段")
                    break
            
            text = "".join(text for _, text in enumerate(context))
            return text
            
        except Exception as e:
            error_msg = f"搜索上下文失败: {str(e)}"
            logging.error(error_msg)
            return None
