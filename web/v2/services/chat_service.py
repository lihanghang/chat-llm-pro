"""
聊天服务类
"""
import logging
import os
from typing import Optional

import gradio as gr
import openai

from src.extract import chat_mem_fin_llm
from src.gpt import GPT, Example, set_openai_key
from src.utils.embedding import get_embedding
from data import prompt_text
try:
    from web.v2.services.model_manager import ModelManager
except ImportError:
    from .model_manager import ModelManager


class ChatService:
    """聊天服务类"""
    
    def __init__(self, model_manager: ModelManager, file_service=None):
        self.model_manager = model_manager
        self.file_service = file_service
        self.mem_api_base = os.getenv("MEM_FIN_OPENAI_API")
    
    def task_with_chat(self, input_txt: str, task: str, model_type: str) -> str:
        """
        对话式任务
        Args:
            input_txt: 输入文本
            task: 任务类型
            model_type: 模型类型
        Returns:
            响应文本
        """
        logging.info(f"Load model name: {model_type}")
        try:
            logging.info(f"Query: {input_txt}")
            
            # 生成提示信息
            prompt = self._generate_prompt(input_txt, task)
            
            if model_type in ["open_ai", "azure"]:
                gpt = self.model_manager.load_model(model_type)
                response, token_num = gpt.get_top_reply(
                    input_txt, task, context="", model_type=model_type
                )
                logging.info(
                    f"text len: {len(input_txt)}. Consumer token num: {token_num}. Response: {response}"
                )
                return response
                
            elif model_type == "all":
                gpt = self.model_manager.load_model("azure")
                mem_response = chat_mem_fin_llm(self.mem_api_base, prompt, task)
                gpt_response, token_num = gpt.get_top_reply(
                    input_txt, task, context="", model_type="azure"
                )
                return f"# 多模型对比结果\n\n## MemectFinLLM\n{mem_response}\n\n## GPT\n{gpt_response}"
                
            else:
                response = chat_mem_fin_llm(self.mem_api_base, prompt, task)
                logging.info(response)
                return response
                
        except Exception as e:
            error_msg = f"处理失败: {str(e)}"
            logging.error(error_msg)
            return f"❌ {error_msg}"
    
    def _generate_prompt(self, text: str, task_type: str) -> str:
        """
        生成提示信息
        Args:
            text: 输入文本
            task_type: 任务类型
        Returns:
            生成的提示信息
        """
        if task_type in prompt_text and prompt_text[task_type]:
            return f"{prompt_text[task_type]} {text.strip()}\n"
        else:
            return text.strip()
    
    def chat_doc(self, query: str, model_type: str, task_type: str = "问答") -> str:
        """
        基于文档的聊天
        Args:
            query: 查询文本
            model_type: 模型类型
            task_type: 任务类型
        Returns:
            响应文本
        """
        try:
            # 获取当前文档存储路径
            if self.file_service:
                store_dir = self.file_service.get_current_store_dir()
            else:
                store_dir = None
                
            if not store_dir:
                return "⚠️ 无文档信息，请先上传一份文档后再提问。"
            
            # 加载文档向量
            embedding_data = self.model_manager.load_document_embedding(store_dir)
            if not embedding_data:
                return "⚠️ 文档向量加载失败，请重新上传文档。"
            
            # 搜索相关内容
            context = self.model_manager.search_context(query, embedding_data)
            if not context:
                return "⚠️ 未找到相关内容，请尝试其他问题。"
            
            # 生成提示信息
            prompt = self._generate_prompt(context, task_type)
            
            # 生成回复
            if model_type in ["azure", "open_ai"]:
                gpt = self.model_manager.load_model(model_type)
                ret, tokens_num = gpt.get_top_reply(
                    query, task_type, context, model_type
                )
                logging.info(f"Context: {context}\nOutput: {ret}")
                logging.info(f"本轮对话消耗tokens: {tokens_num}")
                return f"## {model_type.upper()} 回复\n\n{ret}"
            else:
                ret = chat_mem_fin_llm(self.mem_api_base, prompt, task_type)
                logging.debug(f"Context: {context}\nOutput: {ret}")
                return f"## {model_type.upper()} 回复\n\n{ret}"
                
        except Exception as e:
            error_msg = f"文档聊天失败: {str(e)}"
            logging.error(error_msg)
            return f"❌ {error_msg}"
    
    def add_examples(self, issue: str, reply: str) -> str:
        """
        添加问答示例
        Args:
            issue: 问题
            reply: 回答
        Returns:
            操作结果
        """
        try:
            gpt = self.model_manager.get_current_gpt()
            if not gpt:
                return "⚠️ 模型未初始化，无法添加示例。"
            
            result = gpt.add_example(Example(issue, reply))
            return f"✅ 示例添加成功！\n\n**问题**: {issue}\n**回答**: {reply}"
        except Exception as e:
            error_msg = f"添加示例失败: {str(e)}"
            logging.error(error_msg)
            return f"❌ {error_msg}"
    
    def del_all_examples(self) -> str:
        """
        删除所有示例
        Returns:
            操作结果
        """
        try:
            gpt = self.model_manager.get_current_gpt()
            if not gpt:
                return "⚠️ 模型未初始化，无法删除示例。"
            
            examples = gpt.get_all_examples()
            for ex_id, _ in examples.items():
                gpt.delete_example(ex_id)
            
            return f"✅ 已删除所有示例（共 {len(examples)} 个）"
        except Exception as e:
            error_msg = f"删除示例失败: {str(e)}"
            logging.error(error_msg)
            return f"❌ {error_msg}"
