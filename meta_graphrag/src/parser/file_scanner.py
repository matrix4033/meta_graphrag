"""文件扫描器 - 扫描DDL和Excel文件"""
from pathlib import Path
from typing import List
from utils.logger import setup_logger


class FileScanner:
    """文件扫描器"""
    
    def __init__(self):
        """初始化文件扫描器"""
        self.logger = setup_logger('file_scanner')
    
    def scan_sql_files(self, ddls_path: str) -> List[Path]:
        """
        递归扫描SQL文件
        
        Args:
            ddls_path: DDL文件目录路径
            
        Returns:
            SQL文件路径列表
        """
        path = Path(ddls_path)
        if not path.exists():
            self.logger.error(f"DDL目录不存在: {ddls_path}")
            return []
        
        # 递归查找所有.sql文件
        sql_files = list(path.rglob('*.sql'))
        
        self.logger.info(f"在 {ddls_path} 中找到 {len(sql_files)} 个SQL文件")
        return sql_files
    
    def scan_excel_files(self, metadata_path: str) -> List[Path]:
        """
        扫描Excel文件
        
        Args:
            metadata_path: 元数据文件目录路径
            
        Returns:
            Excel文件路径列表
        """
        path = Path(metadata_path)
        if not path.exists():
            self.logger.error(f"元数据目录不存在: {metadata_path}")
            return []
        
        # 查找所有.xlsx和.xls文件
        excel_files = list(path.glob('*.xlsx')) + list(path.glob('*.xls'))
        
        self.logger.info(f"在 {metadata_path} 中找到 {len(excel_files)} 个Excel文件")
        return excel_files
