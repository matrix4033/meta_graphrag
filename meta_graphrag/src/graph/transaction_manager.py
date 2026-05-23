"""事务管理器"""
from neo4j import Session, Transaction
from typing import Any, Callable, Optional, List, Dict
from utils.error_codes import ErrorCode, ErrorMessage
from utils.logger import get_logger

logger = get_logger(__name__)


class TransactionManager:
    """事务管理器 - 管理Neo4j事务的开启、提交和回滚"""
    
    def __init__(self, session: Session):
        """
        初始化事务管理器
        
        Args:
            session: Neo4j会话对象
        """
        self.session = session
        self.transaction: Optional[Transaction] = None
    
    def begin_transaction(self) -> Transaction:
        """
        开启事务
        
        Returns:
            事务对象
        """
        if self.transaction:
            logger.warning("事务已存在，将先提交当前事务")
            self.commit()
        
        logger.debug("开启新事务")
        self.transaction = self.session.begin_transaction()
        return self.transaction
    
    def commit(self):
        """提交事务"""
        if not self.transaction:
            logger.warning("没有活动的事务可提交")
            return
        
        try:
            logger.debug("提交事务")
            self.transaction.commit()
            self.transaction = None
            logger.debug("事务提交成功")
        except Exception as e:
            error_msg = ErrorMessage.get_message(
                ErrorCode.DB_TRANSACTION_ERROR,
                error=str(e)
            )
            logger.error(error_msg)
            self.rollback()
            raise Exception(error_msg)
    
    def rollback(self):
        """回滚事务"""
        if not self.transaction:
            logger.warning("没有活动的事务可回滚")
            return
        
        try:
            logger.warning("回滚事务")
            self.transaction.rollback()
            self.transaction = None
            logger.info("事务已回滚")
        except Exception as e:
            logger.error(f"事务回滚失败: {e}")
            self.transaction = None
    
    def execute_in_transaction(
        self,
        func: Callable[[Transaction], Any],
        auto_commit: bool = True
    ) -> Any:
        """
        在事务中执行函数
        
        Args:
            func: 要执行的函数，接收Transaction对象作为参数
            auto_commit: 是否自动提交事务
        
        Returns:
            函数执行结果
        """
        tx = self.begin_transaction()
        try:
            result = func(tx)
            if auto_commit:
                self.commit()
            return result
        except Exception as e:
            logger.error(f"事务执行失败: {e}")
            self.rollback()
            raise
    
    def batch_execute(
        self,
        query: str,
        parameters_list: List[Dict[str, Any]],
        batch_size: int = 1000
    ) -> int:
        """
        批量执行查询
        
        Args:
            query: Cypher查询语句
            parameters_list: 参数列表
            batch_size: 批次大小
        
        Returns:
            执行的总记录数
        """
        total_count = 0
        total_batches = (len(parameters_list) + batch_size - 1) // batch_size
        
        logger.info(f"开始批量执行，总记录数: {len(parameters_list)}, 批次大小: {batch_size}, 总批次: {total_batches}")
        
        for i in range(0, len(parameters_list), batch_size):
            batch = parameters_list[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            try:
                tx = self.begin_transaction()
                
                # 使用UNWIND批量执行
                batch_query = f"""
                UNWIND $batch AS params
                {query}
                """
                
                result = tx.run(batch_query, batch=batch)
                summary = result.consume()
                
                self.commit()
                
                batch_count = len(batch)
                total_count += batch_count
                
                logger.info(f"批次 {batch_num}/{total_batches} 执行成功，处理 {batch_count} 条记录")
                
            except Exception as e:
                logger.error(f"批次 {batch_num} 执行失败: {e}")
                self.rollback()
                raise
        
        logger.info(f"批量执行完成，总共处理 {total_count} 条记录")
        return total_count
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if exc_type is not None:
            # 发生异常时回滚
            self.rollback()
        elif self.transaction:
            # 正常退出时提交
            self.commit()
