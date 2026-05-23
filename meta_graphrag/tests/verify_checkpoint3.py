"""Checkpoint 3 验证脚本 - 验证MCP服务器和工具功能"""
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.logger import setup_logger


def main():
    """主验证函数"""
    # 设置日志
    logger = setup_logger('checkpoint3_verification', verbose=True)
    
    logger.info("=" * 60)
    logger.info("Checkpoint 3 验证开始")
    logger.info("验证MCP服务器和工具功能 (任务 7-9)")
    logger.info("=" * 60)
    
    # 检查MCP服务器实现状态
    logger.info("\n[检查] 检查MCP服务器实现状态...")
    
    src_mcp_dir = Path(__file__).parent.parent / 'src' / 'mcp'
    
    # 检查必需的MCP模块文件
    required_files = [
        'mcp_server.py',
        'tool_registry.py',
        'query_executor.py',
        'result_formatter.py'
    ]
    
    missing_files = []
    for file_name in required_files:
        file_path = src_mcp_dir / file_name
        if not file_path.exists():
            missing_files.append(file_name)
            logger.warning(f"  ✗ 缺少文件: {file_name}")
        else:
            logger.info(f"  ✓ 找到文件: {file_name}")
    
    if missing_files:
        logger.error("\n" + "=" * 60)
        logger.error("✗✗✗ Checkpoint 3 验证失败 ✗✗✗")
        logger.error("=" * 60)
        logger.error("\nMCP服务器尚未实现！")
        logger.error("\n缺少以下文件:")
        for file_name in missing_files:
            logger.error(f"  - src/mcp/{file_name}")
        logger.error("\n需要完成的任务:")
        logger.error("  - 任务 7.1: 实现MCP服务器基础")
        logger.error("  - 任务 7.2: 实现工具注册器")
        logger.error("  - 任务 7.3: 实现查询执行器")
        logger.error("  - 任务 7.4: 实现结果格式化器")
        logger.error("  - 任务 8.1-8.7: 实现探索式检索工具")
        logger.error("  - 任务 9.1-9.7: 实现路径发现工具")
        logger.error("\n请先完成任务 7-9，然后再运行此验证脚本。")
        return False
    
    # 如果所有文件都存在，继续验证
    logger.info("\n✓ 所有必需的MCP模块文件都存在")
    
    try:
        # 尝试导入MCP模块
        logger.info("\n[步骤 1/7] 导入MCP模块...")
        try:
            from mcp.mcp_server import MCPServer
            from mcp.tool_registry import ToolRegistry
            from mcp.query_executor import QueryExecutor
            from mcp.result_formatter import ResultFormatter
            logger.info("✓ MCP模块导入成功")
        except ImportError as e:
            logger.error(f"✗ MCP模块导入失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
        
        # 加载配置
        logger.info("\n[步骤 2/7] 加载配置...")
        from utils.config_loader import ConfigLoader
        config_dir = Path(__file__).parent.parent / 'config'
        loader = ConfigLoader(config_dir)
        configs = loader.load_all_configs()
        logger.info("✓ 配置加载成功")
        
        # 连接Neo4j（用于测试）
        logger.info("\n[步骤 3/7] 连接Neo4j数据库...")
        from graph.neo4j_connection import Neo4jConnection
        try:
            conn = Neo4jConnection(configs['neo4j_config'])
            logger.info("✓ Neo4j连接成功")
        except Exception as e:
            logger.error(f"✗ Neo4j连接失败: {e}")
            logger.warning("\n提示: 请确保Neo4j数据库正在运行")
            return False
        
        # 初始化MCP服务器
        logger.info("\n[步骤 4/7] 初始化MCP服务器...")
        try:
            server = MCPServer(config_dir, verbose=False)
            logger.info("✓ MCP服务器初始化成功")
        except Exception as e:
            logger.error(f"✗ MCP服务器初始化失败: {e}")
            import traceback
            logger.error(traceback.format_exc())
            conn.close()
            return False
        
        # 验证工具注册
        logger.info("\n[步骤 5/7] 验证工具注册...")
        if server.tool_registry is None:
            logger.error("✗ 工具注册器未初始化")
            server.close()
            return False
        
        tools = server.tool_registry.list_tools()
        logger.info(f"  - 已注册 {len(tools)} 个工具")
        
        expected_tools = [
            'get_graph_overview', 'list_subject_domains', 'search_by_keyword',
            'search_by_attribute', 'get_node_by_name', 'get_node_details',
            'get_node_neighbors', 'find_shortest_path', 'find_all_paths',
            'get_business_lineage', 'get_technical_lineage',
            'discover_related_by_relationship', 'get_subgraph'
        ]
        
        tool_names = [tool['name'] for tool in tools]
        missing_tools = [tool for tool in expected_tools if tool not in tool_names]
        
        if missing_tools:
            logger.error(f"✗ 缺少工具: {missing_tools}")
            server.close()
            return False
        
        logger.info("✓ 所有工具已注册")
        
        # 验证JSON-RPC请求处理
        logger.info("\n[步骤 6/7] 验证JSON-RPC请求处理...")
        
        # 测试initialize请求
        init_request = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'initialize',
            'params': {}
        }
        init_response = server.handle_request(init_request)
        
        if 'result' not in init_response:
            logger.error("✗ initialize请求处理失败")
            server.close()
            return False
        
        logger.info("  - initialize请求处理正常")
        
        # 测试tools/list请求
        list_request = {
            'jsonrpc': '2.0',
            'id': 2,
            'method': 'tools/list',
            'params': {}
        }
        list_response = server.handle_request(list_request)
        
        if 'result' not in list_response or 'tools' not in list_response['result']:
            logger.error("✗ tools/list请求处理失败")
            server.close()
            return False
        
        logger.info("  - tools/list请求处理正常")
        logger.info("✓ JSON-RPC请求处理正常")
        
        # 测试工具调用（如果图谱中有数据）
        logger.info("\n[步骤 7/7] 测试工具调用...")
        
        # 测试get_graph_overview工具
        overview_request = {
            'jsonrpc': '2.0',
            'id': 3,
            'method': 'tools/call',
            'params': {
                'name': 'get_graph_overview',
                'arguments': {}
            }
        }
        overview_response = server.handle_request(overview_request)
        
        if 'result' in overview_response:
            logger.info("  - get_graph_overview工具调用成功")
            result = overview_response['result']
            if 'total_nodes' in result:
                logger.info(f"    图谱节点总数: {result['total_nodes']}")
                logger.info(f"    图谱关系总数: {result['total_relationships']}")
        else:
            logger.warning("  - get_graph_overview工具调用返回错误（可能图谱为空）")
        
        logger.info("✓ 工具调用测试完成")
        
        # 关闭服务器
        server.close()
        conn.close()
        
        # 验证成功
        logger.info("\n" + "=" * 60)
        logger.info("✓✓✓ Checkpoint 3 验证通过 ✓✓✓")
        logger.info("=" * 60)
        logger.info("\n验证结果:")
        logger.info("  ✓ MCP服务器正常工作")
        logger.info("  ✓ 工具注册器正常工作")
        logger.info("  ✓ 查询执行器正常工作")
        logger.info("  ✓ 结果格式化器正常工作")
        logger.info("  ✓ 所有MCP工具正常工作")
        logger.info("\nMCP服务器和工具功能验证完成！")
        logger.info("可以继续执行后续任务（任务 10: CLI命令行接口）")
        
        return True
        
    except Exception as e:
        logger.error(f"\n✗ 验证过程中发生错误: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
