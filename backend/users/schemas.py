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


# from ninja import Schema
# from typing import Optional, List
# from datetime import datetime


class TeamIn(Schema):
    """团队创建/更新输入结构"""
    name: str
    description: Optional[str] = None
    department_id: Optional[int] = None  # 用于指定所属部门ID


class TeamOut(Schema):
    """团队输出结构"""
    id: int
    name: str
    description: Optional[str]
    department_id: Optional[int]
    department_name: Optional[str]  # 部门名称
    created_at: datetime
    updated_at: datetime
