#!/usr/bin/env python3
"""
文件服务模块
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Optional

class FileService:
    """文件服务类"""
    
    def __init__(self):
        """初始化"""
        self.current_store_dir = None
        
    def process_upload_file(self, file) -> str:
        """
        处理上传文件
        Args:
            file: 上传的文件对象
        Returns:
            处理结果信息
        """
        try:
            if not file:
                return "⚠️ 请选择要上传的文件"
            
            # 验证文件
            if not self._validate_file(file):
                return "⚠️ 文件格式不支持或文件损坏"
            
            # 处理新文件
            result = self._process_new_file(file)
            return result
            
        except Exception as e:
            error_msg = f"文件处理失败: {str(e)}"
            logging.error(error_msg)
            return f"❌ {error_msg}"
    
    def _validate_file(self, file) -> bool:
        """
        验证文件
        Args:
            file: 文件对象
        Returns:
            是否有效
        """
        try:
            if not hasattr(file, 'name') or not file.name:
                return False
            
            # 检查文件扩展名
            allowed_extensions = ['.txt', '.pdf', '.doc', '.docx', '.md']
            file_ext = Path(file.name).suffix.lower()
            
            if file_ext not in allowed_extensions:
                return False
            
            return True
            
        except Exception as e:
            logging.error(f"文件验证失败: {e}")
            return False
    
    def _process_new_file(self, file) -> str:
        """
        处理新文件
        Args:
            file: 文件对象
        Returns:
            处理结果
        """
        try:
            # 创建存储目录
            store_dir = self._create_store_dir()
            
            # 保存文件
            file_path = store_dir / file.name
            with open(file_path, 'wb') as f:
                f.write(file.read())
            
            self.current_store_dir = store_dir
            
            return f"✅ 文件 '{file.name}' 上传成功，已保存到存储目录"
            
        except Exception as e:
            error_msg = f"文件保存失败: {str(e)}"
            logging.error(error_msg)
            return f"❌ {error_msg}"
    
    def _create_store_dir(self) -> Path:
        """
        创建存储目录
        Returns:
            存储目录路径
        """
        # 获取项目根目录
        project_root = Path(__file__).resolve().parents[3]
        store_base = project_root / "data" / "store"
        
        # 创建基础目录
        store_base.mkdir(parents=True, exist_ok=True)
        
        # 创建新的存储目录
        import time
        timestamp = int(time.time())
        store_dir = store_base / f"upload_{timestamp}"
        store_dir.mkdir(exist_ok=True)
        
        return store_dir
    
    def get_current_store_dir(self) -> Optional[Path]:
        """
        获取当前存储目录
        Returns:
            存储目录路径
        """
        return self.current_store_dir
    
    def clear_current_store_dir(self):
        """清理当前存储目录"""
        try:
            if self.current_store_dir and self.current_store_dir.exists():
                shutil.rmtree(self.current_store_dir)
                self.current_store_dir = None
                logging.info("清理存储数据完成")
        except Exception as e:
            logging.error(f"清理存储目录失败: {e}")
