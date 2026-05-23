"""日志系统配置"""
import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str,
    log_file: Optional[Path] = None,
    level: int = logging.INFO,
    verbose: bool = False
) -> logging.Logger:
    """
    配置日志系统
    
    Args:
        name: 日志器名称
        log_file: 日志文件路径（可选）
        level: 日志级别
        verbose: 是否详细输出模式
    
    Returns:
        配置好的日志器
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if verbose else level)
    
    # 清除现有处理器
    logger.handlers.clear()
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器 - 使用 stderr 避免干扰 MCP 的 stdout 通信
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.DEBUG if verbose else level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（如果指定）
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """获取日志器"""
    return logging.getLogger(name)
