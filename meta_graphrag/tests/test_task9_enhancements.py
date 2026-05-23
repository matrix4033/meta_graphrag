"""测试任务9的增强功能"""
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from mcp.query_executor import QueryExecutor
from mcp.result_formatter import ResultFormatter
from mcp.tool_registry import ToolRegistry
from graph.neo4j_connection import Neo4jConnection
from utils.config_loader import ConfigLoader


def test_get_graph_overview_with_subject_domains():
    """测试get_graph_overview工具包含主题域分组统计"""
    print("\n=== 测试 get_graph_overview 包含主题域分组统计 ===")
    
    # 加载配置
    config_dir = Path(__file__).parent.parent / 'config'
    loader = ConfigLoader(config_dir)
    configs = loader.load_all_configs()
    
    # 合并配置
    config = {
        'neo4j': configs['neo4j_config'],
        'mcp': configs['mcp_config'].get('mcp', {})
    }
    
    # 创建Neo4j连接
    neo4j_conn = Neo4jConnection(config['neo4j'])
    
    # 创建查询执行器
    query_executor = QueryExecutor(neo4j_conn, verbose=False)
    
    # 创建结果格式化器
    result_formatter = ResultFormatter(config, verbose=False)
    
    # 创建工具注册器
    tool_registry = ToolRegistry(query_executor, result_formatter, config, verbose=False)
    
    # 调用get_graph_overview工具
    result = tool_registry.call_tool('get_graph_overview', {})
    
    # 解析结果
    import json
    result_data = json.loads(result['content'][0]['text'])
    
    print(f"节点总数: {result_data.get('total_nodes')}")
    print(f"关系总数: {result_data.get('total_relationships')}")
    
    # 验证包含主题域分组统计
    assert 'by_subject_domain' in result_data, "结果应包含by_subject_domain字段"
    
    subject_domain_info = result_data['by_subject_domain']
    assert 'domains' in subject_domain_info, "by_subject_domain应包含domains字段"
    assert 'domain_counts' in subject_domain_info, "by_subject_domain应包含domain_counts字段"
    assert 'total_domains' in subject_domain_info, "by_subject_domain应包含total_domains字段"
    
    print(f"\n主题域总数: {subject_domain_info['total_domains']}")
    print("\n主题域列表:")
    for domain in subject_domain_info['domains']:
        print(f"  - {domain['name']}: {domain['node_count']} 个节点")
    
    print("\n✓ get_graph_overview 包含主题域分组统计测试通过")
    return True


def test_get_node_details_with_include_neighbors():
    """测试get_node_details工具的include_neighbors参数"""
    print("\n=== 测试 get_node_details 的 include_neighbors 参数 ===")
    
    # 加载配置
    config_dir = Path(__file__).parent.parent / 'config'
    loader = ConfigLoader(config_dir)
    configs = loader.load_all_configs()
    
    # 合并配置
    config = {
        'neo4j': configs['neo4j_config'],
        'mcp': configs['mcp_config'].get('mcp', {})
    }
    
    # 创建Neo4j连接
    neo4j_conn = Neo4jConnection(config['neo4j'])
    
    # 创建查询执行器
    query_executor = QueryExecutor(neo4j_conn, verbose=False)
    
    # 创建结果格式化器
    result_formatter = ResultFormatter(config, verbose=False)
    
    # 创建工具注册器
    tool_registry = ToolRegistry(query_executor, result_formatter, config, verbose=False)
    
    # 先搜索一个节点
    search_result = tool_registry.call_tool('search_metadata', {
        'mode': 'keyword',
        'query': '主题域',
        'limit': 1
    })
    
    import json
    search_data = json.loads(search_result['content'][0]['text'])
    
    if not search_data.get('items'):
        print("未找到测试节点，跳过测试")
        return True
    
    node_id = search_data['items'][0]['id']
    print(f"测试节点ID: {node_id}")
    
    # 测试1: include_neighbors=True (默认)
    print("\n测试1: include_neighbors=True (默认)")
    result_with_neighbors = tool_registry.call_tool('get_node_details', {
        'node_id': node_id
    })
    
    data_with_neighbors = json.loads(result_with_neighbors['content'][0]['text'])
    
    assert 'node' in data_with_neighbors, "结果应包含node字段"
    assert 'neighbors' in data_with_neighbors, "结果应包含neighbors字段（默认include_neighbors=True）"
    
    if 'neighbors' in data_with_neighbors:
        neighbors_info = data_with_neighbors['neighbors']
        assert 'summary' in neighbors_info, "neighbors应包含summary字段"
        assert 'nodes' in neighbors_info, "neighbors应包含nodes字段"
        
        summary = neighbors_info['summary']
        print(f"  邻居节点总数: {summary.get('total_count', 0)}")
        print(f"  按类型统计: {summary.get('by_type', {})}")
    
    # 测试2: include_neighbors=False
    print("\n测试2: include_neighbors=False")
    result_without_neighbors = tool_registry.call_tool('get_node_details', {
        'node_id': node_id,
        'include_neighbors': False
    })
    
    data_without_neighbors = json.loads(result_without_neighbors['content'][0]['text'])
    
    assert 'node' in data_without_neighbors, "结果应包含node字段"
    assert 'neighbors' not in data_without_neighbors, "结果不应包含neighbors字段（include_neighbors=False）"
    
    print("  ✓ 不包含邻居节点信息")
    
    print("\n✓ get_node_details 的 include_neighbors 参数测试通过")
    return True


if __name__ == '__main__':
    try:
        test_get_graph_overview_with_subject_domains()
        test_get_node_details_with_include_neighbors()
        print("\n" + "="*60)
        print("所有测试通过！")
        print("="*60)
    except Exception as e:
        print(f"\n测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
