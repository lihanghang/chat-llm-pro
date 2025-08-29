"""
聊天界面组件
"""
import gradio as gr
from typing import List, Dict, Any

try:
    from web.v2.services.chat_service import ChatService
    from web.v2.services.file_service import FileService
except ImportError:
    from ..services.chat_service import ChatService
    from ..services.file_service import FileService


class ChatInterface:
    """聊天界面组件类"""
    
    def __init__(self, chat_service: ChatService, file_service: FileService):
        self.chat_service = chat_service
        self.file_service = file_service
    
    def create_scenario_qa_tab(self) -> gr.Tab:
        """创建场景问答标签页"""
        with gr.Tab("场景问答") as tab:
            with gr.Row():
                with gr.Column():
                    input_text = gr.Textbox(
                        label="我要提问", 
                        placeholder="向大模型提问……"
                    )
                    model_type = gr.Dropdown(
                        choices=["memect", "openai", "azure", "all"],
                        value="memect",
                        label="选择模型类型",
                    )
                    task_type = gr.Radio(
                        choices=["问答", "摘要生成", "事件抽取", "实体抽取", "智能写作", "情感分类", "公告分类", "行业数据分析", "财报数据分析", "答题"],
                        label="场景类型", 
                        value="问答"
                    )
                    submit = gr.Button("问一下", variant="primary")
                
                with gr.Column():
                    output_ret = gr.Text(
                        value="等待提问...",
                        elem_id="output-text",
                        container=True,
                        lines=10,
                        max_lines=20,
                        label="输出结果"
                    )
            
            def process_chat(input_text, task_type, model_type):
                """处理聊天请求"""
                try:
                    if not input_text or not input_text.strip():
                        return "⚠️ 请输入问题内容"
                    
                    print(f"🔍 开始处理: 输入={input_text[:50]}..., 任务类型={task_type}, 模型={model_type}")
                    result = self.chat_service.task_with_chat(input_text, task_type, model_type)
                    print(f"🔍 处理完成，结果长度: {len(result) if result else 0}")
                    print(f"🔍 处理结果前100字符: {result[:100] if result else 'None'}...")
                    
                    # 确保返回的是字符串
                    if result is None:
                        return "❌ 处理失败: 返回结果为空"
                    
                    return str(result)
                except Exception as e:
                    error_msg = f"❌ 处理失败: {str(e)}"
                    print(f"🔍 错误信息: {error_msg}")
                    return error_msg
            
            submit.click(
                fn=process_chat,
                inputs=[input_text, task_type, model_type],
                outputs=output_ret,
            ).then(
                lambda: print("🔍 事件触发完成"),
                outputs=None
            )
            
            # 从 data/example.json 导入示例数据
            try:
                import json
                from pathlib import Path
                
                # 获取项目根目录
                project_root = Path(__file__).resolve().parents[3]
                example_file = project_root / "data" / "example.json"
                
                if example_file.exists():
                    with open(example_file, 'r', encoding='utf-8') as f:
                        example_data = json.load(f)
                        examples = example_data.get("example", [])
                else:
                    # 如果文件不存在，使用默认示例
                    examples = [
                        ["| 行业 | 笔数 | 应收账款余额 | 余额占比 |\n| ---- | ---- | ------------ | -------- |\n| 电力，热力生产和供应业 | 4 | 27938.97 | 30.75% |\n| 土木工程建筑业 | 3 | 21395.21 | 23.54% |\n| 商务服务业 | 3 | 17994.04 | 19.8% |\n| 道路运输业 | 1 | 9894.84 | 10.89% |\n| 公共设施管理业 | 1 | 8455.68 | 9.31% |\n| 研究和试验发展 | 1 | 3919.26 | 4.31% |\n| 科技维广和应用服务业 | 1 | 1274.32 | 1.40% |\n| 合计 | 14 | 90872.33 | 100.00% |", "行业数据分析"],
                        ["帮我写一篇研报，新能源汽车行业，预估比亚迪的股价是286元人民币", "智能写作"]
                    ]
            except Exception as e:
                print(f"加载示例数据失败: {e}")
                # 使用默认示例
                examples = [
                    ["| 行业 | 笔数 | 应收账款余额 | 余额占比 |\n| ---- | ---- | ------------ | -------- |\n| 电力，热力生产和供应业 | 4 | 27938.97 | 30.75% |\n| 土木工程建筑业 | 3 | 21395.21 | 23.54% |\n| 商务服务业 | 3 | 17994.04 | 19.8% |\n| 道路运输业 | 1 | 9894.84 | 10.89% |\n| 公共设施管理业 | 1 | 8455.68 | 9.31% |\n| 研究和试验发展 | 1 | 3919.26 | 4.31% |\n| 科技维广和应用服务业 | 1 | 1274.32 | 1.40% |\n| 合计 | 14 | 90872.33 | 100.00% |", "行业数据分析"],
                    ["帮我写一篇研报，新能源汽车行业，预估比亚迪的股价是286元人民币", "智能写作"]
                ]
            
            # 添加示例
            gr.Examples(
                examples=examples,
                inputs=[input_text, task_type]
            )
        
        return tab
    
    def create_doc_qa_tab(self) -> gr.Tab:
        """创建文档问答标签页"""
        with gr.Tab("MemChatDoc（文档问答）") as tab:
            
            def add_file(history: List[Dict], doc) -> List[Dict]:
                """添加文件上传消息"""
                try:
                    file_info = self.file_service.process_upload_file(doc)
                    history.append({"role": "user", "content": file_info})
                    return history
                except Exception as e:
                    history.append({"role": "user", "content": f"文件上传失败: {str(e)}"})
                    return history
            
            def add_text(history: List[Dict], inp: str) -> tuple:
                """添加文本消息"""
                if inp.strip():
                    history.append({"role": "user", "content": inp})
                return history, ""
            
            def bot(history: List[Dict], model_type: str, task_type: str) -> List[Dict]:
                """处理机器人回复"""
                try:
                    last_user_message = history[-1]["content"]
                    response = self.chat_service.chat_doc(
                        query=last_user_message, 
                        model_type=model_type,
                        task_type=task_type
                    )
                    history.append({"role": "assistant", "content": response})
                except Exception as e:
                    history.append({
                        "role": "assistant", 
                        "content": f"处理失败: {str(e)}"
                    })
                return history
            
            # 聊天机器人组件
            chatbot = gr.Chatbot(
                [{"role": "assistant", "content": "欢迎使用 MemChatDoc，请上传文档。"}],
                show_label=False,
                elem_id="chatbot",
                height=600,
                container=False,
                type="messages",
                render_markdown=True,
            )
            
            model_type = gr.Dropdown(
                choices=["memect", "openai", "azure"], 
                value="memect", 
                label="选择模型类型"
            )
            task_type = gr.Dropdown(
                choices=["问答", "摘要生成", "事件抽取", "实体抽取", "智能写作", "情感分类", "公告分类", "行业数据分析", "财报数据分析", "答题"],
                value="问答",
                label="选择任务类型"
            )
            
            with gr.Row():
                with gr.Column(scale=8):
                    txt = gr.Textbox(
                        show_label=False,
                        placeholder="请输入问题并按回车，或上传文件",
                        container=False,
                    )
                
                with gr.Column(scale=2, min_width=0):
                    btn = gr.UploadButton(
                        label="📁上传文档", 
                        file_types=["file"]
                    )
            
            # 事件绑定
            txt.submit(
                add_text, 
                inputs=[chatbot, txt], 
                outputs=[chatbot, txt], 
                queue=False
            ).then(
                bot, 
                [chatbot, model_type, task_type], 
                chatbot
            )
            
            btn.upload(
                add_file, 
                inputs=[chatbot, btn], 
                outputs=[chatbot]
            ).then(
                bot, 
                [chatbot, model_type, task_type], 
                chatbot
            )
            
            # 清空按钮
            clear = gr.Button("清空对话", variant="secondary")
            clear.click(
                lambda: [], 
                None, 
                chatbot, 
                queue=False
            )
        
        return tab
