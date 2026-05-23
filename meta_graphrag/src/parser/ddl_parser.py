"""DDL解析器 - 解析CREATE TABLE语句"""
import re
import sqlparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from utils.logger import setup_logger


class DDLParser:
    """DDL语句解析器"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化DDL解析器
        
        Args:
            config: 解析器配置
        """
        self.config = config
        self.logger = setup_logger('ddl_parser')
        
        # 获取主题域到数据库的映射
        self.subject_domain_to_database = config.get('subject_domain_to_database', {})
    
    def parse_file_path(self, file_path: Path) -> Dict[str, str]:
        """
        解析文件路径提取主题域
        
        Args:
            file_path: SQL文件路径
            
        Returns:
            包含主题域信息的字典
        """
        # 从路径中提取主题域 (ddls/ZRR/xxx.sql -> ZRR)
        parts = file_path.parts
        if len(parts) >= 2 and parts[0] == 'ddls':
            subject_domain_code = parts[1]
            
            # 根据代码查找主题域名称
            for domain_name, db_code in self.subject_domain_to_database.items():
                if db_code.upper() == subject_domain_code.upper():
                    return {
                        'subject_domain': domain_name,
                        'database': db_code.lower()
                    }
            
            # 如果没找到映射，使用默认值
            return {
                'subject_domain': subject_domain_code,
                'database': subject_domain_code.lower()
            }
        
        # 使用默认值
        return {
            'subject_domain': self.config.get('default_classification', {}).get('subject_domain', '未分类主题域'),
            'database': 'unknown'
        }
    
    def parse_file_name(self, file_name: str) -> Dict[str, str]:
        """
        解析文件名提取业务分类信息
        
        文件名格式: 编号-业务域-业务主题-逻辑名称.sql
        例如: 5.3.1.1_1-基本信息-登记信息-基本登记信息.sql
        
        Args:
            file_name: SQL文件名
            
        Returns:
            包含业务分类信息的字典
        """
        # 移除.sql扩展名
        name_without_ext = file_name.replace('.sql', '')
        
        # 使用正则表达式解析
        # 格式: 编号-业务域-业务主题-逻辑名称
        pattern = r'^([^-]+)-([^-]+)-([^-]+)-(.+)$'
        match = re.match(pattern, name_without_ext)
        
        if match:
            code = match.group(1)
            business_domain = match.group(2)
            business_subject = match.group(3)
            logical_entity = match.group(4)
            
            return {
                'code': code,
                'business_domain': business_domain,
                'business_subject': business_subject,
                'logical_entity': logical_entity
            }
        else:
            self.logger.warning(f"文件名格式不符合规范: {file_name}, 使用默认分类")
            defaults = self.config.get('default_classification', {})
            return {
                'code': 'UNKNOWN',
                'business_domain': defaults.get('business_domain', '未分类业务域'),
                'business_subject': defaults.get('business_subject', '未分类业务主题'),
                'logical_entity': defaults.get('logical_entity', '未分类逻辑实体')
            }
    
    def parse_ddl(self, sql_content: str) -> Dict[str, Any]:
        """
        解析DDL语句
        
        Args:
            sql_content: SQL文件内容
            
        Returns:
            包含表和字段信息的字典
        """
        tables = []
        
        # 使用sqlparse解析SQL
        statements = sqlparse.parse(sql_content)
        
        current_table = None
        
        for statement in statements:
            # 处理CREATE TABLE语句
            if statement.get_type() == 'CREATE':
                table_info = self._parse_create_table(statement)
                if table_info:
                    current_table = table_info
                    tables.append(current_table)
            
            # 处理COMMENT语句
            elif 'COMMENT' in statement.value.upper():
                if current_table:
                    self._parse_comment(statement, current_table)
        
        return {'tables': tables}
    
    def _parse_create_table(self, statement) -> Optional[Dict[str, Any]]:
        """解析CREATE TABLE语句"""
        sql = statement.value
        
        # 提取表名
        table_name_match = re.search(r'CREATE\s+TABLE\s+(\w+)', sql, re.IGNORECASE)
        if not table_name_match:
            return None
        
        table_name = table_name_match.group(1)
        
        # 提取字段定义
        fields = []
        
        # 查找括号内的内容（使用非贪婪匹配）
        paren_match = re.search(r'\((.*?)\);', sql, re.DOTALL)
        if not paren_match:
            # 如果没有分号，尝试匹配到最后一个括号
            paren_match = re.search(r'\((.*)\)', sql, re.DOTALL)
        
        if paren_match:
            fields_text = paren_match.group(1)
            
            # 分割字段定义 - 按逗号和换行符分割
            # 先按换行符分割，然后处理每一行
            lines = fields_text.split('\n')
            current_field = ''
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 如果行以逗号结尾，这是一个完整的字段定义
                if line.endswith(','):
                    current_field += line[:-1].strip()  # 移除逗号
                    if current_field and not current_field.upper().startswith('PRIMARY') and not current_field.upper().startswith('FOREIGN'):
                        field_info = self._parse_field_definition(current_field)
                        if field_info:
                            fields.append(field_info)
                    current_field = ''
                else:
                    # 继续累积当前字段
                    if current_field:
                        current_field += ' ' + line
                    else:
                        current_field = line
            
            # 处理最后一个字段（没有逗号）
            if current_field and not current_field.upper().startswith('PRIMARY') and not current_field.upper().startswith('FOREIGN'):
                field_info = self._parse_field_definition(current_field)
                if field_info:
                    fields.append(field_info)
        
        return {
            'table_name': table_name,
            'comment': None,
            'fields': fields
        }
    
    def _parse_field_definition(self, field_def: str) -> Optional[Dict[str, Any]]:
        """解析字段定义"""
        # 字段格式: field_name TYPE(length) [NOT NULL]
        parts = field_def.split()
        if len(parts) < 2:
            return None
        
        field_name = parts[0]
        data_type_part = parts[1]
        
        # 解析数据类型和长度
        type_match = re.match(r'(\w+)(?:\((\d+)\))?', data_type_part)
        if not type_match:
            return None
        
        data_type = type_match.group(1)
        length = int(type_match.group(2)) if type_match.group(2) else None
        
        # 检查是否有NOT NULL
        nullable = 'NOT NULL' not in field_def.upper()
        
        return {
            'name': field_name,
            'data_type': data_type,
            'length': length,
            'nullable': nullable,
            'comment': None
        }
    
    def _parse_comment(self, statement, table_info: Dict[str, Any]):
        """解析COMMENT语句"""
        sql = statement.value
        
        # COMMENT ON TABLE
        table_comment_match = re.search(
            r"COMMENT\s+ON\s+TABLE\s+(\w+)\s+IS\s+'([^']*)'",
            sql,
            re.IGNORECASE
        )
        if table_comment_match:
            table_info['comment'] = table_comment_match.group(2)
            return
        
        # COMMENT ON COLUMN
        column_comment_match = re.search(
            r"COMMENT\s+ON\s+COLUMN\s+\w+\.(\w+)\s+IS\s+'([^']*)'",
            sql,
            re.IGNORECASE
        )
        if column_comment_match:
            field_name = column_comment_match.group(1)
            comment = column_comment_match.group(2)
            
            # 找到对应的字段并设置注释
            for field in table_info['fields']:
                if field['name'] == field_name:
                    field['comment'] = comment
                    break
    
    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """
        解析单个DDL文件
        
        Args:
            file_path: SQL文件路径
            
        Returns:
            包含完整元数据的字典
        """
        try:
            # 解析路径和文件名
            path_info = self.parse_file_path(file_path)
            name_info = self.parse_file_name(file_path.name)
            
            # 读取文件内容，尝试多种编码
            content = None
            encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030']
            for encoding in encodings:
                try:
                    content = file_path.read_text(encoding=encoding)
                    break
                except (UnicodeDecodeError, LookupError):
                    continue
            
            if content is None:
                # 如果所有编码都失败，使用 utf-8 with errors='ignore'
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                self.logger.warning(f"文件 {file_path} 使用 UTF-8 编码但有字符被忽略")
            
            # 解析DDL
            ddl_info = self.parse_ddl(content)
            
            # 为每个表添加完整的DDL语句
            for table in ddl_info.get('tables', []):
                table['ddl_statement'] = content
            
            # 合并所有信息
            result = {
                'file_path': str(file_path),
                **path_info,
                **name_info,
                **ddl_info
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"解析文件失败: {file_path}, 错误: {e}")
            return None
