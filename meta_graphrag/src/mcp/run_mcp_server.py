#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""MCP服务器启动脚本 - 确保正确的编码设置"""
import os
import sys

# 强制设置环境变量
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'

# 在 Windows 上设置控制台编码
if sys.platform == 'win32':
    import io
    # 重新包装 stdout 和 stderr，使用 utf-8 编码和 surrogateescape 错误处理
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer, 
        encoding='utf-8', 
        errors='surrogateescape',
        newline='\n'
    )
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer, 
        encoding='utf-8', 
        errors='surrogateescape'
    )

# 导入并运行 MCP 服务器
from mcp_server import main

if __name__ == '__main__':
    main()
