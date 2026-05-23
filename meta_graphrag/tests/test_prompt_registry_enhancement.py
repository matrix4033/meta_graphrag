"""测试增强的提示词注册器"""
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from mcp.prompt_registry import PromptRegistry


def test_prompt_registry_initialization():
    """测试提示词注册器初始化"""
    registry = PromptRegistry(verbose=False)
    
    # 验证提示词已注册
    prompts = registry.list_prompts()
    assert len(prompts) > 0, "应该注册了提示词"
    
    # 验证动态模板引擎已初始化
    assert hasattr(registry, 'template_engine'), "应该有动态模板引擎"
    
    print(f"✓ 提示词注册器初始化成功，已注册 {len(prompts)} 个提示词")


def test_dynamic_template_rendering():
    """测试动态模板渲染"""
    registry = PromptRegistry(verbose=False)
    
    # 测试图谱概览提示词
    result = registry.get_prompt('graph-overview')
    assert 'description' in result, "应该包含description"
    assert 'messages' in result, "应该包含messages"
    assert len(result['messages']) > 0, "应该有消息内容"
    
    # 验证消息包含步骤说明
    message_text = result['messages'][0]['content']['text']
    assert '步骤1' in message_text, "应该包含步骤说明"
    assert 'get_graph_overview' in message_text, "应该使用整合后的工具名称"
    assert '错误处理' in message_text, "应该包含错误处理指导"
    
    print("✓ 动态模板渲染成功")


def test_parameterized_prompt_rendering():
    """测试参数化提示词渲染"""
    registry = PromptRegistry(verbose=False)
    
    # 测试搜索表提示词（带参数）
    result1 = registry.get_prompt('search-table', {'keyword': '用户表'})
    message1 = result1['messages'][0]['content']['text']
    assert '用户表' in message1, "应该包含参数值"
    assert 'search_metadata' in message1, "应该使用整合后的工具名称"
    
    # 测试不同参数产生不同内容
    result2 = registry.get_prompt('search-table', {'keyword': '订单表'})
    message2 = result2['messages'][0]['content']['text']
    assert '订单表' in message2, "应该包含不同的参数值"
    assert message1 != message2, "不同参数应该产生不同内容"
    
    print("✓ 参数化提示词渲染成功")


def test_lineage_prompt_with_type():
    """测试血缘提示词支持类型参数"""
    registry = PromptRegistry(verbose=False)
    
    # 测试表血缘提示词（带血缘类型）
    result = registry.get_prompt('table-lineage', {
        'table_name': '用户表',
        'lineage_type': 'business'
    })
    message = result['messages'][0]['content']['text']
    assert '用户表' in message, "应该包含表名"
    assert 'get_lineage' in message, "应该使用整合后的工具名称"
    assert 'business' in message, "应该包含血缘类型"
    
    print("✓ 血缘提示词支持类型参数")


def test_inference_prompts():
    """测试推理提示词"""
    registry = PromptRegistry(verbose=False)
    
    # 测试字段关联推理提示词
    result1 = registry.get_prompt('infer-field-relationships', {
        'field_name': '用户ID',
        'threshold': 0.8
    })
    message1 = result1['messages'][0]['content']['text']
    assert '用户ID' in message1, "应该包含字段名"
    assert 'infer_relationships' in message1, "应该使用推理工具"
    assert '0.8' in message1, "应该包含阈值参数"
    
    # 测试表关系推理提示词
    result2 = registry.get_prompt('infer-table-relationships', {
        'table_name': '用户表',
        'threshold': 0.7
    })
    message2 = result2['messages'][0]['content']['text']
    assert '用户表' in message2, "应该包含表名"
    assert 'infer_relationships' in message2, "应该使用推理工具"
    
    print("✓ 推理提示词测试成功")


def test_multi_step_structure():
    """测试多步骤提示词结构"""
    registry = PromptRegistry(verbose=False)
    
    # 测试复杂的多步骤提示词
    result = registry.get_prompt('compare-tables', {
        'table1': '用户表',
        'table2': '客户表'
    })
    message = result['messages'][0]['content']['text']
    
    # 验证包含多个步骤
    assert '步骤1' in message, "应该包含步骤1"
    assert '步骤2' in message, "应该包含步骤2"
    assert '步骤3' in message, "应该包含步骤3"
    assert '步骤4' in message, "应该包含步骤4"
    
    # 验证包含错误处理
    assert '错误处理' in message, "应该包含错误处理指导"
    
    # 验证包含后续操作建议
    assert '后续操作建议' in message, "应该包含后续操作建议"
    
    print("✓ 多步骤提示词结构完整")


def test_tool_name_updates():
    """测试提示词使用整合后的工具名称"""
    registry = PromptRegistry(verbose=False)
    
    # 获取所有提示词
    prompts = registry.list_prompts()
    
    # 检查几个关键提示词
    test_cases = [
        ('search-table', ['search_metadata']),
        ('search-field', ['search_metadata']),
        ('table-lineage', ['get_lineage']),
        ('field-lineage', ['get_lineage', 'search_metadata']),
        ('infer-field-relationships', ['infer_relationships']),
    ]
    
    for prompt_name, expected_tools in test_cases:
        result = registry.get_prompt(prompt_name, {
            'keyword': 'test',
            'field_name': 'test',
            'table_name': 'test'
        })
        message = result['messages'][0]['content']['text']
        
        for tool in expected_tools:
            assert tool in message, f"提示词 {prompt_name} 应该使用工具 {tool}"
    
    print("✓ 提示词使用整合后的工具名称")


if __name__ == '__main__':
    print("开始测试增强的提示词注册器...\n")
    
    try:
        test_prompt_registry_initialization()
        test_dynamic_template_rendering()
        test_parameterized_prompt_rendering()
        test_lineage_prompt_with_type()
        test_inference_prompts()
        test_multi_step_structure()
        test_tool_name_updates()
        
        print("\n✅ 所有测试通过！")
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
