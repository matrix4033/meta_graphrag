"""测试MCP服务器与增强提示词注册器的集成"""
import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from mcp.prompt_registry import PromptRegistry


def test_mcp_prompt_integration():
    """测试MCP服务器可以正常使用增强的提示词注册器"""
    try:
        # 初始化提示词注册器
        registry = PromptRegistry(verbose=False)
        
        # 验证可以列出提示词
        prompts = registry.list_prompts()
        assert len(prompts) > 0, "应该有提示词"
        
        # 验证可以获取提示词
        for prompt in prompts:
            name = prompt['name']
            result = registry.get_prompt(name, {
                'keyword': 'test',
                'table_name': 'test',
                'field_name': 'test',
                'table1': 'test1',
                'table2': 'test2',
                'entity_name': 'test',
                'domain_name': 'test',
                'lineage_type': 'both',
                'threshold': 0.7
            })
            assert 'description' in result, f"提示词 {name} 应该有description"
            assert 'messages' in result, f"提示词 {name} 应该有messages"
        
        print(f"✓ MCP服务器可以正常使用增强的提示词注册器")
        print(f"✓ 已验证 {len(prompts)} 个提示词")
        return True
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("开始MCP集成测试...\n")
    success = test_mcp_prompt_integration()
    print("\n✅ 集成测试通过！" if success else "\n❌ 集成测试失败！")
    sys.exit(0 if success else 1)
