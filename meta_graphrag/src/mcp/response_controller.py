"""MCP响应大小控制器"""
import json
import sys
from typing import Dict, Any
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logger


class ResponseSizeController:
    """响应大小控制器 - 控制响应大小"""
    
    def __init__(self, max_size: int = 50000, verbose: bool = False):
        """
        初始化响应大小控制器
        
        Args:
            max_size: 最大响应大小（字符数）
            verbose: 是否输出详细日志
        """
        self.logger = setup_logger('response_controller', verbose=verbose)
        self.max_size = max_size
    
    def control_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        控制响应大小，超出限制时截断并添加提示
        
        Args:
            data: 响应数据
            
        Returns:
            Dict: 控制后的响应数据
        """
        try:
            # 序列化为JSON字符串以检查大小
            json_str = json.dumps(data, ensure_ascii=False)
            
            if len(json_str) <= self.max_size:
                # 未超出限制，直接返回
                return data
            
            # 超出限制，需要截断
            self.logger.warning(f"响应大小 {len(json_str)} 超出限制 {self.max_size}，进行截断")
            return self._truncate_with_hint(data, len(json_str))
        
        except Exception as e:
            self.logger.error(f"控制响应大小失败: {e}")
            return data
    
    def _truncate_with_hint(self, data: Dict[str, Any], original_size: int) -> Dict[str, Any]:
        """
        截断数据并添加提示信息
        
        Args:
            data: 原始数据
            original_size: 原始大小
            
        Returns:
            Dict: 截断后的数据
        """
        truncated_data = {}
        
        # 保留元数据和摘要信息
        for key in ['total', 'offset', 'limit', 'has_more', 'pagination', 
                   'summary', 'next_action', 'message', 'node_count', 'edge_count']:
            if key in data:
                truncated_data[key] = data[key]
        
        # 截断结果列表
        if 'items' in data:
            # 计算可以保留多少项
            items = data['items']
            truncated_items = []
            current_size = len(json.dumps(truncated_data, ensure_ascii=False))
            
            for item in items:
                item_size = len(json.dumps(item, ensure_ascii=False))
                if current_size + item_size < self.max_size * 0.9:  # 保留10%空间给提示信息
                    truncated_items.append(item)
                    current_size += item_size
                else:
                    break
            
            truncated_data['items'] = truncated_items
        
        elif 'results' in data:
            # 处理results字段
            results = data['results']
            truncated_results = []
            current_size = len(json.dumps(truncated_data, ensure_ascii=False))
            
            for result in results:
                result_size = len(json.dumps(result, ensure_ascii=False))
                if current_size + result_size < self.max_size * 0.9:
                    truncated_results.append(result)
                    current_size += result_size
                else:
                    break
            
            truncated_data['results'] = truncated_results
        
        elif 'paths' in data:
            # 处理paths字段
            paths = data['paths']
            truncated_paths = []
            current_size = len(json.dumps(truncated_data, ensure_ascii=False))
            
            for path in paths:
                path_size = len(json.dumps(path, ensure_ascii=False))
                if current_size + path_size < self.max_size * 0.9:
                    truncated_paths.append(path)
                    current_size += path_size
                else:
                    break
            
            truncated_data['paths'] = truncated_paths
        
        elif 'nodes' in data:
            # 处理子图数据
            nodes = data['nodes']
            edges = data.get('edges', [])
            
            truncated_nodes = []
            current_size = len(json.dumps(truncated_data, ensure_ascii=False))
            
            for node in nodes:
                node_size = len(json.dumps(node, ensure_ascii=False))
                if current_size + node_size < self.max_size * 0.8:  # 为edges保留空间
                    truncated_nodes.append(node)
                    current_size += node_size
                else:
                    break
            
            truncated_data['nodes'] = truncated_nodes
            
            # 只保留涉及截断后节点的边
            truncated_node_ids = {node['id'] for node in truncated_nodes}
            truncated_edges = [
                edge for edge in edges 
                if edge['source'] in truncated_node_ids and edge['target'] in truncated_node_ids
            ]
            truncated_data['edges'] = truncated_edges
        
        # 添加截断提示
        truncated_data['truncated'] = True
        truncated_data['truncation_info'] = {
            'original_size': original_size,
            'max_size': self.max_size,
            'message': '响应数据过大，已截断部分结果',
            'suggestion': '使用分页参数（offset和limit）获取更多数据，或使用更精确的查询条件'
        }
        
        return truncated_data
