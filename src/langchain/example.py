"""
基于Langchain构建LLM应用
https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/unstructured_file.html
https://eyurtsev.github.io/kor/   extract structured data from text using large language models (LLMs) 🧩.

"""
import asyncio
import json
import logging
import os

import openai
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from kor import create_extraction_chain, Object, Text, extract_from_documents
from langchain.llms import AzureOpenAI
from langchain.schema import Document
from typing import List
from dotenv import load_dotenv

from src.langchain.schema import person_schema
from src.utils.doc import parser_doc, read_file, hashcode_with_file


file_path = 'data/靖远煤电：关于公司董事、监事辞职的公告.pdf'
# 加载并解析文件
hashcode = hashcode_with_file(file_path)
parser_file = parser_doc(file_path, f'data/store/{hashcode}')

# loader = UnstructuredFileLoader(file_path, mode='single')
# docs = loader.load()

contents: list = read_file(parser_file)
txt = ''.join(contents)
logging.debug(txt)

docs: List[Document] = [Document(page_content=txt)]
logging.info(f"txt len: {len(txt)}")

# print(docs[100:300][-1].page_content)
# # 加载向量化工具
# embeddings = HuggingFaceEmbeddings(model_name="GanymedeNil/text2vec-large-chinese", )
# # doc embedding
# vector_store = FAISS.from_documents(docs[100:300], embeddings)



logging.info("Create extract chain")
extraction_chain = create_extraction_chain(llm, person_schema, encoder_or_encoder_class='json')

logging.info("Start extract from doc……")
extraction_results = asyncio.run(
    extract_from_documents(
        chain=extraction_chain,
        documents=docs,
        use_uid=False,
        max_concurrency=1
    )
)

for item in extraction_results:
    if item['data']:
        print(json.dumps(item['data'], ensure_ascii=False, indent=4))

