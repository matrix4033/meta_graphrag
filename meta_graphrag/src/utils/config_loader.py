"""配置加载器"""
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from .error_codes import ErrorCode, ErrorMessage
from .logger import get_logger

logger = get_logger(__name__)


class ConfigLoader:
    """配置加载器 - 读取YAML配置文件"""
    
    def __init__(self, config_dir: Path):
        """
        初始化配置加载器
        
        Args:
            config_dir: 配置文件目录路径
        """
        self.config_dir = Path(config_dir)
        if not self.config_dir.exists():
            raise FileNotFoundError(
                ErrorMessage.get_message(
                    ErrorCode.CONFIG_FILE_NOT_FOUND,
                    file_path=str(self.config_dir)
                )
            )
    
    def load_config(self, config_name: str) -> Dict[str, Any]:
        """
        加载指定的配置文件
        
        Args:
            config_name: 配置文件名（不含扩展名）
        
        Returns:
            配置字典
        
        Raises:
            FileNotFoundError: 配置文件不存在
            yaml.YAMLError: 配置文件格式错误
        """
        config_path = self.config_dir / f"{config_name}.yaml"
        
        if not config_path.exists():
            error_msg = ErrorMessage.get_message(
                ErrorCode.CONFIG_FILE_NOT_FOUND,
                file_path=str(config_path)
            )
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                logger.debug(f"成功加载配置文件: {config_path}")
                return config if config is not None else {}
        except yaml.YAMLError as e:
            error_msg = ErrorMessage.get_message(
                ErrorCode.CONFIG_FORMAT_ERROR,
                file_path=str(config_path),
                error=str(e)
            )
            logger.error(error_msg)
            raise yaml.YAMLError(error_msg)
        except Exception as e:
            error_msg = ErrorMessage.get_message(
                ErrorCode.CONFIG_FORMAT_ERROR,
                file_path=str(config_path),
                error=str(e)
            )
            logger.error(error_msg)
            raise
    
    def load_neo4j_config(self) -> Dict[str, Any]:
        """加载Neo4j配置"""
        return self.load_config('neo4j_config')
    
    def load_parser_config(self) -> Dict[str, Any]:
        """加载解析器配置"""
        return self.load_config('parser_config')
    
    def load_excel_config(self) -> Dict[str, Any]:
        """加载Excel配置"""
        return self.load_config('excel_config')
    
    def load_index_config(self) -> Dict[str, Any]:
        """加载索引配置"""
        return self.load_config('index_config')
    
    def load_mcp_config(self) -> Dict[str, Any]:
        """加载MCP配置"""
        return self.load_config('mcp_config')
    
    def load_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        加载所有配置文件
        
        Returns:
            包含所有配置的字典
        """
        configs = {}
        config_names = ['neo4j_config', 'parser_config', 'excel_config', 'index_config', 'mcp_config']
        
        for config_name in config_names:
            try:
                configs[config_name] = self.load_config(config_name)
            except Exception as e:
                logger.error(f"加载配置 {config_name} 失败: {e}")
                raise
        
        logger.info("所有配置文件加载成功")
        return configs
