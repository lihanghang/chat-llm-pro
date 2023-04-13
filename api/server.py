"""
Memect Fin LLM OpenAI
"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<p>Memect Fin LLM openai.</p>"
