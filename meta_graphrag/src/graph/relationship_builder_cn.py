"""关系构建器（中文版）- 负责创建知识图谱中的各类关系"""
from typing import Optional


class RelationshipBuilderCN:
    """关系构建器（中文版）"""
    
    def __init__(self, session):
        """
        初始化关系构建器
        
        Args:
            session: Neo4j会话对象
        """
        self.session = session
    
    def create_contains(self, parent_id: int, child_id: int) -> None:
        """
        创建包含关系
        
        Args:
            parent_id: 父节点ID
            child_id: 子节点ID
        """
        query = """
        MATCH (parent) WHERE id(parent) = $parent_id
        MATCH (child) WHERE id(child) = $child_id
        MERGE (parent)-[:包含]->(child)
        """
        self.session.run(query, parent_id=parent_id, child_id=child_id)
    
    def create_implements(self, tech_id: int, business_id: int) -> None:
        """
        创建实现关系（技术实现业务）
        
        Args:
            tech_id: 技术实体ID（如数据库）
            business_id: 业务实体ID（如主题域）
        """
        query = """
        MATCH (tech) WHERE id(tech) = $tech_id
        MATCH (business) WHERE id(business) = $business_id
        MERGE (tech)-[:实现]->(business)
        """
        self.session.run(query, tech_id=tech_id, business_id=business_id)
    
    def create_maps_to(self, logical_id: int, physical_id: int) -> None:
        """
        创建映射到关系（逻辑实体映射到物理表）
        
        Args:
            logical_id: 逻辑实体ID
            physical_id: 物理表ID
        """
        query = """
        MATCH (logical:逻辑实体) WHERE id(logical) = $logical_id
        MATCH (physical:物理表) WHERE id(physical) = $physical_id
        MERGE (logical)-[:映射到]->(physical)
        """
        self.session.run(query, logical_id=logical_id, physical_id=physical_id)
    
    def create_references(self, source_id: int, target_id: int,
                         constraint_name: str,
                         source_columns: str,
                         target_columns: str) -> None:
        """
        创建引用关系（外键引用）
        
        Args:
            source_id: 源表ID
            target_id: 目标表ID
            constraint_name: 约束名称
            source_columns: 源列名（逗号分隔）
            target_columns: 目标列名（逗号分隔）
        """
        query = """
        MATCH (source:物理表) WHERE id(source) = $source_id
        MATCH (target:物理表) WHERE id(target) = $target_id
        MERGE (source)-[r:引用]->(target)
        SET r.约束名称 = $constraint_name,
            r.源列 = $source_columns,
            r.目标列 = $target_columns
        """
        self.session.run(
            query,
            source_id=source_id,
            target_id=target_id,
            constraint_name=constraint_name,
            source_columns=source_columns,
            target_columns=target_columns
        )
    
    def create_has_field(self, table_id: int, field_id: int) -> None:
        """
        创建拥有字段关系（物理表包含字段）
        
        Args:
            table_id: 物理表ID
            field_id: 字段ID
        """
        query = """
        MATCH (table:物理表) WHERE id(table) = $table_id
        MATCH (field:字段) WHERE id(field) = $field_id
        MERGE (table)-[:拥有字段]->(field)
        """
        self.session.run(query, table_id=table_id, field_id=field_id)
    
    def create_represents(self, field_id: int, data_element_id: int) -> None:
        """
        创建表示关系（字段表示数据元）
        
        Args:
            field_id: 字段ID
            data_element_id: 数据元ID
        """
        query = """
        MATCH (field:字段) WHERE id(field) = $field_id
        MATCH (de:数据元) WHERE id(de) = $data_element_id
        MERGE (field)-[:表示]->(de)
        """
        self.session.run(query, field_id=field_id, data_element_id=data_element_id)
