"""
知识管理标签页组件
"""
import gradio as gr
from typing import Dict, Any

try:
    from web.v2.services.chat_service import ChatService
except ImportError:
    from ..services.chat_service import ChatService


class KnowledgeTab:
    """知识管理标签页组件类"""
    
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service
    
    def create_knowledge_tab(self) -> gr.Tab:
        """创建增加模型知识标签页"""
        with gr.Tab("增加模型知识") as tab:
            with gr.Column():
                question = gr.Textbox(
                    label="问题", 
                    value="文因互联是做什么的?",
                    placeholder="请输入问题"
                )
                answer = gr.Textbox(
                    label="答案",
                    value="文因互联是国内领先的金融认知智能解决方案的提供商，在知识图谱技术、自然语言处理技术、金融知识建模等方面有深厚积淀。",
                    placeholder="请输入答案",
                    lines=3
                )
                result = gr.Markdown(
                    label="操作结果",
                    value="等待操作...",
                    elem_id="knowledge-result"
                )
            
            with gr.Row():
                submit_example = gr.Button("添加示例", variant="primary")
                clean_example = gr.Button("清空所有示例", variant="secondary")
            
            # 事件绑定
            submit_example.click(
                fn=self.chat_service.add_examples,
                inputs=[question, answer],
                outputs=result
            )
            
            clean_example.click(
                fn=self.chat_service.del_all_examples,
                inputs=[],
                outputs=result
            )
        
        return tab
