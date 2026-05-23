"""Checkpoint 2 验证脚本 - 验证知识图谱构建功能"""
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.config_loader import ConfigLoader
from utils.logger import setup_logger
from graph.neo4j_connection import Neo4jConnection
from graph.node_builder import NodeBuilder
from graph.relationship_builder import RelationshipBuilder
from graph.graph_builder import GraphBuilder


def main():
    """主验证函数"""
    # 设置日志
    logger = setup_logger('checkpoint2_verification', verbose=True)
    
    logger.info("=" * 60)
    logger.info("Checkpoint 2 验证开始")
    logger.info("验证知识图谱构建功能 (任务 4-6)")
    logger.info("=" * 60)
    
    config_dir = Path(__file__).parent.parent / 'config'
    
    try:
        # 步骤 1: 加载配置
        logger.info("\n[步骤 1/10] 加载配置...")
        loader = ConfigLoader(config_dir)
        configs = loader.load_all_configs()
        logger.info("✓ 配置加载成功")
        
        # 步骤 2: 连接Neo4j
        logger.info("\n[步骤 2/10] 连接Neo4j数据库...")
        try:
            conn = Neo4jConnection(configs['neo4j_config'])
            logger.info("✓ Neo4j连接建立成功")
        except Exception as e:
            logger.error(f"✗ Neo4j连接失败: {e}")
            logger.warning("\n提示: 请确保Neo4j数据库正在运行")
            return False
        
        # 步骤 3: 清空测试数据
        logger.info("\n[步骤 3/10] 清空测试数据...")
        with conn.get_session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        logger.info("✓ 测试数据已清空")
        
        # 步骤 4: 测试节点构建器
        logger.info("\n[步骤 4/10] 测试节点构建器...")
        with conn.get_session() as session:
            node_builder = NodeBuilder(session)
            
            # 测试创建主题域节点
            logger.info("  - 测试创建主题域节点...")
            subject_domain_id = node_builder.create_subject_domain("测试主题域")
            assert subject_domain_id is not None
            logger.info(f"    ✓ 主题域节点创建成功 (ID: {subject_domain_id})")
            
            # 测试创建数据库节点
            logger.info("  - 测试创建数据库节点...")
            database_id = node_builder.create_database("test_db")
            assert database_id is not None
            logger.info(f"    ✓ 数据库节点创建成功 (ID: {database_id})")
            
            # 测试创建业务域节点
            logger.info("  - 测试创建业务域节点...")
            business_domain_id = node_builder.create_business_domain(
                "测试业务域", subject_domain_id
            )
            assert business_domain_id is not None
            logger.info(f"    ✓ 业务域节点创建成功 (ID: {business_domain_id})")
            
            # 测试创建业务主题节点
            logger.info("  - 测试创建业务主题节点...")
            business_subject_id = node_builder.create_business_subject(
                "测试业务主题", business_domain_id
            )
            assert business_subject_id is not None
            logger.info(f"    ✓ 业务主题节点创建成功 (ID: {business_subject_id})")
            
            # 测试创建逻辑实体节点
            logger.info("  - 测试创建逻辑实体节点...")
            logical_entity_id = node_builder.create_logical_entity(
                "测试逻辑实体", "TEST001", business_subject_id
            )
            assert logical_entity_id is not None
            logger.info(f"    ✓ 逻辑实体节点创建成功 (ID: {logical_entity_id})")
            
            # 测试创建物理表节点
            logger.info("  - 测试创建物理表节点...")
            physical_table_id = node_builder.create_physical_table(
                "test_table", "test_db", "测试表"
            )
            assert physical_table_id is not None
            logger.info(f"    ✓ 物理表节点创建成功 (ID: {physical_table_id})")
            
            # 测试创建字段节点
            logger.info("  - 测试创建字段节点...")
            field_id = node_builder.create_field(
                "test_field", "VARCHAR", 100, False, "测试字段",
                physical_table_id, "测试业务术语", "测试数源单位", "GB/T 2261.1-2003"
            )
            assert field_id is not None
            logger.info(f"    ✓ 字段节点创建成功 (ID: {field_id})")
        
        logger.info("✓ 节点构建器测试通过")
        
        # 步骤 5: 测试关系构建器
        logger.info("\n[步骤 5/10] 测试关系构建器...")
        with conn.get_session() as session:
            rel_builder = RelationshipBuilder(session)
            
            # 测试创建IMPLEMENTS关系
            logger.info("  - 测试创建IMPLEMENTS关系...")
            rel_builder.create_implements(database_id, subject_domain_id)
            logger.info("    ✓ IMPLEMENTS关系创建成功")
            
            # 测试创建Database->PhysicalTable CONTAINS关系
            logger.info("  - 测试创建Database->PhysicalTable CONTAINS关系...")
            rel_builder.create_contains(database_id, physical_table_id)
            logger.info("    ✓ Database->PhysicalTable CONTAINS关系创建成功")
            
            # 测试创建MAPS_TO关系
            logger.info("  - 测试创建MAPS_TO关系...")
            rel_builder.create_maps_to(logical_entity_id, physical_table_id)
            logger.info("    ✓ MAPS_TO关系创建成功")
        
        logger.info("✓ 关系构建器测试通过")
        
        # 步骤 6: 验证节点去重
        logger.info("\n[步骤 6/10] 验证节点去重功能...")
        with conn.get_session() as session:
            node_builder = NodeBuilder(session)
            
            # 尝试创建重复的主题域节点
            logger.info("  - 测试全局唯一节点去重...")
            duplicate_id = node_builder.create_subject_domain("测试主题域")
            assert duplicate_id == subject_domain_id
            logger.info("    ✓ 全局唯一节点去重正常")
            
            # 尝试创建重复的业务域节点
            logger.info("  - 测试结构唯一节点去重...")
            duplicate_bd_id = node_builder.create_business_domain(
                "测试业务域", subject_domain_id
            )
            assert duplicate_bd_id == business_domain_id
            logger.info("    ✓ 结构唯一节点去重正常")
        
        logger.info("✓ 节点去重功能正常")
        
        # 步骤 7: 验证图谱结构
        logger.info("\n[步骤 7/10] 验证图谱结构...")
        with conn.get_session() as session:
            # 验证节点数量
            result = session.run("MATCH (n) RETURN count(n) as count")
            node_count = result.single()['count']
            logger.info(f"  - 节点总数: {node_count}")
            assert node_count == 7  # 7个不同类型的节点
            
            # 验证关系数量
            result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            rel_count = result.single()['count']
            logger.info(f"  - 关系总数: {rel_count}")
            assert rel_count >= 6  # 至少6个关系
            
            # 验证业务层路径
            logger.info("  - 验证业务层路径...")
            result = session.run("""
                MATCH path = (sd:SubjectDomain {name: '测试主题域'})
                    -[:CONTAINS]->(bd:BusinessDomain {name: '测试业务域'})
                    -[:CONTAINS]->(bs:BusinessSubject {name: '测试业务主题'})
                    -[:CONTAINS]->(le:LogicalEntity {logical_name: '测试逻辑实体'})
                RETURN length(path) as path_length
            """)
            record = result.single()
            assert record is not None
            assert record['path_length'] == 3
            logger.info("    ✓ 业务层路径正确")
            
            # 验证技术层路径
            logger.info("  - 验证技术层路径...")
            result = session.run("""
                MATCH path = (db:Database {name: 'test_db'})
                    -[:CONTAINS]->(pt:PhysicalTable {table_name: 'test_table'})
                    -[:HAS_FIELD]->(f:Field {name: 'test_field'})
                RETURN length(path) as path_length
            """)
            record = result.single()
            assert record is not None
            assert record['path_length'] == 2
            logger.info("    ✓ 技术层路径正确")
            
            # 验证映射关系
            logger.info("  - 验证映射关系...")
            result = session.run("""
                MATCH (le:LogicalEntity {logical_name: '测试逻辑实体'})
                    -[:MAPS_TO]->(pt:PhysicalTable {table_name: 'test_table'})
                RETURN count(*) as count
            """)
            assert result.single()['count'] == 1
            logger.info("    ✓ 映射关系正确")
            
            # 验证IMPLEMENTS关系
            logger.info("  - 验证IMPLEMENTS关系...")
            result = session.run("""
                MATCH (db:Database {name: 'test_db'})
                    -[:IMPLEMENTS]->(sd:SubjectDomain {name: '测试主题域'})
                RETURN count(*) as count
            """)
            assert result.single()['count'] == 1
            logger.info("    ✓ IMPLEMENTS关系正确")
        
        logger.info("✓ 图谱结构验证通过")
        
        # 步骤 8: 测试图谱构建器
        logger.info("\n[步骤 8/10] 测试图谱构建器...")
        
        # 准备测试数据
        test_ddl_data = [
            {
                'file_path': 'ddls/ZRR/5.3.1.1_1-基本信息-登记信息-基本登记信息.sql',
                'subject_domain': '自然人',
                'business_domain': '基本信息',
                'business_subject': '登记信息',
                'logical_entity': '基本登记信息',
                'code': '5.3.1.1_1',
                'database': 'zrr',
                'tables': [
                    {
                        'table_name': 'dwd_zrr_jbdjxx_new',
                        'comment': '基本登记信息表',
                        'fields': [
                            {
                                'name': 'xm',
                                'data_type': 'VARCHAR',
                                'length': 100,
                                'nullable': False,
                                'comment': '姓名'
                            },
                            {
                                'name': 'sfzh',
                                'data_type': 'VARCHAR',
                                'length': 18,
                                'nullable': False,
                                'comment': '身份证号'
                            }
                        ]
                    }
                ]
            }
        ]
        
        test_excel_data = [
            {
                'logical_entity': '基本登记信息',
                'table_name': 'dwd_zrr_jbdjxx_new',
                'field_name': 'xm',
                'business_term': '自然人姓名',
                'data_source_unit': '公安部门',
                'data_standard': 'GB/T 2261.1-2003'
            }
        ]
        
        # 清空之前的测试数据
        with conn.get_session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        
        # 使用图谱构建器构建
        logger.info("  - 执行图谱构建...")
        graph_builder = GraphBuilder(conn, configs)
        graph_builder.build_graph(test_ddl_data, test_excel_data)
        logger.info("    ✓ 图谱构建完成")
        
        logger.info("✓ 图谱构建器测试通过")
        
        # 步骤 9: 验证完整图谱
        logger.info("\n[步骤 9/10] 验证完整图谱...")
        with conn.get_session() as session:
            # 验证所有节点类型都存在
            logger.info("  - 验证节点类型...")
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(*) as count
                ORDER BY label
            """)
            node_types = {record['label']: record['count'] for record in result}
            logger.info(f"    节点类型统计: {node_types}")
            
            expected_types = ['SubjectDomain', 'BusinessDomain', 'BusinessSubject', 
                            'LogicalEntity', 'Database', 'PhysicalTable', 'Field']
            for node_type in expected_types:
                assert node_type in node_types, f"缺少节点类型: {node_type}"
            logger.info("    ✓ 所有节点类型都存在")
            
            # 验证关系类型
            logger.info("  - 验证关系类型...")
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(*) as count
                ORDER BY rel_type
            """)
            rel_types = {record['rel_type']: record['count'] for record in result}
            logger.info(f"    关系类型统计: {rel_types}")
            
            expected_rels = ['CONTAINS', 'IMPLEMENTS', 'MAPS_TO', 'HAS_FIELD']
            for rel_type in expected_rels:
                assert rel_type in rel_types, f"缺少关系类型: {rel_type}"
            logger.info("    ✓ 所有关系类型都存在")
            
            # 验证业务语义属性
            logger.info("  - 验证业务语义属性...")
            result = session.run("""
                MATCH (f:Field {name: 'xm'})
                RETURN f.business_term as business_term,
                       f.data_source_unit as data_source_unit,
                       f.data_standard as data_standard
            """)
            record = result.single()
            assert record is not None
            assert record['business_term'] == '自然人姓名'
            assert record['data_source_unit'] == '公安部门'
            assert record['data_standard'] == 'GB/T 2261.1-2003'
            logger.info("    ✓ 业务语义属性正确")
        
        logger.info("✓ 完整图谱验证通过")
        
        # 步骤 10: 清理测试数据
        logger.info("\n[步骤 10/10] 清理测试数据...")
        with conn.get_session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        logger.info("✓ 测试数据已清理")
        
        # 关闭连接
        conn.close()
        
        # 验证成功
        logger.info("\n" + "=" * 60)
        logger.info("✓✓✓ Checkpoint 2 验证通过 ✓✓✓")
        logger.info("=" * 60)
        logger.info("\n验证结果:")
        logger.info("  ✓ 节点构建器正常工作")
        logger.info("  ✓ 关系构建器正常工作")
        logger.info("  ✓ 节点去重功能正常")
        logger.info("  ✓ 图谱结构正确")
        logger.info("  ✓ 图谱构建器正常工作")
        logger.info("  ✓ 业务语义属性正确")
        logger.info("\n知识图谱构建功能验证完成！")
        logger.info("可以继续执行后续任务（任务 7-9: MCP服务器实现）")
        
        return True
        
    except AssertionError as e:
        logger.error(f"\n✗ 验证失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False
    except Exception as e:
        logger.error(f"\n✗ 验证过程中发生错误: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
