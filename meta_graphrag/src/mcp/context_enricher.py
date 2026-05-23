"""MCP上下文增强器"""
import sys
from typing import Dict, Any, Optional
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logger


class ContextEnricher:
    """上下文增强器 - 为节点添加业务上下文信息"""
    
    def __init__(self, query_executor, verbose: bool = False):
        """
        初始化上下文增强器
        
        Args:
            query_executor: 查询执行器实例
            verbose: 是否输出详细日志
        """
        self.logger = setup_logger('context_enricher', verbose=verbose)
        self.query_executor = query_executor
    
    def enrich_field_result(self, field_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        为Field节点添加所属表信息
        
        Args:
            field_data: 字段数据
            
        Returns:
            Dict: 增强后的字段数据
        """
        field_id = field_data.get('id')
        if field_id is None:
            return field_data
        
        # 查询字段所属的物理表
        query = """
        MATCH (pt:PhysicalTable)-[:HAS_FIELD]->(f:Field)
        WHERE id(f) = $field_id
        RETURN pt.table_name as table_name
        """
        
        try:
            result = self.query_executor.execute_single_query(query, {'field_id': field_id})
            if result and 'table_name' in result:
                # 将table_name添加到properties中
                if 'properties' in field_data:
                    field_data['properties']['table_name'] = result['table_name']
                else:
                    field_data['table_name'] = result['table_name']
            
            return field_data
        
        except Exception as e:
            self.logger.error(f"为字段添加表信息失败: {e}")
            return field_data
    
    def enrich_node_details(self, node_data: Dict[str, Any], node_type: str) -> Dict[str, Any]:
        """
        为节点详情添加业务层级位置
        
        Args:
            node_data: 节点数据
            node_type: 节点类型
            
        Returns:
            Dict: 增强后的节点数据
        """
        node_id = node_data.get('id')
        if node_id is None:
            return node_data
        
        business_context = None
        
        # 根据节点类型获取业务上下文
        if node_type == 'Field':
            business_context = self._get_field_context(node_id)
        elif node_type == 'PhysicalTable':
            business_context = self._get_table_context(node_id)
        elif node_type == 'LogicalEntity':
            business_context = self._get_logical_entity_context(node_id)
        
        # 添加业务上下文到节点数据
        if business_context:
            node_data['business_context'] = business_context
        
        return node_data
    
    def _get_field_context(self, field_id: int) -> Optional[Dict[str, Any]]:
        """
        获取字段的业务上下文
        
        Args:
            field_id: 字段ID
            
        Returns:
            Optional[Dict]: 业务上下文信息
        """
        query = """
        MATCH (db:Database)-[:CONTAINS]->(pt:PhysicalTable)-[:HAS_FIELD]->(f:Field)
        WHERE id(f) = $field_id
        OPTIONAL MATCH (le:LogicalEntity)-[:MAPS_TO]->(pt)
        OPTIONAL MATCH (sd:SubjectDomain)-[:CONTAINS*]->(le)
        RETURN 
            db.name as database_name,
            pt.table_name as table_name,
            le.logical_name as logical_entity_name,
            sd.name as subject_domain_name,
            f.business_term as business_term,
            f.data_source_unit as data_source_unit,
            f.data_standard as data_standard
        """
        
        try:
            result = self.query_executor.execute_single_query(query, {'field_id': field_id})
            if result:
                context = {
                    'technical_path': {
                        'database': result.get('database_name'),
                        'table': result.get('table_name')
                    }
                }
                
                # 添加业务路径（如果存在）
                if result.get('subject_domain_name') or result.get('logical_entity_name'):
                    context['business_path'] = {
                        'subject_domain': result.get('subject_domain_name'),
                        'logical_entity': result.get('logical_entity_name')
                    }
                
                # 添加业务属性（如果存在）
                business_attrs = {}
                if result.get('business_term'):
                    business_attrs['business_term'] = result.get('business_term')
                if result.get('data_source_unit'):
                    business_attrs['data_source_unit'] = result.get('data_source_unit')
                if result.get('data_standard'):
                    business_attrs['data_standard'] = result.get('data_standard')
                
                if business_attrs:
                    context['business_attributes'] = business_attrs
                
                return context
        
        except Exception as e:
            self.logger.error(f"获取字段业务上下文失败: {e}")
            return None
    
    def _get_table_context(self, table_id: int) -> Optional[Dict[str, Any]]:
        """
        获取物理表的业务上下文
        
        Args:
            table_id: 表ID
            
        Returns:
            Optional[Dict]: 业务上下文信息
        """
        query = """
        MATCH (db:Database)-[:CONTAINS]->(pt:PhysicalTable)
        WHERE id(pt) = $table_id
        OPTIONAL MATCH (le:LogicalEntity)-[:MAPS_TO]->(pt)
        OPTIONAL MATCH (sd:SubjectDomain)-[:CONTAINS*]->(le)
        RETURN 
            db.name as database_name,
            le.logical_name as logical_entity_name,
            sd.name as subject_domain_name
        """
        
        try:
            result = self.query_executor.execute_single_query(query, {'table_id': table_id})
            if result:
                context = {
                    'technical_path': {
                        'database': result.get('database_name')
                    }
                }
                
                # 添加业务路径（如果存在）
                if result.get('subject_domain_name') or result.get('logical_entity_name'):
                    context['business_path'] = {
                        'subject_domain': result.get('subject_domain_name'),
                        'logical_entity': result.get('logical_entity_name')
                    }
                
                return context
        
        except Exception as e:
            self.logger.error(f"获取表业务上下文失败: {e}")
            return None
    
    def _get_logical_entity_context(self, entity_id: int) -> Optional[Dict[str, Any]]:
        """
        获取逻辑实体的业务上下文
        
        Args:
            entity_id: 实体ID
            
        Returns:
            Optional[Dict]: 业务上下文信息
        """
        query = """
        MATCH (sd:SubjectDomain)-[:CONTAINS*]->(le:LogicalEntity)
        WHERE id(le) = $entity_id
        RETURN sd.name as subject_domain_name
        """
        
        try:
            result = self.query_executor.execute_single_query(query, {'entity_id': entity_id})
            if result:
                return {
                    'business_path': {
                        'subject_domain': result.get('subject_domain_name')
                    }
                }
        
        except Exception as e:
            self.logger.error(f"获取逻辑实体业务上下文失败: {e}")
            return None
