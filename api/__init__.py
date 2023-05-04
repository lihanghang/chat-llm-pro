import os

import dotenv
import openai
from langchain.chat_models import AzureChatOpenAI

config = dotenv.dotenv_values('.env')
openai.api_type = config["API_TYPE"]
os.environ['OPENAI_API_BASE'] = config["OPENAI_API_BASE"]
os.environ['OPENAI_API_VERSION'] = config["OPENAI_API_VERSION"]
# fix 尽量用这种方式设置azure的可以，测试了下openai_api_key不起作用。
os.environ['OPENAI_API_KEY'] = config["AZURE_OPENAI_API_KEY"]


azure_llm = AzureChatOpenAI(
    deployment_name="gpt-35-turbo",
    temperature=0,
    max_tokens=2048
)



