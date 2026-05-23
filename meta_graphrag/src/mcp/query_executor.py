"""MCP查询执行器"""
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logger
from graph.neo4j_connection import Neo4jConnection


def clean_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    清理记录中的无效UTF-8字符、代理字符和Neo4j特殊类型
    
    Args:
        record: 数据库记录
        
    Returns:
        清理后的记录
    """
    def clean_value(v: Any) -> Any:
        # 处理Neo4j DateTime类型
        if hasattr(v, 'iso_format'):
            return v.iso_format()
        # 处理Neo4j Date类型
        elif hasattr(v, '__class__') and v.__class__.__name__ in ['DateTime', 'Date', 'Time']:
            return str(v)
        # 处理字符串
        elif isinstance(v, str):
            try:
                # 先尝试编码，如果有代理字符会失败
                v.encode('utf-8')
                return v
            except UnicodeEncodeError:
                # 有无效字符，过滤掉代理字符（U+D800 到 U+DFFF）
                cleaned = ''.join(char for char in v if not (0xD800 <= ord(char) <= 0xDFFF))
                return cleaned
        elif isinstance(v, dict):
            return {clean_value(k): clean_value(val) for k, val in v.items()}
        elif isinstance(v, list):
            return [clean_value(item) for item in v]
        else:
            return v
    
    return clean_value(record)


class QueryExecutor:
    """查询执行器 - 执行Cypher查询"""
    
    def __init__(self, neo4j_conn: Neo4jConnection, verbose: bool = False):
        """
        初始化查询执行器
        
        Args:
            neo4j_conn: Neo4j连接实例
            verbose: 是否输出详细日志
        """
        self.logger = setup_logger('query_executor', verbose=verbose)
        self.neo4j_conn = neo4j_conn
    
    def execute_query(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        执行Cypher查询
        
        Args:
            query: Cypher查询语句
            parameters: 查询参数
            
        Returns:
            List: 查询结果列表
        """
        if parameters is None:
            parameters = {}
        
        try:
            self.logger.debug(f"执行查询: {query}")
            self.logger.debug(f"查询参数: {parameters}")
            
            with self.neo4j_conn.get_session() as session:
                result = session.run(query, parameters)
                records = [clean_record(dict(record)) for record in result]
                
                self.logger.debug(f"查询返回 {len(records)} 条记录")
                return records
        
        except Exception as e:
            self.logger.error(f"查询执行失败: {e}")
            self.logger.error(f"查询语句: {query}")
            self.logger.error(f"查询参数: {parameters}")
            raise
    
    def execute_single_query(self, query: str, parameters: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        执行Cypher查询并返回单条记录
        
        Args:
            query: Cypher查询语句
            parameters: 查询参数
            
        Returns:
            Optional[Dict]: 查询结果，如果没有结果则返回None
        """
        results = self.execute_query(query, parameters)
        return results[0] if results else None
    
    def get_node_by_id(self, node_id: int) -> Optional[Dict[str, Any]]:
        """
        通过ID获取节点
        
        Args:
            node_id: 节点ID
            
        Returns:
            Optional[Dict]: 节点数据
        """
        query = """
        MATCH (n)
        WHERE id(n) = $node_id
        RETURN id(n) as id, labels(n) as labels, properties(n) as properties
        """
        return self.execute_single_query(query, {'node_id': node_id})
    
    def get_node_by_name_and_type(self, node_name: str, node_type: str) -> Optional[Dict[str, Any]]:
        """
        通过名称和类型获取节点
        
        Args:
            node_name: 节点名称
            node_type: 节点类型
            
        Returns:
            Optional[Dict]: 节点数据
        """
        # 根据节点类型确定名称属性
        name_property = 'logical_name' if node_type == 'LogicalEntity' else 'name'
        if node_type == 'PhysicalTable':
            name_property = 'table_name'
        
        query = f"""
        MATCH (n:{node_type})
        WHERE n.{name_property} = $node_name
        RETURN id(n) as id, labels(n) as labels, properties(n) as properties
        """
        return self.execute_single_query(query, {'node_name': node_name})
    
    def get_graph_statistics(self) -> Dict[str, Any]:
        """
        获取图谱统计信息
        
        Returns:
            Dict: 统计信息
        """
        # 获取节点统计
        node_query = """
        MATCH (n)
        RETURN labels(n)[0] as label, count(*) as count
        ORDER BY label
        """
        node_results = self.execute_query(node_query)
        node_counts = {record['label']: record['count'] for record in node_results}
        
        # 获取关系统计
        rel_query = """
        MATCH ()-[r]->()
        RETURN type(r) as rel_type, count(*) as count
        ORDER BY rel_type
        """
        rel_results = self.execute_query(rel_query)
        rel_counts = {record['rel_type']: record['count'] for record in rel_results}
        
        # 计算总数
        total_nodes = sum(node_counts.values())
        total_relationships = sum(rel_counts.values())
        
        # 获取主题域分组统计
        subject_domain_stats = self.get_subject_domain_statistics()
        
        return {
            'node_counts': node_counts,
            'relationship_counts': rel_counts,
            'total_nodes': total_nodes,
            'total_relationships': total_relationships,
            'by_subject_domain': subject_domain_stats
        }
    
    def get_subject_domain_statistics(self) -> Dict[str, Any]:
        """
        获取按主题域分组的节点统计
        
        Returns:
            Dict: 主题域统计信息
        """
        # 获取所有主题域及其包含的节点数量
        query = """
        MATCH (sd:SubjectDomain)
        OPTIONAL MATCH (sd)-[:CONTAINS*]->(n)
        WHERE n:LogicalEntity OR n:PhysicalTable
        WITH sd, count(DISTINCT n) as node_count
        RETURN id(sd) as id, sd.name as name, node_count
        ORDER BY sd.name
        """
        
        results = self.execute_query(query)
        
        # 构建主题域统计
        domain_stats = {}
        subject_domains = []
        
        for record in results:
            domain_name = record['name']
            node_count = record['node_count']
            
            domain_stats[domain_name] = node_count
            subject_domains.append({
                'id': record['id'],
                'name': domain_name,
                'node_count': node_count
            })
        
        return {
            'domains': subject_domains,
            'domain_counts': domain_stats,
            'total_domains': len(subject_domains)
        }
    
    def search_nodes_by_keyword(self, keyword: str, node_types: List[str] = None,
                                offset: int = 0, limit: int = 20) -> List[Dict[str, Any]]:
        """
        通过关键词搜索节点
        
        Args:
            keyword: 搜索关键词
            node_types: 节点类型过滤器
            offset: 分页偏移量
            limit: 返回结果数量
            
        Returns:
            List: 搜索结果
        """
        # 构建节点类型过滤条件
        if node_types:
            label_filter = " OR ".join([f"n:{node_type}" for node_type in node_types])
            label_condition = f"({label_filter})"
        else:
            label_condition = "TRUE"
        
        query = f"""
        MATCH (n)
        WHERE {label_condition}
          AND (
            toLower(toString(n.name)) CONTAINS toLower($keyword)
            OR toLower(toString(n.logical_name)) CONTAINS toLower($keyword)
            OR toLower(toString(n.table_name)) CONTAINS toLower($keyword)
            OR toLower(toString(n.comment)) CONTAINS toLower($keyword)
            OR toLower(toString(n.business_term)) CONTAINS toLower($keyword)
          )
        RETURN id(n) as id, labels(n)[0] as type, properties(n) as properties
        ORDER BY type, id(n)
        SKIP $offset
        LIMIT $limit
        """
        
        return self.execute_query(query, {
            'keyword': keyword,
            'offset': offset,
            'limit': limit
        })
    
    def search_nodes_by_attribute(self, node_type: str, attribute_name: str, 
                                  attribute_value: str, offset: int = 0, 
                                  limit: int = 20) -> List[Dict[str, Any]]:
        """
        通过属性搜索节点
        
        Args:
            node_type: 节点类型
            attribute_name: 属性名
            attribute_value: 属性值
            offset: 分页偏移量
            limit: 返回结果数量
            
        Returns:
            List: 搜索结果
        """
        query = f"""
        MATCH (n:{node_type})
        WHERE n.{attribute_name} = $attribute_value
        RETURN id(n) as id, labels(n)[0] as type, properties(n) as properties
        ORDER BY id(n)
        SKIP $offset
        LIMIT $limit
        """
        
        return self.execute_query(query, {
            'attribute_value': attribute_value,
            'offset': offset,
            'limit': limit
        })
    
    def get_node_neighbors(self, node_id: int, depth: int = 1, 
                          relationship_types: List[str] = None) -> List[Dict[str, Any]]:
        """
        获取节点的邻居节点
        
        Args:
            node_id: 节点ID
            depth: 深度
            relationship_types: 关系类型过滤器
            
        Returns:
            List: 邻居节点列表
        """
        # 构建关系类型过滤条件
        if relationship_types:
            rel_filter = "|".join(relationship_types)
            rel_pattern = f"[r:{rel_filter}*1..{depth}]"
        else:
            rel_pattern = f"[r*1..{depth}]"
        
        query = f"""
        MATCH (start)-{rel_pattern}-(neighbor)
        WHERE id(start) = $node_id
        RETURN DISTINCT id(neighbor) as id, labels(neighbor)[0] as type, 
               properties(neighbor) as properties
        ORDER BY type, id
        """
        
        return self.execute_query(query, {'node_id': node_id})
    
    def find_shortest_path(self, start_node_id: int, end_node_id: int) -> Optional[Dict[str, Any]]:
        """
        查找最短路径
        
        Args:
            start_node_id: 起始节点ID
            end_node_id: 目标节点ID
            
        Returns:
            Optional[Dict]: 路径信息
        """
        query = """
        MATCH (start), (end)
        WHERE id(start) = $start_node_id AND id(end) = $end_node_id
        MATCH path = shortestPath((start)-[*]-(end))
        RETURN path, length(path) as path_length
        """
        
        result = self.execute_single_query(query, {
            'start_node_id': start_node_id,
            'end_node_id': end_node_id
        })
        
        return result
    
    def find_all_paths(self, start_node_id: int, end_node_id: int, 
                      max_depth: int = 5) -> List[Dict[str, Any]]:
        """
        查找所有路径
        
        Args:
            start_node_id: 起始节点ID
            end_node_id: 目标节点ID
            max_depth: 最大深度
            
        Returns:
            List: 路径列表
        """
        query = f"""
        MATCH (start), (end)
        WHERE id(start) = $start_node_id AND id(end) = $end_node_id
        MATCH path = (start)-[*1..{max_depth}]-(end)
        RETURN path, length(path) as path_length
        ORDER BY path_length
        """
        
        return self.execute_query(query, {
            'start_node_id': start_node_id,
            'end_node_id': end_node_id
        })
    
    def get_business_lineage(self, entity_name: str, entity_type: str = None) -> List[Dict[str, Any]]:
        """
        获取业务血缘路径
        
        Args:
            entity_name: 实体名称
            entity_type: 实体类型
            
        Returns:
            List: 业务血缘路径
        """
        # 如果没有指定类型，尝试两种类型
        if entity_type is None:
            # 先尝试LogicalEntity
            result = self.get_business_lineage(entity_name, 'LogicalEntity')
            if result:
                return result
            # 再尝试PhysicalTable
            return self.get_business_lineage(entity_name, 'PhysicalTable')
        
        if entity_type == 'LogicalEntity':
            query = """
            MATCH path = (sd:SubjectDomain)-[:CONTAINS*]->(le:LogicalEntity)
            WHERE le.logical_name = $entity_name
            RETURN path, length(path) as path_length
            """
        else:  # PhysicalTable
            query = """
            MATCH (pt:PhysicalTable {table_name: $entity_name})
            MATCH (le:LogicalEntity)-[:MAPS_TO]->(pt)
            MATCH path = (sd:SubjectDomain)-[:CONTAINS*]->(le)
            RETURN path, length(path) as path_length
            """
        
        return self.execute_query(query, {'entity_name': entity_name})
    
    def get_technical_lineage(self, entity_name: str, entity_type: str = None) -> List[Dict[str, Any]]:
        """
        获取技术血缘路径
        
        Args:
            entity_name: 实体名称
            entity_type: 实体类型
            
        Returns:
            List: 技术血缘路径
        """
        # 如果没有指定类型，尝试两种类型
        if entity_type is None:
            # 先尝试PhysicalTable
            result = self.get_technical_lineage(entity_name, 'PhysicalTable')
            if result:
                return result
            # 再尝试Field
            return self.get_technical_lineage(entity_name, 'Field')
        
        if entity_type == 'PhysicalTable':
            query = """
            MATCH path = (db:Database)-[:CONTAINS]->(pt:PhysicalTable)
            WHERE pt.table_name = $entity_name
            RETURN path, length(path) as path_length
            """
        else:  # Field
            query = """
            MATCH path = (db:Database)-[:CONTAINS]->(pt:PhysicalTable)-[:HAS_FIELD]->(f:Field)
            WHERE f.name = $entity_name
            RETURN path, length(path) as path_length
            """
        
        return self.execute_query(query, {'entity_name': entity_name})
    
    def discover_related_by_relationship(self, node_id: int, 
                                        relationship_type: str) -> List[Dict[str, Any]]:
        """
        通过关系类型发现相关节点
        
        Args:
            node_id: 节点ID
            relationship_type: 关系类型
            
        Returns:
            List: 相关节点列表
        """
        query = f"""
        MATCH (start)-[r:{relationship_type}]-(related)
        WHERE id(start) = $node_id
        RETURN id(related) as id, labels(related)[0] as type, 
               properties(related) as properties, type(r) as relationship
        ORDER BY type, id
        """
        
        return self.execute_query(query, {'node_id': node_id})
    
    def get_subgraph(self, node_id: int, depth: int = 2, 
                    node_types: List[str] = None) -> Dict[str, Any]:
        """
        获取子图
        
        Args:
            node_id: 中心节点ID
            depth: 深度
            node_types: 节点类型过滤器
            
        Returns:
            Dict: 子图数据
        """
        # 构建节点类型过滤条件
        if node_types:
            label_filter = " OR ".join([f"neighbor:{node_type}" for node_type in node_types])
            label_condition = f"AND ({label_filter})"
        else:
            label_condition = ""
        
        # 获取节点
        nodes_query = f"""
        MATCH (center)-[*0..{depth}]-(neighbor)
        WHERE id(center) = $node_id {label_condition}
        RETURN DISTINCT id(neighbor) as id, labels(neighbor)[0] as type, 
               properties(neighbor) as properties
        """
        nodes = self.execute_query(nodes_query, {'node_id': node_id})
        
        # 获取节点ID列表
        node_ids = [node['id'] for node in nodes]
        
        # 获取这些节点之间的关系
        edges_query = """
        MATCH (n1)-[r]->(n2)
        WHERE id(n1) IN $node_ids AND id(n2) IN $node_ids
        RETURN id(n1) as source, id(n2) as target, type(r) as relationship
        """
        edges = self.execute_query(edges_query, {'node_ids': node_ids})
        
        return {
            'nodes': nodes,
            'edges': edges
        }
