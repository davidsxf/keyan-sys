from ninja import Schema
from typing import List, Optional
from datetime import datetime

class CategoryIn(Schema):
    name: str
    parent_id: Optional[int] = None
    weight: int = 0
    sort_order: int = 0

class CategoryOut(Schema):
    id: int
    name: str
    parent_id: Optional[int]
    weight: int
    sort_order: int
    children: List['CategoryOut'] = []
    
# 解决自引用问题
CategoryOut.update_forward_refs()


## orgs 机构
class OrgIn(Schema):
    """组织创建/更新输入结构"""
    name: str
    description: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    org_type: Optional[str] = None

class OrgOut(Schema):
    """组织输出结构"""
    id: int
    name: str
    description: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    org_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class Message(Schema):
    """通用消息响应"""
    message: str
    success: bool