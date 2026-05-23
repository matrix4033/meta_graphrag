"""Checkpoint 1 验证脚本 - 验证配置系统和Neo4j连接"""
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from utils.config_loader import ConfigLoader
from utils.config_validator import ConfigValidator
from utils.logger import setup_logger
from graph.neo4j_connection import Neo4jConnection
from graph.transaction_manager import TransactionManager
from graph.index_manager import IndexManager


def main():
    """主验证函数"""
    # 设置日志
    logger = setup_logger('checkpoint1_verification', verbose=True)
    
    logger.info("=" * 60)
    logger.info("Checkpoint 1 验证开始")
    logger.info("=" * 60)
    
    config_dir = Path(__file__).parent / 'config'
    
    try:
        # 步骤 1: 测试配置加载
        logger.info("\n[步骤 1/6] 测试配置加载器...")
        loader = ConfigLoader(config_dir)
        configs = loader.load_all_configs()
        logger.info("✓ 配置加载成功")
        logger.info(f"  - 已加载 {len(configs)} 个配置文件")
        
        # 步骤 2: 测试配置验证
        logger.info("\n[步骤 2/6] 测试配置验证器...")
        validator = ConfigValidator()
        is_valid, errors = validator.validate_all_configs(configs)
        
        if not is_valid:
            logger.error("✗ 配置验证失败:")
            for error in errors:
                logger.error(f"  - {error}")
            return False
        
        logger.info("✓ 配置验证通过")
        
        # 步骤 3: 测试Neo4j连接
        logger.info("\n[步骤 3/6] 测试Neo4j连接...")
        try:
            conn = Neo4jConnection(configs['neo4j_config'])
            logger.info("✓ Neo4j连接建立成功")
        except Exception as e:
            logger.error(f"✗ Neo4j连接失败: {e}")
            logger.warning("\n提示: 请确保Neo4j数据库正在运行")
            logger.warning("  - 检查config/neo4j_config.yaml中的连接参数")
            logger.warning("  - 确认Neo4j服务已启动")
            return False
        
        # 步骤 4: 测试连接验证
        logger.info("\n[步骤 4/6] 验证Neo4j连接状态...")
        if not conn.verify_connection():
            logger.error("✗ Neo4j连接验证失败")
            conn.close()
            return False
        logger.info("✓ Neo4j连接状态正常")
        
        # 步骤 5: 测试事务管理
        logger.info("\n[步骤 5/6] 测试事务管理器...")
        try:
            with conn.get_session() as session:
                tx_manager = TransactionManager(session)
                
                # 执行测试查询
                tx = tx_manager.begin_transaction()
                result = tx.run("RETURN 'Checkpoint 1 Test' as message, datetime() as timestamp")
                record = result.single()
                
                logger.info(f"  - 测试查询结果: {record['message']}")
                logger.info(f"  - 时间戳: {record['timestamp']}")
                
                tx_manager.commit()
                logger.info("✓ 事务管理器工作正常")
        except Exception as e:
            logger.error(f"✗ 事务管理器测试失败: {e}")
            conn.close()
            return False
        
        # 步骤 6: 测试索引管理器
        logger.info("\n[步骤 6/6] 测试索引管理器...")
        try:
            with conn.get_session() as session:
                index_manager = IndexManager(session, configs['index_config'])
                
                # 测试索引存在性检查
                test_index_exists = index_manager._index_exists('test_non_existent_index')
                assert not test_index_exists
                
                logger.info("✓ 索引管理器初始化成功")
        except Exception as e:
            logger.error(f"✗ 索引管理器测试失败: {e}")
            conn.close()
            return False
        
        # 关闭连接
        conn.close()
        
        # 验证成功
        logger.info("\n" + "=" * 60)
        logger.info("✓✓✓ Checkpoint 1 验证通过 ✓✓✓")
        logger.info("=" * 60)
        logger.info("\n验证结果:")
        logger.info("  ✓ 配置系统正常工作")
        logger.info("  ✓ Neo4j连接正常工作")
        logger.info("  ✓ 事务管理器正常工作")
        logger.info("  ✓ 索引管理器正常工作")
        logger.info("\n可以继续执行后续任务！")
        
        return True
        
    except Exception as e:
        logger.error(f"\n✗ 验证过程中发生错误: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
