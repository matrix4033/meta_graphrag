"""节点构建器 - 负责创建知识图谱中的各类节点"""
from typing import Optional, Dict, Any
from datetime import datetime


class NodeBuilder:
    """节点构建器"""
    
    def __init__(self, session):
        """
        初始化节点构建器
        
        Args:
            session: Neo4j会话对象
        """
        self.session = session
    
    def create_subject_domain(self, name: str) -> int:
        """
        创建主题域节点（全局唯一）
        
        Args:
            name: 主题域名称
            
        Returns:
            节点ID
        """
        query = """
        MERGE (n:SubjectDomain {name: $name})
        ON CREATE SET n.created_at = datetime()
        RETURN id(n) as node_id
        """
        result = self.session.run(query, name=name)
        return result.single()['node_id']
    
    def create_database(self, name: str) -> int:
        """
        创建数据库节点（全局唯一）
        
        Args:
            name: 数据库名称
            
        Returns:
            节点ID
        """
        query = """
        MERGE (n:Database {name: $name})
        ON CREATE SET n.created_at = datetime()
        RETURN id(n) as node_id
        """
        result = self.session.run(query, name=name)
        return result.single()['node_id']
    
    def create_business_domain(self, name: str, parent_id: int) -> int:
        """
        创建业务域节点（结构唯一 - 同一主题域下唯一）
        
        Args:
            name: 业务域名称
            parent_id: 父节点（主题域）ID
            
        Returns:
            节点ID
        """
        query = """
        MATCH (parent:SubjectDomain) WHERE id(parent) = $parent_id
        MERGE (parent)-[:CONTAINS]->(node:BusinessDomain {name: $name})
        ON CREATE SET node.created_at = datetime()
        RETURN id(node) as node_id
        """
        result = self.session.run(query, name=name, parent_id=parent_id)
        return result.single()['node_id']
    
    def create_business_subject(self, name: str, parent_id: int) -> int:
        """
        创建业务主题节点（结构唯一 - 同一业务域下唯一）
        
        Args:
            name: 业务主题名称
            parent_id: 父节点（业务域）ID
            
        Returns:
            节点ID
        """
        query = """
        MATCH (parent:BusinessDomain) WHERE id(parent) = $parent_id
        MERGE (parent)-[:CONTAINS]->(node:BusinessSubject {name: $name})
        ON CREATE SET node.created_at = datetime()
        RETURN id(node) as node_id
        """
        result = self.session.run(query, name=name, parent_id=parent_id)
        return result.single()['node_id']
    
    def create_logical_entity(self, logical_name: str, code: str, parent_id: int) -> int:
        """
        创建逻辑实体节点（结构唯一 - 同一业务主题下唯一）
        
        Args:
            logical_name: 逻辑实体名称
            code: 编号
            parent_id: 父节点（业务主题）ID
            
        Returns:
            节点ID
        """
        query = """
        MATCH (parent:BusinessSubject) WHERE id(parent) = $parent_id
        MERGE (parent)-[:CONTAINS]->(node:LogicalEntity {logical_name: $logical_name})
        ON CREATE SET node.code = $code, node.created_at = datetime()
        RETURN id(node) as node_id
        """
        result = self.session.run(query, logical_name=logical_name, code=code, parent_id=parent_id)
        return result.single()['node_id']
    
    def create_physical_table(self, table_name: str, database_name: str, 
                             comment: Optional[str] = None,
                             ddl_statement: Optional[str] = None) -> int:
        """
        创建物理表节点（全局唯一）
        
        Args:
            table_name: 物理表名称
            database_name: 数据库名称
            comment: 表注释
            ddl_statement: 完整的DDL语句
            
        Returns:
            节点ID
        """
        query = """
        MERGE (n:PhysicalTable {table_name: $table_name})
        ON CREATE SET 
            n.name = $table_name,
            n.database_name = $database_name,
            n.comment = $comment,
            n.ddl_statement = $ddl_statement,
            n.created_at = datetime()
        ON MATCH SET
            n.name = $table_name,
            n.database_name = $database_name,
            n.comment = $comment,
            n.ddl_statement = $ddl_statement
        RETURN id(n) as node_id
        """
        result = self.session.run(
            query, 
            table_name=table_name, 
            database_name=database_name,
            comment=comment,
            ddl_statement=ddl_statement
        )
        return result.single()['node_id']
    
    def create_data_element(self, name: str, logical_entity_name: str,
                           business_description: Optional[str] = None,
                           data_source_unit: Optional[str] = None,
                           data_standard: Optional[str] = None,
                           data_format: Optional[str] = None,
                           value_domain: Optional[str] = None) -> Optional[str]:
        """
        创建数据元节点（结构唯一 - 同一逻辑实体下唯一）
        
        Args:
            name: 数据元名称
            logical_entity_id: 所属逻辑实体ID
            business_description: 业务说明
            data_source_unit: 数源单位
            data_standard: 数据标准
            data_format: 数据元格式
            value_domain: 值域
            
        Returns:
            节点标识（不返回内部ID，避免使用id()）
        """
        query = """
        MATCH (le:LogicalEntity {logical_name: $logical_entity_name})
        MERGE (le)-[:HAS_DATA_ELEMENT]->(de:DataElement {name: $name})
        ON CREATE SET 
            de.business_description = $business_description,
            de.data_source_unit = $data_source_unit,
            de.data_standard = $data_standard,
            de.data_format = $data_format,
            de.value_domain = $value_domain,
            de.created_at = datetime()
        ON MATCH SET
            de.business_description = COALESCE($business_description, de.business_description),
            de.data_source_unit = COALESCE($data_source_unit, de.data_source_unit),
            de.data_standard = COALESCE($data_standard, de.data_standard),
            de.data_format = COALESCE($data_format, de.data_format),
            de.value_domain = COALESCE($value_domain, de.value_domain)
        RETURN de.name as de_name
        """
        result = self.session.run(
            query,
            name=name,
            logical_entity_name=logical_entity_name,
            business_description=business_description,
            data_source_unit=data_source_unit,
            data_standard=data_standard,
            data_format=data_format,
            value_domain=value_domain
        )
        record = result.single()
        if record is None:
            return None
        return record['de_name']
    
    def create_field(self, name: str, data_type: str, length: Optional[int] = None,
                    nullable: bool = True, comment: Optional[str] = None,
                    parent_id: Optional[int] = None,
                    business_term: Optional[str] = None,
                    data_source_unit: Optional[str] = None,
                    data_standard: Optional[str] = None) -> int:
        """
        创建字段节点（结构唯一 - 同一物理表下唯一）
        
        Args:
            name: 字段名称
            data_type: 数据类型
            length: 字段长度
            nullable: 是否可空
            comment: 字段注释
            parent_id: 父节点（物理表）ID
            business_term: 业务术语
            data_source_unit: 数源单位
            data_standard: 数据标准
            
        Returns:
            节点ID
        """
        if parent_id is None:
            # 如果没有父节点，直接创建字段节点
            query = """
            CREATE (n:Field {
                name: $name,
                data_type: $data_type,
                length: $length,
                nullable: $nullable,
                comment: $comment,
                business_term: $business_term,
                data_source_unit: $data_source_unit,
                data_standard: $data_standard,
                created_at: datetime()
            })
            RETURN id(n) as node_id
            """
            result = self.session.run(
                query,
                name=name,
                data_type=data_type,
                length=length,
                nullable=nullable,
                comment=comment,
                business_term=business_term,
                data_source_unit=data_source_unit,
                data_standard=data_standard
            )
        else:
            # 如果有父节点，通过HAS_FIELD关系保证唯一性
            # 先查找是否存在
            check_query = """
            MATCH (parent:PhysicalTable) WHERE id(parent) = $parent_id
            OPTIONAL MATCH (parent)-[:HAS_FIELD]->(existing:Field {name: $name})
            RETURN id(existing) as existing_id
            """
            check_result = self.session.run(check_query, parent_id=parent_id, name=name)
            record = check_result.single()
            
            if record and record['existing_id'] is not None:
                # 节点已存在，更新业务语义属性
                update_query = """
                MATCH (field:Field) WHERE id(field) = $field_id
                SET field.business_term = COALESCE($business_term, field.business_term),
                    field.data_source_unit = COALESCE($data_source_unit, field.data_source_unit),
                    field.data_standard = COALESCE($data_standard, field.data_standard)
                RETURN id(field) as node_id
                """
                result = self.session.run(
                    update_query,
                    field_id=record['existing_id'],
                    business_term=business_term,
                    data_source_unit=data_source_unit,
                    data_standard=data_standard
                )
            else:
                # 节点不存在，创建新节点
                create_query = """
                MATCH (parent:PhysicalTable) WHERE id(parent) = $parent_id
                CREATE (parent)-[:HAS_FIELD]->(field:Field {
                    name: $name,
                    data_type: $data_type,
                    length: $length,
                    nullable: $nullable,
                    comment: $comment,
                    business_term: $business_term,
                    data_source_unit: $data_source_unit,
                    data_standard: $data_standard,
                    created_at: datetime()
                })
                RETURN id(field) as node_id
                """
                result = self.session.run(
                    create_query,
                    parent_id=parent_id,
                    name=name,
                    data_type=data_type,
                    length=length,
                    nullable=nullable,
                    comment=comment,
                    business_term=business_term,
                    data_source_unit=data_source_unit,
                    data_standard=data_standard
                )
        
        return result.single()['node_id']
