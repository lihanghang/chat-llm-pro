import os
import sys

import gradio as gr

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.insert(0, os.path.split(rootPath)[0])

from app import host, port, openai_key, model_name
from data import example
from src.gpt import set_openai_key, GPT, Example

set_openai_key(openai_key)
model_type = 'MemFinLLM'

gpt = GPT(engine=model_name,
          temperature=0.6,
          max_tokens=1024
          )


def add_examples(issue, reply):
    """Generate QA example"""
    return gpt.add_example(Example(issue, reply))


def del_all_examples():
    [gpt.delete_example(ex_id) for ex_id, _ in gpt.get_all_examples().items()]
    return gpt.get_all_examples()


with gr.Blocks(css="footer {visibility: hidden}", title='ChatLLM for NLP') as demo:
    gr.Markdown(f"<h1 style='text-align: center;'>NLP应用场景演示</h1>")
    gr.Markdown(f'> Model by {model_type}. Contact us via https://www.memect.cn/ .')
    with gr.Tab("模型推理"):
        input_doc = gr.Textbox(label="input", value="介绍下文因互联")
        task_type = gr.Radio(choices=["摘要生成", "事件抽取", "问答", "实体抽取", "写作", "公告分类", "情感分类"],
                             label="任务类型", value='问答')
        output_ret = gr.Text(label='output')
        submit = gr.Button("Submit")
        submit.click(fn=gpt.get_top_reply, inputs=[input_doc, task_type], outputs=output_ret)
        gr.Examples(example, [input_doc, task_type])

    with gr.Tab("增加模型知识"):
        with gr.Column():  # 列排列
            question = gr.Textbox(label="question", value="文因互联是做什么的?")
            answer = gr.Textbox(label="answer", value="文因互联是国内领先的金融认知智能解决方案的提供商，在知识图谱技术、自然语言处理技术、金融知识建模等方面有深厚积淀。")
            result = gr.Textbox(label='result')
        submit_example = gr.Button("submit_example")
        clean_example = gr.Button("clean_example")
        submit_example.click(fn=add_examples, inputs=[question, answer], outputs=result)
        clean_example.click(del_all_examples, inputs=[], outputs=result)

demo.launch(server_name=host, server_port=int(port), share=True)
