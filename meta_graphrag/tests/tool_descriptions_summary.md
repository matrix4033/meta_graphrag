# 工具描述和分类总结 (Task 12.1)

## 概述

本文档总结了所有MCP工具的category字段和增强的description，确保符合以下要求：
- 所有工具都有category字段（overview、search、detail、lineage、relationship、inference）
- 所有description限制在200字符内
- 包含使用场景和后续工具建议
- 使用一致的中文术语

## 工具列表

### 1. get_graph_overview
- **分类**: overview (概览工具)
- **描述**: [概览工具] 获取图谱整体结构统计，包括节点类型、关系类型数量及主题域分布。数据治理的入口工具。后续可用：search_metadata定位资产
- **字符数**: 72
- **使用场景**: 数据治理的入口工具，了解图谱整体结构
- **后续工具**: search_metadata

### 2. search_metadata
- **分类**: search (搜索工具)
- **描述**: [搜索工具] 统一的元数据搜索入口，支持关键词、属性、精确匹配三种模式定位元数据资产。后续可用：get_node_details查看详情，get_lineage追溯血缘
- **字符数**: 84
- **使用场景**: 根据关键词或属性定位元数据资产
- **后续工具**: get_node_details, get_lineage
- **搜索模式**:
  - keyword: 关键词搜索
  - attribute: 属性搜索
  - exact: 精确匹配

### 3. get_node_details
- **分类**: detail (详情工具)
- **描述**: [详情工具] 获取单个元数据资产的完整属性和直接关联的邻居节点摘要。后续可用：get_lineage追溯血缘，find_path发现关系路径，get_subgraph查看子图
- **字符数**: 87
- **使用场景**: 获取单个元数据资产的完整属性和直接关联
- **后续工具**: get_lineage, find_path, get_subgraph

### 4. get_lineage
- **分类**: lineage (血缘工具)
- **描述**: [血缘工具] 数据治理核心工具，追溯数据的业务归属和技术实现路径。支持业务血缘、技术血缘及字段级血缘。后续可用：get_node_details查看路径节点详情
- **字符数**: 80
- **使用场景**: 数据治理核心工具，追溯数据的业务归属和技术实现路径
- **后续工具**: get_node_details
- **血缘类型**:
  - business: 业务血缘
  - technical: 技术血缘
  - both: 两者都返回

### 5. find_path
- **分类**: relationship (关系工具)
- **描述**: [关系工具] 发现元数据之间的关联关系路径，支持最短路径、所有路径和按关系类型查找三种模式。后续可用：get_node_details查看路径节点详情
- **字符数**: 75
- **使用场景**: 发现元数据之间的关联关系路径
- **后续工具**: get_node_details
- **查找模式**:
  - shortest: 最短路径
  - all: 所有路径
  - by_relationship: 按关系类型查找

### 6. get_subgraph
- **分类**: relationship (关系工具)
- **描述**: [关系工具] 获取以指定节点为中心的子图结构，可按节点类型过滤。用于探索局部关系网络。后续可用：get_node_details查看子图节点详情
- **字符数**: 72
- **使用场景**: 探索局部关系网络
- **后续工具**: get_node_details

### 7. infer_relationships
- **分类**: inference (推理工具)
- **描述**: [推理工具] 基于业务术语和结构相似性推理元数据之间的潜在关联，支持字段关联和表关系推理。发现隐藏的数据关系。后续可用：get_node_details验证推理结果
- **字符数**: 82
- **使用场景**: 推理元数据之间的潜在关联，发现隐藏的数据关系
- **后续工具**: get_node_details
- **推理目标**:
  - fields: 字段关联推理
  - tables: 表关系推理

## 工具分类统计

- **overview (概览工具)**: 1个工具
  - get_graph_overview
  
- **search (搜索工具)**: 1个工具
  - search_metadata
  
- **detail (详情工具)**: 1个工具
  - get_node_details
  
- **lineage (血缘工具)**: 1个工具
  - get_lineage
  
- **relationship (关系工具)**: 2个工具
  - find_path
  - get_subgraph
  
- **inference (推理工具)**: 1个工具
  - infer_relationships

## 术语一致性

所有工具描述使用以下标准中文术语：
- 元数据/元数据资产
- 节点
- 关系/关联
- 血缘/血缘路径
- 主题域
- 物理表
- 字段
- 业务术语
- 数据治理

## 验证结果

✓ 所有7个工具都有有效的category字段
✓ 所有description长度都在200字符以内（最长87字符）
✓ 所有工具都包含分类标签
✓ 所有工具的inputSchema都包含完整的参数描述
✓ 所有工具都使用一致的中文术语

## 需求覆盖

本实现满足以下需求：
- **需求 1.1**: 每个工具提供包含功能分类、用途说明、输入参数、输出格式的完整描述 ✓
- **需求 1.2**: 工具按数据治理场景分为六个类别 ✓
- **需求 1.3**: 工具描述明确说明每个参数的类型、是否必需、默认值和取值范围 ✓
- **需求 1.4**: 工具描述包含典型使用场景和推荐的后续工具调用 ✓
- **需求 1.5**: 工具描述使用一致的中文术语 ✓
- **需求 7.3**: 工具描述简洁明了，单个工具的description字段不超过200个字符 ✓
