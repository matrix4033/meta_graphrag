"""关系构建器 - 负责创建知识图谱中的各类关系"""
from typing import Optional


class RelationshipBuilder:
    """关系构建器"""
    
    def __init__(self, session):
        """
        初始化关系构建器
        
        Args:
            session: Neo4j会话对象
        """
        self.session = session
    
    def create_contains_by_names(self, database_name: str, table_name: str) -> None:
        """
        创建CONTAINS关系（Database 包含 PhysicalTable），基于属性匹配，避免使用id()
        
        Args:
            database_name: 数据库名称（Database.name）
            table_name: 物理表名称（PhysicalTable.table_name）
        """
        query = """
        MATCH (db:Database {name: $database_name})
        MATCH (pt:PhysicalTable {table_name: $table_name})
        MERGE (db)-[:CONTAINS]->(pt)
        """
        self.session.run(query, database_name=database_name, table_name=table_name)
    
    def create_implements_by_names(self, database_name: str, subject_domain_name: str) -> None:
        """
        创建IMPLEMENTS关系（Database 实现 SubjectDomain），基于属性匹配
        
        Args:
            database_name: Database.name
            subject_domain_name: SubjectDomain.name
        """
        query = """
        MATCH (db:Database {name: $database_name})
        MATCH (sd:SubjectDomain {name: $subject_domain_name})
        MERGE (db)-[:IMPLEMENTS]->(sd)
        """
        self.session.run(query, database_name=database_name, subject_domain_name=subject_domain_name)
    
    def create_maps_to_by_names(self, logical_name: str, table_name: str) -> None:
        """
        创建MAPS_TO关系（LogicalEntity 映射到 PhysicalTable），基于属性匹配
        
        Args:
            logical_name: LogicalEntity.logical_name
            table_name: PhysicalTable.table_name
        """
        query = """
        MATCH (le:LogicalEntity {logical_name: $logical_name})
        MATCH (pt:PhysicalTable {table_name: $table_name})
        MERGE (le)-[:MAPS_TO]->(pt)
        """
        self.session.run(query, logical_name=logical_name, table_name=table_name)
    
    def create_references(self, source_id: int, target_id: int,
                         constraint_name: str,
                         source_columns: str,
                         target_columns: str) -> None:
        """
        创建REFERENCES关系（外键引用）
        
        Args:
            source_id: 源表ID
            target_id: 目标表ID
            constraint_name: 约束名称
            source_columns: 源列名（逗号分隔）
            target_columns: 目标列名（逗号分隔）
        """
        query = """
        MATCH (source:PhysicalTable) WHERE id(source) = $source_id
        MATCH (target:PhysicalTable) WHERE id(target) = $target_id
        MERGE (source)-[r:REFERENCES]->(target)
        SET r.constraint_name = $constraint_name,
            r.source_columns = $source_columns,
            r.target_columns = $target_columns
        """
        self.session.run(
            query,
            source_id=source_id,
            target_id=target_id,
            constraint_name=constraint_name,
            source_columns=source_columns,
            target_columns=target_columns
        )
    
    def create_has_field_by_names(self, table_name: str, field_name: str) -> None:
        """
        创建HAS_FIELD关系（PhysicalTable 包含 Field），基于属性匹配
        
        Args:
            table_name: PhysicalTable.table_name
            field_name: Field.name
        """
        query = """
        MATCH (pt:PhysicalTable {table_name: $table_name})
        MATCH (f:Field {name: $field_name})
        MERGE (pt)-[:HAS_FIELD]->(f)
        """
        self.session.run(query, table_name=table_name, field_name=field_name)
    
    def create_represents_by_names(self, table_name: str, field_name: str,
                                   logical_name: str, data_element_name: str) -> None:
        """
        创建REPRESENTS关系（Field 表示 DataElement），基于属性匹配并带上下文，避免重复/误连。
        
        Args:
            table_name: PhysicalTable.table_name
            field_name: Field.name（该字段属表）
            logical_name: LogicalEntity.logical_name
            data_element_name: DataElement.name（该数据元属逻辑实体）
        """
        query = """
        MATCH (pt:PhysicalTable {table_name: $table_name})-[:HAS_FIELD]->(f:Field {name: $field_name})
        MATCH (le:LogicalEntity {logical_name: $logical_name})-[:HAS_DATA_ELEMENT]->(de:DataElement {name: $data_element_name})
        MERGE (f)-[:REPRESENTS]->(de)
        """
        self.session.run(
            query,
            table_name=table_name,
            field_name=field_name,
            logical_name=logical_name,
            data_element_name=data_element_name,
        )
