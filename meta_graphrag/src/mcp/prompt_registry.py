"""MCP提示词注册器"""
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logger


class DynamicTemplateEngine:
    """动态模板引擎 - 根据参数动态生成提示词内容"""
    
    def __init__(self, logger):
        self.logger = logger
    
    def render_prompt(self, template: Dict[str, Any], arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据参数动态渲染提示词
        
        Args:
            template: 提示词模板
            arguments: 参数字典
            
        Returns:
            Dict: 渲染后的提示词，包含description和messages
        """
        name = template['name']
        description = template['description']
        
        # 生成动态消息内容
        messages = self._render_messages(name, template, arguments)
        
        return {
            'description': description,
            'messages': messages
        }
    
    def _render_messages(self, name: str, template: Dict[str, Any], arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        渲染消息内容，包含步骤说明和错误处理指导
        
        Args:
            name: 提示词名称
            template: 提示词模板
            arguments: 参数字典
            
        Returns:
            List: 消息列表
        """
        # 根据提示词类型选择渲染器
        if name == 'graph-overview':
            return self._render_graph_overview(arguments)
        elif name == 'search-table':
            return self._render_search_table(arguments)
        elif name == 'search-field':
            return self._render_search_field(arguments)
        elif name == 'find-tables-in-domain':
            return self._render_find_tables_in_domain(arguments)
        elif name == 'table-lineage':
            return self._render_table_lineage(arguments)
        elif name == 'field-lineage':
            return self._render_field_lineage(arguments)
        elif name == 'explore-entity':
            return self._render_explore_entity(arguments)
        elif name == 'compare-tables':
            return self._render_compare_tables(arguments)
        elif name == 'find-related-tables':
            return self._render_find_related_tables(arguments)
        elif name == 'infer-field-relationships':
            return self._render_infer_field_relationships(arguments)
        elif name == 'infer-table-relationships':
            return self._render_infer_table_relationships(arguments)
        else:
            # 默认渲染
            return [{'role': 'user', 'content': {'type': 'text', 'text': f'执行提示词: {name}'}}]
    
    def _render_graph_overview(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """渲染图谱概览提示词"""
        return [{
            'role': 'user',
            'content': {
                'type': 'text',
                'text': '''🎯 任务：了解元数据知识图谱的整体情况

📋 执行步骤：

【步骤1】调用工具获取统计
工具：get_graph_overview
参数：无需参数
预期：返回节点类型、关系类型数量及主题域分布

【步骤2】解读统计结果
重点关注：
- 节点类型分布（by_node_type）：有多少表、字段、业务域等
- 关系类型分布（by_relationship_type）：资产之间的关联方式
- 主题域分布（by_subject_domain）：数据按业务如何分类

【步骤3】生成结构化报告
格式要求：
1. 总体规模：总节点数、总关系数
2. 资产分布：各类型节点的数量和占比
3. 业务分类：主题域及其包含的资产数量
4. 关键发现：数据资产最集中的领域

💡 提示：
- 这是数据治理的入口工具，建议首次使用
- 根据统计结果，可以使用 search_metadata 定位具体资产
- 如果某个主题域资产很多，可以深入探索该领域

⚠️ 错误处理：
- 工具调用失败 → 检查Neo4j连接状态
- 返回空结果 → 图谱可能未初始化，需要先导入数据

请按照上述步骤执行，并以清晰的结构化方式展示结果。'''
            }
        }]
    
    def _render_search_table(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """渲染搜索表提示词"""
        keyword = args.get('keyword', '')
        return [{
            'role': 'user',
            'content': {
                'type': 'text',
                'text': f'''🎯 任务：搜索包含关键词 "{keyword}" 的表

📋 执行步骤：

【步骤1】执行关键词搜索
工具：search_metadata
参数：
{{
  "mode": "keyword",
  "query": "{keyword}",
  "node_types": ["PhysicalTable", "LogicalEntity"],
  "limit": 20
}}
预期：返回匹配的表列表，每个表包含 node_id、name、type 等属性

【步骤2】分析搜索结果
对于每个找到的表：
- 记录表名（name）和节点ID（node_id）
- 注意表类型（PhysicalTable 或 LogicalEntity）
- 如果有 comment 属性，记录业务说明

【步骤3】（可选）获取详细信息
如果需要更多信息，对重点表使用：
工具：get_node_details
参数：{{"node_id": <从步骤1获取>}}

【步骤4】生成结构化报告
格式要求：
1. 搜索摘要：找到多少个表
2. 表列表：
   - 表名
   - 类型（物理表/逻辑实体）
   - 业务说明（如果有）
   - 节点ID（供后续使用）
3. 如果结果较多，按业务域或类型分组

💡 后续操作建议：
- 查看表结构 → get_node_details (include_neighbors=true)
- 查看血缘关系 → get_lineage (lineage_type="both")
- 查找相关表 → get_subgraph (depth=2)

⚠️ 错误处理：
- 搜索无结果 → 尝试更短的关键词（如"{keyword[:3]}"）
- 结果过多 → 使用更具体的关键词或添加过滤条件
- 不确定表名 → 先用 get_graph_overview 了解有哪些表

请按照上述步骤执行，并以清晰的列表形式展示结果。'''
            }
        }]
    
    def _render_search_field(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """渲染搜索字段提示词"""
        keyword = args.get('keyword', '')
        return [{
            'role': 'user',
            'content': {
                'type': 'text',
                'text': f'''请搜索包含关键词 "{keyword}" 的字段：

**步骤1：执行字段搜索**
- 使用 `search_metadata` 工具，参数：
  - mode: "keyword"
  - query: "{keyword}"
  - node_types: ["Field"]
- 预期结果：匹配的字段列表，包含table_name属性

**步骤2：获取字段详情**
- 对于找到的每个字段，使用 `get_node_details` 获取完整信息
- 关注：数据类型（data_type）、业务术语（business_term）、所属表（table_name）

**步骤3：分析字段分布**
- 如果有多个同名字段，说明它们分别属于哪些表
- 识别字段的业务含义和使用场景

**错误处理：**
- 如果搜索无结果，尝试搜索业务术语而非字段名
- 可以使用 `search_metadata` 的 attribute 模式搜索 business_term 属性

**后续操作建议：**
- 使用 `get_lineage` 查看字段的技术血缘（Field类型支持）
- 使用 `infer_relationships` 查找相关字段

请列出搜索结果并提供详细说明。'''
            }
        }]
    
    def _render_find_tables_in_domain(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """渲染查找域内表提示词"""
        domain_name = args.get('domain_name', '')
        return [{
            'role': 'user',
            'content': {
                'type': 'text',
                'text': f'''请查找业务域 "{domain_name}" 下的所有表：

**步骤1：定位业务域节点**
- 使用 `search_metadata` 工具，参数：
  - mode: "exact"
  - query: "{domain_name}"
  - node_type: "BusinessDomain"
- 预期结果：业务域节点的ID

**步骤2：获取域内资产**
- 使用 `get_node_details` 获取业务域详情，参数 include_neighbors: true
- 或使用 `get_subgraph` 获取以该业务域为中心的子图
- 预期结果：该业务域下的所有逻辑实体和物理表

**步骤3：整理表信息**
- 列出所有表的名称和业务说明
- 按表的业务分类展示

**错误处理：**
- 如果找不到业务域，使用 `search_metadata` 的 keyword 模式模糊搜索
- 如果业务域存在但无关联表，说明该域可能为空或数据未完整导入

**后续操作建议：**
- 使用 `get_lineage` 查看表的完整业务血缘
- 使用 `compare-tables` 比较同域内表的结构差异

请按照表的业务分类展示结果。'''
            }
        }]
    
    def _render_table_lineage(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """渲染表血缘提示词"""
        table_name = args.get('table_name', '')
        lineage_type = args.get('lineage_type', 'both')
        
        type_desc = {
            'business': '业务血缘（主题域 → 业务域 → 业务主题 → 逻辑实体）',
            'technical': '技术血缘（数据库 → Schema → 物理表）',
            'both': '业务血缘和技术血缘'
        }.get(lineage_type, '血缘')
        
        return [{
            'role': 'user',
            'content': {
                'type': 'text',
                'text': f'''请获取表 "{table_name}" 的{type_desc}：

**步骤1：执行血缘查询**
- 使用 `get_lineage` 工具，参数：
  - entity_name: "{table_name}"
  - lineage_type: "{lineage_type}"
  - entity_type: "PhysicalTable" 或 "LogicalEntity"（可选，用于精确匹配）
- 预期结果：完整的血缘路径

**步骤2：解析血缘路径**
- 业务血缘：展示从主题域到逻辑实体的完整业务分类
- 技术血缘：展示从数据库到物理表的完整技术层级
- 解释每一层级的含义

**步骤3：可视化展示**
- 以清晰的路径图方式展示血缘关系
- 标注每个节点的关键属性

**错误处理：**
- 如果找不到表，先使用 `search_metadata` 搜索表名
- 如果血缘路径不完整，说明元数据可能未完全建立关联

**后续操作建议：**
- 使用 `get_node_details` 查看路径中任意节点的详细信息
- 使用 `find_path` 探索节点间的其他关联路径

请以清晰的路径图方式展示血缘关系。'''
            }
        }]
    
    def _render_field_lineage(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """渲染字段血缘提示词"""
        field_name = args.get('field_name', '')
        return [{
            'role': 'user',
            'content': {
                'type': 'text',
                'text': f'''请获取字段 "{field_name}" 的完整血缘信息：

**步骤1：搜索字段**
- 使用 `search_metadata` 工具，参数：
  - mode: "keyword"
  - query: "{field_name}"
  - node_types: ["Field"]
- 预期结果：匹配的字段列表（可能有多个同名字段）

**步骤2：获取字段详情**
- 对每个字段使用 `get_node_details` 获取详细信息
- 关注：数据类型、业务术语、所属表（table_name）

**步骤3：获取技术血缘**
- 使用 `get_lineage` 工具，参数：
  - entity_name: "{field_name}"
  - lineage_type: "technical"
  - entity_type: "Field"
- 预期结果：字段 → 物理表 → 数据库的完整路径

**步骤4：汇总信息**
- 如果有多个同名字段，分别展示每个字段的信息
- 说明字段的业务含义和技术位置

**错误处理：**
- 如果搜索无结果，检查字段名是否正确
- 如果技术血缘不支持Field类型，说明需要先查询所属表的血缘

**后续操作建议：**
- 使用 `infer_relationships` 查找业务相关的字段
- 使用 `get_node_details` 查看所属表的完整结构

请详细展示字段的元数据信息和血缘关系。'''
            }
        }]
    
    def _render_explore_entity(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """渲染探索实体提示词"""
        entity_name = args.get('entity_name', '')
        entity_type = args.get('entity_type', '')
        type_hint = f"，类型为 {entity_type}" if entity_type else ""
        
        return [{
            'role': 'user',
            'content': {
                'type': 'text',
                'text': f'''请深入探索实体 "{entity_name}"{type_hint} 的详细信息：

**步骤1：定位实体**
- 使用 `search_metadata` 工具，参数：
  - mode: "exact" 或 "keyword"
  - query: "{entity_name}"
  - node_type: "{entity_type}" （如果已知类型）
- 预期结果：实体节点的ID

**步骤2：获取实体详情**
- 使用 `get_node_details` 获取实体的所有属性，参数：
  - node_id: <从步骤1获取>
  - include_neighbors: true
- 预期结果：完整属性和邻居节点摘要

**步骤3：分析关联关系**
- 从邻居节点中识别关键关联：
  - 上级节点（业务归属）
  - 下级节点（包含的子资产）
  - 平级节点（相关资产）

**步骤4：评估重要性**
- 分析该实体在知识图谱中的位置
- 说明其业务价值和使用场景

**错误处理：**
- 如果找不到实体，尝试模糊搜索或检查名称拼写
- 如果邻居节点过多，使用 `get_subgraph` 获取更完整的关联视图

**后续操作建议：**
- 使用 `get_lineage` 查看完整血缘
- 使用 `find_path` 探索与其他实体的关联路径

请全面展示该实体的元数据信息和关联关系。'''
            }
        }]
    
    def _render_compare_tables(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """渲染比较表提示词"""
        table1 = args.get('table1', '')
        table2 = args.get('table2', '')
        return [{
            'role': 'user',
            'content': {
                'type': 'text',
                'text': f'''请比较表 "{table1}" 和 "{table2}" 的结构差异：

**步骤1：搜索两个表**
- 使用 `search_metadata` 分别搜索两个表
- 获取表的节点ID

**步骤2：获取表详情**
- 对每个表使用 `get_node_details` 获取详细信息
- 使用 `get_subgraph` 获取表的字段结构（depth=1）

**步骤3：比较分析**
- 字段数量差异
- 同名字段的数据类型差异
- 各自独有的字段
- 业务域归属差异
- 业务含义的相似度

**步骤4：生成对比报告**
- 以对比表格的形式展示差异
- 计算结构相似度
- 说明主要差异点

**错误处理：**
- 如果找不到表，检查表名是否正确
- 如果表没有字段信息，说明元数据可能不完整

**后续操作建议：**
- 使用 `infer_relationships` 推理两表的潜在关联
- 使用 `get_lineage` 比较两表的业务归属

请以对比表格的形式展示比较结果。'''
            }
        }]
    
    def _render_find_related_tables(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """渲染查找相关表提示词"""
        table_name = args.get('table_name', '')
        return [{
            'role': 'user',
            'content': {
                'type': 'text',
                'text': f'''请查找与表 "{table_name}" 相关的其他表：

**步骤1：定位目标表**
- 使用 `search_metadata` 搜索表 "{table_name}"
- 获取表的节点ID

**步骤2：获取关联子图**
- 使用 `get_subgraph` 获取以该表为中心的子图，参数：
  - node_id: <从步骤1获取>
  - depth: 2
  - node_types: ["PhysicalTable", "LogicalEntity"]（可选，过滤表类型）
- 预期结果：相关表的网络

**步骤3：分析关联类型**
- 同一业务主题下的表（通过业务血缘关联）
- 同一业务域下的表（通过业务归属关联）
- 有字段关联的表（通过推理发现）

**步骤4：排序和展示**
- 按关联强度排序
- 说明每个相关表与目标表的关系
- 提供相关表的简要说明

**错误处理：**
- 如果子图过大，减小depth参数
- 如果找不到相关表，使用 `get_lineage` 查看业务归属

**后续操作建议：**
- 使用 `find_path` 查看具体的关联路径
- 使用 `infer_relationships` 推理潜在的表关系

请按关联强度排序展示相关表。'''
            }
        }]
    
    def _render_infer_field_relationships(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """渲染推理字段关系提示词"""
        field_name = args.get('field_name', '')
        threshold = args.get('threshold', 0.7)
        
        return [{
            'role': 'user',
            'content': {
                'type': 'text',
                'text': f'''请推理与字段 "{field_name}" 相关的其他字段：

**步骤1：搜索源字段**
- 使用 `search_metadata` 搜索字段 "{field_name}"
- 获取字段的节点ID

**步骤2：执行关联推理**
- 使用 `infer_relationships` 工具，参数：
  - target: "fields"
  - source_id: <从步骤1获取>
  - threshold: {threshold}
- 预期结果：相关字段列表，包含相似度分数和推理依据

**步骤3：分析推理结果**
- 精确匹配：相同业务术语的字段（confidence=1.0）
- 名称相似：字段名相似的字段
- 说明每个推理结果的依据（evidence字段）

**步骤4：验证和应用**
- 对于高置信度的关联，使用 `get_node_details` 查看详情
- 评估推理结果的业务合理性

**错误处理：**
- 如果推理结果为空，降低threshold参数
- 如果结果过多，提高threshold参数

**后续操作建议：**
- 使用 `get_node_details` 查看相关字段的详细信息
- 使用 `compare-tables` 比较包含这些字段的表

推理可以帮助发现隐藏的数据关联和治理机会。'''
            }
        }]
    
    def _render_infer_table_relationships(self, args: Dict[str, Any]) -> List[Dict[str, Any]]:
        """渲染推理表关系提示词"""
        table_name = args.get('table_name', '')
        threshold = args.get('threshold', 0.7)
        
        return [{
            'role': 'user',
            'content': {
                'type': 'text',
                'text': f'''请推理与表 "{table_name}" 可能存在关联的其他表：

**步骤1：搜索源表**
- 使用 `search_metadata` 搜索表 "{table_name}"
- 获取表的节点ID

**步骤2：执行关系推理**
- 使用 `infer_relationships` 工具，参数：
  - target: "tables"
  - source_id: <从步骤1获取>
  - threshold: {threshold}
- 预期结果：可能关联的表列表，包含推理类型和依据

**步骤3：分析推理类型**
- 潜在外键关系：字段名匹配主键模式
- 相似结构：表结构相似度高
- 说明每个推理结果的依据（evidence字段）

**步骤4：验证推理结果**
- 对于潜在外键，使用 `get_node_details` 查看字段详情
- 评估关联的业务合理性

**错误处理：**
- 如果推理结果为空，降低threshold参数
- 如果结果过多，提高threshold参数或添加过滤条件

**后续操作建议：**
- 使用 `find_path` 验证推理出的关联路径
- 使用 `compare-tables` 详细比较表结构

推理可以帮助发现未显式建模的数据关系。'''
            }
        }]


class PromptRegistry:
    """提示词注册器 - 管理所有MCP预定义提示词模板"""
    
    def __init__(self, verbose: bool = False):
        """
        初始化提示词注册器
        
        Args:
            verbose: 是否输出详细日志
        """
        self.logger = setup_logger('prompt_registry', verbose=verbose)
        
        # 提示词定义
        self.prompts: Dict[str, Dict[str, Any]] = {}
        
        # 初始化动态模板引擎
        self.template_engine = DynamicTemplateEngine(self.logger)
        
        # 注册所有提示词
        self._register_all_prompts()
        
        self.logger.info(f"提示词注册器初始化完成，已注册 {len(self.prompts)} 个提示词")
    
    def _register_all_prompts(self):
        """注册所有MCP提示词"""
        # 图谱概览类提示词
        self._register_overview_prompts()
        
        # 搜索类提示词
        self._register_search_prompts()
        
        # 血缘分析类提示词
        self._register_lineage_prompts()
        
        # 数据探索类提示词
        self._register_exploration_prompts()
        
        # 推理类提示词
        self._register_inference_prompts()
    
    def _register_overview_prompts(self):
        """注册图谱概览类提示词"""
        self.register_prompt(
            name='graph-overview',
            description='获取元数据知识图谱的整体概览，包括节点类型、关系类型、统计信息和主题域分布',
            arguments=[]
        )
    
    def _register_search_prompts(self):
        """注册搜索类提示词"""
        self.register_prompt(
            name='search-table',
            description='搜索包含指定关键词的物理表或逻辑实体',
            arguments=[
                {
                    'name': 'keyword',
                    'description': '要搜索的表名关键词',
                    'required': True
                }
            ]
        )
        
        self.register_prompt(
            name='search-field',
            description='搜索包含指定关键词的字段',
            arguments=[
                {
                    'name': 'keyword',
                    'description': '要搜索的字段名或业务术语关键词',
                    'required': True
                }
            ]
        )
        
        self.register_prompt(
            name='find-tables-in-domain',
            description='查找指定业务域下的所有表',
            arguments=[
                {
                    'name': 'domain_name',
                    'description': '业务域名称',
                    'required': True
                }
            ]
        )
    
    def _register_lineage_prompts(self):
        """注册血缘分析类提示词"""
        self.register_prompt(
            name='table-lineage',
            description='获取指定表的血缘路径，支持业务血缘、技术血缘或两者',
            arguments=[
                {
                    'name': 'table_name',
                    'description': '表名称',
                    'required': True
                },
                {
                    'name': 'lineage_type',
                    'description': '血缘类型：business（业务血缘）、technical（技术血缘）、both（两者）',
                    'required': False
                }
            ]
        )
        
        self.register_prompt(
            name='field-lineage',
            description='获取指定字段的完整血缘信息，包括所属表和技术层级',
            arguments=[
                {
                    'name': 'field_name',
                    'description': '字段名称',
                    'required': True
                }
            ]
        )
    
    def _register_exploration_prompts(self):
        """注册数据探索类提示词"""
        self.register_prompt(
            name='explore-entity',
            description='深入探索指定实体的详细信息及其关联关系',
            arguments=[
                {
                    'name': 'entity_name',
                    'description': '实体名称',
                    'required': True
                },
                {
                    'name': 'entity_type',
                    'description': '实体类型（如 LogicalEntity, PhysicalTable, Field 等）',
                    'required': False
                }
            ]
        )
        
        self.register_prompt(
            name='compare-tables',
            description='比较两个表的结构和字段差异',
            arguments=[
                {
                    'name': 'table1',
                    'description': '第一个表名',
                    'required': True
                },
                {
                    'name': 'table2',
                    'description': '第二个表名',
                    'required': True
                }
            ]
        )
        
        self.register_prompt(
            name='find-related-tables',
            description='查找与指定表相关的其他表',
            arguments=[
                {
                    'name': 'table_name',
                    'description': '表名称',
                    'required': True
                }
            ]
        )
    
    def _register_inference_prompts(self):
        """注册推理类提示词"""
        self.register_prompt(
            name='infer-field-relationships',
            description='推理字段之间的潜在业务关联，基于业务术语和名称相似性',
            arguments=[
                {
                    'name': 'field_name',
                    'description': '字段名称',
                    'required': True
                },
                {
                    'name': 'threshold',
                    'description': '相似度阈值（0.0-1.0），默认0.7',
                    'required': False
                }
            ]
        )
        
        self.register_prompt(
            name='infer-table-relationships',
            description='推理表之间的潜在关联关系，基于字段匹配和结构相似性',
            arguments=[
                {
                    'name': 'table_name',
                    'description': '表名称',
                    'required': True
                },
                {
                    'name': 'threshold',
                    'description': '相似度阈值（0.0-1.0），默认0.7',
                    'required': False
                }
            ]
        )
    
    def register_prompt(self, name: str, description: str, arguments: List[Dict[str, Any]]):
        """
        注册提示词
        
        Args:
            name: 提示词名称
            description: 提示词描述
            arguments: 参数列表
        """
        self.prompts[name] = {
            'name': name,
            'description': description,
            'arguments': arguments
        }
        self.logger.debug(f"注册提示词: {name}")
    
    def list_prompts(self) -> List[Dict[str, Any]]:
        """
        列出所有提示词
        
        Returns:
            List: 提示词列表
        """
        return list(self.prompts.values())
    
    def get_prompt(self, name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        获取提示词内容（使用动态模板引擎）
        
        Args:
            name: 提示词名称
            arguments: 提示词参数
            
        Returns:
            Dict: 提示词内容，包含description和messages
        """
        if name not in self.prompts:
            raise ValueError(f"Unknown prompt: {name}")
        
        arguments = arguments or {}
        
        # 使用动态模板引擎渲染提示词
        return self.template_engine.render_prompt(self.prompts[name], arguments)

