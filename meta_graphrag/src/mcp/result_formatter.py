"""MCP结果格式化器"""
import sys
from typing import Dict, Any, List
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logger
from mcp.models import PaginationInfo
from mcp.response_controller import ResponseSizeController


def clean_string_value(value: Any) -> Any:
    """
    清理字符串中的代理字符和Neo4j特殊类型
    
    Args:
        value: 输入值
        
    Returns:
        清理后的值
    """
    # 处理Neo4j DateTime类型
    if hasattr(value, 'iso_format'):
        return value.iso_format()
    # 处理Neo4j Date类型
    elif hasattr(value, '__class__') and value.__class__.__name__ in ['DateTime', 'Date', 'Time']:
        return str(value)
    elif isinstance(value, str):
        try:
            value.encode('utf-8')
            return value
        except UnicodeEncodeError:
            # 过滤掉代理字符（U+D800 到 U+DFFF）
            return ''.join(char for char in value if not (0xD800 <= ord(char) <= 0xDFFF))
    return value


class PaginationHandler:
    """分页处理器 - 处理分页信息"""
    
    def __init__(self, default_page_size: int = 20):
        """
        初始化分页处理器
        
        Args:
            default_page_size: 默认每页数量
        """
        self.default_page_size = default_page_size
    
    def format_paginated_results(self, results: List[Dict[str, Any]], 
                                 offset: int = 0, 
                                 limit: int = None,
                                 total: int = None) -> Dict[str, Any]:
        """
        格式化分页结果，返回total、offset、limit、has_more
        
        Args:
            results: 结果列表
            offset: 偏移量
            limit: 限制数量
            total: 总数量（如果已知）
            
        Returns:
            Dict: 格式化后的分页结果
        """
        if limit is None:
            limit = self.default_page_size
        
        # 如果没有提供总数，使用结果数量
        if total is None:
            total = len(results)
        
        # 检查是否还有更多结果
        has_more = (offset + limit) < total
        
        pagination = PaginationInfo(
            total=total,
            offset=offset,
            limit=limit,
            has_more=has_more
        )
        
        return {
            'items': results,
            'pagination': {
                'total': pagination.total,
                'offset': pagination.offset,
                'limit': pagination.limit,
                'has_more': pagination.has_more
            }
        }


class ResultFormatter:
    """结果格式化器 - 格式化查询结果"""
    
    def __init__(self, mcp_config: Dict[str, Any], verbose: bool = False):
        """
        初始化结果格式化器
        
        Args:
            mcp_config: MCP配置
            verbose: 是否输出详细日志
        """
        self.logger = setup_logger('result_formatter', verbose=verbose)
        self.mcp_config = mcp_config
        self.max_results = mcp_config.get('mcp', {}).get('max_results', 100)
        self.default_page_size = mcp_config.get('mcp', {}).get('default_page_size', 20)
        self.pagination_handler = PaginationHandler(self.default_page_size)
        
        # 初始化响应大小控制器
        max_response_size = mcp_config.get('mcp', {}).get('max_response_size', 50000)
        self.response_controller = ResponseSizeController(max_response_size, verbose=verbose)
    
    def format_node(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        格式化节点数据
        
        Args:
            node_data: 节点数据
            
        Returns:
            Dict: 格式化后的节点数据
        """
        return {
            'id': node_data.get('id'),
            'type': node_data.get('type') or (node_data.get('labels', [None])[0] if 'labels' in node_data else None),
            'properties': node_data.get('properties', {})
        }
    
    def format_node_list(self, nodes: List[Dict[str, Any]], simplified: bool = True) -> List[Dict[str, Any]]:
        """
        格式化节点列表，支持精简模式
        
        Args:
            nodes: 节点列表
            simplified: 是否使用精简模式（只返回id、name、type等关键属性）
            
        Returns:
            List: 格式化后的节点列表
        """
        if simplified:
            # 精简模式：只返回关键属性
            simplified_nodes = []
            for node in nodes:
                node_type = node.get('type') or (node.get('labels', [None])[0] if 'labels' in node else None)
                properties = node.get('properties', {})
                
                # 提取名称（根据节点类型）
                name = (properties.get('name') or 
                       properties.get('table_name') or 
                       properties.get('logical_name') or 
                       properties.get('comment', '')[:50])  # 如果没有名称，使用注释的前50个字符
                
                simplified_nodes.append({
                    'id': node.get('id'),
                    'type': node_type,
                    'name': name
                })
            return simplified_nodes
        else:
            # 完整模式
            return [self.format_node(node) for node in nodes]
    
    def format_paginated_results(self, results: List[Dict[str, Any]], 
                                 offset: int = 0, limit: int = None,
                                 total: int = None, simplified: bool = True) -> Dict[str, Any]:
        """
        格式化分页结果
        
        Args:
            results: 结果列表
            offset: 偏移量
            limit: 限制数量
            total: 总数量（如果已知）
            simplified: 是否使用精简模式
            
        Returns:
            Dict: 格式化后的分页结果
        """
        formatted_results = self.format_node_list(results, simplified=simplified)
        return self.pagination_handler.format_paginated_results(
            formatted_results, offset, limit, total
        )
    
    def format_path(self, path_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        格式化路径数据，以层级结构展示节点和关系
        
        Args:
            path_data: 路径数据
            
        Returns:
            Dict: 格式化后的路径数据
        """
        path = path_data.get('path')
        if path is None:
            return None
        
        # 提取路径中的节点和关系
        nodes = []
        relationships = []
        hierarchical_path = []
        
        # Neo4j path对象包含nodes和relationships
        if hasattr(path, 'nodes'):
            for node in path.nodes:
                # 清理节点属性中的代理字符
                properties = {key: clean_string_value(value) for key, value in dict(node).items()}
                
                nodes.append({
                    'id': node.id,
                    'type': list(node.labels)[0] if node.labels else None,
                    'properties': properties
                })
        
        if hasattr(path, 'relationships'):
            for rel in path.relationships:
                # 清理关系属性中的代理字符
                properties = {key: clean_string_value(value) for key, value in dict(rel).items()}
                
                relationships.append({
                    'type': rel.type,
                    'start_node': rel.start_node.id,
                    'end_node': rel.end_node.id,
                    'properties': properties
                })
        
        # 构建层级结构路径
        if nodes:
            for i, node in enumerate(nodes):
                hierarchical_path.append({
                    'step': i,
                    'node': {
                        'id': node['id'],
                        'type': node['type'],
                        'name': node['properties'].get('name') or 
                               node['properties'].get('table_name') or 
                               node['properties'].get('logical_name')
                    }
                })
                
                # 添加关系（如果不是最后一个节点）
                if i < len(relationships):
                    hierarchical_path.append({
                        'step': i,
                        'relationship': relationships[i]['type']
                    })
        
        return {
            'nodes': nodes,
            'relationships': relationships,
            'hierarchical_path': hierarchical_path,
            'length': path_data.get('path_length', len(relationships))
        }
    
    def format_path_list(self, paths: List[Dict[str, Any]], 
                        max_paths: int = None) -> Dict[str, Any]:
        """
        格式化路径列表
        
        Args:
            paths: 路径列表
            max_paths: 最大路径数量
            
        Returns:
            Dict: 格式化后的路径列表
        """
        if max_paths is None:
            max_paths = self.mcp_config.get('mcp', {}).get('max_paths', 50)
        
        total = len(paths)
        limited_paths = paths[:max_paths]
        
        formatted_paths = []
        for path_data in limited_paths:
            formatted_path = self.format_path(path_data)
            if formatted_path:
                formatted_paths.append(formatted_path)
        
        return {
            'paths': formatted_paths,
            'total': total,
            'returned': len(formatted_paths),
            'has_more': total > max_paths
        }
    
    def format_subgraph(self, subgraph_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        格式化子图数据
        
        Args:
            subgraph_data: 子图数据
            
        Returns:
            Dict: 格式化后的子图数据
        """
        nodes = subgraph_data.get('nodes', [])
        edges = subgraph_data.get('edges', [])
        
        return {
            'nodes': self.format_node_list(nodes),
            'edges': [
                {
                    'source': edge['source'],
                    'target': edge['target'],
                    'relationship': edge['relationship']
                }
                for edge in edges
            ],
            'node_count': len(nodes),
            'edge_count': len(edges)
        }
    
    def format_statistics(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """
        格式化统计信息
        
        Args:
            stats: 统计信息
            
        Returns:
            Dict: 格式化后的统计信息
        """
        formatted_stats = {
            'node_counts': stats.get('node_counts', {}),
            'relationship_counts': stats.get('relationship_counts', {}),
            'total_nodes': stats.get('total_nodes', 0),
            'total_relationships': stats.get('total_relationships', 0)
        }
        
        # 添加主题域分组统计
        if 'by_subject_domain' in stats:
            formatted_stats['by_subject_domain'] = stats['by_subject_domain']
        
        return formatted_stats
    
    def format_node_details(self, node_data: Dict[str, Any], 
                           neighbors: List[Dict[str, Any]],
                           include_neighbors: bool = True) -> Dict[str, Any]:
        """
        格式化节点详情
        
        Args:
            node_data: 节点数据
            neighbors: 邻居节点列表
            include_neighbors: 是否包含邻居节点信息
            
        Returns:
            Dict: 格式化后的节点详情
        """
        result = {
            'node': self.format_node(node_data)
        }
        
        # 如果需要包含邻居节点信息
        if include_neighbors:
            # 分类邻居节点（入边和出边）
            incoming = []
            outgoing = []
            
            for neighbor in neighbors:
                # 这里简化处理，实际应该根据关系方向分类
                # 暂时都放入incoming
                incoming.append(self.format_node(neighbor))
            
            # 生成邻居节点摘要
            neighbor_summary = {
                'total_count': len(neighbors),
                'incoming_count': len(incoming),
                'outgoing_count': len(outgoing)
            }
            
            # 按类型统计邻居节点
            type_counts = {}
            for neighbor in neighbors:
                node_type = neighbor.get('type') or (neighbor.get('labels', [None])[0] if 'labels' in neighbor else None)
                type_counts[node_type] = type_counts.get(node_type, 0) + 1
            
            neighbor_summary['by_type'] = type_counts
            
            result['neighbors'] = {
                'summary': neighbor_summary,
                'nodes': self.format_node_list(neighbors, simplified=True)
            }
        
        return result
    
    def format_error(self, error_message: str) -> Dict[str, Any]:
        """
        格式化错误信息
        
        Args:
            error_message: 错误消息
            
        Returns:
            Dict: 格式化后的错误信息
        """
        return {
            'error': error_message
        }
    
    def check_depth_limit(self, depth: int) -> bool:
        """
        检查深度是否超过限制
        
        Args:
            depth: 深度值
            
        Returns:
            bool: 是否在限制内
        """
        max_depth = self.mcp_config.get('mcp', {}).get('max_path_depth', 10)
        return depth <= max_depth
    
    def get_max_depth(self) -> int:
        """
        获取最大深度限制
        
        Returns:
            int: 最大深度
        """
        return self.mcp_config.get('mcp', {}).get('max_path_depth', 10)
    
    def format_empty_result(self, query_type: str, query_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        格式化空结果，返回原因和建议操作
        
        Args:
            query_type: 查询类型（search, path, lineage等）
            query_params: 查询参数
            
        Returns:
            Dict: 包含空结果提示的响应
        """
        suggestions = {
            'search': '尝试使用更宽泛的关键词，或检查节点类型过滤条件',
            'path': '检查起始和目标节点ID是否正确，或尝试增加最大深度',
            'lineage': '检查实体名称是否正确，或尝试不指定实体类型',
            'neighbors': '该节点可能没有邻居节点，或尝试增加深度参数',
            'subgraph': '该节点可能是孤立节点，或尝试增加深度参数'
        }
        
        next_actions = {
            'search': '使用get_graph_overview工具查看可用的节点类型和数量',
            'path': '使用search_metadata工具查找有效的节点ID',
            'lineage': '使用search_metadata工具查找实体',
            'neighbors': '使用get_node_details工具查看节点详情',
            'subgraph': '使用get_node_neighbors工具查看直接邻居'
        }
        
        return {
            'results': [],
            'total': 0,
            'message': f'未找到匹配的结果',
            'reason': suggestions.get(query_type, '未找到匹配的结果'),
            'suggested_action': next_actions.get(query_type, '尝试调整查询参数')
        }
    
    def generate_result_summary(self, results: List[Dict[str, Any]], 
                               result_type: str) -> Dict[str, Any]:
        """
        为复杂结果生成摘要信息
        
        Args:
            results: 结果列表
            result_type: 结果类型（nodes, paths, lineage等）
            
        Returns:
            Dict: 包含摘要和后续操作建议的信息
        """
        summary = {
            'total_count': len(results),
            'result_type': result_type
        }
        
        # 根据结果类型生成特定摘要
        if result_type == 'nodes':
            # 统计节点类型分布
            type_counts = {}
            for result in results:
                node_type = result.get('type')
                type_counts[node_type] = type_counts.get(node_type, 0) + 1
            
            summary['type_distribution'] = type_counts
            summary['summary_text'] = f"找到{len(results)}个节点，包含{len(type_counts)}种类型"
            summary['next_action'] = "使用get_node_details工具查看具体节点的详细信息"
        
        elif result_type == 'paths':
            # 统计路径长度分布
            if results:
                lengths = [r.get('length', 0) for r in results]
                summary['min_length'] = min(lengths)
                summary['max_length'] = max(lengths)
                summary['avg_length'] = sum(lengths) / len(lengths)
            
            summary['summary_text'] = f"找到{len(results)}条路径"
            summary['next_action'] = "分析路径中的节点和关系，了解数据流向"
        
        elif result_type == 'lineage':
            summary['summary_text'] = f"找到{len(results)}条血缘路径"
            summary['next_action'] = "分析血缘路径，了解数据的业务归属或技术实现"
        
        return summary
