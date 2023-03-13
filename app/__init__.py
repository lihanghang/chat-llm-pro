import os
from dotenv import load_dotenv

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
host = os.getenv("HOST")
port = os.getenv("PORT")
model_name = os.getenv("MODEL_NAME")
