"""MCP工具注册器"""
import sys
from typing import Dict, Any, List, Callable
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logger import setup_logger


class ToolRegistry:
    """工具注册器 - 管理所有MCP工具"""
    
    def __init__(self, query_executor, result_formatter, mcp_config: Dict[str, Any], verbose: bool = False):
        """
        初始化工具注册器
        
        Args:
            query_executor: 查询执行器实例
            result_formatter: 结果格式化器实例
            mcp_config: MCP配置
            verbose: 是否输出详细日志
        """
        self.logger = setup_logger('tool_registry', verbose=verbose)
        self.query_executor = query_executor
        self.result_formatter = result_formatter
        self.mcp_config = mcp_config
        
        # 初始化上下文增强器
        from mcp.context_enricher import ContextEnricher
        self.context_enricher = ContextEnricher(query_executor, verbose=verbose)
        
        # 初始化推理引擎
        from mcp.inference_engine import InferenceEngine
        self.inference_engine = InferenceEngine(query_executor, verbose=verbose)
        
        # 工具定义
        self.tools: Dict[str, Dict[str, Any]] = {}
        
        # 工具处理函数
        self.tool_handlers: Dict[str, Callable] = {}
        
        # 注册所有工具
        self._register_all_tools()
        
        self.logger.info(f"工具注册器初始化完成，已注册 {len(self.tools)} 个工具")
    
    def _register_all_tools(self):
        """注册所有MCP工具"""
        # 探索式检索工具
        self._register_exploration_tools()
        
        # 路径发现工具
        self._register_path_discovery_tools()
        
        # 推理工具
        self._register_inference_tools()
    
    def _register_exploration_tools(self):
        """注册探索式检索工具"""
        # 1. get_graph_overview
        self.register_tool(
            name='get_graph_overview',
            category='overview',
            description='''【概览工具】获取元数据知识图谱的整体结构统计

🎯 使用场景：
- 初次了解图谱时，获取全局视图
- 数据治理评估，了解资产分布
- 确定后续探索的起点

📊 返回信息：
- 节点类型及数量（主题域、业务域、逻辑实体、物理表、字段等）
- 关系类型及数量
- 按主题域分组的统计信息

🔄 典型工作流：
1. 使用本工具获取概览
2. 根据统计结果，使用 search_metadata 定位感兴趣的资产
3. 使用 get_node_details 查看资产详情

💡 提示：这是数据治理的入口工具，建议首次使用时先调用此工具了解图谱规模''',
            input_schema={
                'type': 'object',
                'properties': {},
                'required': []
            },
            handler=self._handle_get_graph_overview
        )
        
        # 1.5. search_metadata - 整合后的搜索工具
        self.register_tool(
            name='search_metadata',
            category='search',
            description='''【搜索工具】统一的元数据搜索入口，支持三种搜索模式

🎯 使用场景：
- 查找包含特定关键词的表或字段（keyword模式）
- 按特定属性值查找资产（attribute模式）
- 精确定位已知名称的资产（exact模式）

📋 三种搜索模式：

1️⃣ keyword模式（关键词搜索）：
   - 适用：模糊搜索，不确定完整名称
   - 必需参数：mode="keyword", query="关键词"
   - 可选参数：node_types=["PhysicalTable", "Field"] 限定类型
   - 示例：搜索包含"客户"的所有表和字段

2️⃣ attribute模式（属性搜索）：
   - 适用：按特定属性值查找（如业务术语、注释等）
   - 必需参数：mode="attribute", node_type="Field", attribute_name="business_term", query="客户编号"
   - 示例：查找业务术语为"客户编号"的所有字段

3️⃣ exact模式（精确匹配）：
   - 适用：已知完整名称，需要精确定位
   - 必需参数：mode="exact", query="表名", node_type="PhysicalTable"
   - 示例：精确查找名为"T_CUSTOMER"的表

🔄 典型工作流：
1. 使用本工具搜索资产（获得node_id）
2. 使用 get_node_details 查看资产详情
3. 使用 get_lineage 追溯血缘关系

💡 提示：
- 搜索结果包含node_id，可用于后续工具调用
- Field类型结果会自动包含table_name属性
- 支持分页，默认返回20条结果''',
            input_schema={
                'type': 'object',
                'properties': {
                    'mode': {
                        'type': 'string',
                        'enum': ['keyword', 'attribute', 'exact'],
                        'description': '搜索模式：keyword=关键词模糊搜索, attribute=按属性值搜索, exact=精确名称匹配'
                    },
                    'query': {
                        'type': 'string',
                        'description': '搜索内容：关键词（keyword模式）、属性值（attribute模式）或完整名称（exact模式）'
                    },
                    'node_type': {
                        'type': 'string',
                        'description': '节点类型，常用值：SubjectDomain（主题域）、BusinessDomain（业务域）、BusinessSubject（业务主题）、LogicalEntity（逻辑实体）、PhysicalTable（物理表）、Field（字段）。attribute和exact模式必需，keyword模式可选'
                    },
                    'node_types': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': '节点类型列表（仅keyword模式使用），用于同时搜索多种类型，如["PhysicalTable", "LogicalEntity"]'
                    },
                    'attribute_name': {
                        'type': 'string',
                        'description': '属性名（仅attribute模式使用），常用值：business_term（业务术语）、comment（注释）、data_type（数据类型）'
                    },
                    'offset': {
                        'type': 'integer',
                        'default': 0,
                        'description': '分页偏移量，用于获取后续结果'
                    },
                    'limit': {
                        'type': 'integer',
                        'default': 20,
                        'description': '返回结果数量，默认20条，最大100条'
                    }
                },
                'required': []
            },
            handler=self._handle_search_metadata
        )
        

        
        # 6. get_node_details
        self.register_tool(
            name='get_node_details',
            category='detail',
            description='''【详情工具】获取单个元数据资产的完整属性和直接关联信息

🎯 使用场景：
- 查看资产的所有元数据属性
- 了解资产的直接关联关系
- 验证搜索结果的详细信息

📊 返回信息：
- 节点的所有属性（名称、类型、注释、业务术语等）
- 直接关联的邻居节点摘要（可选）
- 节点在图谱中的位置信息

🔄 典型工作流：
1. 使用 search_metadata 获取node_id
2. 使用本工具查看详细信息
3. 根据需要使用 get_lineage 追溯血缘，或使用 find_path 探索关系路径

💡 提示：
- node_id 从搜索结果中获取
- include_neighbors=true 可以看到直接关联的节点
- 对于Field类型，会显示所属表信息
- 对于Table类型，会显示包含的字段列表''',
            input_schema={
                'type': 'object',
                'properties': {
                    'node_id': {
                        'type': 'integer', 
                        'description': '节点ID（从search_metadata等工具的返回结果中获取）'
                    },
                    'include_neighbors': {
                        'type': 'boolean', 
                        'default': True, 
                        'description': '是否包含邻居节点摘要。true=显示直接关联的节点（推荐），false=仅显示节点自身属性'
                    }
                },
                'required': ['node_id']
            },
            handler=self._handle_get_node_details
        )

    
    def _register_path_discovery_tools(self):
        """注册路径发现工具"""
        # 7.5. get_lineage - 整合后的血缘工具
        self.register_tool(
            name='get_lineage',
            category='lineage',
            description='''【血缘工具】数据治理核心工具，追溯数据的业务归属和技术实现路径

🎯 使用场景：
- 了解数据的业务归属（属于哪个主题域、业务域、业务主题）
- 了解数据的技术位置（在哪个数据库、Schema、表中）
- 影响分析：变更某个数据时，需要了解其上下游关系
- 数据溯源：追踪数据的来源和流向

📋 三种血缘类型：

1️⃣ business（业务血缘）：
   - 路径：主题域 → 业务域 → 业务主题 → 逻辑实体
   - 适用：了解数据的业务分类和归属
   - 示例：查看"客户表"属于哪个业务域

2️⃣ technical（技术血缘）：
   - 路径：数据库 → Schema → 物理表 → 字段
   - 适用：了解数据的物理存储位置
   - 示例：查看"客户表"存储在哪个数据库

3️⃣ both（两者都返回）：
   - 同时返回业务血缘和技术血缘
   - 适用：全面了解数据的业务和技术上下文

🔄 典型工作流：
1. 使用 search_metadata 找到目标实体
2. 使用本工具获取血缘路径
3. 使用 get_node_details 查看路径中任意节点的详情

💡 提示：
- entity_name 可以是表名或字段名
- 如果有同名实体，建议指定 entity_type 精确匹配
- 字段级血缘需要指定 entity_type="Field"
- 血缘路径按层级结构返回，便于理解数据的组织方式''',
            input_schema={
                'type': 'object',
                'properties': {
                    'entity_name': {
                        'type': 'string',
                        'description': '实体名称：表名（如"T_CUSTOMER"）或字段名（如"CUSTOMER_ID"）'
                    },
                    'lineage_type': {
                        'type': 'string',
                        'enum': ['business', 'technical', 'both'],
                        'description': '血缘类型：business=业务血缘（主题域→业务域→业务主题→逻辑实体），technical=技术血缘（数据库→Schema→物理表），both=同时返回两种血缘（推荐）'
                    },
                    'entity_type': {
                        'type': 'string',
                        'enum': ['LogicalEntity', 'PhysicalTable', 'Field'],
                        'description': '实体类型（可选）：LogicalEntity=逻辑实体，PhysicalTable=物理表，Field=字段。用于精确匹配同名实体'
                    }
                },
                'required': ['entity_name']
            },
            handler=self._handle_get_lineage
        )
        
        # 7.6. find_path - 整合后的路径发现工具
        self.register_tool(
            name='find_path',
            category='relationship',
            description='''【关系工具】发现元数据之间的关联关系路径

🎯 使用场景：
- 探索两个资产之间的关联关系
- 发现数据资产的关系网络
- 分析资产间的依赖关系
- 按特定关系类型查找相关资产

📋 三种查找模式：

1️⃣ shortest（最短路径）：
   - 查找两个节点之间的最短关联路径
   - 必需参数：start_node_id, end_node_id, mode="shortest"
   - 适用：快速了解两个资产的关系
   - 示例：查找"客户表"和"订单表"之间的最短关联

2️⃣ all（所有路径）：
   - 查找两个节点之间的所有可能路径
   - 必需参数：start_node_id, end_node_id, mode="all"
   - 可选参数：max_depth（默认5，最大10）
   - 适用：全面分析两个资产的所有关联方式
   - 示例：查找"客户表"和"订单表"的所有关联路径

3️⃣ by_relationship（按关系类型查找）：
   - 查找通过特定关系类型关联的所有节点
   - 必需参数：start_node_id, relationship_type, mode="by_relationship"
   - 适用：查找特定关系的相关资产
   - 示例：查找"客户表"的所有"CONTAINS"关系（包含的字段）

🔄 典型工作流：
1. 使用 search_metadata 获取起始和目标节点的node_id
2. 使用本工具查找路径
3. 使用 get_node_details 查看路径中节点的详情

💡 提示：
- 常用关系类型：BELONGS_TO（归属）、CONTAINS（包含）、MAPS_TO（映射）、HAS_FIELD（有字段）
- max_depth 越大，查询时间越长，建议从小值开始
- shortest模式最快，适合快速探索
- by_relationship模式可以发现特定类型的关联网络''',
            input_schema={
                'type': 'object',
                'properties': {
                    'start_node_id': {
                        'type': 'integer',
                        'description': '起始节点ID（从search_metadata等工具获取）'
                    },
                    'end_node_id': {
                        'type': 'integer',
                        'description': '目标节点ID（shortest和all模式必需，by_relationship模式不需要）'
                    },
                    'mode': {
                        'type': 'string',
                        'enum': ['shortest', 'all', 'by_relationship'],
                        'description': '查找模式：shortest=最短路径（最快），all=所有路径（全面），by_relationship=按关系类型查找（定向）'
                    },
                    'relationship_type': {
                        'type': 'string',
                        'description': '关系类型（仅by_relationship模式使用）。常用值：BELONGS_TO、CONTAINS、MAPS_TO、HAS_FIELD、PART_OF'
                    },
                    'max_depth': {
                        'type': 'integer',
                        'default': 5,
                        'description': '最大搜索深度（仅all模式使用），默认5，最大10。深度越大查询越慢'
                    }
                },
                'required': ['start_node_id']
            },
            handler=self._handle_find_path
        )
        

        
        # 13. get_subgraph
        self.register_tool(
            name='get_subgraph',
            category='relationship',
            description='''【关系工具】获取以指定节点为中心的子图结构，探索局部关系网络

🎯 使用场景：
- 探索某个资产周围的关系网络
- 了解资产的上下文环境
- 发现相关的数据资产
- 可视化局部数据架构

📊 返回信息：
- 中心节点及其周围指定深度内的所有节点
- 节点之间的关系
- 可按节点类型过滤，只返回感兴趣的节点

🔄 典型工作流：
1. 使用 search_metadata 找到中心节点的node_id
2. 使用本工具获取子图（depth=1或2）
3. 使用 get_node_details 查看子图中任意节点的详情

💡 提示：
- depth=1：仅直接关联的节点（最快）
- depth=2：包含二度关联的节点（推荐）
- depth=3+：关系网络较大，查询较慢
- node_types 过滤可以减少结果数量，如只看表：["PhysicalTable", "LogicalEntity"]
- 适合探索"这个表周围有哪些相关的表和字段"这类问题''',
            input_schema={
                'type': 'object',
                'properties': {
                    'node_id': {
                        'type': 'integer', 
                        'description': '中心节点ID（从search_metadata等工具获取）'
                    },
                    'depth': {
                        'type': 'integer', 
                        'default': 2, 
                        'description': '子图深度：1=直接关联，2=二度关联（推荐），3+=更大范围。深度越大结果越多，查询越慢'
                    },
                    'node_types': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': '节点类型过滤（可选），只返回指定类型的节点。示例：["PhysicalTable", "LogicalEntity"]只返回表，["Field"]只返回字段'
                    }
                },
                'required': ['node_id']
            },
            handler=self._handle_get_subgraph
        )
    
    def register_tool(self, name: str, description: str, input_schema: Dict[str, Any], 
                     handler: Callable, category: str = None):
        """
        注册工具
        
        Args:
            name: 工具名称
            description: 工具描述
            input_schema: 输入schema
            handler: 处理函数
            category: 工具分类（可选）
        """
        tool_def = {
            'name': name,
            'description': description,
            'inputSchema': input_schema
        }
        if category:
            tool_def['category'] = category
        
        self.tools[name] = tool_def
        self.tool_handlers[name] = handler
        self.logger.debug(f"注册工具: {name}")
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        列出所有工具
        
        Returns:
            List: 工具列表
        """
        enabled_tools = self.mcp_config.get('mcp', {}).get('enabled_tools', [])
        
        if enabled_tools:
            # 只返回启用的工具
            return [tool for name, tool in self.tools.items() if name in enabled_tools]
        else:
            # 返回所有工具
            return list(self.tools.values())
    
    def _create_mcp_response(self, data: Any) -> Dict[str, Any]:
        """
        创建MCP标准响应格式
        
        Args:
            data: 要返回的数据
            
        Returns:
            Dict: MCP标准格式的响应
        """
        import json
        return {
            'content': [
                {
                    'type': 'text',
                    'text': json.dumps(data, ensure_ascii=False, indent=2)
                }
            ]
        }
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        调用工具
        
        Args:
            tool_name: 工具名称
            arguments: 工具参数
            
        Returns:
            Any: 工具执行结果
        """
        if tool_name not in self.tool_handlers:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        handler = self.tool_handlers[tool_name]
        self.logger.debug(f"调用工具: {tool_name}, 参数: {arguments}")
        
        try:
            result = handler(arguments)
            return result
        except Exception as e:
            self.logger.error(f"工具执行失败: {tool_name}, 错误: {e}")
            raise
    
    # 工具处理函数 - 探索式检索工具（任务 8）
    def _handle_get_graph_overview(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """处理get_graph_overview工具"""
        stats = self.query_executor.get_graph_statistics()
        formatted_stats = self.result_formatter.format_statistics(stats)
        return self._create_mcp_response(formatted_stats)
    

    
    def _handle_search_metadata(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理search_metadata工具 - 整合keyword、attribute、exact三种搜索模式
        
        Args:
            arguments: 工具参数
            
        Returns:
            Dict: MCP响应
        """
        mode = arguments.get('mode', 'keyword')
        offset = arguments.get('offset', 0)
        limit = arguments.get('limit', 20)
        
        # 根据mode参数调用不同的搜索逻辑
        if mode == 'keyword':
            # 关键词搜索模式
            query = arguments.get('query')
            if not query:
                return self._create_mcp_response({
                    'error': 'Missing required parameter: query (for mode=keyword)'
                })
            
            node_types = arguments.get('node_types')
            results = self.query_executor.search_nodes_by_keyword(
                query, node_types, offset, limit
            )
            
        elif mode == 'attribute':
            # 属性搜索模式
            node_type = arguments.get('node_type')
            attribute_name = arguments.get('attribute_name')
            query = arguments.get('query')
            
            if not node_type or not attribute_name or not query:
                return self._create_mcp_response({
                    'error': 'Missing required parameters for mode=attribute: node_type, attribute_name, query'
                })
            
            results = self.query_executor.search_nodes_by_attribute(
                node_type, attribute_name, query, offset, limit
            )
            
        elif mode == 'exact':
            # 精确匹配模式
            query = arguments.get('query')
            node_type = arguments.get('node_type')
            
            if not query or not node_type:
                return self._create_mcp_response({
                    'error': 'Missing required parameters for mode=exact: query, node_type'
                })
            
            result = self.query_executor.get_node_by_name_and_type(query, node_type)
            
            if result:
                # 精确匹配返回单个结果，包装成列表格式
                results = [result]
            else:
                results = []
        
        else:
            return self._create_mcp_response({
                'error': f'Invalid mode: {mode}. Must be one of: keyword, attribute, exact'
            })
        
        # 为Field类型节点添加table_name（需求5.2）
        enriched_results = []
        for result in results:
            node_type = result.get('type') or (result.get('labels', [None])[0] if isinstance(result.get('labels'), list) else None)
            if node_type == 'Field':
                # 使用context_enricher为Field节点添加table_name
                result = self.context_enricher.enrich_field_result(result)
            enriched_results.append(result)
        
        # 格式化分页结果
        formatted_results = self.result_formatter.format_paginated_results(
            enriched_results, offset, limit
        )
        
        return self._create_mcp_response(formatted_results)

    
    def _handle_get_node_details(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """处理get_node_details工具"""
        node_id = arguments['node_id']
        include_neighbors = arguments.get('include_neighbors', True)
        
        # 获取节点信息
        node_data = self.query_executor.get_node_by_id(node_id)
        if not node_data:
            return self._create_mcp_response({'error': f'Node not found: {node_id}'})
        
        # 根据参数决定是否获取邻居节点
        neighbors = []
        if include_neighbors:
            neighbors = self.query_executor.get_node_neighbors(node_id, depth=1)
        
        formatted_result = self.result_formatter.format_node_details(node_data, neighbors, include_neighbors)
        return self._create_mcp_response(formatted_result)

    
    # 工具处理函数 - 路径发现工具（任务 9）
    
    def _handle_get_lineage(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理get_lineage工具 - 整合business和technical血缘查询
        
        Args:
            arguments: 工具参数
            
        Returns:
            Dict: MCP响应
        """
        entity_name = arguments['entity_name']
        lineage_type = arguments.get('lineage_type', 'both')
        entity_type = arguments.get('entity_type')
        
        result_data = {}
        
        # 根据lineage_type参数调用不同的血缘查询
        if lineage_type in ['business', 'both']:
            # 业务血缘查询
            business_results = self.query_executor.get_business_lineage(entity_name, entity_type)
            
            if business_results:
                result_data['business_lineage'] = self.result_formatter.format_path_list(business_results)
            else:
                result_data['business_lineage'] = {
                    'paths': [],
                    'message': f'No business lineage found for: {entity_name}'
                }
        
        if lineage_type in ['technical', 'both']:
            # 技术血缘查询
            technical_results = self.query_executor.get_technical_lineage(entity_name, entity_type)
            
            if technical_results:
                result_data['technical_lineage'] = self.result_formatter.format_path_list(technical_results)
            else:
                result_data['technical_lineage'] = {
                    'paths': [],
                    'message': f'No technical lineage found for: {entity_name}'
                }
        
        # 如果两种血缘都没有找到，返回错误
        if lineage_type == 'both':
            if not result_data.get('business_lineage', {}).get('paths') and \
               not result_data.get('technical_lineage', {}).get('paths'):
                result_data = {
                    'error': f'No lineage found for: {entity_name}',
                    'suggestion': 'Try searching for the entity first using search_metadata tool'
                }
        elif lineage_type == 'business':
            if not result_data.get('business_lineage', {}).get('paths'):
                result_data = {
                    'error': f'No business lineage found for: {entity_name}',
                    'suggestion': 'Verify the entity exists and has business lineage relationships'
                }
        elif lineage_type == 'technical':
            if not result_data.get('technical_lineage', {}).get('paths'):
                result_data = {
                    'error': f'No technical lineage found for: {entity_name}',
                    'suggestion': 'Verify the entity exists and has technical lineage relationships'
                }
        
        return self._create_mcp_response(result_data)
    
    def _handle_find_path(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理find_path工具 - 整合shortest、all、by_relationship三种模式
        
        Args:
            arguments: 工具参数
            
        Returns:
            Dict: MCP响应
        """
        start_node_id = arguments['start_node_id']
        mode = arguments.get('mode', 'shortest')
        
        # 根据mode参数调用不同的路径查找逻辑
        if mode == 'shortest':
            # 最短路径模式
            end_node_id = arguments.get('end_node_id')
            if not end_node_id:
                return self._create_mcp_response({
                    'error': 'Missing required parameter: end_node_id (for mode=shortest)'
                })
            
            result = self.query_executor.find_shortest_path(start_node_id, end_node_id)
            
            if result:
                formatted_result = self.result_formatter.format_path(result)
            else:
                formatted_result = {
                    'error': 'No path found between the specified nodes',
                    'suggestion': 'Try using mode=all to find alternative paths or verify the node IDs exist'
                }
        
        elif mode == 'all':
            # 所有路径模式
            end_node_id = arguments.get('end_node_id')
            if not end_node_id:
                return self._create_mcp_response({
                    'error': 'Missing required parameter: end_node_id (for mode=all)'
                })
            
            max_depth = arguments.get('max_depth', 5)
            
            # 检查深度限制
            if not self.result_formatter.check_depth_limit(max_depth):
                max_allowed = self.result_formatter.get_max_depth()
                formatted_result = {
                    'error': f'Max depth exceeded. Maximum allowed depth is {max_allowed}, requested {max_depth}'
                }
            else:
                results = self.query_executor.find_all_paths(start_node_id, end_node_id, max_depth)
                
                if results:
                    formatted_result = self.result_formatter.format_path_list(results)
                else:
                    formatted_result = {
                        'error': 'No paths found between the specified nodes',
                        'suggestion': 'Try increasing max_depth or verify the node IDs exist'
                    }
        
        elif mode == 'by_relationship':
            # 按关系类型查找模式
            relationship_type = arguments.get('relationship_type')
            if not relationship_type:
                return self._create_mcp_response({
                    'error': 'Missing required parameter: relationship_type (for mode=by_relationship)'
                })
            
            results = self.query_executor.discover_related_by_relationship(
                start_node_id, relationship_type
            )
            
            if results:
                formatted_result = {
                    'related_nodes': self.result_formatter.format_node_list(results),
                    'count': len(results),
                    'relationship_type': relationship_type
                }
            else:
                formatted_result = {
                    'related_nodes': [],
                    'count': 0,
                    'message': f'No nodes found with relationship type: {relationship_type}',
                    'suggestion': 'Verify the relationship type exists or try a different relationship'
                }
        
        else:
            return self._create_mcp_response({
                'error': f'Invalid mode: {mode}. Must be one of: shortest, all, by_relationship'
            })
        
        return self._create_mcp_response(formatted_result)

    
    def _handle_get_subgraph(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """处理get_subgraph工具"""
        node_id = arguments['node_id']
        depth = arguments.get('depth', 2)
        node_types = arguments.get('node_types')
        
        # 检查深度限制
        if not self.result_formatter.check_depth_limit(depth):
            max_allowed = self.result_formatter.get_max_depth()
            error_result = {
                'error': f'Max depth exceeded. Maximum allowed depth is {max_allowed}, requested {depth}'
            }
            return self._create_mcp_response(error_result)
        
        subgraph_data = self.query_executor.get_subgraph(node_id, depth, node_types)
        formatted_result = self.result_formatter.format_subgraph(subgraph_data)
        return self._create_mcp_response(formatted_result)
    
    def _register_inference_tools(self):
        """注册推理工具"""
        # infer_relationships - 整合后的推理工具
        self.register_tool(
            name='infer_relationships',
            category='inference',
            description='''【推理工具】基于业务术语和结构相似性推理元数据之间的潜在关联

🎯 使用场景：
- 发现未显式建模的数据关系
- 识别可能的外键关系
- 查找业务相关的字段
- 数据质量检查：发现命名不一致的相关字段

📋 两种推理目标：

1️⃣ fields（字段关联推理）：
   - 基于业务术语精确匹配（confidence=1.0）
   - 基于字段名相似性推理（confidence<1.0）
   - 必需参数：target="fields", source_id或source_name
   - 可选参数：business_term（指定业务术语进行精确匹配）
   - 示例：查找与"CUSTOMER_ID"相关的其他字段

2️⃣ tables（表关系推理）：
   - 推理潜在的外键关系（字段名匹配主键模式）
   - 推理结构相似的表（字段组成相似）
   - 必需参数：target="tables", source_id或source_name
   - 示例：查找与"客户表"可能有关联的其他表

🔄 典型工作流：
1. 使用 search_metadata 找到源节点的node_id
2. 使用本工具进行推理（设置合适的threshold）
3. 使用 get_node_details 验证推理结果的合理性

💡 提示：
- threshold=0.7（默认）：平衡精度和召回率
- threshold=1.0：仅返回精确匹配（业务术语完全相同）
- threshold=0.5：返回更多可能的关联（包含较弱的相似性）
- 推理结果包含confidence和evidence，说明推理依据
- 推理不保证100%准确，需要人工验证''',
            input_schema={
                'type': 'object',
                'properties': {
                    'target': {
                        'type': 'string',
                        'enum': ['fields', 'tables'],
                        'description': '推理目标：fields=字段关联推理（查找相关字段），tables=表关系推理（查找可能关联的表）'
                    },
                    'source_id': {
                        'type': 'integer',
                        'description': '源节点ID（从search_metadata获取）。与source_name二选一，优先使用source_id'
                    },
                    'source_name': {
                        'type': 'string',
                        'description': '源节点名称（字段名或表名）。与source_id二选一，当不知道ID时使用'
                    },
                    'business_term': {
                        'type': 'string',
                        'description': '业务术语（仅用于fields推理，可选）。指定后会查找具有相同业务术语的字段（精确匹配）'
                    },
                    'threshold': {
                        'type': 'number',
                        'default': 0.7,
                        'description': '相似度阈值（0.0-1.0）。1.0=仅精确匹配，0.7=平衡（推荐），0.5=包含较弱相似性。阈值越低，结果越多但准确性越低'
                    }
                },
                'required': ['target']
            },
            handler=self._handle_infer_relationships
        )
    
    def _handle_infer_relationships(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理infer_relationships工具 - 整合字段关联推理和表关系推理
        
        Args:
            arguments: 工具参数
            
        Returns:
            Dict: MCP响应
        """
        target = arguments['target']
        source_id = arguments.get('source_id')
        source_name = arguments.get('source_name')
        threshold = arguments.get('threshold', 0.7)
        
        # 验证参数
        if not source_id and not source_name:
            return self._create_mcp_response({
                'error': 'Missing required parameter: either source_id or source_name must be provided',
                'suggestion': 'Provide either source_id (node ID) or source_name (node name)'
            })
        
        # 根据target参数调用不同的推理逻辑
        if target == 'fields':
            # 字段关联推理
            business_term = arguments.get('business_term')
            
            try:
                inference_results = self.inference_engine.infer_related_fields(
                    field_id=source_id,
                    field_name=source_name,
                    business_term=business_term,
                    threshold=threshold
                )
                
                # 格式化结果
                formatted_results = [result.to_dict() for result in inference_results]
                
                result_data = {
                    'target': 'fields',
                    'inferences': formatted_results,
                    'count': len(formatted_results),
                    'threshold': threshold
                }
                
                if not formatted_results:
                    result_data['message'] = 'No related fields found with the specified threshold'
                    result_data['suggestion'] = 'Try lowering the threshold or verify the source field exists'
                
            except Exception as e:
                self.logger.error(f"字段关联推理失败: {e}")
                result_data = {
                    'error': f'Field inference failed: {str(e)}',
                    'suggestion': 'Verify the source field ID or name is valid'
                }
        
        elif target == 'tables':
            # 表关系推理
            try:
                inference_results = self.inference_engine.infer_table_relationships(
                    table_id=source_id,
                    table_name=source_name,
                    threshold=threshold
                )
                
                # 格式化结果
                formatted_results = [result.to_dict() for result in inference_results]
                
                result_data = {
                    'target': 'tables',
                    'inferences': formatted_results,
                    'count': len(formatted_results),
                    'threshold': threshold
                }
                
                if not formatted_results:
                    result_data['message'] = 'No related tables found with the specified threshold'
                    result_data['suggestion'] = 'Try lowering the threshold or verify the source table exists'
                
            except Exception as e:
                self.logger.error(f"表关系推理失败: {e}")
                result_data = {
                    'error': f'Table inference failed: {str(e)}',
                    'suggestion': 'Verify the source table ID or name is valid'
                }
        
        else:
            result_data = {
                'error': f'Invalid target: {target}. Must be one of: fields, tables'
            }
        
        return self._create_mcp_response(result_data)
