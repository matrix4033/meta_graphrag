"""配置验证器"""
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
from .error_codes import ErrorCode, ErrorMessage
from .logger import get_logger

logger = get_logger(__name__)


class ConfigValidator:
    """配置验证器 - 验证配置文件的正确性"""
    
    def validate_all_configs(self, configs: Dict[str, Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """
        验证所有配置文件
        
        Args:
            configs: 包含所有配置的字典
        
        Returns:
            (是否有效, 错误消息列表)
        """
        errors = []
        
        # 验证Neo4j配置
        if 'neo4j_config' in configs:
            neo4j_errors = self.validate_neo4j_config(configs['neo4j_config'])
            errors.extend(neo4j_errors)
        else:
            errors.append("缺少Neo4j配置")
        
        # 验证解析器配置
        if 'parser_config' in configs:
            parser_errors = self.validate_parser_config(configs['parser_config'])
            errors.extend(parser_errors)
        else:
            errors.append("缺少解析器配置")
        
        # 验证Excel配置
        if 'excel_config' in configs:
            excel_errors = self.validate_excel_config(configs['excel_config'])
            errors.extend(excel_errors)
        else:
            errors.append("缺少Excel配置")
        
        # 验证索引配置
        if 'index_config' in configs:
            index_errors = self.validate_index_config(configs['index_config'])
            errors.extend(index_errors)
        else:
            errors.append("缺少索引配置")
        
        # 验证MCP配置
        if 'mcp_config' in configs:
            mcp_errors = self.validate_mcp_config(configs['mcp_config'])
            errors.extend(mcp_errors)
        else:
            errors.append("缺少MCP配置")
        
        is_valid = len(errors) == 0
        if is_valid:
            logger.info("所有配置验证通过")
        else:
            logger.error(f"配置验证失败，发现 {len(errors)} 个错误")
            for error in errors:
                logger.error(f"  - {error}")
        
        return is_valid, errors
    
    def validate_neo4j_config(self, config: Dict[str, Any]) -> List[str]:
        """验证Neo4j配置"""
        errors = []
        
        neo4j_config = config.get('neo4j', {})
        
        # 检查必需字段
        required_fields = ['uri', 'username', 'password']
        for field in required_fields:
            if field not in neo4j_config or not neo4j_config[field]:
                errors.append(f"Neo4j配置缺少必需字段: {field}")
        
        # 验证URI格式
        uri = neo4j_config.get('uri', '')
        if uri and not uri.startswith(('bolt://', 'neo4j://', 'bolt+s://', 'neo4j+s://')):
            errors.append(f"Neo4j URI格式错误: {uri}，应以 bolt:// 或 neo4j:// 开头")
        
        # 验证数值类型字段
        numeric_fields = {
            'max_connection_lifetime': (0, 86400),
            'max_connection_pool_size': (1, 1000),
            'connection_timeout': (1, 300)
        }
        
        for field, (min_val, max_val) in numeric_fields.items():
            if field in neo4j_config:
                value = neo4j_config[field]
                if not isinstance(value, (int, float)):
                    errors.append(f"Neo4j配置 {field} 必须是数值类型")
                elif not (min_val <= value <= max_val):
                    errors.append(f"Neo4j配置 {field} 必须在 {min_val} 到 {max_val} 之间")
        
        return errors
    
    def validate_parser_config(self, config: Dict[str, Any]) -> List[str]:
        """验证解析器配置"""
        errors = []
        
        # 验证文件名正则表达式
        filename_pattern = config.get('filename_pattern', {}).get('regex')
        if filename_pattern:
            try:
                re.compile(filename_pattern)
            except re.error as e:
                errors.append(f"文件名正则表达式无效: {str(e)}")
        else:
            errors.append("缺少文件名解析正则表达式")
        
        # 验证路径正则表达式
        path_pattern = config.get('path_pattern', {}).get('regex')
        if path_pattern:
            try:
                re.compile(path_pattern)
            except re.error as e:
                errors.append(f"路径正则表达式无效: {str(e)}")
        else:
            errors.append("缺少路径解析正则表达式")
        
        # 验证主题域映射
        mapping = config.get('subject_domain_to_database', {})
        if not isinstance(mapping, dict):
            errors.append("主题域到数据库映射必须是字典类型")
        elif len(mapping) == 0:
            errors.append("主题域到数据库映射不能为空")
        
        # 验证默认分类值
        default_classification = config.get('default_classification', {})
        required_defaults = ['subject_domain', 'business_domain', 'business_subject', 'logical_entity']
        for field in required_defaults:
            if field not in default_classification:
                errors.append(f"缺少默认分类值: {field}")
        
        return errors
    
    def validate_excel_config(self, config: Dict[str, Any]) -> List[str]:
        """验证Excel配置"""
        errors = []
        
        # 验证列名映射
        column_mapping = config.get('column_mapping', {})
        if not isinstance(column_mapping, dict):
            errors.append("列名映射必须是字典类型")
        else:
            required_columns = ['logical_entity', 'table_name', 'field_name', 
                              'business_term', 'data_source_unit', 'data_standard']
            for column in required_columns:
                if column not in column_mapping:
                    errors.append(f"缺少列名映射: {column}")
                elif 'patterns' not in column_mapping[column]:
                    errors.append(f"列名映射 {column} 缺少 patterns 字段")
                elif not isinstance(column_mapping[column]['patterns'], list):
                    errors.append(f"列名映射 {column} 的 patterns 必须是列表类型")
        
        # 验证编码顺序
        encoding_order = config.get('encoding_order', [])
        if not isinstance(encoding_order, list):
            errors.append("编码顺序必须是列表类型")
        elif len(encoding_order) == 0:
            errors.append("编码顺序不能为空")
        
        return errors
    
    def validate_index_config(self, config: Dict[str, Any]) -> List[str]:
        """验证索引配置"""
        errors = []
        
        indexes = config.get('indexes', {})
        
        # 验证唯一索引
        unique_indexes = indexes.get('unique_indexes', [])
        if not isinstance(unique_indexes, list):
            errors.append("唯一索引配置必须是列表类型")
        else:
            for idx, index in enumerate(unique_indexes):
                if 'node_label' not in index:
                    errors.append(f"唯一索引 {idx} 缺少 node_label 字段")
                if 'property' not in index:
                    errors.append(f"唯一索引 {idx} 缺少 property 字段")
        
        # 验证普通索引
        regular_indexes = indexes.get('regular_indexes', [])
        if not isinstance(regular_indexes, list):
            errors.append("普通索引配置必须是列表类型")
        else:
            for idx, index in enumerate(regular_indexes):
                if 'node_label' not in index:
                    errors.append(f"普通索引 {idx} 缺少 node_label 字段")
                if 'property' not in index:
                    errors.append(f"普通索引 {idx} 缺少 property 字段")
        
        # 验证全文索引
        fulltext_indexes = indexes.get('fulltext_indexes', [])
        if not isinstance(fulltext_indexes, list):
            errors.append("全文索引配置必须是列表类型")
        else:
            for idx, index in enumerate(fulltext_indexes):
                if 'name' not in index:
                    errors.append(f"全文索引 {idx} 缺少 name 字段")
                if 'node_label' not in index:
                    errors.append(f"全文索引 {idx} 缺少 node_label 字段")
                if 'properties' not in index:
                    errors.append(f"全文索引 {idx} 缺少 properties 字段")
                elif not isinstance(index['properties'], list):
                    errors.append(f"全文索引 {idx} 的 properties 必须是列表类型")
        
        return errors
    
    def validate_mcp_config(self, config: Dict[str, Any]) -> List[str]:
        """验证MCP配置"""
        errors = []
        
        mcp_config = config.get('mcp', {})
        
        # 验证数值配置
        numeric_fields = {
            'max_results': (1, 10000),
            'default_page_size': (1, 1000),
            'max_path_depth': (1, 20),
            'max_paths': (1, 1000)
        }
        
        for field, (min_val, max_val) in numeric_fields.items():
            if field in mcp_config:
                value = mcp_config[field]
                if not isinstance(value, int):
                    errors.append(f"MCP配置 {field} 必须是整数类型")
                elif not (min_val <= value <= max_val):
                    errors.append(f"MCP配置 {field} 必须在 {min_val} 到 {max_val} 之间")
        
        # 验证启用的工具列表
        enabled_tools = mcp_config.get('enabled_tools', [])
        if not isinstance(enabled_tools, list):
            errors.append("启用的工具列表必须是列表类型")
        elif len(enabled_tools) == 0:
            errors.append("启用的工具列表不能为空")
        
        return errors
