"""测试InputValidator类"""
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from mcp.input_validator import (
    InputValidator, 
    ValidationError, 
    ValidationResult,
    INVALID_PARAM_TYPE,
    MISSING_REQUIRED_PARAM,
    PARAM_OUT_OF_RANGE,
    NODE_NOT_FOUND
)


def test_missing_required_params():
    """测试缺少必需参数"""
    validator = InputValidator()
    
    input_schema = {
        'type': 'object',
        'properties': {
            'keyword': {'type': 'string'},
            'limit': {'type': 'integer'}
        },
        'required': ['keyword']
    }
    
    # 缺少必需参数
    result = validator.validate('test_tool', {}, input_schema)
    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].code == MISSING_REQUIRED_PARAM
    assert 'keyword' in result.errors[0].message
    print("✓ 测试缺少必需参数通过")


def test_invalid_param_type():
    """测试参数类型错误"""
    validator = InputValidator()
    
    input_schema = {
        'type': 'object',
        'properties': {
            'node_id': {'type': 'integer'},
            'name': {'type': 'string'}
        },
        'required': ['node_id']
    }
    
    # 类型错误：node_id应该是integer
    result = validator.validate('test_tool', {'node_id': 'abc'}, input_schema)
    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].code == INVALID_PARAM_TYPE
    assert result.errors[0].parameter == 'node_id'
    assert result.errors[0].expected == 'integer'
    print("✓ 测试参数类型错误通过")


def test_param_out_of_range_enum():
    """测试参数值不在枚举范围内"""
    validator = InputValidator()
    
    input_schema = {
        'type': 'object',
        'properties': {
            'mode': {
                'type': 'string',
                'enum': ['keyword', 'attribute', 'exact']
            }
        },
        'required': ['mode']
    }
    
    # 值不在枚举范围内
    result = validator.validate('test_tool', {'mode': 'invalid'}, input_schema)
    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].code == PARAM_OUT_OF_RANGE
    assert result.errors[0].parameter == 'mode'
    print("✓ 测试枚举值范围检查通过")


def test_param_out_of_range_number():
    """测试数值参数超出范围"""
    validator = InputValidator()
    
    input_schema = {
        'type': 'object',
        'properties': {
            'limit': {
                'type': 'integer',
                'minimum': 1,
                'maximum': 100
            }
        },
        'required': []
    }
    
    # 值小于最小值
    result = validator.validate('test_tool', {'limit': 0}, input_schema)
    assert not result.is_valid
    assert result.errors[0].code == PARAM_OUT_OF_RANGE
    
    # 值大于最大值
    result = validator.validate('test_tool', {'limit': 101}, input_schema)
    assert not result.is_valid
    assert result.errors[0].code == PARAM_OUT_OF_RANGE
    print("✓ 测试数值范围检查通过")


def test_valid_params():
    """测试有效参数"""
    validator = InputValidator()
    
    input_schema = {
        'type': 'object',
        'properties': {
            'keyword': {'type': 'string'},
            'limit': {'type': 'integer', 'minimum': 1, 'maximum': 100},
            'node_types': {'type': 'array', 'items': {'type': 'string'}}
        },
        'required': ['keyword']
    }
    
    # 有效参数
    result = validator.validate('test_tool', {
        'keyword': 'test',
        'limit': 20,
        'node_types': ['Field', 'PhysicalTable']
    }, input_schema)
    assert result.is_valid
    assert len(result.errors) == 0
    print("✓ 测试有效参数通过")


def test_array_item_type():
    """测试数组元素类型检查"""
    validator = InputValidator()
    
    input_schema = {
        'type': 'object',
        'properties': {
            'node_types': {
                'type': 'array',
                'items': {'type': 'string'}
            }
        },
        'required': []
    }
    
    # 数组元素类型错误
    result = validator.validate('test_tool', {'node_types': ['Field', 123]}, input_schema)
    assert not result.is_valid
    assert result.errors[0].code == INVALID_PARAM_TYPE
    assert 'node_types[1]' in result.errors[0].parameter
    print("✓ 测试数组元素类型检查通过")


def test_create_error_response():
    """测试创建错误响应"""
    validator = InputValidator()
    
    errors = [
        ValidationError(
            code=MISSING_REQUIRED_PARAM,
            message="缺少必需参数: keyword",
            parameter="keyword"
        )
    ]
    
    response = validator.create_error_response('test_tool', errors)
    assert 'error' in response
    assert response['error']['code'] == 'INVALID_INPUT'
    assert response['error']['tool'] == 'test_tool'
    assert len(response['error']['details']) == 1
    print("✓ 测试创建错误响应通过")


def test_create_node_not_found_error():
    """测试创建节点不存在错误"""
    validator = InputValidator()
    
    response = validator.create_node_not_found_error(12345)
    assert 'error' in response
    assert response['error']['code'] == NODE_NOT_FOUND
    assert response['error']['node_id'] == 12345
    assert 'suggestion' in response['error']
    print("✓ 测试创建节点不存在错误通过")


def test_multiple_errors():
    """测试多个验证错误"""
    validator = InputValidator()
    
    input_schema = {
        'type': 'object',
        'properties': {
            'keyword': {'type': 'string'},
            'limit': {'type': 'integer', 'minimum': 1},
            'mode': {'type': 'string', 'enum': ['a', 'b']}
        },
        'required': ['keyword']
    }
    
    # 多个错误：缺少必需参数、类型错误、范围错误
    result = validator.validate('test_tool', {
        'limit': 'abc',
        'mode': 'invalid'
    }, input_schema)
    assert not result.is_valid
    assert len(result.errors) >= 2  # 至少有缺少必需参数和其他错误
    print("✓ 测试多个验证错误通过")


def run_all_tests():
    """运行所有测试"""
    print("\n=== 测试InputValidator ===\n")
    
    try:
        test_missing_required_params()
        test_invalid_param_type()
        test_param_out_of_range_enum()
        test_param_out_of_range_number()
        test_valid_params()
        test_array_item_type()
        test_create_error_response()
        test_create_node_not_found_error()
        test_multiple_errors()
        
        print("\n✅ 所有测试通过！")
        return True
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
