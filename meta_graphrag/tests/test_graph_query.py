"""测试图谱查询功能 - 验证图谱数据的完整性和可查询性"""
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.config_loader import ConfigLoader
from utils.logger import setup_logger
from graph.neo4j_connection import Neo4jConnection


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def query_graph_overview(session):
    """查询图谱概览"""
    print_section("图谱概览")
    
    # 查询节点统计
    result = session.run("""
        MATCH (n)
        RETURN labels(n)[0] as node_type, count(*) as count
        ORDER BY node_type
    """)
    
    print("\n节点统计:")
    total_nodes = 0
    for record in result:
        node_type = record['node_type']
        count = record['count']
        total_nodes += count
        print(f"  {node_type:20s}: {count:5d} 个")
    print(f"  {'总计':20s}: {total_nodes:5d} 个")
    
    # 查询关系统计
    result = session.run("""
        MATCH ()-[r]->()
        RETURN type(r) as rel_type, count(*) as count
        ORDER BY rel_type
    """)
    
    print("\n关系统计:")
    total_rels = 0
    for record in result:
        rel_type = record['rel_type']
        count = record['count']
        total_rels += count
        print(f"  {rel_type:20s}: {count:5d} 个")
    print(f"  {'总计':20s}: {total_rels:5d} 个")


def query_subject_domains(session):
    """查询所有主题域"""
    print_section("主题域列表")
    
    result = session.run("""
        MATCH (sd:SubjectDomain)
        RETURN sd.name as name, sd.created_at as created_at
        ORDER BY sd.name
    """)
    
    print("\n主题域:")
    for i, record in enumerate(result, 1):
        print(f"  {i}. {record['name']}")
        print(f"     创建时间: {record['created_at']}")


def query_business_hierarchy(session):
    """查询业务层级结构"""
    print_section("业务层级结构")
    
    result = session.run("""
        MATCH path = (sd:SubjectDomain)-[:CONTAINS]->(bd:BusinessDomain)
                    -[:CONTAINS]->(bs:BusinessSubject)
                    -[:CONTAINS]->(le:LogicalEntity)
        RETURN sd.name as subject_domain,
               bd.name as business_domain,
               bs.name as business_subject,
               le.logical_name as logical_entity,
               le.code as code
        ORDER BY sd.name, bd.name, bs.name, le.logical_name
        LIMIT 10
    """)
    
    print("\n业务层级 (前10条):")
    current_sd = None
    current_bd = None
    current_bs = None
    
    for record in result:
        sd = record['subject_domain']
        bd = record['business_domain']
        bs = record['business_subject']
        le = record['logical_entity']
        code = record['code']
        
        if sd != current_sd:
            print(f"\n  📁 {sd}")
            current_sd = sd
            current_bd = None
            current_bs = None
        
        if bd != current_bd:
            print(f"    └─ 📂 {bd}")
            current_bd = bd
            current_bs = None
        
        if bs != current_bs:
            print(f"       └─ 📋 {bs}")
            current_bs = bs
        
        print(f"          └─ 📄 {le} ({code})")


def query_technical_structure(session):
    """查询技术层结构"""
    print_section("技术层结构")
    
    result = session.run("""
        MATCH (db:Database)-[:CONTAINS]->(pt:PhysicalTable)
        OPTIONAL MATCH (pt)-[:HAS_FIELD]->(f:Field)
        RETURN db.name as database,
               pt.table_name as table_name,
               pt.comment as table_comment,
               count(f) as field_count
        ORDER BY db.name, pt.table_name
        LIMIT 10
    """)
    
    print("\n数据库和表 (前10条):")
    current_db = None
    
    for record in result:
        db = record['database']
        table = record['table_name']
        comment = record['table_comment'] or ''
        field_count = record['field_count']
        
        if db != current_db:
            print(f"\n  🗄️  {db}")
            current_db = db
        
        print(f"    └─ 📊 {table}")
        if comment:
            print(f"       说明: {comment}")
        print(f"       字段数: {field_count}")


def query_field_details(session):
    """查询字段详情"""
    print_section("字段详情示例")
    
    result = session.run("""
        MATCH (pt:PhysicalTable)-[:HAS_FIELD]->(f:Field)
        WHERE f.business_term IS NOT NULL
        RETURN pt.table_name as table_name,
               f.name as field_name,
               f.data_type as data_type,
               f.length as length,
               f.nullable as nullable,
               f.comment as comment,
               f.business_term as business_term,
               f.data_source_unit as data_source_unit,
               f.data_standard as data_standard
        ORDER BY pt.table_name, f.name
        LIMIT 5
    """)
    
    print("\n字段详情 (前5个有业务语义的字段):")
    for i, record in enumerate(result, 1):
        print(f"\n  {i}. 表: {record['table_name']}")
        print(f"     字段名: {record['field_name']}")
        print(f"     数据类型: {record['data_type']}", end='')
        if record['length']:
            print(f"({record['length']})", end='')
        print(f", 可空: {'是' if record['nullable'] else '否'}")
        if record['comment']:
            print(f"     注释: {record['comment']}")
        if record['business_term']:
            print(f"     业务术语: {record['business_term']}")
        if record['data_source_unit']:
            print(f"     数源单位: {record['data_source_unit']}")
        if record['data_standard']:
            print(f"     数据标准: {record['data_standard']}")


def query_mappings(session):
    """查询业务到技术的映射关系"""
    print_section("业务-技术映射关系")
    
    result = session.run("""
        MATCH (le:LogicalEntity)-[:MAPS_TO]->(pt:PhysicalTable)
        RETURN le.logical_name as logical_entity,
               pt.table_name as physical_table,
               pt.database_name as database
        ORDER BY le.logical_name
        LIMIT 10
    """)
    
    print("\n逻辑实体 → 物理表映射 (前10条):")
    for i, record in enumerate(result, 1):
        print(f"  {i}. {record['logical_entity']}")
        print(f"     → {record['database']}.{record['physical_table']}")


def query_implements_relations(session):
    """查询数据库实现主题域的关系"""
    print_section("数据库-主题域实现关系")
    
    result = session.run("""
        MATCH (db:Database)-[:IMPLEMENTS]->(sd:SubjectDomain)
        RETURN db.name as database,
               sd.name as subject_domain
        ORDER BY db.name
    """)
    
    print("\n数据库 → 主题域:")
    for record in result:
        print(f"  {record['database']} → {record['subject_domain']}")


def query_sample_paths(session):
    """查询示例路径"""
    print_section("完整路径示例")
    
    result = session.run("""
        MATCH path = (sd:SubjectDomain)-[:CONTAINS]->(bd:BusinessDomain)
                    -[:CONTAINS]->(bs:BusinessSubject)
                    -[:CONTAINS]->(le:LogicalEntity)
                    -[:MAPS_TO]->(pt:PhysicalTable)
                    <-[:CONTAINS]-(db:Database)
                    -[:IMPLEMENTS]->(sd)
        RETURN sd.name as subject_domain,
               bd.name as business_domain,
               bs.name as business_subject,
               le.logical_name as logical_entity,
               pt.table_name as physical_table,
               db.name as database,
               length(path) as path_length
        LIMIT 3
    """)
    
    print("\n完整业务-技术路径 (前3条):")
    for i, record in enumerate(result, 1):
        print(f"\n  路径 {i} (长度: {record['path_length']}):")
        print(f"    主题域: {record['subject_domain']}")
        print(f"    └─ 业务域: {record['business_domain']}")
        print(f"       └─ 业务主题: {record['business_subject']}")
        print(f"          └─ 逻辑实体: {record['logical_entity']}")
        print(f"             ↓ MAPS_TO")
        print(f"          物理表: {record['physical_table']}")
        print(f"          └─ 数据库: {record['database']}")
        print(f"             ↓ IMPLEMENTS")
        print(f"          主题域: {record['subject_domain']}")


def search_by_keyword(session, keyword):
    """按关键词搜索"""
    print_section(f"关键词搜索: '{keyword}'")
    
    result = session.run("""
        MATCH (n)
        WHERE n.name CONTAINS $keyword
           OR n.logical_name CONTAINS $keyword
           OR n.table_name CONTAINS $keyword
           OR n.comment CONTAINS $keyword
           OR n.business_term CONTAINS $keyword
        RETURN labels(n)[0] as node_type,
               COALESCE(n.name, n.logical_name, n.table_name) as name,
               COALESCE(n.comment, n.business_term, '') as description
        LIMIT 10
    """, keyword=keyword)
    
    print(f"\n搜索结果 (前10条):")
    count = 0
    for record in result:
        count += 1
        print(f"  {count}. [{record['node_type']}] {record['name']}")
        if record['description']:
            print(f"     {record['description']}")
    
    if count == 0:
        print("  未找到匹配结果")


def main():
    """主函数"""
    logger = setup_logger('graph_query_test', verbose=True)
    
    print("\n" + "=" * 60)
    print("  知识图谱查询测试")
    print("=" * 60)
    
    config_dir = Path(__file__).parent.parent / 'config'
    
    try:
        # 加载配置
        loader = ConfigLoader(config_dir)
        configs = loader.load_all_configs()
        
        # 连接Neo4j
        conn = Neo4jConnection(configs['neo4j_config'])
        
        with conn.get_session() as session:
            # 1. 图谱概览
            query_graph_overview(session)
            
            # 2. 主题域列表
            query_subject_domains(session)
            
            # 3. 业务层级结构
            query_business_hierarchy(session)
            
            # 4. 技术层结构
            query_technical_structure(session)
            
            # 5. 字段详情
            query_field_details(session)
            
            # 6. 映射关系
            query_mappings(session)
            
            # 7. 实现关系
            query_implements_relations(session)
            
            # 8. 完整路径示例
            query_sample_paths(session)
            
            # 9. 关键词搜索示例
            search_by_keyword(session, "基本")
            search_by_keyword(session, "姓名")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("  查询测试完成")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"\n查询测试失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
