from ninja import Schema
from typing import List, Optional
from datetime import datetime,date
from enum import Enum

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



class DepartmentOption(Schema):
    """部门选项"""
    id: int
    name: str




class TeamIn(Schema):
    """团队创建/更新输入结构"""
    name: str
    description: Optional[str] = None
    research_field: Optional[str] = None  # 研究领域
    department_id: Optional[int] = None  # 用于指定所属部门ID


class TeamOut(Schema):
    """团队输出结构"""
    id: int
    name: str
    description: Optional[str]
    research_field: Optional[str]  # 研究领域
    department_id: Optional[int]
    department_name: Optional[str]  # 部门名称
    created_at: datetime
    updated_at: datetime

class TeamOption(Schema):
    """团队选项"""
    id: int
    name: str

## 员工

class StaffStatus(str, Enum):
    ON_DUTY = "在职"
    OFF_DUTY = "离职"
    RETIRE = "退休"

class StaffIn(Schema):
    """员工创建/更新输入结构"""
    name: str
    gender: Optional[str] = "男"
    birthday: Optional[date] = None
    email: Optional[str] = None
    entry_date: Optional[date] = None
    department_id: Optional[int] = None
    team_id: Optional[int] = None
    position: Optional[str] = None
    is_team_leader: bool = False
    status: StaffStatus = StaffStatus.ON_DUTY
    phone: Optional[str] = None
    remark: Optional[str] = None

class StaffOut(Schema):
    """员工输出结构"""
    id: int
    name: str
    gender: Optional[str]
    birthday: Optional[date]
    email: Optional[str]
    entry_date: Optional[date]
    department_id: Optional[int]
    department_name: Optional[str]
    team_id: Optional[int]
    team_name: Optional[str]
    position: Optional[str]
    is_team_leader: bool
    status: str
    phone: Optional[str]
    remark: Optional[str]
    created_at: datetime
    updated_at: datetime

