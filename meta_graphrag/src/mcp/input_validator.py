"""MCP输入验证器"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


# 错误代码常量
INVALID_PARAM_TYPE = "INVALID_PARAM_TYPE"
MISSING_REQUIRED_PARAM = "MISSING_REQUIRED_PARAM"
PARAM_OUT_OF_RANGE = "PARAM_OUT_OF_RANGE"
NODE_NOT_FOUND = "NODE_NOT_FOUND"


@dataclass
class ValidationError:
    """验证错误"""
    code: str
    message: str
    parameter: Optional[str] = None
    expected: Optional[Any] = None
    actual: Optional[Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        result = {
            'code': self.code,
            'message': self.message
        }
        if self.parameter:
            result['parameter'] = self.parameter
        if self.expected is not None:
            result['expected'] = self.expected
        if self.actual is not None:
            result['actual'] = self.actual
        return result


@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    errors: List[ValidationError]
    
    @staticmethod
    def success() -> 'ValidationResult':
        """创建成功的验证结果"""
        return ValidationResult(is_valid=True, errors=[])
    
    @staticmethod
    def failure(errors: List[ValidationError]) -> 'ValidationResult':
        """创建失败的验证结果"""
        return ValidationResult(is_valid=False, errors=errors)


class InputValidator:
    """输入验证器 - 负责参数类型检查、必需参数验证和范围验证"""
    
    def __init__(self):
        """初始化输入验证器"""
        pass
    
    def validate(self, tool_name: str, arguments: Dict[str, Any], 
                 input_schema: Dict[str, Any]) -> ValidationResult:
        """
        验证工具输入参数
        
        Args:
            tool_name: 工具名称
            arguments: 工具参数
            input_schema: 输入schema定义
            
        Returns:
            ValidationResult: 验证结果
        """
        errors = []
        
        # 获取schema定义
        properties = input_schema.get('properties', {})
        required = input_schema.get('required', [])
        
        # 1. 检查必需参数
        missing_params = self._check_required_params(arguments, required)
        if missing_params:
            errors.append(ValidationError(
                code=MISSING_REQUIRED_PARAM,
                message=f"缺少必需参数: {', '.join(missing_params)}",
                parameter=', '.join(missing_params)
            ))
        
        # 2. 检查参数类型和范围
        for param_name, param_value in arguments.items():
            if param_name not in properties:
                # 参数不在schema中，跳过（允许额外参数）
                continue
            
            param_schema = properties[param_name]
            
            # 类型检查
            type_error = self._check_param_type(param_name, param_value, param_schema)
            if type_error:
                errors.append(type_error)
            
            # 范围检查
            range_error = self._check_param_range(param_name, param_value, param_schema)
            if range_error:
                errors.append(range_error)
        
        if errors:
            return ValidationResult.failure(errors)
        return ValidationResult.success()
    
    def _check_required_params(self, arguments: Dict[str, Any], 
                               required: List[str]) -> List[str]:
        """
        检查必需参数
        
        Args:
            arguments: 实际参数
            required: 必需参数列表
            
        Returns:
            List[str]: 缺失的参数列表
        """
        missing = []
        for param in required:
            if param not in arguments or arguments[param] is None:
                missing.append(param)
        return missing
    
    def _check_param_type(self, param_name: str, param_value: Any, 
                         param_schema: Dict[str, Any]) -> Optional[ValidationError]:
        """
        检查参数类型
        
        Args:
            param_name: 参数名
            param_value: 参数值
            param_schema: 参数schema
            
        Returns:
            Optional[ValidationError]: 如果类型不匹配返回错误，否则返回None
        """
        expected_type = param_schema.get('type')
        if not expected_type:
            return None
        
        # 类型映射
        type_map = {
            'string': str,
            'integer': int,
            'number': (int, float),
            'boolean': bool,
            'array': list,
            'object': dict
        }
        
        expected_python_type = type_map.get(expected_type)
        if not expected_python_type:
            return None
        
        # 检查类型
        if not isinstance(param_value, expected_python_type):
            actual_type = type(param_value).__name__
            return ValidationError(
                code=INVALID_PARAM_TYPE,
                message=f"参数 '{param_name}' 类型错误",
                parameter=param_name,
                expected=expected_type,
                actual=actual_type
            )
        
        # 如果是数组，检查元素类型
        if expected_type == 'array' and 'items' in param_schema:
            items_schema = param_schema['items']
            items_type = items_schema.get('type')
            if items_type:
                items_python_type = type_map.get(items_type)
                for i, item in enumerate(param_value):
                    if not isinstance(item, items_python_type):
                        return ValidationError(
                            code=INVALID_PARAM_TYPE,
                            message=f"参数 '{param_name}' 的数组元素类型错误",
                            parameter=f"{param_name}[{i}]",
                            expected=items_type,
                            actual=type(item).__name__
                        )
        
        return None
    
    def _check_param_range(self, param_name: str, param_value: Any, 
                          param_schema: Dict[str, Any]) -> Optional[ValidationError]:
        """
        检查参数范围
        
        Args:
            param_name: 参数名
            param_value: 参数值
            param_schema: 参数schema
            
        Returns:
            Optional[ValidationError]: 如果超出范围返回错误，否则返回None
        """
        # 检查枚举值
        if 'enum' in param_schema:
            allowed_values = param_schema['enum']
            if param_value not in allowed_values:
                return ValidationError(
                    code=PARAM_OUT_OF_RANGE,
                    message=f"参数 '{param_name}' 的值不在允许范围内",
                    parameter=param_name,
                    expected=f"one of {allowed_values}",
                    actual=param_value
                )
        
        # 检查数值范围
        if isinstance(param_value, (int, float)):
            # 最小值
            if 'minimum' in param_schema:
                if param_value < param_schema['minimum']:
                    return ValidationError(
                        code=PARAM_OUT_OF_RANGE,
                        message=f"参数 '{param_name}' 小于最小值",
                        parameter=param_name,
                        expected=f">= {param_schema['minimum']}",
                        actual=param_value
                    )
            
            # 最大值
            if 'maximum' in param_schema:
                if param_value > param_schema['maximum']:
                    return ValidationError(
                        code=PARAM_OUT_OF_RANGE,
                        message=f"参数 '{param_name}' 大于最大值",
                        parameter=param_name,
                        expected=f"<= {param_schema['maximum']}",
                        actual=param_value
                    )
        
        # 检查字符串长度
        if isinstance(param_value, str):
            if 'minLength' in param_schema:
                if len(param_value) < param_schema['minLength']:
                    return ValidationError(
                        code=PARAM_OUT_OF_RANGE,
                        message=f"参数 '{param_name}' 长度小于最小长度",
                        parameter=param_name,
                        expected=f"length >= {param_schema['minLength']}",
                        actual=f"length = {len(param_value)}"
                    )
            
            if 'maxLength' in param_schema:
                if len(param_value) > param_schema['maxLength']:
                    return ValidationError(
                        code=PARAM_OUT_OF_RANGE,
                        message=f"参数 '{param_name}' 长度大于最大长度",
                        parameter=param_name,
                        expected=f"length <= {param_schema['maxLength']}",
                        actual=f"length = {len(param_value)}"
                    )
        
        # 检查数组长度
        if isinstance(param_value, list):
            if 'minItems' in param_schema:
                if len(param_value) < param_schema['minItems']:
                    return ValidationError(
                        code=PARAM_OUT_OF_RANGE,
                        message=f"参数 '{param_name}' 数组长度小于最小长度",
                        parameter=param_name,
                        expected=f"length >= {param_schema['minItems']}",
                        actual=f"length = {len(param_value)}"
                    )
            
            if 'maxItems' in param_schema:
                if len(param_value) > param_schema['maxItems']:
                    return ValidationError(
                        code=PARAM_OUT_OF_RANGE,
                        message=f"参数 '{param_name}' 数组长度大于最大长度",
                        parameter=param_name,
                        expected=f"length <= {param_schema['maxItems']}",
                        actual=f"length = {len(param_value)}"
                    )
        
        return None
    
    def create_error_response(self, tool_name: str, errors: List[ValidationError], 
                             example: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        创建标准化错误响应
        
        Args:
            tool_name: 工具名称
            errors: 验证错误列表
            example: 正确调用示例（可选）
            
        Returns:
            Dict: 错误响应
        """
        response = {
            'error': {
                'code': 'INVALID_INPUT',
                'message': '参数验证失败',
                'tool': tool_name,
                'details': [error.to_dict() for error in errors]
            }
        }
        
        if example:
            response['error']['example'] = example
        
        return response
    
    def create_node_not_found_error(self, node_id: int, 
                                    suggestion: Optional[str] = None) -> Dict[str, Any]:
        """
        创建节点不存在错误响应
        
        Args:
            node_id: 节点ID
            suggestion: 建议操作（可选）
            
        Returns:
            Dict: 错误响应
        """
        response = {
            'error': {
                'code': NODE_NOT_FOUND,
                'message': f'节点ID {node_id} 不存在',
                'node_id': node_id
            }
        }
        
        if suggestion:
            response['error']['suggestion'] = suggestion
        else:
            response['error']['suggestion'] = '请使用search_metadata工具查找有效的节点ID'
        
        return response
