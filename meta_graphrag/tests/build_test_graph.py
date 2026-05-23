"""构建测试图谱 - 用于测试查询功能"""
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.config_loader import ConfigLoader
from utils.logger import setup_logger
from graph.neo4j_connection import Neo4jConnection
from graph.graph_builder import GraphBuilder


def main():
    """主函数"""
    logger = setup_logger('build_test_graph', verbose=True)
    
    logger.info("=" * 60)
    logger.info("构建测试图谱")
    logger.info("=" * 60)
    
    config_dir = Path(__file__).parent.parent / 'config'
    
    try:
        # 加载配置
        logger.info("\n加载配置...")
        loader = ConfigLoader(config_dir)
        configs = loader.load_all_configs()
        
        # 连接Neo4j
        logger.info("连接Neo4j数据库...")
        conn = Neo4jConnection(configs['neo4j_config'])
        
        # 清空现有数据
        logger.info("清空现有数据...")
        with conn.get_session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        
        # 准备测试数据
        logger.info("\n准备测试数据...")
        
        # DDL数据 - 自然人主题域
        ddl_data = [
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
                            },
                            {
                                'name': 'csrq',
                                'data_type': 'DATE',
                                'length': None,
                                'nullable': True,
                                'comment': '出生日期'
                            }
                        ]
                    }
                ]
            },
            {
                'file_path': 'ddls/ZRR/5.3.1.1_2-基本信息-登记信息-身份证件信息.sql',
                'subject_domain': '自然人',
                'business_domain': '基本信息',
                'business_subject': '登记信息',
                'logical_entity': '身份证件信息',
                'code': '5.3.1.1_2',
                'database': 'zrr',
                'tables': [
                    {
                        'table_name': 'dwd_zrr_sfzjxx',
                        'comment': '身份证件信息表',
                        'fields': [
                            {
                                'name': 'zjhm',
                                'data_type': 'VARCHAR',
                                'length': 50,
                                'nullable': False,
                                'comment': '证件号码'
                            },
                            {
                                'name': 'zjlx',
                                'data_type': 'VARCHAR',
                                'length': 10,
                                'nullable': False,
                                'comment': '证件类型'
                            }
                        ]
                    }
                ]
            },
            {
                'file_path': 'ddls/ZRR/5.3.1.2_1-基本信息-生理体征信息-出生信息.sql',
                'subject_domain': '自然人',
                'business_domain': '基本信息',
                'business_subject': '生理体征信息',
                'logical_entity': '出生信息',
                'code': '5.3.1.2_1',
                'database': 'zrr',
                'tables': [
                    {
                        'table_name': 'dwd_zrr_csxx',
                        'comment': '出生信息表',
                        'fields': [
                            {
                                'name': 'csrq',
                                'data_type': 'DATE',
                                'length': None,
                                'nullable': False,
                                'comment': '出生日期'
                            },
                            {
                                'name': 'csdz',
                                'data_type': 'VARCHAR',
                                'length': 200,
                                'nullable': True,
                                'comment': '出生地址'
                            }
                        ]
                    }
                ]
            },
            # 死亡库主题域
            {
                'file_path': 'ddls/SWK/1_1-死亡库-权威库-死亡人员基本信息表.sql',
                'subject_domain': '死亡库',
                'business_domain': '权威库',
                'business_subject': '死亡人员信息',
                'logical_entity': '死亡人员基本信息',
                'code': '1_1',
                'database': 'swk',
                'tables': [
                    {
                        'table_name': 'dwd_swk_swryjbxx',
                        'comment': '死亡人员基本信息表',
                        'fields': [
                            {
                                'name': 'xm',
                                'data_type': 'VARCHAR',
                                'length': 100,
                                'nullable': False,
                                'comment': '姓名'
                            },
                            {
                                'name': 'swrq',
                                'data_type': 'DATE',
                                'length': None,
                                'nullable': False,
                                'comment': '死亡日期'
                            }
                        ]
                    }
                ]
            }
        ]
        
        # Excel元数据 - 业务语义
        excel_data = [
            {
                'logical_entity': '基本登记信息',
                'table_name': 'dwd_zrr_jbdjxx_new',
                'field_name': 'xm',
                'business_term': '自然人姓名',
                'data_source_unit': '公安部门',
                'data_standard': 'GB/T 2261.1-2003'
            },
            {
                'logical_entity': '基本登记信息',
                'table_name': 'dwd_zrr_jbdjxx_new',
                'field_name': 'sfzh',
                'business_term': '居民身份证号码',
                'data_source_unit': '公安部门',
                'data_standard': 'GB 11643-1999'
            },
            {
                'logical_entity': '身份证件信息',
                'table_name': 'dwd_zrr_sfzjxx',
                'field_name': 'zjhm',
                'business_term': '证件号码',
                'data_source_unit': '公安部门',
                'data_standard': None
            }
        ]
        
        # 构建图谱
        logger.info("\n开始构建图谱...")
        graph_builder = GraphBuilder(conn, configs)
        graph_builder.build_graph(ddl_data, excel_data)
        
        # 验证构建结果
        logger.info("\n验证构建结果...")
        with conn.get_session() as session:
            # 统计节点
            result = session.run("MATCH (n) RETURN count(n) as count")
            node_count = result.single()['count']
            logger.info(f"  节点总数: {node_count}")
            
            # 统计关系
            result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
            rel_count = result.single()['count']
            logger.info(f"  关系总数: {rel_count}")
            
            # 按类型统计节点
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(*) as count
                ORDER BY label
            """)
            logger.info("\n  节点类型统计:")
            for record in result:
                logger.info(f"    {record['label']:20s}: {record['count']}")
            
            # 按类型统计关系
            result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as type, count(*) as count
                ORDER BY type
            """)
            logger.info("\n  关系类型统计:")
            for record in result:
                logger.info(f"    {record['type']:20s}: {record['count']}")
        
        conn.close()
        
        logger.info("\n" + "=" * 60)
        logger.info("✓ 测试图谱构建完成")
        logger.info("=" * 60)
        logger.info("\n现在可以运行 'python tests/test_graph_query.py' 来查询图谱")
        
        return True
        
    except Exception as e:
        logger.error(f"\n构建失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
