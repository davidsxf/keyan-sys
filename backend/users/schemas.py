from ninja import Schema
from typing import List, Optional
from datetime import datetime

class DepartmentIn(Schema):
    """部门创建/更新输入结构"""
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None  # 用于指定父部门ID

class DepartmentOut(Schema):
    """部门输出结构（包含可能的子部门）"""
    id: int
    name: str
    description: Optional[str]
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    children: List['DepartmentOut'] = []  # 子部门列表

# 解决 Schema 自引用问题
DepartmentOut.update_forward_refs()
