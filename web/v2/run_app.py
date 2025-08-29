#!/usr/bin/env python3
"""
启动应用脚本
"""

import sys
import os
from pathlib import Path

def main():
    """主函数"""
    # 获取项目根目录
    project_root = Path(__file__).resolve().parents[2]
    
    # 添加项目根目录到 Python 路径
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # 导入并运行应用
    from web.v2.chat_server import main as app_main
    app_main()

if __name__ == "__main__":
    main()
