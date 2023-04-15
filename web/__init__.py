import os

from dotenv import load_dotenv

load_dotenv()
office_openai_key = os.getenv("OFFICE_OPENAI_API_KEY")
host = os.getenv("HOST")
port = os.getenv("PORT")
office_model_name = os.getenv("OFFICE_MODEL_NAME")
api_server = os.getenv("API_SERVER")
# azure openai
azure_model_name = os.getenv('AZURE_MODEL_NAME')
azure_openai_key = os.getenv("AZURE_OPENAI_API_KEY")
api_type = os.getenv("API_TYPE")
api_base = os.getenv("OPENAI_API_BASE")
api_version = os.getenv("OPENAI_API_VERSION")