"""
基于 Gradio 进行应用构建
重构版本 - 使用模块化架构
"""
import logging
import os
import shutil
import sys
from pathlib import Path

import gradio as gr

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from web import host, port

# 导入自定义模块
from web.v2.components.chat_interface import ChatInterface
from web.v2.components.knowledge_tab import KnowledgeTab
from web.v2.services.chat_service import ChatService
from web.v2.services.file_service import FileService
from web.v2.services.model_manager import ModelManager
from web.v2.utils.error_handler import handle_errors


class ChatLLMApp:
    """ChatLLM 应用主类"""
    
    def __init__(self):
        """初始化应用"""
        self.model_manager = ModelManager()
        self.file_service = FileService()
        self.chat_service = ChatService(self.model_manager, self.file_service)
        
        # 初始化组件
        self.chat_interface = ChatInterface(self.chat_service, self.file_service)
        self.knowledge_tab = KnowledgeTab(self.chat_service)
    
    @handle_errors
    def init_store_dir(self, store_dir: str) -> None:
        """
        初始化存储目录
        Args:
            store_dir: 存储目录路径
        """
        if not os.path.exists(store_dir):
            os.makedirs(store_dir, exist_ok=True)
            logging.info(f"创建存储目录: {store_dir}")
            return
        
        # 清理现有数据
        for root, dirs, files in os.walk(store_dir):
            for item in dirs:
                dir_path = os.path.join(root, item)
                shutil.rmtree(dir_path)
        logging.info("清理存储数据完成")
    
    def create_app(self) -> gr.Blocks:
        """
        创建 Gradio 应用
        Returns:
            Gradio Blocks 应用实例
        """
        # 自定义 CSS 样式
        custom_css = """
        footer {visibility: hidden}
        .markdown-body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
        }
        .markdown-body h1, .markdown-body h2, .markdown-body h3 {
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }
        .markdown-body code {
            background-color: #f6f8fa;
            padding: 0.2em 0.4em;
            border-radius: 3px;
        }
        .gradio-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        """
        
        with gr.Blocks(
            css=custom_css,
            title="ChatLLM Pro - 大语言模型应用体验",
            theme=gr.themes.Soft()
        ) as demo:
            
            # 页面标题
            gr.Markdown(
                "# 🤖 ChatLLM Pro\n"
                "## 大语言模型应用体验平台\n\n"
                "> 由 MemFinLLM 提供技术支持 | "
                "[联系我们](https://www.memect.cn/)"
            )
            
            # 创建标签页
            with gr.Tabs():
                # 场景问答标签页
                self.chat_interface.create_scenario_qa_tab()
                
                # 文档问答标签页
                self.chat_interface.create_doc_qa_tab()
                
                # 知识管理标签页
                self.knowledge_tab.create_knowledge_tab()
            
            # 页脚信息
            gr.Markdown(
                "---\n"
                "**ChatLLM Pro** - 让 AI 对话更简单、更智能\n\n"
                "支持多种模型：MemectFinLLM、OpenAI GPT、Azure OpenAI"
            )
        
        return demo
    
    def run(self) -> None:
        """运行应用"""
        try:
            # 初始化存储目录
            self.init_store_dir("data/store")
            
            # 创建应用
            demo = self.create_app()
            
            # 启动应用
            print(f"🚀 启动应用: http://{host}:{port}")
            demo.launch(
                server_name=host,
                server_port=int(port),
                share=True,
                show_error=True,
                quiet=False
            )
            
        except Exception as e:
            logging.error(f"应用启动失败: {str(e)}")
            print(f"❌ 应用启动失败: {str(e)}")
            raise


def main():
    """主函数"""
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建并运行应用
    app = ChatLLMApp()
    app.run()


if __name__ == "__main__":
    main()
