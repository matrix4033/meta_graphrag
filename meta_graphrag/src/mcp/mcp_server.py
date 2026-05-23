"""MCP服务器实现"""
import json
import sys
import os
import warnings
from typing import Dict, Any, List, Optional
from pathlib import Path

# 禁用所有警告，避免干扰 MCP 的 stdout 通信
warnings.filterwarnings('ignore')

# 设置UTF-8编码以避免Windows GBK编码问题
if sys.platform == 'win32':
    import io
    # 重新包装 stdin, stdout, stderr 使用 UTF-8 编码
    sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='surrogateescape')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='surrogateescape', newline='\n')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='surrogateescape')

# 禁用Neo4j驱动的警告输出到stdout
import logging
logging.getLogger('neo4j').setLevel(logging.ERROR)
logging.getLogger('neo4j.io').setLevel(logging.ERROR)
logging.getLogger('neo4j.pool').setLevel(logging.ERROR)

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logger
from utils.config_loader import ConfigLoader
from graph.neo4j_connection import Neo4jConnection


def clean_string(s: Any) -> Any:
    """
    清理字符串中的无效UTF-8字符和代理字符，并处理Neo4j特殊类型
    
    Args:
        s: 输入值（可能是字符串、字典、列表等）
        
    Returns:
        清理后的值
    """
    # 处理Neo4j DateTime类型
    if hasattr(s, 'iso_format'):
        return s.iso_format()
    # 处理Neo4j Date/Time类型
    if hasattr(s, '__class__') and s.__class__.__name__ in ['DateTime', 'Date', 'Time', 'Duration']:
        return str(s)
    
    if isinstance(s, str):
        # 移除代理字符和其他无效字符
        try:
            # 先尝试编码，如果有代理字符会失败
            s.encode('utf-8')
            return s
        except UnicodeEncodeError:
            # 有无效字符，过滤掉代理字符（U+D800 到 U+DFFF）
            cleaned = ''.join(char for char in s if not (0xD800 <= ord(char) <= 0xDFFF))
            return cleaned
    elif isinstance(s, dict):
        return {clean_string(k): clean_string(v) for k, v in s.items()}
    elif isinstance(s, list):
        return [clean_string(item) for item in s]
    else:
        return s


class MCPServer:
    """MCP服务器 - 实现Model Context Protocol规范"""
    
    def __init__(self, config_dir: Path, verbose: bool = False, stdio_mode: bool = False):
        """
        初始化MCP服务器
        
        Args:
            config_dir: 配置文件目录
            verbose: 是否输出详细日志
            stdio_mode: 是否为stdio模式（会禁用日志以避免干扰通信）
        """
        # 在stdio模式下禁用日志，避免干扰JSON-RPC通信
        if stdio_mode:
            self.logger = setup_logger('mcp_server', verbose=False, level=logging.CRITICAL)
        else:
            self.logger = setup_logger('mcp_server', verbose=verbose)
        self.config_dir = config_dir
        self.verbose = verbose and not stdio_mode  # stdio模式下强制关闭verbose
        
        # 加载配置
        self.logger.info("加载配置文件...")
        loader = ConfigLoader(config_dir)
        self.configs = loader.load_all_configs()
        
        # 连接Neo4j
        self.logger.info("连接Neo4j数据库...")
        try:
            self.neo4j_conn = Neo4jConnection(self.configs['neo4j_config'])
            self.logger.info("[OK] Neo4j连接成功")
        except Exception as e:
            self.logger.critical(f"Neo4j连接失败: {e}")
            raise
        
        # 验证图谱数据
        self.logger.info("验证图谱数据...")
        if not self._verify_graph_data():
            self.logger.warning("图谱数据验证失败，某些工具可能无法正常工作")
        else:
            self.logger.info("[OK] 图谱数据验证通过")
        
        # 初始化查询执行器和结果格式化器
        from mcp.query_executor import QueryExecutor
        from mcp.result_formatter import ResultFormatter
        from mcp.tool_registry import ToolRegistry
        from mcp.prompt_registry import PromptRegistry
        
        # stdio模式下禁用所有组件的日志
        component_verbose = verbose and not stdio_mode
        self.query_executor = QueryExecutor(self.neo4j_conn, verbose=component_verbose)
        self.result_formatter = ResultFormatter(self.configs, verbose=component_verbose)
        self.tool_registry = ToolRegistry(
            self.query_executor, 
            self.result_formatter, 
            self.configs, 
            verbose=component_verbose
        )
        self.prompt_registry = PromptRegistry(verbose=component_verbose)
        
        self.logger.info("MCP服务器初始化完成")
    
    def _verify_graph_data(self) -> bool:
        """
        验证图谱数据是否存在
        
        Returns:
            bool: 验证是否通过
        """
        try:
            with self.neo4j_conn.get_session() as session:
                # 检查是否存在SubjectDomain节点
                result = session.run("MATCH (n:SubjectDomain) RETURN count(n) as count")
                subject_domain_count = result.single()['count']
                
                # 检查是否存在BusinessDomain节点
                result = session.run("MATCH (n:BusinessDomain) RETURN count(n) as count")
                business_domain_count = result.single()['count']
                
                # 检查是否存在BusinessSubject节点
                result = session.run("MATCH (n:BusinessSubject) RETURN count(n) as count")
                business_subject_count = result.single()['count']
                
                # 检查是否存在LogicalEntity节点
                result = session.run("MATCH (n:LogicalEntity) RETURN count(n) as count")
                logical_entity_count = result.single()['count']
                
                self.logger.debug(f"图谱节点统计: SubjectDomain={subject_domain_count}, "
                                f"BusinessDomain={business_domain_count}, "
                                f"BusinessSubject={business_subject_count}, "
                                f"LogicalEntity={logical_entity_count}")
                
                # 至少应该有一些节点
                return (subject_domain_count > 0 or business_domain_count > 0 or 
                       business_subject_count > 0 or logical_entity_count > 0)
        except Exception as e:
            self.logger.error(f"验证图谱数据时发生错误: {e}")
            return False
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理JSON-RPC请求
        
        Args:
            request: JSON-RPC请求对象
            
        Returns:
            Dict: JSON-RPC响应对象
        """
        try:
            # 验证请求格式
            if 'jsonrpc' not in request or request['jsonrpc'] != '2.0':
                return self._create_error_response(
                    None, -32600, "Invalid Request: jsonrpc version must be 2.0"
                )
            
            if 'method' not in request:
                return self._create_error_response(
                    request.get('id'), -32600, "Invalid Request: missing method"
                )
            
            method = request['method']
            params = request.get('params', {})
            request_id = request.get('id')
            
            self.logger.debug(f"处理请求: method={method}, params={params}")
            
            # 处理不同的方法
            if method == 'initialize':
                return self._handle_initialize(request_id, params)
            elif method == 'tools/list':
                return self._handle_tools_list(request_id)
            elif method == 'tools/call':
                return self._handle_tools_call(request_id, params)
            elif method == 'prompts/list':
                return self._handle_prompts_list(request_id)
            elif method == 'prompts/get':
                return self._handle_prompts_get(request_id, params)
            else:
                return self._create_error_response(
                    request_id, -32601, f"Method not found: {method}"
                )
        
        except Exception as e:
            self.logger.error(f"处理请求时发生错误: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return self._create_error_response(
                request.get('id'), -32603, f"Internal error: {str(e)}"
            )
    
    def _handle_initialize(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理initialize请求
        
        Args:
            request_id: 请求ID
            params: 请求参数
            
        Returns:
            Dict: 响应对象
        """
        return self._create_success_response(request_id, {
            'protocolVersion': '2024-11-05',
            'capabilities': {
                'tools': {},
                'prompts': {}
            },
            'serverInfo': {
                'name': 'metadata-knowledge-graph-mcp-server',
                'version': '1.0.0'
            }
        })
    
    def _handle_tools_list(self, request_id: Any) -> Dict[str, Any]:
        """
        处理tools/list请求
        
        Args:
            request_id: 请求ID
            
        Returns:
            Dict: 响应对象
        """
        if self.tool_registry is None:
            return self._create_error_response(
                request_id, -32603, "Tool registry not initialized"
            )
        
        tools = self.tool_registry.list_tools()
        return self._create_success_response(request_id, {'tools': tools})
    
    def _handle_tools_call(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理tools/call请求
        
        Args:
            request_id: 请求ID
            params: 请求参数
            
        Returns:
            Dict: 响应对象
        """
        if self.tool_registry is None:
            return self._create_error_response(
                request_id, -32603, "Tool registry not initialized"
            )
        
        tool_name = params.get('name')
        tool_arguments = params.get('arguments', {})
        
        if not tool_name:
            return self._create_error_response(
                request_id, -32602, "Invalid params: missing tool name"
            )
        
        try:
            self.logger.info(f"开始执行工具: {tool_name}")
            result = self.tool_registry.call_tool(tool_name, tool_arguments)
            self.logger.info(f"工具执行完成: {tool_name}")
            
            # 清理结果中的无效字符
            self.logger.debug("清理结果中的无效字符...")
            result = clean_string(result)
            self.logger.debug("清理完成")
            
            self.logger.info(f"创建成功响应: {tool_name}")
            response = self._create_success_response(request_id, result)
            self.logger.info(f"响应创建完成: {tool_name}")
            return response
        except Exception as e:
            self.logger.error(f"工具调用失败: {tool_name}, 错误: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            error_msg = clean_string(str(e))
            return self._create_error_response(
                request_id, -32603, f"Tool execution error: {error_msg}"
            )
    
    def _handle_prompts_list(self, request_id: Any) -> Dict[str, Any]:
        """
        处理prompts/list请求
        
        Args:
            request_id: 请求ID
            
        Returns:
            Dict: 响应对象
        """
        if self.prompt_registry is None:
            return self._create_error_response(
                request_id, -32603, "Prompt registry not initialized"
            )
        
        prompts = self.prompt_registry.list_prompts()
        return self._create_success_response(request_id, {'prompts': prompts})
    
    def _handle_prompts_get(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理prompts/get请求
        
        Args:
            request_id: 请求ID
            params: 请求参数
            
        Returns:
            Dict: 响应对象
        """
        if self.prompt_registry is None:
            return self._create_error_response(
                request_id, -32603, "Prompt registry not initialized"
            )
        
        prompt_name = params.get('name')
        prompt_arguments = params.get('arguments', {})
        
        if not prompt_name:
            return self._create_error_response(
                request_id, -32602, "Invalid params: missing prompt name"
            )
        
        try:
            self.logger.info(f"获取提示词: {prompt_name}")
            result = self.prompt_registry.get_prompt(prompt_name, prompt_arguments)
            self.logger.info(f"提示词获取完成: {prompt_name}")
            
            # 清理结果中的无效字符
            result = clean_string(result)
            
            return self._create_success_response(request_id, result)
        except ValueError as e:
            self.logger.error(f"提示词不存在: {prompt_name}")
            return self._create_error_response(
                request_id, -32602, str(e)
            )
        except Exception as e:
            self.logger.error(f"获取提示词失败: {prompt_name}, 错误: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            error_msg = clean_string(str(e))
            return self._create_error_response(
                request_id, -32603, f"Prompt error: {error_msg}"
            )
    
    def _create_success_response(self, request_id: Any, result: Any) -> Dict[str, Any]:
        """
        创建成功响应
        
        Args:
            request_id: 请求ID
            result: 结果数据
            
        Returns:
            Dict: JSON-RPC响应对象
        """
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'result': result
        }
    
    def _create_error_response(self, request_id: Any, code: int, message: str) -> Dict[str, Any]:
        """
        创建错误响应
        
        Args:
            request_id: 请求ID
            code: 错误代码
            message: 错误消息
            
        Returns:
            Dict: JSON-RPC响应对象
        """
        return {
            'jsonrpc': '2.0',
            'id': request_id,
            'error': {
                'code': code,
                'message': message
            }
        }
    
    def run_stdio(self):
        """
        通过标准输入/输出运行MCP服务器
        """
        self.logger.info("MCP服务器启动 (stdio模式)")
        self.logger.info("等待客户端请求...")
        
        try:
            while True:
                # 从标准输入读取请求
                line = sys.stdin.readline()
                if not line:
                    break
                
                try:
                    self.logger.debug(f"收到请求: {line.strip()[:100]}...")
                    request = json.loads(line)
                    
                    self.logger.info(f"处理请求: method={request.get('method')}, id={request.get('id')}")
                    response = self.handle_request(request)
                    self.logger.info(f"请求处理完成: id={request.get('id')}")
                    
                    # 清理响应中的无效字符
                    self.logger.debug("清理响应中的无效字符...")
                    response = clean_string(response)
                    self.logger.debug("清理完成")
                    
                    # 将响应写入标准输出，使用ensure_ascii=False支持中文
                    self.logger.debug("序列化响应为JSON...")
                    try:
                        response_json = json.dumps(response, ensure_ascii=False)
                        self.logger.debug(f"JSON序列化成功，长度: {len(response_json)}")
                    except Exception as json_err:
                        self.logger.error(f"JSON序列化失败: {json_err}")
                        # 尝试找出问题
                        import traceback
                        self.logger.error(traceback.format_exc())
                        # 返回错误响应
                        error_response = self._create_error_response(
                            request.get('id'), -32603, f"JSON serialization error: {str(json_err)}"
                        )
                        response_json = json.dumps(error_response, ensure_ascii=False)
                    
                    self.logger.debug("写入响应到stdout...")
                    sys.stdout.write(response_json + '\n')
                    sys.stdout.flush()
                    self.logger.info(f"响应已发送: id={request.get('id')}")
                    
                except json.JSONDecodeError as e:
                    self.logger.error(f"JSON解析错误: {e}")
                    error_response = self._create_error_response(
                        None, -32700, f"Parse error: {str(e)}"
                    )
                    sys.stdout.write(json.dumps(error_response) + '\n')
                    sys.stdout.flush()
                except Exception as e:
                    self.logger.error(f"处理请求时发生错误: {e}")
                    import traceback
                    self.logger.error(traceback.format_exc())
                    # 尝试发送错误响应
                    try:
                        error_response = self._create_error_response(
                            request.get('id') if 'request' in locals() else None,
                            -32603,
                            f"Internal error: {str(e)}"
                        )
                        sys.stdout.write(json.dumps(error_response) + '\n')
                        sys.stdout.flush()
                    except:
                        pass
        
        except KeyboardInterrupt:
            self.logger.info("收到中断信号，关闭服务器...")
        except Exception as e:
            self.logger.error(f"服务器运行错误: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
        finally:
            self.close()
    
    def close(self):
        """关闭MCP服务器"""
        self.logger.info("关闭MCP服务器...")
        if self.neo4j_conn:
            self.neo4j_conn.close()
        self.logger.info("MCP服务器已关闭")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='元数据知识图谱MCP服务器')
    parser.add_argument('--config-dir', type=str, default='./config',
                       help='配置文件目录路径')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='详细输出模式（注意：stdio模式下会自动禁用以避免干扰通信）')
    
    args = parser.parse_args()
    
    # 解析配置目录路径，支持相对路径和绝对路径
    config_dir = Path(args.config_dir)
    if not config_dir.is_absolute():
        # 如果是相对路径，相对于当前工作目录
        config_dir = Path.cwd() / config_dir
    
    if not config_dir.exists():
        print(f"错误：配置目录不存在: {config_dir}", file=sys.stderr)
        sys.exit(1)
    
    try:
        # stdio_mode=True 会自动禁用日志
        server = MCPServer(config_dir, verbose=args.verbose, stdio_mode=True)
        server.run_stdio()
    except Exception as e:
        print(f"错误：MCP服务器启动失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
