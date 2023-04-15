"""
基于Langchain构建LLM应用
https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/unstructured_file.html
https://eyurtsev.github.io/kor/   extract structured data from text using large language models (LLMs) 🧩.
TODO 接入文因大模型到信息提取链
"""
import asyncio
import json
import logging
from abc import ABC, abstractmethod

import openai
import requests
from kor import create_extraction_chain, extract_from_documents
from langchain import PromptTemplate, LLMChain, Modal
from langchain.schema import Document
from typing import List

from data import prompt_text
from src.langchain.schema import person_schema
from src.utils.doc import parser_doc, read_file, hashcode_with_file
import os
from dotenv import load_dotenv

# load_dotenv()
# openai.api_type = os.getenv("AZURE_API_TYPE")
# openai.api_base = os.getenv("OPENAI_API_BASE")
# openai.api_version = os.getenv("OPENAI_API_VERSION")
# openai.api_key = os.getenv("OPENAI_API_KEY")

from langchain.chat_models import ChatOpenAI, AzureChatOpenAI
from langchain.llms import AzureOpenAI

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='[%(pastime)s] {%(pathname)s:%(lineno)d} %(levelness)s - %(message)s',
                    datefmt='%H:%M:%S')
logger.setLevel(logging.INFO)


class LLMExtract:
    """
    大模型抽取类
    """
    def __int__(self, llm, schema, docs):
        self.llm = llm
        self.schema = schema
        self.docs = docs


class ModelSelector:
    """模型选择器"""
    def __int__(self, chat_models):
        self.chat_models = chat_models

    @property
    def models(self):
        return self.chat_models


#
# azure_llm = AzureChatOpenAI(
#         deployment_name="gpt-35-turbo",
#         temperature=0,
#         max_tokens=2000,
#         frequency_penalty=0,
#         presence_penalty=0,
#         top_p=1.0
# )
#
# llm = AzureOpenAI(
#     deployment_name="text-davinci-003",
#     temperature=0,
#     max_tokens=2000,
#     frequency_penalty=0,
#     presence_penalty=0,
#     top_p=1.0
# )
#

class BaseModels(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError


class openai_gpt35(BaseModels):
    def execute(self, **kwargs):

        return ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            max_tokens=2000,
            frequency_penalty=0,
            presence_penalty=0,
            top_p=1.0,
            request_timeout=120,
            max_retries=10
    )


class MyModal(Modal):

    def _call(self, prompt: str, stop=None) -> str:
        body = {"prompt": prompt}
        response = requests.post(self.endpoint_url, json=body)
        return response.json()['response']


def parser_pdf(file_path) -> List[Document]:
    logging.info("加载并解析文件……")
    file_name = file_path.name
    hashcode = hashcode_with_file(file_name)
    parser_file = parser_doc(file_name, f'data/store/{hashcode}')
    contents: list = read_file(parser_file)
    txt = ''.join(contents)
    docs = [Document(page_content=txt)]
    return docs


def extract_doc(schema, llm_type, docs=[]):
    llm_obj = llm if llm_type == 'MemectLLM' else openai_llm            # azure_llm
    logging.info("Create extract chain")
    extraction_chain = create_extraction_chain(llm_obj, schema, encoder_or_encoder_class='json')
    logging.info("Start extract from doc……")
    extraction_results = asyncio.run(
        extract_from_documents(
            chain=extraction_chain,
            documents=docs,
            use_uid=False,
            max_concurrency=2
        )
    )
    ret = json.dumps(extraction_results[0]['data'], ensure_ascii=False, indent=4)
    logging.info(ret)
    return ret


def chat_mem_fin_llm(endpoint_url, input_text, task_type):
    mem_llm = MyModal(endpoint_url=endpoint_url)
    query = f"{prompt_text[task_type]} {input_text.strip()}"
    prompt_template = PromptTemplate(input_variables=["query"],
                                     template=f'{{query}}')
    llm_chain = LLMChain(llm=mem_llm, prompt=prompt_template)
    response = llm_chain.run(query)
    return response


if __name__ == '__main__':
    chat_models = {"azure_gpt35": None,
                   "azure_gpt3": None,
                   "openai_gpt35": openai_gpt35()
                   }
    model = "openai_gpt35"
    model_obj = chat_models.get(model)
    if model_obj:
        print(model_obj)
    else:
        raise f"{model}暂未接入。"
