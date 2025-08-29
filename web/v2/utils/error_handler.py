"""
错误处理工具类
"""
import logging
from typing import Any, Callable
from functools import wraps

import gradio as gr


def handle_errors(func: Callable) -> Callable:
    """
    错误处理装饰器
    Args:
        func: 要装饰的函数
    Returns:
        装饰后的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = f"操作失败: {str(e)}"
            logging.error(f"{func.__name__}: {error_msg}")
            return f"❌ {error_msg}"
    
    return wrapper


def validate_input(text: str, max_length: int = 1000) -> bool:
    """
    验证输入文本
    Args:
        text: 输入文本
        max_length: 最大长度
    Returns:
        是否有效
    """
    if not text or not text.strip():
        return False
    
    if len(text) > max_length:
        return False
    
    return True


def format_error_message(error: Exception, context: str = "") -> str:
    """
    格式化错误消息
    Args:
        error: 异常对象
        context: 上下文信息
    Returns:
        格式化的错误消息
    """
    error_type = type(error).__name__
    error_msg = str(error)
    
    if context:
        return f"❌ {context}: {error_type} - {error_msg}"
    else:
        return f"❌ {error_type}: {error_msg}"


def safe_execute(func: Callable, *args, **kwargs) -> tuple[Any, bool]:
    """
    安全执行函数
    Args:
        func: 要执行的函数
        *args: 位置参数
        **kwargs: 关键字参数
    Returns:
        (结果, 是否成功)
    """
    try:
        result = func(*args, **kwargs)
        return result, True
    except Exception as e:
        logging.error(f"函数执行失败 {func.__name__}: {str(e)}")
        return None, False
