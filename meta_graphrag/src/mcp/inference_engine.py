"""MCP推理引擎 - 发现元数据之间的潜在关联"""
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logger
from mcp.models import InferenceResult


class InferenceEngine:
    """推理引擎 - 发现潜在的业务关联"""
    
    def __init__(self, query_executor, similarity_threshold: float = 0.7, verbose: bool = False):
        """
        初始化推理引擎
        
        Args:
            query_executor: 查询执行器实例
            similarity_threshold: 相似度阈值（0.0-1.0）
            verbose: 是否输出详细日志
        """
        self.logger = setup_logger('inference_engine', verbose=verbose)
        self.query_executor = query_executor
        self.similarity_threshold = similarity_threshold
        self.logger.info(f"推理引擎初始化完成，相似度阈值: {similarity_threshold}")
    
    def infer_related_fields(self, field_id: int = None, field_name: str = None,
                            business_term: str = None, threshold: float = None) -> List[InferenceResult]:
        """
        基于业务术语相似性推理字段之间的潜在关联
        
        推理策略：
        1. 精确匹配：相同business_term的字段
        2. 模糊匹配：business_term包含相同关键词
        3. 语义相似：基于字段名称和注释的相似度
        
        Args:
            field_id: 字段ID（可选）
            field_name: 字段名称（可选）
            business_term: 业务术语（可选）
            threshold: 相似度阈值（可选，默认使用初始化时的阈值）
            
        Returns:
            List[InferenceResult]: 推理结果列表
        """
        threshold = threshold or self.similarity_threshold
        results = []
        
        self.logger.debug(f"开始字段关联推理: field_id={field_id}, field_name={field_name}, "
                         f"business_term={business_term}, threshold={threshold}")
        
        # 如果提供了field_id，先获取字段信息
        if field_id:
            field_data = self.query_executor.get_node_by_id(field_id)
            if not field_data:
                self.logger.warning(f"字段ID {field_id} 不存在")
                return results
            
            properties = field_data.get('properties', {})
            field_name = properties.get('name')
            business_term = properties.get('business_term')
        
        # 策略1: 精确匹配business_term
        if business_term:
            exact_matches = self._find_exact_term_matches(field_id, business_term)
            for match in exact_matches:
                results.append(InferenceResult(
                    source_id=field_id or 0,
                    target_id=match['id'],
                    inference_type='EXACT_TERM_MATCH',
                    confidence=1.0,
                    evidence=f"相同业务术语: {match['business_term']}"
                ))
            
            self.logger.debug(f"精确匹配找到 {len(exact_matches)} 个相关字段")
        
        # 策略2: 字段名称相似性
        if field_name:
            name_matches = self._find_name_similarity_matches(field_id, field_name, threshold)
            for match in name_matches:
                # 避免重复添加已经通过精确匹配找到的字段
                if not any(r.target_id == match['id'] for r in results):
                    results.append(InferenceResult(
                        source_id=field_id or 0,
                        target_id=match['id'],
                        inference_type='NAME_SIMILARITY',
                        confidence=match['similarity'],
                        evidence=f"字段名称相似: {match['name']} (相似度: {match['similarity']:.2f})"
                    ))
            
            self.logger.debug(f"名称相似性匹配找到 {len(name_matches)} 个相关字段")
        
        self.logger.info(f"字段关联推理完成，共找到 {len(results)} 个潜在关联")
        return results
    
    def infer_table_relationships(self, table_id: int = None, table_name: str = None,
                                  threshold: float = None) -> List[InferenceResult]:
        """
        基于字段匹配推理表之间的潜在外键关系
        
        推理策略：
        1. 主键-外键模式：字段名以_id结尾且与其他表主键匹配
        2. 命名约定：字段名包含其他表名
        3. 数据类型匹配：相同类型和长度的字段
        
        Args:
            table_id: 表ID（可选）
            table_name: 表名称（可选）
            threshold: 相似度阈值（可选，默认使用初始化时的阈值）
            
        Returns:
            List[InferenceResult]: 推理结果列表
        """
        threshold = threshold or self.similarity_threshold
        results = []
        
        self.logger.debug(f"开始表关系推理: table_id={table_id}, table_name={table_name}, "
                         f"threshold={threshold}")
        
        # 如果提供了table_id，先获取表信息
        if table_id:
            table_data = self.query_executor.get_node_by_id(table_id)
            if not table_data:
                self.logger.warning(f"表ID {table_id} 不存在")
                return results
            
            properties = table_data.get('properties', {})
            table_name = properties.get('table_name') or properties.get('name')
        
        if not table_name:
            self.logger.warning("未提供表名称")
            return results
        
        # 策略1: 检测潜在外键
        fk_candidates = self._find_potential_foreign_keys(table_id, table_name)
        for candidate in fk_candidates:
            results.append(InferenceResult(
                source_id=table_id or 0,
                target_id=candidate['target_table_id'],
                inference_type='POTENTIAL_FOREIGN_KEY',
                confidence=candidate['confidence'],
                evidence=f"字段 {candidate['source_field']} 可能引用 {candidate['target_table']}.{candidate['target_field']}"
            ))
        
        self.logger.debug(f"外键推理找到 {len(fk_candidates)} 个潜在关系")
        
        # 策略2: 检测相似结构的表
        similar_tables = self._find_similar_structure_tables(table_id, table_name, threshold)
        for table in similar_tables:
            # 避免重复添加
            if not any(r.target_id == table['id'] for r in results):
                results.append(InferenceResult(
                    source_id=table_id or 0,
                    target_id=table['id'],
                    inference_type='SIMILAR_STRUCTURE',
                    confidence=table['similarity'],
                    evidence=f"表结构相似度: {table['similarity']:.2f}, 共同字段: {', '.join(table['common_fields'][:5])}"
                ))
        
        self.logger.debug(f"结构相似性推理找到 {len(similar_tables)} 个相关表")
        
        self.logger.info(f"表关系推理完成，共找到 {len(results)} 个潜在关联")
        return results
    
    def _find_exact_term_matches(self, field_id: int, business_term: str) -> List[Dict[str, Any]]:
        """
        查找具有相同业务术语的字段
        
        Args:
            field_id: 字段ID
            business_term: 业务术语
            
        Returns:
            List[Dict]: 匹配的字段列表
        """
        if field_id:
            query = """
            MATCH (t1:PhysicalTable)-[:HAS_FIELD]->(f1:Field)
            WHERE id(f1) = $field_id
            MATCH (t2:PhysicalTable)-[:HAS_FIELD]->(f2:Field)
            WHERE f1.business_term = f2.business_term 
              AND id(f1) <> id(f2)
              AND id(t1) <> id(t2)
            RETURN id(f2) as id, f2.name as name, f2.business_term as business_term,
                   t2.table_name as table_name
            LIMIT 50
            """
            params = {'field_id': field_id}
        else:
            query = """
            MATCH (t:PhysicalTable)-[:HAS_FIELD]->(f:Field)
            WHERE f.business_term = $business_term
            RETURN id(f) as id, f.name as name, f.business_term as business_term,
                   t.table_name as table_name
            LIMIT 50
            """
            params = {'business_term': business_term}
        
        return self.query_executor.execute_query(query, params)
    
    def _find_name_similarity_matches(self, field_id: int, field_name: str, 
                                     threshold: float) -> List[Dict[str, Any]]:
        """
        查找名称相似的字段
        
        Args:
            field_id: 字段ID
            field_name: 字段名称
            threshold: 相似度阈值
            
        Returns:
            List[Dict]: 相似字段列表
        """
        # 简单的名称相似性：检查字段名是否包含相同的关键词
        # 这里使用基于子串匹配的简单相似度计算
        
        if field_id:
            query = """
            MATCH (t1:PhysicalTable)-[:HAS_FIELD]->(f1:Field)
            WHERE id(f1) = $field_id
            MATCH (t2:PhysicalTable)-[:HAS_FIELD]->(f2:Field)
            WHERE id(f1) <> id(f2)
              AND id(t1) <> id(t2)
              AND (
                toLower(f2.name) CONTAINS toLower($field_name)
                OR toLower($field_name) CONTAINS toLower(f2.name)
              )
            RETURN id(f2) as id, f2.name as name, t2.table_name as table_name
            LIMIT 50
            """
            params = {'field_id': field_id, 'field_name': field_name}
        else:
            query = """
            MATCH (t:PhysicalTable)-[:HAS_FIELD]->(f:Field)
            WHERE toLower(f.name) CONTAINS toLower($field_name)
              OR toLower($field_name) CONTAINS toLower(f.name)
            RETURN id(f) as id, f.name as name, t.table_name as table_name
            LIMIT 50
            """
            params = {'field_name': field_name}
        
        results = self.query_executor.execute_query(query, params)
        
        # 计算相似度并过滤
        filtered_results = []
        for result in results:
            similarity = self._calculate_name_similarity(field_name, result['name'])
            if similarity >= threshold:
                result['similarity'] = similarity
                filtered_results.append(result)
        
        # 按相似度排序
        filtered_results.sort(key=lambda x: x['similarity'], reverse=True)
        
        return filtered_results
    
    def _calculate_name_similarity(self, name1: str, name2: str) -> float:
        """
        计算两个字段名的相似度
        
        使用简单的Jaccard相似度：基于字符集合的交集和并集
        
        Args:
            name1: 字段名1
            name2: 字段名2
            
        Returns:
            float: 相似度（0.0-1.0）
        """
        # 转换为小写
        name1 = name1.lower()
        name2 = name2.lower()
        
        # 如果完全相同，返回1.0
        if name1 == name2:
            return 1.0
        
        # 计算字符集合的Jaccard相似度
        set1 = set(name1)
        set2 = set(name2)
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        if union == 0:
            return 0.0
        
        jaccard = intersection / union
        
        # 如果一个名称包含另一个，增加相似度
        if name1 in name2 or name2 in name1:
            jaccard = min(1.0, jaccard + 0.3)
        
        return jaccard
    
    def _find_potential_foreign_keys(self, table_id: int, table_name: str) -> List[Dict[str, Any]]:
        """
        查找潜在的外键关系
        
        Args:
            table_id: 表ID
            table_name: 表名称
            
        Returns:
            List[Dict]: 潜在外键关系列表
        """
        if table_id:
            query = """
            MATCH (t1:PhysicalTable)-[:HAS_FIELD]->(f1:Field)
            WHERE id(t1) = $table_id
              AND (f1.name ENDS WITH '_id' OR f1.name ENDS WITH 'Id' OR f1.name ENDS WITH '_ID')
            MATCH (t2:PhysicalTable)-[:HAS_FIELD]->(f2:Field)
            WHERE id(t2) <> id(t1)
              AND (f2.name = 'id' OR f2.name = 'ID' OR f2.name = f1.name)
              AND f1.data_type = f2.data_type
            RETURN id(t2) as target_table_id, t2.table_name as target_table,
                   f1.name as source_field, f2.name as target_field,
                   0.8 as confidence
            LIMIT 50
            """
            params = {'table_id': table_id}
        else:
            query = """
            MATCH (t1:PhysicalTable {table_name: $table_name})-[:HAS_FIELD]->(f1:Field)
            WHERE (f1.name ENDS WITH '_id' OR f1.name ENDS WITH 'Id' OR f1.name ENDS WITH '_ID')
            MATCH (t2:PhysicalTable)-[:HAS_FIELD]->(f2:Field)
            WHERE t1.table_name <> t2.table_name
              AND (f2.name = 'id' OR f2.name = 'ID' OR f2.name = f1.name)
              AND f1.data_type = f2.data_type
            RETURN id(t2) as target_table_id, t2.table_name as target_table,
                   f1.name as source_field, f2.name as target_field,
                   0.8 as confidence
            LIMIT 50
            """
            params = {'table_name': table_name}
        
        return self.query_executor.execute_query(query, params)
    
    def _find_similar_structure_tables(self, table_id: int, table_name: str, 
                                      threshold: float) -> List[Dict[str, Any]]:
        """
        查找结构相似的表
        
        Args:
            table_id: 表ID
            table_name: 表名称
            threshold: 相似度阈值
            
        Returns:
            List[Dict]: 相似表列表
        """
        # 获取源表的所有字段
        if table_id:
            source_fields_query = """
            MATCH (t:PhysicalTable)-[:HAS_FIELD]->(f:Field)
            WHERE id(t) = $table_id
            RETURN collect(f.name) as field_names
            """
            params = {'table_id': table_id}
        else:
            source_fields_query = """
            MATCH (t:PhysicalTable {table_name: $table_name})-[:HAS_FIELD]->(f:Field)
            RETURN collect(f.name) as field_names
            """
            params = {'table_name': table_name}
        
        source_result = self.query_executor.execute_single_query(source_fields_query, params)
        if not source_result:
            return []
        
        source_fields = set(source_result['field_names'])
        
        # 获取其他表及其字段
        if table_id:
            other_tables_query = """
            MATCH (t:PhysicalTable)-[:HAS_FIELD]->(f:Field)
            WHERE id(t) <> $table_id
            WITH t, collect(f.name) as field_names
            RETURN id(t) as id, t.table_name as table_name, field_names
            """
            params = {'table_id': table_id}
        else:
            other_tables_query = """
            MATCH (t:PhysicalTable)-[:HAS_FIELD]->(f:Field)
            WHERE t.table_name <> $table_name
            WITH t, collect(f.name) as field_names
            RETURN id(t) as id, t.table_name as table_name, field_names
            """
            params = {'table_name': table_name}
        
        other_tables = self.query_executor.execute_query(other_tables_query, params)
        
        # 计算相似度
        similar_tables = []
        for table in other_tables:
            target_fields = set(table['field_names'])
            
            # 计算Jaccard相似度
            intersection = source_fields & target_fields
            union = source_fields | target_fields
            
            if union:
                similarity = len(intersection) / len(union)
                
                if similarity >= threshold:
                    similar_tables.append({
                        'id': table['id'],
                        'table_name': table['table_name'],
                        'similarity': similarity,
                        'common_fields': list(intersection)
                    })
        
        # 按相似度排序
        similar_tables.sort(key=lambda x: x['similarity'], reverse=True)
        
        return similar_tables[:20]  # 限制返回数量
