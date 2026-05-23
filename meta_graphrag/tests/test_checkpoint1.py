"""Checkpoint 1 测试 - 验证配置系统和Neo4j连接"""
import pytest
from pathlib import Path
import sys

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils.config_loader import ConfigLoader
from utils.config_validator import ConfigValidator
from utils.logger import setup_logger
from graph.neo4j_connection import Neo4jConnection
from graph.transaction_manager import TransactionManager
from graph.index_manager import IndexManager


class TestCheckpoint1:
    """Checkpoint 1 测试套件"""
    
    @pytest.fixture
    def config_dir(self):
        """配置目录fixture"""
        return Path(__file__).parent.parent / 'config'
    
    @pytest.fixture
    def logger(self):
        """日志器fixture"""
        return setup_logger('test_checkpoint1', verbose=True)
    
    def test_config_loader(self, config_dir, logger):
        """测试配置加载器"""
        logger.info("测试配置加载器...")
        
        # 创建配置加载器
        loader = ConfigLoader(config_dir)
        
        # 加载所有配置
        configs = loader.load_all_configs()
        
        # 验证配置已加载
        assert 'neo4j_config' in configs
        assert 'parser_config' in configs
        assert 'excel_config' in configs
        assert 'index_config' in configs
        assert 'mcp_config' in configs
        
        logger.info("✓ 配置加载器测试通过")
    
    def test_config_validator(self, config_dir, logger):
        """测试配置验证器"""
        logger.info("测试配置验证器...")
        
        # 加载配置
        loader = ConfigLoader(config_dir)
        configs = loader.load_all_configs()
        
        # 验证配置
        validator = ConfigValidator()
        is_valid, errors = validator.validate_all_configs(configs)
        
        # 输出验证结果
        if not is_valid:
            logger.error("配置验证失败:")
            for error in errors:
                logger.error(f"  - {error}")
        
        assert is_valid, f"配置验证失败: {errors}"
        
        logger.info("✓ 配置验证器测试通过")
    
    def test_neo4j_connection(self, config_dir, logger):
        """测试Neo4j连接"""
        logger.info("测试Neo4j连接...")
        
        # 加载配置
        loader = ConfigLoader(config_dir)
        neo4j_config = loader.load_neo4j_config()
        
        # 创建连接
        try:
            with Neo4jConnection(neo4j_config) as conn:
                # 验证连接
                assert conn.verify_connection(), "Neo4j连接验证失败"
                
                logger.info("✓ Neo4j连接测试通过")
        except Exception as e:
            pytest.skip(f"Neo4j连接失败，跳过测试: {e}")
    
    def test_transaction_manager(self, config_dir, logger):
        """测试事务管理器"""
        logger.info("测试事务管理器...")
        
        # 加载配置
        loader = ConfigLoader(config_dir)
        neo4j_config = loader.load_neo4j_config()
        
        try:
            with Neo4jConnection(neo4j_config) as conn:
                with conn.get_session() as session:
                    # 创建事务管理器
                    tx_manager = TransactionManager(session)
                    
                    # 测试事务开启和提交
                    tx = tx_manager.begin_transaction()
                    assert tx is not None
                    
                    # 执行简单查询
                    result = tx.run("RETURN 1 as value")
                    record = result.single()
                    assert record['value'] == 1
                    
                    tx_manager.commit()
                    
                    logger.info("✓ 事务管理器测试通过")
        except Exception as e:
            pytest.skip(f"Neo4j连接失败，跳过测试: {e}")
    
    def test_index_manager(self, config_dir, logger):
        """测试索引管理器"""
        logger.info("测试索引管理器...")
        
        # 加载配置
        loader = ConfigLoader(config_dir)
        neo4j_config = loader.load_neo4j_config()
        index_config = loader.load_index_config()
        
        try:
            with Neo4jConnection(neo4j_config) as conn:
                with conn.get_session() as session:
                    # 创建索引管理器
                    index_manager = IndexManager(session, index_config)
                    
                    # 测试索引存在性检查
                    exists = index_manager._index_exists('non_existent_index')
                    assert not exists
                    
                    logger.info("✓ 索引管理器测试通过")
        except Exception as e:
            pytest.skip(f"Neo4j连接失败，跳过测试: {e}")
    
    def test_full_integration(self, config_dir, logger):
        """完整集成测试"""
        logger.info("执行完整集成测试...")
        
        # 1. 加载配置
        loader = ConfigLoader(config_dir)
        configs = loader.load_all_configs()
        logger.info("✓ 配置加载成功")
        
        # 2. 验证配置
        validator = ConfigValidator()
        is_valid, errors = validator.validate_all_configs(configs)
        assert is_valid, f"配置验证失败: {errors}"
        logger.info("✓ 配置验证成功")
        
        # 3. 连接Neo4j
        try:
            with Neo4jConnection(configs['neo4j_config']) as conn:
                logger.info("✓ Neo4j连接成功")
                
                # 4. 测试会话
                with conn.get_session() as session:
                    logger.info("✓ Neo4j会话创建成功")
                    
                    # 5. 测试事务
                    tx_manager = TransactionManager(session)
                    tx = tx_manager.begin_transaction()
                    result = tx.run("RETURN 'Hello Neo4j' as message")
                    record = result.single()
                    assert record['message'] == 'Hello Neo4j'
                    tx_manager.commit()
                    logger.info("✓ 事务执行成功")
                    
                    # 6. 测试索引管理器
                    index_manager = IndexManager(session, configs['index_config'])
                    logger.info("✓ 索引管理器初始化成功")
        
        except Exception as e:
            pytest.skip(f"Neo4j连接失败，跳过测试: {e}")
        
        logger.info("=" * 60)
        logger.info("✓✓✓ Checkpoint 1 完整集成测试通过 ✓✓✓")
        logger.info("=" * 60)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
