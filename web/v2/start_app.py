#!/usr/bin/env python3
"""
智能启动脚本 - 自动处理端口冲突
"""
import os
import sys
import subprocess
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parents[2]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def kill_port(port):
    """杀死占用指定端口的进程"""
    try:
        result = subprocess.run(
            f"lsof -ti:{port} | xargs kill -9",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ 已释放端口 {port}")
        else:
            print(f"ℹ️ 端口 {port} 未被占用")
    except Exception as e:
        print(f"⚠️ 释放端口失败: {e}")

def check_port_available(port):
    """检查端口是否可用"""
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def start_app():
    """启动应用"""
    print("🚀 启动 ChatLLM Pro 应用...")
    
    # 获取端口配置
    from web import host, port
    target_port = int(port)
    
    print(f"📍 目标端口: {target_port}")
    
    # 检查并释放端口
    if not check_port_available(target_port):
        print(f"⚠️ 端口 {target_port} 被占用，正在释放...")
        kill_port(target_port)
        time.sleep(2)  # 等待端口释放
    
    # 再次检查端口
    if check_port_available(target_port):
        print(f"✅ 端口 {target_port} 可用")
    else:
        print(f"❌ 端口 {target_port} 仍被占用，尝试使用其他端口...")
        # 尝试其他端口
        for alt_port in range(target_port + 1, target_port + 10):
            if check_port_available(alt_port):
                print(f"✅ 使用备用端口: {alt_port}")
                os.environ["PORT"] = str(alt_port)
                break
        else:
            print("❌ 无法找到可用端口")
            return False
    
    # 激活虚拟环境并启动应用
    try:
        venv_python = project_root / ".venv" / "bin" / "python"
        if not venv_python.exists():
            venv_python = project_root / ".venv" / "Scripts" / "python.exe"
        
        if venv_python.exists():
            cmd = [str(venv_python), "web/v2/run_app.py"]
        else:
            cmd = ["python", "web/v2/run_app.py"]
        
        print("🎯 启动应用...")
        subprocess.run(cmd, cwd=project_root)
        
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    start_app()
