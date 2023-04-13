import os

from dotenv import load_dotenv

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
host = os.getenv("HOST")
port = os.getenv("PORT")
model_name = os.getenv("MODEL_NAME")
api_server = os.getenv("API_SERVER")
# azure openai
api_type = os.getenv("API_TYPE")
api_base = os.getenv("OPENAI_API_BASE")
api_version = os.getenv("OPENAI_API_VERSION")