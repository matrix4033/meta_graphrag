"""索引管理器"""
from neo4j import Session
from typing import Dict, Any, List
from utils.error_codes import ErrorCode, ErrorMessage
from utils.logger import get_logger

logger = get_logger(__name__)


class IndexManager:
    """索引管理器 - 管理Neo4j索引的创建"""
    
    def __init__(self, session: Session, config: Dict[str, Any]):
        """
        初始化索引管理器
        
        Args:
            session: Neo4j会话对象
            config: 索引配置字典
        """
        self.session = session
        self.config = config.get('indexes', {})
    
    def create_all_indexes(self):
        """创建所有配置的索引"""
        logger.info("开始创建索引...")
        
        # 创建唯一索引
        unique_indexes = self.config.get('unique_indexes', [])
        for index_config in unique_indexes:
            self.create_unique_index(
                index_config['node_label'],
                index_config['property']
            )
        
        # 创建普通索引
        regular_indexes = self.config.get('regular_indexes', [])
        for index_config in regular_indexes:
            self.create_regular_index(
                index_config['node_label'],
                index_config['property']
            )
        
        # 创建全文索引
        fulltext_indexes = self.config.get('fulltext_indexes', [])
        for index_config in fulltext_indexes:
            self.create_fulltext_index(
                index_config['name'],
                index_config['node_label'],
                index_config['properties']
            )
        
        logger.info("所有索引创建完成")
    
    def create_unique_index(self, node_label: str, property_name: str):
        """
        创建唯一索引
        
        Args:
            node_label: 节点标签
            property_name: 属性名
        """
        index_name = f"unique_{node_label.lower()}_{property_name}"
        
        try:
            # 检查索引是否已存在
            if self._index_exists(index_name):
                logger.debug(f"唯一索引已存在: {index_name}")
                return
            
            query = f"""
            CREATE CONSTRAINT {index_name}
            FOR (n:{node_label})
            REQUIRE n.{property_name} IS UNIQUE
            """
            
            logger.debug(f"创建唯一索引: {index_name}")
            self.session.run(query)
            logger.info(f"唯一索引创建成功: {node_label}.{property_name}")
            
        except Exception as e:
            error_msg = ErrorMessage.get_message(
                ErrorCode.INDEX_CREATION_ERROR,
                index_name=index_name,
                error=str(e)
            )
            logger.error(error_msg)
            # 不抛出异常，继续创建其他索引
    
    def create_regular_index(self, node_label: str, property_name: str):
        """
        创建普通索引
        
        Args:
            node_label: 节点标签
            property_name: 属性名
        """
        index_name = f"index_{node_label.lower()}_{property_name}"
        
        try:
            # 检查索引是否已存在
            if self._index_exists(index_name):
                logger.debug(f"普通索引已存在: {index_name}")
                return
            
            query = f"""
            CREATE INDEX {index_name}
            FOR (n:{node_label})
            ON (n.{property_name})
            """
            
            logger.debug(f"创建普通索引: {index_name}")
            self.session.run(query)
            logger.info(f"普通索引创建成功: {node_label}.{property_name}")
            
        except Exception as e:
            error_msg = ErrorMessage.get_message(
                ErrorCode.INDEX_CREATION_ERROR,
                index_name=index_name,
                error=str(e)
            )
            logger.error(error_msg)
            # 不抛出异常，继续创建其他索引
    
    def create_fulltext_index(
        self,
        index_name: str,
        node_label: str,
        properties: List[str]
    ):
        """
        创建全文索引
        
        Args:
            index_name: 索引名称
            node_label: 节点标签
            properties: 属性列表
        """
        try:
            # 检查索引是否已存在
            if self._index_exists(index_name):
                logger.debug(f"全文索引已存在: {index_name}")
                return
            
            properties_str = ', '.join([f'n.{prop}' for prop in properties])
            
            query = f"""
            CREATE FULLTEXT INDEX {index_name}
            FOR (n:{node_label})
            ON EACH [{properties_str}]
            """
            
            logger.debug(f"创建全文索引: {index_name}")
            self.session.run(query)
            logger.info(f"全文索引创建成功: {index_name} on {node_label}[{', '.join(properties)}]")
            
        except Exception as e:
            error_msg = ErrorMessage.get_message(
                ErrorCode.INDEX_CREATION_ERROR,
                index_name=index_name,
                error=str(e)
            )
            logger.error(error_msg)
            # 不抛出异常，继续创建其他索引
    
    def _index_exists(self, index_name: str) -> bool:
        """
        检查索引是否存在
        
        Args:
            index_name: 索引名称
        
        Returns:
            索引是否存在
        """
        try:
            query = "SHOW INDEXES"
            result = self.session.run(query)
            
            for record in result:
                if record.get('name') == index_name:
                    return True
            
            return False
        except Exception as e:
            logger.warning(f"检查索引是否存在时出错: {e}")
            return False
    
    def drop_all_indexes(self):
        """删除所有索引（用于测试）"""
        try:
            logger.warning("正在删除所有索引...")
            
            # 获取所有索引
            result = self.session.run("SHOW INDEXES")
            indexes = [record['name'] for record in result]
            
            # 删除每个索引
            for index_name in indexes:
                try:
                    self.session.run(f"DROP INDEX {index_name} IF EXISTS")
                    logger.debug(f"删除索引: {index_name}")
                except Exception as e:
                    logger.warning(f"删除索引 {index_name} 失败: {e}")
            
            logger.info("所有索引已删除")
            
        except Exception as e:
            logger.error(f"删除索引时出错: {e}")
