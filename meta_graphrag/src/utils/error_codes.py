"""错误码和错误消息定义"""


class ErrorCode:
    """错误码定义"""
    
    # 配置错误 (1xxx)
    CONFIG_FILE_NOT_FOUND = 1001
    CONFIG_FORMAT_ERROR = 1002
    CONFIG_VALIDATION_ERROR = 1003
    
    # 文件解析错误 (2xxx)
    FILE_NOT_FOUND = 2001
    FILE_ENCODING_ERROR = 2002
    FILE_FORMAT_ERROR = 2003
    DDL_PARSE_ERROR = 2004
    EXCEL_PARSE_ERROR = 2005
    
    # 数据库错误 (3xxx)
    DB_CONNECTION_ERROR = 3001
    DB_TRANSACTION_ERROR = 3002
    DB_QUERY_ERROR = 3003
    DB_CONSTRAINT_ERROR = 3004
    
    # 图谱构建错误 (4xxx)
    NODE_CREATION_ERROR = 4001
    RELATIONSHIP_CREATION_ERROR = 4002
    INDEX_CREATION_ERROR = 4003
    DATA_VALIDATION_ERROR = 4004
    
    # MCP服务器错误 (5xxx)
    MCP_INIT_ERROR = 5001
    MCP_TOOL_ERROR = 5002
    MCP_REQUEST_ERROR = 5003
    MCP_RESPONSE_ERROR = 5004


class ErrorMessage:
    """错误消息模板"""
    
    MESSAGES = {
        ErrorCode.CONFIG_FILE_NOT_FOUND: "配置文件未找到: {file_path}",
        ErrorCode.CONFIG_FORMAT_ERROR: "配置文件格式错误: {file_path}, 错误: {error}",
        ErrorCode.CONFIG_VALIDATION_ERROR: "配置验证失败: {errors}",
        ErrorCode.FILE_NOT_FOUND: "文件未找到: {file_path}",
        ErrorCode.FILE_ENCODING_ERROR: "文件编码错误: {file_path}, 尝试的编码: {encodings}",
        ErrorCode.FILE_FORMAT_ERROR: "文件格式错误: {file_path}, 错误: {error}",
        ErrorCode.DDL_PARSE_ERROR: "DDL解析错误: {file_path}, 错误: {error}",
        ErrorCode.EXCEL_PARSE_ERROR: "Excel解析错误: {file_path}, 错误: {error}",
        ErrorCode.DB_CONNECTION_ERROR: "数据库连接失败: {uri}, 错误: {error}",
        ErrorCode.DB_TRANSACTION_ERROR: "事务执行失败: {error}",
        ErrorCode.DB_QUERY_ERROR: "查询执行失败: {query}, 错误: {error}",
        ErrorCode.DB_CONSTRAINT_ERROR: "约束违反: {error}",
        ErrorCode.NODE_CREATION_ERROR: "节点创建失败: {node_data}, 错误: {error}",
        ErrorCode.RELATIONSHIP_CREATION_ERROR: "关系创建失败: {rel_data}, 错误: {error}",
        ErrorCode.INDEX_CREATION_ERROR: "索引创建失败: {index_name}, 错误: {error}",
        ErrorCode.DATA_VALIDATION_ERROR: "数据验证失败: {error}",
        ErrorCode.MCP_INIT_ERROR: "MCP服务器初始化失败: {error}",
        ErrorCode.MCP_TOOL_ERROR: "MCP工具执行失败: {tool_name}, 错误: {error}",
        ErrorCode.MCP_REQUEST_ERROR: "MCP请求处理失败: {error}",
        ErrorCode.MCP_RESPONSE_ERROR: "MCP响应生成失败: {error}",
    }
    
    @staticmethod
    def get_message(error_code: int, **kwargs) -> str:
        """获取格式化的错误消息"""
        template = ErrorMessage.MESSAGES.get(error_code, "未知错误: {error}")
        try:
            return template.format(**kwargs)
        except KeyError:
            return f"错误码 {error_code}: {kwargs}"
