"""测试物理表DDL属性"""
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from graph.neo4j_connection import Neo4jConnection
import yaml


def load_config(config_path: str) -> dict:
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def test_physical_table_ddl():
    """测试物理表是否包含DDL语句属性"""
    # 加载配置
    config_dir = Path('config')
    neo4j_config = load_config(config_dir / 'neo4j_config.yaml')
    
    # 连接Neo4j
    connection = Neo4jConnection(neo4j_config)
    
    try:
        with connection.get_session() as session:
            # 查询所有物理表节点
            query = """
            MATCH (pt:物理表)
            RETURN pt.表名 as table_name, 
                   pt.DDL语句 as ddl_statement,
                   pt.注释 as comment
            LIMIT 5
            """
            result = session.run(query)
            
            print("物理表DDL属性测试结果：\n")
            print("=" * 80)
            
            count = 0
            for record in result:
                count += 1
                table_name = record['table_name']
                ddl_statement = record['ddl_statement']
                comment = record['comment']
                
                print(f"\n表名: {table_name}")
                print(f"注释: {comment}")
                print(f"DDL语句: {'存在' if ddl_statement else '不存在'}")
                
                if ddl_statement:
                    # 显示DDL的前200个字符
                    preview = ddl_statement[:200] + "..." if len(ddl_statement) > 200 else ddl_statement
                    print(f"DDL预览:\n{preview}")
                
                print("-" * 80)
            
            if count == 0:
                print("未找到物理表节点，请先运行 rebuild_graph_cn.py 构建图谱")
            else:
                print(f"\n✓ 测试完成，共检查了 {count} 个物理表节点")
    
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        raise
    finally:
        connection.close()


if __name__ == '__main__':
    test_physical_table_ddl()
