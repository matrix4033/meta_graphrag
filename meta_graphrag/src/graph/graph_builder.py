"""图谱构建器 - 协调整个知识图谱的构建流程"""
from typing import List, Dict, Any, Optional
from .node_builder import NodeBuilder
from .relationship_builder import RelationshipBuilder
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.logger import setup_logger


class GraphBuilder:
    """图谱构建器"""
    
    def __init__(self, connection, configs: Dict[str, Any]):
        """
        初始化图谱构建器
        
        Args:
            connection: Neo4j连接对象
            configs: 配置字典
        """
        self.connection = connection
        self.configs = configs
        self.logger = setup_logger('graph_builder')
        
        # 缓存节点ID，避免重复查询
        self.subject_domain_cache = {}  # name -> id
        self.database_cache = {}  # name -> id
        self.business_domain_cache = {}  # (parent_id, name) -> id
        self.business_subject_cache = {}  # (parent_id, name) -> id
        self.logical_entity_cache = {}  # (parent_id, logical_name) -> id
        self.physical_table_cache = {}  # table_name -> id
        self.data_element_cache = {}  # (logical_entity_name, data_element_name) -> marker
        # 反向索引：逻辑实体ID -> 逻辑名称
        self._logical_id_to_name = {}

    def _get_logical_name_by_id(self, le_id: int) -> str:
        """从缓存反查逻辑实体名称（用于避免使用id()进行图查询）"""
        return self._logical_id_to_name.get(le_id, "")
    
    def build_graph(self, ddl_data: List[Dict[str, Any]], 
                   excel_data: List[Dict[str, Any]]) -> None:
        """
        构建知识图谱
        
        执行顺序：
        1. 创建业务层节点
        2. 创建业务层关系
        3. 创建技术层节点
        4. 创建技术层关系
        5. 创建映射关系
        6. 补充业务语义
        
        Args:
            ddl_data: DDL解析数据列表
            excel_data: Excel解析数据列表
        """
        self.logger.info("开始构建知识图谱...")
        
        with self.connection.get_session() as session:
            node_builder = NodeBuilder(session)
            rel_builder = RelationshipBuilder(session)
            
            # 步骤 1: 构建业务层
            self.logger.info("步骤 1/6: 构建业务层...")
            self._build_business_layer(ddl_data, node_builder, rel_builder)
            
            # 步骤 2: 构建技术层
            self.logger.info("步骤 2/6: 构建技术层...")
            self._build_technical_layer(ddl_data, node_builder, rel_builder)
            
            # 步骤 3: 创建映射关系
            self.logger.info("步骤 3/6: 创建映射关系...")
            self._create_mapping_relationships(ddl_data, rel_builder)
            
            # 步骤 4: 创建数据元节点
            self.logger.info("步骤 4/6: 创建数据元节点...")
            self._create_data_elements(excel_data, node_builder)
            
            # 步骤 5: 关联字段和数据元
            self.logger.info("步骤 5/6: 关联字段和数据元...")
            self._link_fields_to_data_elements(rel_builder)
            
            # 步骤 6: 补充业务语义（保留用于向后兼容）
            self.logger.info("步骤 6/6: 补充业务语义...")
            self._enrich_business_semantics(excel_data, node_builder)
            
            self.logger.info("知识图谱构建完成")
    
    def _build_business_layer(self, ddl_data: List[Dict[str, Any]], 
                             node_builder: NodeBuilder,
                             rel_builder: RelationshipBuilder) -> None:
        """构建业务层节点和关系"""
        for item in ddl_data:
            # 创建主题域节点
            subject_domain = item.get('subject_domain')
            if subject_domain and subject_domain not in self.subject_domain_cache:
                sd_id = node_builder.create_subject_domain(subject_domain)
                self.subject_domain_cache[subject_domain] = sd_id
                self.logger.debug(f"创建主题域: {subject_domain} (ID: {sd_id})")
            
            # 创建数据库节点
            database = item.get('database')
            if database and database not in self.database_cache:
                db_id = node_builder.create_database(database)
                self.database_cache[database] = db_id
                self.logger.debug(f"创建数据库: {database} (ID: {db_id})")
                
                # 创建数据库→主题域IMPLEMENTS关系
                if subject_domain:
                    rel_builder.create_implements_by_names(database, subject_domain)
                    self.logger.debug(f"创建IMPLEMENTS关系: {database} -> {subject_domain}")
            
            # 创建业务域节点
            business_domain = item.get('business_domain')
            if business_domain and subject_domain:
                sd_id = self.subject_domain_cache[subject_domain]
                cache_key = (sd_id, business_domain)
                if cache_key not in self.business_domain_cache:
                    bd_id = node_builder.create_business_domain(business_domain, sd_id)
                    self.business_domain_cache[cache_key] = bd_id
                    self.logger.debug(f"创建业务域: {business_domain} (ID: {bd_id})")
            
            # 创建业务主题节点
            business_subject = item.get('business_subject')
            if business_subject and business_domain and subject_domain:
                sd_id = self.subject_domain_cache[subject_domain]
                bd_id = self.business_domain_cache[(sd_id, business_domain)]
                cache_key = (bd_id, business_subject)
                if cache_key not in self.business_subject_cache:
                    bs_id = node_builder.create_business_subject(business_subject, bd_id)
                    self.business_subject_cache[cache_key] = bs_id
                    self.logger.debug(f"创建业务主题: {business_subject} (ID: {bs_id})")
            
            # 创建逻辑实体节点
            logical_entity = item.get('logical_entity')
            code = item.get('code', '')
            if logical_entity and business_subject and business_domain and subject_domain:
                sd_id = self.subject_domain_cache[subject_domain]
                bd_id = self.business_domain_cache[(sd_id, business_domain)]
                bs_id = self.business_subject_cache[(bd_id, business_subject)]
                cache_key = (bs_id, logical_entity)
                if cache_key not in self.logical_entity_cache:
                    le_id = node_builder.create_logical_entity(logical_entity, code, bs_id)
                    self.logical_entity_cache[cache_key] = le_id
                    self._logical_id_to_name[le_id] = logical_entity
                    self.logger.debug(f"创建逻辑实体: {logical_entity} (ID: {le_id})")
    
    def _build_technical_layer(self, ddl_data: List[Dict[str, Any]],
                               node_builder: NodeBuilder,
                               rel_builder: RelationshipBuilder) -> None:
        """构建技术层节点和关系"""
        for item in ddl_data:
            database = item.get('database')
            tables = item.get('tables', [])
            
            for table in tables:
                table_name = table.get('table_name')
                comment = table.get('comment')
                
                # 创建物理表节点
                if table_name and table_name not in self.physical_table_cache:
                    ddl_statement = table.get('ddl_statement')
                    pt_id = node_builder.create_physical_table(table_name, database, comment, ddl_statement)
                    self.physical_table_cache[table_name] = pt_id
                    self.logger.debug(f"创建物理表: {table_name} (ID: {pt_id})")
                    
                    # 创建数据库→物理表CONTAINS关系
                    if database:
                        rel_builder.create_contains_by_names(database, table_name)
                        self.logger.debug(f"创建CONTAINS关系: {database} -> {table_name}")
                
                # 创建字段节点
                pt_id = self.physical_table_cache.get(table_name)
                if pt_id:
                    fields = table.get('fields', [])
                    for field in fields:
                        field_name = field.get('name')
                        data_type = field.get('data_type')
                        length = field.get('length')
                        nullable = field.get('nullable', True)
                        field_comment = field.get('comment')
                        
                        # 创建字段节点（会自动创建HAS_FIELD关系）
                        field_id = node_builder.create_field(
                            field_name, data_type, length, nullable, field_comment,
                            parent_id=pt_id
                        )
                        self.logger.debug(f"创建字段: {table_name}.{field_name} (ID: {field_id})")
    
    def _create_mapping_relationships(self, ddl_data: List[Dict[str, Any]],
                                     rel_builder: RelationshipBuilder) -> None:
        """创建逻辑实体到物理表的映射关系"""
        for item in ddl_data:
            logical_entity = item.get('logical_entity')
            business_subject = item.get('business_subject')
            business_domain = item.get('business_domain')
            subject_domain = item.get('subject_domain')
            tables = item.get('tables', [])
            
            # 获取逻辑实体ID
            if logical_entity and business_subject and business_domain and subject_domain:
                sd_id = self.subject_domain_cache.get(subject_domain)
                if sd_id:
                    bd_id = self.business_domain_cache.get((sd_id, business_domain))
                    if bd_id:
                        bs_id = self.business_subject_cache.get((bd_id, business_subject))
                        if bs_id:
                            le_id = self.logical_entity_cache.get((bs_id, logical_entity))
                            
                            if le_id:
                                # 为每个物理表创建映射关系
                                for table in tables:
                                    table_name = table.get('table_name')
                                    pt_id = self.physical_table_cache.get(table_name)
                                    
                                    if table_name:
                                        rel_builder.create_maps_to_by_names(logical_entity, table_name)
                                        self.logger.debug(
                                            f"创建MAPS_TO关系: {logical_entity} -> {table_name}"
                                        )
                                    else:
                                        self.logger.warning(
                                            f"物理表不存在，跳过映射: {table_name}"
                                        )
                            else:
                                self.logger.warning(
                                    f"逻辑实体不存在，跳过映射: {logical_entity}"
                                )
    
    def _create_data_elements(self, excel_data: List[Dict[str, Any]],
                             node_builder: NodeBuilder) -> None:
        """创建数据元节点并关联到逻辑实体"""
        if not excel_data:
            self.logger.info("没有Excel数据，跳过数据元创建")
            return
        
        self.logger.info(f"开始创建数据元节点，共 {len(excel_data)} 条记录")
        
        created_count = 0
        for item in excel_data:
            logical_entity = item.get('logical_entity')
            business_term = item.get('business_term')  # 数据元名称
            business_description = item.get('business_description')
            data_source_unit = item.get('data_source_unit')
            data_standard = item.get('data_standard')
            data_format = item.get('data_format')
            value_domain = item.get('value_domain')
            
            if not logical_entity or not business_term:
                continue
            
            # 创建数据元节点
            cache_key = (logical_entity, business_term)
            if cache_key not in self.data_element_cache:
                de_created = node_builder.create_data_element(
                    name=business_term,
                    logical_entity_name=logical_entity,
                    business_description=business_description,
                    data_source_unit=data_source_unit,
                    data_standard=data_standard,
                    data_format=data_format,
                    value_domain=value_domain
                )
                if de_created is not None:
                    self.data_element_cache[cache_key] = business_term
                    created_count += 1
                    self.logger.debug(f"创建数据元: {logical_entity}.{business_term}")
        
        self.logger.info(f"成功创建 {created_count} 个数据元节点")
    
    def _link_fields_to_data_elements(self, rel_builder: RelationshipBuilder) -> None:
        """通过COMMENT匹配，创建字段到数据元的REPRESENTS关系"""
        self.logger.info("开始关联字段和数据元...")
        
        linked_count = 0
        with self.connection.get_session() as session:
            # 遍历所有数据元
            for (logical_name, de_name), _marker in self.data_element_cache.items():
                # 查找该逻辑实体映射的物理表
                table_result = session.run("""
                    MATCH (le:LogicalEntity {logical_name: $logical_name})-[:MAPS_TO]->(pt:PhysicalTable)
                    RETURN pt.table_name as table_name
                """, logical_name=logical_name)
                
                for table_record in table_result:
                    table_name = table_record['table_name']
                    
                    # 查找comment匹配的字段
                    field_result = session.run("""
                        MATCH (pt:PhysicalTable {table_name: $table_name})-[:HAS_FIELD]->(f:Field)
                        WHERE f.comment = $de_name
                        RETURN f.name as field_name
                    """, table_name=table_name, de_name=de_name)
                    
                    for field_record in field_result:
                        field_name = field_record['field_name']
                        rel_builder.create_represents_by_names(table_name, field_name,
                                                                 logical_name, de_name)
                        linked_count += 1
                        self.logger.debug(
                            f"关联字段和数据元: {table_name}.{field_name} -> {de_name}"
                        )
        
        self.logger.info(f"成功关联 {linked_count} 个字段和数据元")
    
    def _enrich_business_semantics(self, excel_data: List[Dict[str, Any]],
                                   node_builder: NodeBuilder) -> None:
        """补充业务语义信息到字段节点"""
        if not excel_data:
            self.logger.info("没有Excel数据，跳过业务语义补充")
            return
        
        self.logger.info(f"开始补充业务语义，共 {len(excel_data)} 条记录")
        
        # 按逻辑实体分组Excel数据
        excel_by_entity = {}
        for item in excel_data:
            logical_entity = item.get('logical_entity')
            if logical_entity:
                if logical_entity not in excel_by_entity:
                    excel_by_entity[logical_entity] = []
                excel_by_entity[logical_entity].append(item)
        
        self.logger.info(f"Excel数据涵盖 {len(excel_by_entity)} 个逻辑实体")
        
        # 遍历每个逻辑实体
        updated_count = 0
        for logical_entity, items in excel_by_entity.items():
            # 查找逻辑实体ID（需要遍历缓存因为键是(bs_id, logical_entity)）
            le_id = None
            for (bs_id, le_name), cached_id in self.logical_entity_cache.items():
                if le_name == logical_entity:
                    le_id = cached_id
                    break
            
            if not le_id:
                self.logger.warning(f"逻辑实体不存在: {logical_entity}")
                continue
            
            # 查找该逻辑实体映射的物理表
            # 通过MAPS_TO关系查找
            with self.connection.get_session() as session:
                logical_name = self._get_logical_name_by_id(le_id)
                result = session.run("""
                    MATCH (le:LogicalEntity {logical_name: $logical_name})-[:MAPS_TO]->(pt:PhysicalTable)
                    RETURN pt.table_name as table_name
                """, logical_name=logical_name)
                
                for record in result:
                    table_name = record['table_name']
                    
                    # 为该表的每个字段补充业务语义
                    for item in items:
                        business_term = item.get('business_term')
                        data_source_unit = item.get('data_source_unit')
                        data_standard = item.get('data_standard')
                        
                        if not business_term:
                            continue
                        
                        # 查找字段（通过业务术语匹配comment）
                        # 因为Excel中的"数据元名称"对应DDL中的COMMENT
                        field_result = session.run("""
                            MATCH (pt:PhysicalTable {table_name: $table_name})-[:HAS_FIELD]->(f:Field)
                            WHERE f.comment = $business_term
                            RETURN f.name as field_name
                        """, table_name=table_name, business_term=business_term)

                        field_record = field_result.single()
                        if field_record:
                            field_name = field_record['field_name']
                            # 更新字段的业务语义属性（属性匹配）
                            session.run("""
                                MATCH (pt:PhysicalTable {table_name: $table_name})-[:HAS_FIELD]->(field:Field {name: $field_name})
                                SET field.business_term = COALESCE($business_term, field.business_term),
                                    field.data_source_unit = COALESCE($data_source_unit, field.data_source_unit),
                                    field.data_standard = COALESCE($data_standard, field.data_standard)
                            """, table_name=table_name, field_name=field_name,
                                business_term=business_term,
                                data_source_unit=data_source_unit, data_standard=data_standard)
                            
                            updated_count += 1
                            self.logger.debug(
                                f"补充业务语义: {table_name}.{field_name} -> {business_term}"
                            )
        
        self.logger.info(f"成功补充 {updated_count} 个字段的业务语义")
