"""MCP数据模型类"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class EnhancedNodeResult:
    """增强的节点结果"""
    id: int
    type: str
    name: str
    properties: Dict[str, Any]
    business_context: Optional[Dict[str, Any]] = None


@dataclass
class PaginationInfo:
    """分页信息"""
    total: int
    offset: int
    limit: int
    has_more: bool


@dataclass
class EnhancedListResult:
    """增强的列表结果"""
    items: List[Dict[str, Any]]
    pagination: PaginationInfo
    summary: Optional[str] = None
    next_action: Optional[str] = None


@dataclass
class ErrorResponse:
    """错误响应"""
    code: str
    message: str
    details: List[Dict[str, Any]] = field(default_factory=list)
    example: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        result = {
            'error': {
                'code': self.code,
                'message': self.message,
                'details': self.details
            }
        }
        if self.example:
            result['error']['example'] = self.example
        return result


@dataclass
class InferenceResult:
    """推理结果"""
    source_id: int
    target_id: int
    inference_type: str
    confidence: float
    evidence: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'source_id': self.source_id,
            'target_id': self.target_id,
            'inference_type': self.inference_type,
            'confidence': self.confidence,
            'evidence': self.evidence
        }
