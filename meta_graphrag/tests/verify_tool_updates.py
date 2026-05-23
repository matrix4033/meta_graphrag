"""验证工具更新"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from mcp.tool_registry import ToolRegistry
from mcp.query_executor import QueryExecutor
from mcp.result_formatter import ResultFormatter
from utils.config_loader import ConfigLoader

# 加载配置
config_dir = Path(__file__).parent.parent / 'config'
loader = ConfigLoader(config_dir)
configs = loader.load_all_configs()

# 创建组件
query_executor = QueryExecutor(configs, verbose=False)
result_formatter = ResultFormatter(configs, verbose=False)
tool_registry = ToolRegistry(query_executor, result_formatter, configs, verbose=False)

# 获取工具列表
tools = tool_registry.list_tools()

print(f'✓ MCP服务器成功初始化')
print(f'✓ 已注册 {len(tools)} 个工具')
print()
print('工具列表:')
for tool in tools:
    category = tool.get('category', 'N/A')
    desc_len = len(tool.get('description', ''))
    print(f'  - {tool["name"]:25s} [{category:12s}] ({desc_len} chars)')
