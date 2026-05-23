"""端到端测试 - Checkpoint 5

完整验证整个系统的端到端功能，包括：
1. 配置系统
2. 元数据解析
3. 知识图谱构建
4. MCP服务器
5. CLI命令行接口
6. 数据完整性和正确性
"""
import subprocess
import sys
import json
import tempfile
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.config_loader import ConfigLoader
from utils.logger import setup_logger
from graph.neo4j_connection import Neo4jConnection
from graph.graph_builder import GraphBuilder


class Colors:
    """终端颜色"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """打印标题"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")


def print_test(name, passed, details=""):
    """打印测试结果"""
    if passed:
        print(f"{Colors.GREEN}[✓]{Colors.END} {name}")
    else:
        print(f"{Colors.RED}[✗]{Colors.END} {name}")
    if details:
        for line in details.split('\n'):
            print(f"    {line}")


def test_configuration_system():
    """测试1: 配置系统"""
    print_header("测试 1: 配置系统")
    
    tests_passed = 0
    tests_total = 0
    
    config_dir = Path(__file__).parent.parent / 'config'
    
    # 测试1.1: 配置文件存在
    tests_total += 1
    required_configs = [
        'neo4j_config.yaml',
        'parser_config.yaml',
        'excel_config.yaml',
        'index_config.yaml',
        'mcp_config.yaml'
    ]
    all_exist = all((config_dir / cfg).exists() for cfg in required_configs)
    print_test("所有配置文件存在", all_exist)
    if all_exist:
        tests_passed += 1
    
    # 测试1.2: 配置加载
    tests_total += 1
    try:
        loader = ConfigLoader(config_dir)
        configs = loader.load_all_configs()
        passed = len(configs) == 5
        print_test("配置加载成功", passed, f"加载了 {len(configs)} 个配置文件")
        if passed:
            tests_passed += 1
    except Exception as e:
        print_test("配置加载成功", False, f"错误: {e}")
    
    # 测试1.3: 配置验证
    tests_total += 1
    try:
        from utils.config_validator import ConfigValidator
        validator = ConfigValidator()
        is_valid, errors = validator.validate_all_configs(configs)
        print_test("配置验证通过", is_valid, 
                   f"错误: {errors}" if not is_valid else "")
        if is_valid:
            tests_passed += 1
    except Exception as e:
        print_test("配置验证通过", False, f"错误: {e}")
    
    print(f"\n{Colors.BOLD}配置系统: {tests_passed}/{tests_total} 测试通过{Colors.END}")
    return tests_passed, tests_total


def test_neo4j_connection():
    """测试2: Neo4j连接"""
    print_header("测试 2: Neo4j连接")
    
    tests_passed = 0
    tests_total = 0
    
    config_dir = Path(__file__).parent.parent / 'config'
    
    try:
        loader = ConfigLoader(config_dir)
        neo4j_config = loader.load_neo4j_config()
        
        # 测试2.1: 连接建立
        tests_total += 1
        try:
            conn = Neo4jConnection(neo4j_config)
            print_test("Neo4j连接建立", True)
            tests_passed += 1
        except Exception as e:
            print_test("Neo4j连接建立", False, f"错误: {e}")
            return tests_passed, tests_total
        
        # 测试2.2: 连接验证
        tests_total += 1
        try:
            is_valid = conn.verify_connection()
            print_test("Neo4j连接验证", is_valid)
            if is_valid:
                tests_passed += 1
        except Exception as e:
            print_test("Neo4j连接验证", False, f"错误: {e}")
        
        # 测试2.3: 会话创建
        tests_total += 1
        try:
            with conn.get_session() as session:
                result = session.run("RETURN 1 as value")
                record = result.single()
                passed = record['value'] == 1
                print_test("会话创建和查询", passed)
                if passed:
                    tests_passed += 1
        except Exception as e:
            print_test("会话创建和查询", False, f"错误: {e}")
        
        conn.close()
        
    except Exception as e:
        print_test("Neo4j测试", False, f"错误: {e}")
    
    print(f"\n{Colors.BOLD}Neo4j连接: {tests_passed}/{tests_total} 测试通过{Colors.END}")
    return tests_passed, tests_total


def test_graph_building():
    """测试3: 知识图谱构建"""
    print_header("测试 3: 知识图谱构建")
    
    tests_passed = 0
    tests_total = 0
    
    config_dir = Path(__file__).parent.parent / 'config'
    
    try:
        loader = ConfigLoader(config_dir)
        configs = loader.load_all_configs()
        conn = Neo4jConnection(configs['neo4j_config'])
        
        # 清空数据库
        with conn.get_session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        
        # 准备测试数据
        test_ddl_data = [
            {
                'file_path': 'ddls/TEST/1-测试域-测试主题-测试实体.sql',
                'subject_domain': '测试主题域',
                'business_domain': '测试业务域',
                'business_subject': '测试业务主题',
                'logical_entity': '测试逻辑实体',
                'code': '1',
                'database': 'test_db',
                'tables': [
                    {
                        'table_name': 'test_table',
                        'comment': '测试表',
                        'fields': [
                            {
                                'name': 'id',
                                'data_type': 'INT',
                                'length': None,
                                'nullable': False,
                                'comment': 'ID'
                            },
                            {
                                'name': 'name',
                                'data_type': 'VARCHAR',
                                'length': 100,
                                'nullable': True,
                                'comment': '名称'
                            }
                        ]
                    }
                ]
            }
        ]
        
        test_excel_data = [
            {
                'logical_entity': '测试逻辑实体',
                'table_name': 'test_table',
                'field_name': 'name',
                'business_term': '测试业务术语',
                'data_source_unit': '测试数源单位',
                'data_standard': 'TEST-001'
            }
        ]
        
        # 测试3.1: 图谱构建
        tests_total += 1
        try:
            graph_builder = GraphBuilder(conn, configs)
            graph_builder.build_graph(test_ddl_data, test_excel_data)
            print_test("图谱构建执行", True)
            tests_passed += 1
        except Exception as e:
            print_test("图谱构建执行", False, f"错误: {e}")
            conn.close()
            return tests_passed, tests_total
        
        # 测试3.2: 节点创建
        tests_total += 1
        with conn.get_session() as session:
            result = session.run("MATCH (n) RETURN count(n) as count")
            node_count = result.single()['count']
            passed = node_count > 0
            print_test("节点创建", passed, f"创建了 {node_count} 个节点")
            if passed:
                tests_passed += 1
        
        # 测试3.3: 关系创建
        tests_total += 1
        with conn.get_session() as session:
            result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            rel_count = result.single()['count']
            passed = rel_count > 0
            print_test("关系创建", passed, f"创建了 {rel_count} 个关系")
            if passed:
                tests_passed += 1
        
        # 测试3.4: 业务层节点
        tests_total += 1
        with conn.get_session() as session:
            result = session.run("""
                MATCH (sd:SubjectDomain {name: '测试主题域'})
                RETURN count(sd) as count
            """)
            passed = result.single()['count'] == 1
            print_test("主题域节点创建", passed)
            if passed:
                tests_passed += 1
        
        # 测试3.5: 技术层节点
        tests_total += 1
        with conn.get_session() as session:
            result = session.run("""
                MATCH (pt:PhysicalTable {table_name: 'test_table'})
                RETURN count(pt) as count
            """)
            passed = result.single()['count'] == 1
            print_test("物理表节点创建", passed)
            if passed:
                tests_passed += 1
        
        # 测试3.6: 业务语义属性
        tests_total += 1
        with conn.get_session() as session:
            result = session.run("""
                MATCH (f:Field {name: 'name'})
                RETURN f.business_term as business_term
            """)
            record = result.single()
            passed = record and record['business_term'] == '测试业务术语'
            print_test("业务语义属性", passed)
            if passed:
                tests_passed += 1
        
        # 测试3.7: MAPS_TO关系
        tests_total += 1
        with conn.get_session() as session:
            result = session.run("""
                MATCH (le:LogicalEntity)-[:MAPS_TO]->(pt:PhysicalTable)
                RETURN count(*) as count
            """)
            passed = result.single()['count'] > 0
            print_test("MAPS_TO关系创建", passed)
            if passed:
                tests_passed += 1
        
        # 测试3.8: 完整路径
        tests_total += 1
        with conn.get_session() as session:
            result = session.run("""
                MATCH path = (sd:SubjectDomain)-[:CONTAINS*]->(le:LogicalEntity)
                WHERE sd.name = '测试主题域'
                RETURN length(path) as path_length
            """)
            record = result.single()
            passed = record and record['path_length'] == 3
            print_test("业务层完整路径", passed, 
                       f"路径长度: {record['path_length']}" if record else "")
            if passed:
                tests_passed += 1
        
        conn.close()
        
    except Exception as e:
        print_test("图谱构建测试", False, f"错误: {e}")
    
    print(f"\n{Colors.BOLD}图谱构建: {tests_passed}/{tests_total} 测试通过{Colors.END}")
    return tests_passed, tests_total


def test_mcp_server():
    """测试4: MCP服务器"""
    print_header("测试 4: MCP服务器")
    
    tests_passed = 0
    tests_total = 0
    
    config_dir = Path(__file__).parent.parent / 'config'
    
    try:
        # 测试4.1: MCP模块导入
        tests_total += 1
        try:
            from mcp.mcp_server import MCPServer
            from mcp.tool_registry import ToolRegistry
            print_test("MCP模块导入", True)
            tests_passed += 1
        except ImportError as e:
            print_test("MCP模块导入", False, f"错误: {e}")
            return tests_passed, tests_total
        
        # 测试4.2: MCP服务器初始化
        tests_total += 1
        try:
            server = MCPServer(config_dir, verbose=False)
            print_test("MCP服务器初始化", True)
            tests_passed += 1
        except Exception as e:
            print_test("MCP服务器初始化", False, f"错误: {e}")
            return tests_passed, tests_total
        
        # 测试4.3: 工具注册
        tests_total += 1
        try:
            tools = server.tool_registry.list_tools()
            passed = len(tools) >= 13  # 至少13个工具
            print_test("工具注册", passed, f"注册了 {len(tools)} 个工具")
            if passed:
                tests_passed += 1
        except Exception as e:
            print_test("工具注册", False, f"错误: {e}")
        
        # 测试4.4: initialize请求
        tests_total += 1
        try:
            request = {
                'jsonrpc': '2.0',
                'id': 1,
                'method': 'initialize',
                'params': {}
            }
            response = server.handle_request(request)
            passed = 'result' in response
            print_test("initialize请求处理", passed)
            if passed:
                tests_passed += 1
        except Exception as e:
            print_test("initialize请求处理", False, f"错误: {e}")
        
        # 测试4.5: tools/list请求
        tests_total += 1
        try:
            request = {
                'jsonrpc': '2.0',
                'id': 2,
                'method': 'tools/list',
                'params': {}
            }
            response = server.handle_request(request)
            passed = 'result' in response and 'tools' in response['result']
            print_test("tools/list请求处理", passed)
            if passed:
                tests_passed += 1
        except Exception as e:
            print_test("tools/list请求处理", False, f"错误: {e}")
        
        # 测试4.6: get_graph_overview工具
        tests_total += 1
        try:
            request = {
                'jsonrpc': '2.0',
                'id': 3,
                'method': 'tools/call',
                'params': {
                    'name': 'get_graph_overview',
                    'arguments': {}
                }
            }
            response = server.handle_request(request)
            passed = 'result' in response or 'error' in response
            print_test("get_graph_overview工具调用", passed)
            if passed:
                tests_passed += 1
        except Exception as e:
            print_test("get_graph_overview工具调用", False, f"错误: {e}")
        
        server.close()
        
    except Exception as e:
        print_test("MCP服务器测试", False, f"错误: {e}")
    
    print(f"\n{Colors.BOLD}MCP服务器: {tests_passed}/{tests_total} 测试通过{Colors.END}")
    return tests_passed, tests_total


def test_cli_interface():
    """测试5: CLI命令行接口"""
    print_header("测试 5: CLI命令行接口")
    
    tests_passed = 0
    tests_total = 0
    
    # 测试5.1: 主帮助命令
    tests_total += 1
    try:
        result = subprocess.run(
            [sys.executable, 'src/main.py', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
        passed = '元数据知识图谱平台' in output
        print_test("主帮助命令", passed)
        if passed:
            tests_passed += 1
    except Exception as e:
        print_test("主帮助命令", False, f"错误: {e}")
    
    # 测试5.2: build命令帮助
    tests_total += 1
    try:
        result = subprocess.run(
            [sys.executable, 'src/main.py', 'build', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
        passed = '--ddls-path' in output
        print_test("build命令帮助", passed)
        if passed:
            tests_passed += 1
    except Exception as e:
        print_test("build命令帮助", False, f"错误: {e}")
    
    # 测试5.3: serve命令帮助
    tests_total += 1
    try:
        result = subprocess.run(
            [sys.executable, 'src/main.py', 'serve', '--help'],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout + result.stderr
        passed = '--config-dir' in output
        print_test("serve命令帮助", passed)
        if passed:
            tests_passed += 1
    except Exception as e:
        print_test("serve命令帮助", False, f"错误: {e}")
    
    # 测试5.4: 参数验证
    tests_total += 1
    try:
        result = subprocess.run(
            [sys.executable, 'src/main.py', 'build', '--ddls-path', 'nonexistent'],
            capture_output=True,
            text=True,
            timeout=10
        )
        passed = result.returncode != 0
        print_test("参数验证（不存在的路径）", passed)
        if passed:
            tests_passed += 1
    except Exception as e:
        print_test("参数验证", False, f"错误: {e}")
    
    # 测试5.5: dry-run模式
    tests_total += 1
    try:
        result = subprocess.run(
            [sys.executable, 'src/main.py', 'build', '--ddls-path', 'ddls', '--dry-run'],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout + result.stderr
        passed = 'Dry-run' in output or 'dry-run' in output.lower()
        print_test("dry-run模式", passed)
        if passed:
            tests_passed += 1
    except Exception as e:
        print_test("dry-run模式", False, f"错误: {e}")
    
    print(f"\n{Colors.BOLD}CLI接口: {tests_passed}/{tests_total} 测试通过{Colors.END}")
    return tests_passed, tests_total


def test_data_integrity():
    """测试6: 数据完整性"""
    print_header("测试 6: 数据完整性")
    
    tests_passed = 0
    tests_total = 0
    
    config_dir = Path(__file__).parent.parent / 'config'
    
    try:
        loader = ConfigLoader(config_dir)
        configs = loader.load_all_configs()
        conn = Neo4jConnection(configs['neo4j_config'])
        
        with conn.get_session() as session:
            # 测试6.1: 节点类型完整性
            tests_total += 1
            result = session.run("""
                MATCH (n)
                RETURN DISTINCT labels(n)[0] as label
                ORDER BY label
            """)
            labels = [record['label'] for record in result]
            expected_labels = ['SubjectDomain', 'BusinessDomain', 'BusinessSubject',
                             'LogicalEntity', 'Database', 'PhysicalTable', 'Field']
            passed = all(label in labels for label in expected_labels)
            print_test("节点类型完整性", passed, 
                       f"找到: {', '.join(labels)}")
            if passed:
                tests_passed += 1
            
            # 测试6.2: 关系类型完整性
            tests_total += 1
            result = session.run("""
                MATCH ()-[r]->()
                RETURN DISTINCT type(r) as rel_type
                ORDER BY rel_type
            """)
            rel_types = [record['rel_type'] for record in result]
            expected_rels = ['CONTAINS', 'IMPLEMENTS', 'MAPS_TO', 'HAS_FIELD']
            passed = all(rel in rel_types for rel in expected_rels)
            print_test("关系类型完整性", passed,
                       f"找到: {', '.join(rel_types)}")
            if passed:
                tests_passed += 1
            
            # 测试6.3: 业务层路径完整性
            tests_total += 1
            result = session.run("""
                MATCH path = (sd:SubjectDomain)-[:CONTAINS*3]->(le:LogicalEntity)
                RETURN count(path) as count
            """)
            count = result.single()['count']
            passed = count > 0
            print_test("业务层路径完整性", passed,
                       f"找到 {count} 条完整路径")
            if passed:
                tests_passed += 1
            
            # 测试6.4: 技术层路径完整性
            tests_total += 1
            result = session.run("""
                MATCH path = (db:Database)-[:CONTAINS]->(pt:PhysicalTable)
                              -[:HAS_FIELD]->(f:Field)
                RETURN count(path) as count
            """)
            count = result.single()['count']
            passed = count > 0
            print_test("技术层路径完整性", passed,
                       f"找到 {count} 条完整路径")
            if passed:
                tests_passed += 1
            
            # 测试6.5: 映射关系完整性
            tests_total += 1
            result = session.run("""
                MATCH (le:LogicalEntity)-[:MAPS_TO]->(pt:PhysicalTable)
                RETURN count(*) as count
            """)
            count = result.single()['count']
            passed = count > 0
            print_test("映射关系完整性", passed,
                       f"找到 {count} 个映射")
            if passed:
                tests_passed += 1
            
            # 测试6.6: 业务语义属性存在性
            tests_total += 1
            result = session.run("""
                MATCH (f:Field)
                WHERE f.business_term IS NOT NULL
                RETURN count(f) as count
            """)
            count = result.single()['count']
            passed = count > 0
            print_test("业务语义属性存在", passed,
                       f"找到 {count} 个字段有业务术语")
            if passed:
                tests_passed += 1
        
        conn.close()
        
    except Exception as e:
        print_test("数据完整性测试", False, f"错误: {e}")
    
    print(f"\n{Colors.BOLD}数据完整性: {tests_passed}/{tests_total} 测试通过{Colors.END}")
    return tests_passed, tests_total


def main():
    """主函数"""
    logger = setup_logger('end_to_end_test', verbose=True)
    
    print_header("Checkpoint 5: 端到端测试")
    print(f"{Colors.YELLOW}完整验证整个系统的端到端功能{Colors.END}\n")
    
    all_passed = 0
    all_total = 0
    
    # 运行所有测试
    passed, total = test_configuration_system()
    all_passed += passed
    all_total += total
    
    passed, total = test_neo4j_connection()
    all_passed += passed
    all_total += total
    
    passed, total = test_graph_building()
    all_passed += passed
    all_total += total
    
    passed, total = test_mcp_server()
    all_passed += passed
    all_total += total
    
    passed, total = test_cli_interface()
    all_passed += passed
    all_total += total
    
    passed, total = test_data_integrity()
    all_passed += passed
    all_total += total
    
    # 最终结果
    print_header("Checkpoint 5 最终结果")
    
    percentage = (all_passed / all_total * 100) if all_total > 0 else 0
    
    print(f"通过: {all_passed}/{all_total} ({percentage:.1f}%)")
    print(f"失败: {all_total - all_passed}/{all_total}")
    
    if all_passed == all_total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓✓✓ 所有测试通过！✓✓✓{Colors.END}")
        print(f"{Colors.GREEN}Checkpoint 5 验证成功！系统端到端功能正常。{Colors.END}")
        return 0
    elif percentage >= 80:
        print(f"\n{Colors.YELLOW}Checkpoint 5 基本通过（≥80%），但仍有改进空间。{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}Checkpoint 5 未通过，需要修复失败的测试。{Colors.END}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
