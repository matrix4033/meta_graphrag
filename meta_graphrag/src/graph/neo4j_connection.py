"""Neo4j数据库连接管理"""
from neo4j import GraphDatabase, Driver, Session
from typing import Dict, Any, Optional
from utils.error_codes import ErrorCode, ErrorMessage
from utils.logger import get_logger

logger = get_logger(__name__)


class Neo4jConnection:
    """Neo4j数据库连接管理器"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化Neo4j连接
        
        Args:
            config: Neo4j配置字典
        
        Raises:
            Exception: 连接失败时抛出异常
        """
        self.config = config.get('neo4j', {})
        self.uri = self.config.get('uri')
        self.username = self.config.get('username')
        self.password = self.config.get('password')
        self.database = self.config.get('database', 'neo4j')
        
        self.driver: Optional[Driver] = None
        self._connect()
    
    def _connect(self):
        """建立数据库连接"""
        try:
            logger.info(f"正在连接Neo4j数据库: {self.uri}")
            
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password),
                max_connection_lifetime=self.config.get('max_connection_lifetime', 3600),
                max_connection_pool_size=self.config.get('max_connection_pool_size', 50),
                connection_timeout=self.config.get('connection_timeout', 30)
            )
            
            # 验证连接
            self.driver.verify_connectivity()
            logger.info("Neo4j数据库连接成功")
            
        except Exception as e:
            error_msg = ErrorMessage.get_message(
                ErrorCode.DB_CONNECTION_ERROR,
                uri=self.uri,
                error=str(e)
            )
            logger.critical(error_msg)
            raise Exception(error_msg)
    
    def get_session(self) -> Session:
        """
        获取数据库会话
        
        Returns:
            Neo4j会话对象
        """
        if not self.driver:
            raise Exception("数据库连接未建立")
        
        return self.driver.session(database=self.database)
    
    def close(self):
        """关闭数据库连接"""
        if self.driver:
            logger.info("正在关闭Neo4j数据库连接")
            self.driver.close()
            self.driver = None
            logger.info("Neo4j数据库连接已关闭")
    
    def verify_connection(self) -> bool:
        """
        验证数据库连接是否正常
        
        Returns:
            连接是否正常
        """
        try:
            if not self.driver:
                return False
            
            self.driver.verify_connectivity()
            return True
        except Exception as e:
            logger.error(f"数据库连接验证失败: {e}")
            return False
    
    def clear_database(self):
        """清空数据库（删除所有节点和关系）"""
        try:
            logger.warning("正在清空Neo4j数据库...")
            with self.get_session() as session:
                # 删除所有节点和关系
                session.run("MATCH (n) DETACH DELETE n")
                logger.info("数据库已清空")
        except Exception as e:
            error_msg = ErrorMessage.get_message(
                ErrorCode.DB_QUERY_ERROR,
                query="MATCH (n) DETACH DELETE n",
                error=str(e)
            )
            logger.error(error_msg)
            raise Exception(error_msg)
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
