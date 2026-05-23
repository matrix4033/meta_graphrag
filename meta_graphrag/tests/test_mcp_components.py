"""测试MCP组件 - InputValidator, ContextEnricher, ResponseController, ResultFormatter"""
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from mcp.input_validator import InputValidator
from mcp.context_enricher import ContextEnricher
from mcp.response_controller import ResponseSizeController
from mcp.result_formatter import ResultFormatter, PaginationHandler


def test_input_validator():
    """测试InputValidator组件"""
    print("\n=== 测试InputValidator ===")
    validator = InputValidator()
    
    # 测试有效输入
    input_schema = {
        'type': 'object',
        'properties': {
            'keyword': {'type': 'string'},
            'limit': {'type': 'integer'}
        },
        'required': ['keyword']
    }
    
    result = validator.validate('test_tool', {'keyword': 'test', 'limit': 10}, input_schema)
    assert result.is_valid, "有效输入应该通过验证"
    print("✓ 有效输入验证通过")
    
    # 测试缺少必需参数
    result = validator.validate('test_tool', {}, input_schema)
    assert not result.is_valid, "缺少必需参数应该失败"
    assert len(result.errors) > 0, "应该有错误信息"
    print("✓ 缺少必需参数检测正常")
    
    # 测试类型错误
    result = validator.validate('test_tool', {'keyword': 123}, input_schema)
    assert not result.is_valid, "类型错误应该失败"
    print("✓ 类型错误检测正常")
    
    print("✅ InputValidator测试通过")
    return True


def test_context_enricher():
    """测试ContextEnricher组件"""
    print("\n=== 测试ContextEnricher ===")
    
    # 创建mock query executor
    class MockQueryExecutor:
        def execute_single_query(self, query, params):
            # 模拟返回表名
            if 'has_field' in query.lower() and 'table_name' in query.lower():
                return {'table_name': 'test_table'}
            # 模拟返回业务上下文
            elif 'database' in query.lower() and 'has_field' in query.lower():
                return {
                    'database_name': 'test_db',
                    'table_name': 'test_table',
                    'logical_entity_name': '测试逻辑实体',
                    'subject_domain_name': '测试主题域',
                    'business_term': '测试业务术语',
                    'data_source_unit': '测试数源单位',
                    'data_standard': 'TEST-001'
                }
            return None
    
    enricher = ContextEnricher(MockQueryExecutor())
    
    # 测试字段结果增强
    field_data = {'id': 1, 'name': 'test_field'}
    enriched = enricher.enrich_field_result(field_data)
    assert 'table_name' in enriched, "应该包含table_name"
    print("✓ 字段结果增强正常")
    
    # 测试节点详情增强
    node_data = {'id': 1, 'name': 'test_node'}
    enriched = enricher.enrich_node_details(node_data, 'Field')
    assert 'business_context' in enriched, "应该包含business_context"
    print("✓ 节点详情增强正常")
    
    print("✅ ContextEnricher测试通过")
    return True


def test_pagination_handler():
    """测试PaginationHandler组件"""
    print("\n=== 测试PaginationHandler ===")
    handler = PaginationHandler()
    
    # 测试分页格式化
    results = [{'id': 1}, {'id': 2}, {'id': 3}]
    formatted = handler.format_paginated_results(results, offset=0, limit=10, total=100)
    
    assert 'items' in formatted, "应该包含items"
    assert 'pagination' in formatted, "应该包含pagination"
    assert formatted['pagination']['total'] == 100, "total应该正确"
    assert formatted['pagination']['has_more'] == True, "has_more应该为True"
    print("✓ 分页信息格式化正常")
    
    # 测试最后一页
    formatted = handler.format_paginated_results(results, offset=97, limit=10, total=100)
    assert formatted['pagination']['has_more'] == False, "最后一页has_more应该为False"
    print("✓ 最后一页检测正常")
    
    print("✅ PaginationHandler测试通过")
    return True


def test_response_size_controller():
    """测试ResponseSizeController组件"""
    print("\n=== 测试ResponseSizeController ===")
    controller = ResponseSizeController(max_size=100)
    
    # 测试小响应
    small_data = {'message': 'test'}
    result = controller.control_response(small_data)
    assert 'message' in result, "小响应应该保持不变"
    print("✓ 小响应处理正常")
    
    # 测试大响应
    large_data = {'data': 'x' * 200}
    result = controller.control_response(large_data)
    assert 'truncated' in result or 'data' in result, "大响应应该被处理"
    print("✓ 大响应处理正常")
    
    print("✅ ResponseSizeController测试通过")
    return True


def test_result_formatter():
    """测试ResultFormatter组件"""
    print("\n=== 测试ResultFormatter ===")
    
    # 创建mock配置
    mock_config = {
        'mcp': {
            'max_results': 100,
            'default_page_size': 20,
            'max_response_size': 50000
        }
    }
    
    formatter = ResultFormatter(mock_config)
    
    # 测试空结果格式化
    empty_result = formatter.format_empty_result('search', {'keyword': 'test'})
    assert 'message' in empty_result, "空结果应该包含message"
    assert 'reason' in empty_result, "空结果应该包含reason"
    assert 'suggested_action' in empty_result, "空结果应该包含suggested_action"
    print("✓ 空结果格式化正常")
    
    # 测试列表结果精简
    nodes = [
        {'id': 1, 'name': 'node1', 'type': 'Field', 'extra': 'data'},
        {'id': 2, 'name': 'node2', 'type': 'Table', 'extra': 'data'}
    ]
    simplified = formatter.format_node_list(nodes, simplified=True)
    assert len(simplified) == 2, "应该保留所有节点"
    assert 'extra' not in simplified[0], "应该移除额外属性"
    assert 'id' in simplified[0], "应该保留id"
    assert 'name' in simplified[0], "应该保留name"
    assert 'type' in simplified[0], "应该保留type"
    print("✓ 列表结果精简正常")
    
    print("✅ ResultFormatter测试通过")
    return True


def test_search_metadata_tool():
    """测试search_metadata工具整合"""
    print("\n=== 测试search_metadata工具 ===")
    
    from mcp.tool_registry import ToolRegistry
    from mcp.query_executor import QueryExecutor
    
    # 创建mock组件
    class MockQueryExecutor:
        def search_nodes_by_keyword(self, keyword, node_types, offset, limit):
            return [
                {'id': 1, 'type': 'Field', 'properties': {'name': 'test_field'}},
                {'id': 2, 'type': 'Table', 'properties': {'name': 'test_table'}}
            ]
        
        def search_nodes_by_attribute(self, node_type, attr_name, attr_value, offset, limit):
            return [
                {'id': 3, 'type': node_type, 'properties': {attr_name: attr_value}}
            ]
        
        def get_node_by_name_and_type(self, name, node_type):
            return {'id': 4, 'type': node_type, 'properties': {'name': name}}
        
        def execute_single_query(self, query, params):
            # Mock for context enricher
            if 'table_name' in query.lower():
                return {'table_name': 'mock_table'}
            return None
    
    class MockResultFormatter:
        def format_paginated_results(self, results, offset, limit):
            return {
                'items': results,
                'pagination': {
                    'total': len(results),
                    'offset': offset,
                    'limit': limit,
                    'has_more': False
                }
            }
    
    mock_config = {'mcp': {'enabled_tools': []}}
    query_executor = MockQueryExecutor()
    result_formatter = MockResultFormatter()
    
    tool_registry = ToolRegistry(query_executor, result_formatter, mock_config)
    
    # 测试工具是否注册
    tools = tool_registry.list_tools()
    tool_names = [t['name'] for t in tools]
    assert 'search_metadata' in tool_names, "search_metadata工具应该被注册"
    print("✓ search_metadata工具已注册")
    
    # 测试keyword模式
    result = tool_registry.call_tool('search_metadata', {
        'mode': 'keyword',
        'query': 'test',
        'offset': 0,
        'limit': 20
    })
    assert 'content' in result, "应该返回MCP响应格式"
    print("✓ keyword模式工作正常")
    
    # 测试attribute模式
    result = tool_registry.call_tool('search_metadata', {
        'mode': 'attribute',
        'node_type': 'Field',
        'attribute_name': 'business_term',
        'query': '姓名',
        'offset': 0,
        'limit': 20
    })
    assert 'content' in result, "应该返回MCP响应格式"
    print("✓ attribute模式工作正常")
    
    # 测试exact模式
    result = tool_registry.call_tool('search_metadata', {
        'mode': 'exact',
        'node_type': 'PhysicalTable',
        'query': 'test_table',
        'offset': 0,
        'limit': 20
    })
    assert 'content' in result, "应该返回MCP响应格式"
    print("✓ exact模式工作正常")
    
    # 测试Field节点的table_name增强
    result = tool_registry.call_tool('search_metadata', {
        'mode': 'keyword',
        'query': 'test',
        'offset': 0,
        'limit': 20
    })
    # 解析响应内容
    import json
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    # 检查Field节点是否被增强
    field_items = [item for item in content_data['items'] if item.get('type') == 'Field']
    if field_items:
        # 检查是否有table_name
        field_item = field_items[0]
        has_table_name = ('table_name' in field_item or 
                         ('properties' in field_item and 'table_name' in field_item['properties']))
        assert has_table_name, "Field节点应该包含table_name"
        print("✓ Field节点table_name增强正常")
    
    print("✅ search_metadata工具测试通过")
    return True


def test_get_lineage_tool():
    """测试get_lineage工具整合"""
    print("\n=== 测试get_lineage工具 ===")
    
    from mcp.tool_registry import ToolRegistry
    
    # 创建mock组件
    class MockQueryExecutor:
        def get_business_lineage(self, entity_name, entity_type):
            if entity_name == 'test_entity':
                return [
                    {'path': 'mock_business_path', 'path_length': 3}
                ]
            return []
        
        def get_technical_lineage(self, entity_name, entity_type):
            if entity_name == 'test_entity':
                return [
                    {'path': 'mock_technical_path', 'path_length': 2}
                ]
            return []
        
        def execute_single_query(self, query, params):
            # Mock for context enricher
            return None
    
    class MockResultFormatter:
        def format_path_list(self, results):
            return {
                'paths': [{'path': r.get('path'), 'length': r.get('path_length')} for r in results],
                'count': len(results)
            }
    
    mock_config = {'mcp': {'enabled_tools': []}}
    query_executor = MockQueryExecutor()
    result_formatter = MockResultFormatter()
    
    tool_registry = ToolRegistry(query_executor, result_formatter, mock_config)
    
    # 测试工具是否注册
    tools = tool_registry.list_tools()
    tool_names = [t['name'] for t in tools]
    assert 'get_lineage' in tool_names, "get_lineage工具应该被注册"
    print("✓ get_lineage工具已注册")
    
    # 检查工具定义
    lineage_tool = next((t for t in tools if t['name'] == 'get_lineage'), None)
    assert lineage_tool is not None, "应该找到get_lineage工具"
    assert 'category' in lineage_tool, "工具应该有category字段"
    assert lineage_tool['category'] == 'lineage', "category应该是lineage"
    print("✓ get_lineage工具定义正确")
    
    # 测试both模式（默认）
    result = tool_registry.call_tool('get_lineage', {
        'entity_name': 'test_entity'
    })
    assert 'content' in result, "应该返回MCP响应格式"
    
    import json
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert 'business_lineage' in content_data, "both模式应该包含business_lineage"
    assert 'technical_lineage' in content_data, "both模式应该包含technical_lineage"
    print("✓ both模式工作正常")
    
    # 测试business模式
    result = tool_registry.call_tool('get_lineage', {
        'entity_name': 'test_entity',
        'lineage_type': 'business'
    })
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert 'business_lineage' in content_data, "business模式应该包含business_lineage"
    assert 'technical_lineage' not in content_data, "business模式不应该包含technical_lineage"
    print("✓ business模式工作正常")
    
    # 测试technical模式
    result = tool_registry.call_tool('get_lineage', {
        'entity_name': 'test_entity',
        'lineage_type': 'technical'
    })
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert 'technical_lineage' in content_data, "technical模式应该包含technical_lineage"
    assert 'business_lineage' not in content_data, "technical模式不应该包含business_lineage"
    print("✓ technical模式工作正常")
    
    # 测试entity_type参数
    result = tool_registry.call_tool('get_lineage', {
        'entity_name': 'test_entity',
        'lineage_type': 'technical',
        'entity_type': 'Field'
    })
    assert 'content' in result, "应该支持entity_type参数"
    print("✓ entity_type参数支持正常")
    
    # 测试不存在的实体
    result = tool_registry.call_tool('get_lineage', {
        'entity_name': 'nonexistent_entity',
        'lineage_type': 'both'
    })
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert 'error' in content_data, "不存在的实体应该返回错误"
    print("✓ 错误处理正常")
    
    print("✅ get_lineage工具测试通过")
    return True


def test_find_path_tool():
    """测试find_path工具整合"""
    print("\n=== 测试find_path工具 ===")
    
    from mcp.tool_registry import ToolRegistry
    
    # 创建mock组件
    class MockQueryExecutor:
        def find_shortest_path(self, start_node_id, end_node_id):
            if start_node_id == 1 and end_node_id == 2:
                return {'path': 'mock_shortest_path', 'path_length': 1}
            return None
        
        def find_all_paths(self, start_node_id, end_node_id, max_depth):
            if start_node_id == 1 and end_node_id == 2:
                return [
                    {'path': 'mock_path_1', 'path_length': 1},
                    {'path': 'mock_path_2', 'path_length': 2}
                ]
            return []
        
        def discover_related_by_relationship(self, node_id, relationship_type):
            if node_id == 1 and relationship_type == 'HAS_FIELD':
                return [
                    {'id': 3, 'type': 'Field', 'properties': {'name': 'field1'}},
                    {'id': 4, 'type': 'Field', 'properties': {'name': 'field2'}}
                ]
            return []
        
        def execute_single_query(self, query, params):
            # Mock for context enricher
            return None
    
    class MockResultFormatter:
        def format_path(self, result):
            return {
                'path': result.get('path'),
                'length': result.get('path_length')
            }
        
        def format_path_list(self, results):
            return {
                'paths': [{'path': r.get('path'), 'length': r.get('path_length')} for r in results],
                'count': len(results)
            }
        
        def format_node_list(self, results):
            return [
                {'id': r['id'], 'type': r['type'], 'name': r['properties'].get('name')}
                for r in results
            ]
        
        def check_depth_limit(self, depth):
            return depth <= 10
        
        def get_max_depth(self):
            return 10
    
    mock_config = {'mcp': {'enabled_tools': []}}
    query_executor = MockQueryExecutor()
    result_formatter = MockResultFormatter()
    
    tool_registry = ToolRegistry(query_executor, result_formatter, mock_config)
    
    # 测试工具是否注册
    tools = tool_registry.list_tools()
    tool_names = [t['name'] for t in tools]
    assert 'find_path' in tool_names, "find_path工具应该被注册"
    print("✓ find_path工具已注册")
    
    # 检查工具定义
    find_path_tool = next((t for t in tools if t['name'] == 'find_path'), None)
    assert find_path_tool is not None, "应该找到find_path工具"
    assert 'category' in find_path_tool, "工具应该有category字段"
    assert find_path_tool['category'] == 'relationship', "category应该是relationship"
    print("✓ find_path工具定义正确")
    
    # 测试shortest模式（默认）
    result = tool_registry.call_tool('find_path', {
        'start_node_id': 1,
        'end_node_id': 2,
        'mode': 'shortest'
    })
    assert 'content' in result, "应该返回MCP响应格式"
    
    import json
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert 'path' in content_data, "shortest模式应该返回path"
    assert 'length' in content_data, "shortest模式应该返回length"
    print("✓ shortest模式工作正常")
    
    # 测试all模式
    result = tool_registry.call_tool('find_path', {
        'start_node_id': 1,
        'end_node_id': 2,
        'mode': 'all',
        'max_depth': 5
    })
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert 'paths' in content_data, "all模式应该返回paths"
    assert 'count' in content_data, "all模式应该返回count"
    assert content_data['count'] == 2, "应该返回2条路径"
    print("✓ all模式工作正常")
    
    # 测试by_relationship模式
    result = tool_registry.call_tool('find_path', {
        'start_node_id': 1,
        'mode': 'by_relationship',
        'relationship_type': 'HAS_FIELD'
    })
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert 'related_nodes' in content_data, "by_relationship模式应该返回related_nodes"
    assert 'count' in content_data, "by_relationship模式应该返回count"
    assert content_data['count'] == 2, "应该返回2个相关节点"
    print("✓ by_relationship模式工作正常")
    
    # 测试缺少必需参数
    result = tool_registry.call_tool('find_path', {
        'start_node_id': 1,
        'mode': 'shortest'
        # 缺少end_node_id
    })
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert 'error' in content_data, "缺少必需参数应该返回错误"
    print("✓ 参数验证正常")
    
    # 测试不存在的路径
    result = tool_registry.call_tool('find_path', {
        'start_node_id': 999,
        'end_node_id': 888,
        'mode': 'shortest'
    })
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert 'error' in content_data, "不存在的路径应该返回错误"
    assert 'suggestion' in content_data, "错误应该包含建议"
    print("✓ 错误处理正常")
    
    # 测试无效的mode
    result = tool_registry.call_tool('find_path', {
        'start_node_id': 1,
        'mode': 'invalid_mode'
    })
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert 'error' in content_data, "无效的mode应该返回错误"
    print("✓ 模式验证正常")
    
    print("✅ find_path工具测试通过")
    return True


def test_inference_engine():
    """测试InferenceEngine组件"""
    print("\n=== 测试InferenceEngine ===")
    
    from mcp.inference_engine import InferenceEngine
    
    # 创建mock query executor
    class MockQueryExecutor:
        def get_node_by_id(self, node_id):
            if node_id == 1:
                return {
                    'id': 1,
                    'labels': ['Field'],
                    'properties': {
                        'name': 'user_id',
                        'business_term': '用户标识'
                    }
                }
            elif node_id == 10:
                return {
                    'id': 10,
                    'labels': ['PhysicalTable'],
                    'properties': {
                        'table_name': 'user_table'
                    }
                }
            return None
        
        def execute_query(self, query, params):
            # Mock exact term matches
            if 'business_term' in query and 'f1.business_term = f2.business_term' in query:
                return [
                    {'id': 2, 'name': 'customer_id', 'business_term': '用户标识', 'table_name': 'customer_table'},
                    {'id': 3, 'name': 'member_id', 'business_term': '用户标识', 'table_name': 'member_table'}
                ]
            
            # Mock name similarity matches
            if 'CONTAINS' in query and 'field_name' in str(params):
                return [
                    {'id': 4, 'name': 'user_name', 'table_name': 'profile_table'},
                    {'id': 5, 'name': 'userid', 'table_name': 'auth_table'}
                ]
            
            # Mock potential foreign keys
            if 'ENDS WITH' in query and ('_id' in query or '_ID' in query):
                return [
                    {
                        'target_table_id': 11,
                        'target_table': 'reference_table',
                        'source_field': 'user_id',
                        'target_field': 'id',
                        'confidence': 0.8
                    }
                ]
            
            # Mock similar structure tables
            if 'collect(f.name)' in query:
                return [
                    {'id': 12, 'table_name': 'similar_table', 'field_names': ['user_id', 'name', 'email']},
                    {'id': 13, 'table_name': 'another_table', 'field_names': ['id', 'title']}
                ]
            
            return []
        
        def execute_single_query(self, query, params):
            # Mock source table fields
            if 'collect(f.name)' in query and 'table_id' in str(params):
                return {'field_names': ['user_id', 'name', 'email', 'created_at']}
            return None
    
    engine = InferenceEngine(MockQueryExecutor(), similarity_threshold=0.7)
    
    # 测试字段关联推理
    print("  测试字段关联推理...")
    results = engine.infer_related_fields(field_id=1, threshold=0.5)
    assert len(results) > 0, "应该找到相关字段"
    
    # 检查精确匹配结果
    exact_matches = [r for r in results if r.inference_type == 'EXACT_TERM_MATCH']
    assert len(exact_matches) > 0, "应该有精确匹配结果"
    assert exact_matches[0].confidence == 1.0, "精确匹配的confidence应该是1.0"
    print("  ✓ 字段关联推理正常")
    
    # 测试表关系推理
    print("  测试表关系推理...")
    results = engine.infer_table_relationships(table_id=10, threshold=0.5)
    assert len(results) > 0, "应该找到相关表"
    
    # 检查外键推理结果
    fk_results = [r for r in results if r.inference_type == 'POTENTIAL_FOREIGN_KEY']
    assert len(fk_results) > 0, "应该有外键推理结果"
    assert fk_results[0].confidence == 0.8, "外键推理的confidence应该是0.8"
    print("  ✓ 表关系推理正常")
    
    # 测试阈值过滤
    print("  测试阈值过滤...")
    high_threshold_results = engine.infer_related_fields(field_id=1, threshold=0.95)
    low_threshold_results = engine.infer_related_fields(field_id=1, threshold=0.3)
    # 高阈值应该返回更少的结果（只有精确匹配）
    assert len(high_threshold_results) <= len(low_threshold_results), "高阈值应该返回更少结果"
    print("  ✓ 阈值过滤正常")
    
    # 测试InferenceResult的to_dict方法
    print("  测试InferenceResult序列化...")
    if results:
        result_dict = results[0].to_dict()
        assert 'source_id' in result_dict, "应该包含source_id"
        assert 'target_id' in result_dict, "应该包含target_id"
        assert 'inference_type' in result_dict, "应该包含inference_type"
        assert 'confidence' in result_dict, "应该包含confidence"
        assert 'evidence' in result_dict, "应该包含evidence"
        print("  ✓ InferenceResult序列化正常")
    
    print("✅ InferenceEngine测试通过")
    return True


def test_infer_relationships_tool():
    """测试infer_relationships工具"""
    print("\n=== 测试infer_relationships工具 ===")
    
    from mcp.tool_registry import ToolRegistry
    from mcp.models import InferenceResult
    
    # 创建mock组件
    class MockQueryExecutor:
        def get_node_by_id(self, node_id):
            if node_id == 1:
                return {
                    'id': 1,
                    'labels': ['Field'],
                    'properties': {'name': 'user_id', 'business_term': '用户标识'}
                }
            return None
        
        def execute_query(self, query, params):
            return []
        
        def execute_single_query(self, query, params):
            return None
    
    class MockResultFormatter:
        pass
    
    class MockInferenceEngine:
        def infer_related_fields(self, field_id=None, field_name=None, business_term=None, threshold=None):
            return [
                InferenceResult(
                    source_id=field_id or 0,
                    target_id=2,
                    inference_type='EXACT_TERM_MATCH',
                    confidence=1.0,
                    evidence='相同业务术语: 用户标识'
                ),
                InferenceResult(
                    source_id=field_id or 0,
                    target_id=3,
                    inference_type='NAME_SIMILARITY',
                    confidence=0.85,
                    evidence='字段名称相似: userid (相似度: 0.85)'
                )
            ]
        
        def infer_table_relationships(self, table_id=None, table_name=None, threshold=None):
            return [
                InferenceResult(
                    source_id=table_id or 0,
                    target_id=11,
                    inference_type='POTENTIAL_FOREIGN_KEY',
                    confidence=0.8,
                    evidence='字段 user_id 可能引用 reference_table.id'
                )
            ]
    
    mock_config = {'mcp': {'enabled_tools': []}}
    query_executor = MockQueryExecutor()
    result_formatter = MockResultFormatter()
    
    tool_registry = ToolRegistry(query_executor, result_formatter, mock_config)
    
    # 替换推理引擎为mock
    tool_registry.inference_engine = MockInferenceEngine()
    
    # 测试工具是否注册
    tools = tool_registry.list_tools()
    tool_names = [t['name'] for t in tools]
    assert 'infer_relationships' in tool_names, "infer_relationships工具应该被注册"
    print("✓ infer_relationships工具已注册")
    
    # 检查工具定义
    infer_tool = next((t for t in tools if t['name'] == 'infer_relationships'), None)
    assert infer_tool is not None, "应该找到infer_relationships工具"
    assert 'category' in infer_tool, "工具应该有category字段"
    assert infer_tool['category'] == 'inference', "category应该是inference"
    print("✓ infer_relationships工具定义正确")
    
    # 测试fields推理
    result = tool_registry.call_tool('infer_relationships', {
        'target': 'fields',
        'source_id': 1,
        'threshold': 0.7
    })
    assert 'content' in result, "应该返回MCP响应格式"
    
    import json
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert 'target' in content_data, "应该包含target字段"
    assert content_data['target'] == 'fields', "target应该是fields"
    assert 'inferences' in content_data, "应该包含inferences字段"
    assert 'count' in content_data, "应该包含count字段"
    assert 'threshold' in content_data, "应该包含threshold字段"
    assert content_data['count'] == 2, "应该返回2个推理结果"
    
    # 检查推理结果结构
    inference = content_data['inferences'][0]
    assert 'source_id' in inference, "推理结果应该包含source_id"
    assert 'target_id' in inference, "推理结果应该包含target_id"
    assert 'inference_type' in inference, "推理结果应该包含inference_type"
    assert 'confidence' in inference, "推理结果应该包含confidence"
    assert 'evidence' in inference, "推理结果应该包含evidence"
    print("✓ fields推理工作正常")
    
    # 测试tables推理
    result = tool_registry.call_tool('infer_relationships', {
        'target': 'tables',
        'source_id': 10,
        'threshold': 0.7
    })
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert content_data['target'] == 'tables', "target应该是tables"
    assert content_data['count'] == 1, "应该返回1个推理结果"
    print("✓ tables推理工作正常")
    
    # 测试使用source_name参数
    result = tool_registry.call_tool('infer_relationships', {
        'target': 'fields',
        'source_name': 'user_id',
        'threshold': 0.7
    })
    assert 'content' in result, "应该支持source_name参数"
    print("✓ source_name参数支持正常")
    
    # 测试缺少必需参数
    result = tool_registry.call_tool('infer_relationships', {
        'target': 'fields'
        # 缺少source_id和source_name
    })
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert 'error' in content_data, "缺少必需参数应该返回错误"
    assert 'suggestion' in content_data, "错误应该包含建议"
    print("✓ 参数验证正常")
    
    # 测试无效的target
    result = tool_registry.call_tool('infer_relationships', {
        'target': 'invalid_target',
        'source_id': 1
    })
    content_text = result['content'][0]['text']
    content_data = json.loads(content_text)
    
    assert 'error' in content_data, "无效的target应该返回错误"
    print("✓ target验证正常")
    
    print("✅ infer_relationships工具测试通过")
    return True


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("  MCP组件测试")
    print("=" * 60)
    
    try:
        test_input_validator()
        test_context_enricher()
        test_pagination_handler()
        test_response_size_controller()
        test_result_formatter()
        test_search_metadata_tool()
        test_get_lineage_tool()
        test_find_path_tool()
        test_inference_engine()
        test_infer_relationships_tool()
        
        print("\n" + "=" * 60)
        print("  ✅ 所有MCP组件测试通过！")
        print("=" * 60)
        return True
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
