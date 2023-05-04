"""
Memect Fin LLM OpenAI
"""
import json
import logging
import traceback

from flask import Flask, request
from kor import create_extraction_chain

from api import azure_llm
from model import schema
app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


@app.route("/api/v1/llm")
def index():
    return "<p>Memect Fin LLM openai.</p>"


@app.route("/api/v1/llm/model_list")
def model():
    schema_name = [item for item in dir(schema) if item.endswith('schema')]
    return {"data": schema_name, "code": 1, "msg": "success", "success": 'true'}


@app.route("/api/v1/llm/extraction", methods=['POST'])
def extract():
    """
    基于大模型抽取文本字段。
    doc
    text
    model_name
    """

    try:
        args = request.get_json()
        txt, model_name = args['text'], args['model_name']
        extract_schema = getattr(schema, model_name)
        # logging.info(f"schema: {extract_schema}")
        extraction_chain = create_extraction_chain(azure_llm, extract_schema, encoder_or_encoder_class='json')
        # extract from text
        result = extraction_chain.predict_and_parse(text=txt)['data']
        logging.info(f"提取结果为：{result}")
        if result is None:
            result["data"] = None
        result['success'] = 'true'
        # 0 未开始，1 提取成功
        result['code'] = 1
        result['msg'] = "extract success."
        # format
        result_format = json.dumps(result, ensure_ascii=False, indent=4)
        return app.make_response((result_format, "200"))

    except Exception as e:
        logging.error(traceback.format_exc())


if __name__ == '__main__':
    logging.info('Prepare to start server, ')
    app.run(host='127.0.0.1', port=9910, debug=True)
