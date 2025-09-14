from typing import Optional, List
from datetime import date, datetime
from ninja import Schema
from django.utils.translation import gettext_lazy as _


class ProjectIn(Schema):
    title: str
    number: str
    funding_number: Optional[str] = None
    leader_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    category_id: Optional[int] = None
    type: Optional[str] = None
    budget: Optional[float] = None
    research_area: Optional[str] = None
    source_id: Optional[int] = None
    undertake: str
    remark: Optional[str] = None


class ProjectOut(Schema):
    id: int
    title: str
    number: str
    funding_number: Optional[str] = None
    leader_id: Optional[int] = None
    leader_name: Optional[str] = None  # 负责人姓名
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    status_display: str  # 状态显示值
    category_id: Optional[int] = None
    category_name: Optional[str] = None  # 类别名称
    type: Optional[str] = None  # 类型
    type_name: Optional[str] = None  # 类型名称
    budget: Optional[float] = None
    research_area: Optional[str] = None
    source_id: Optional[int] = None
    source_name: Optional[str] = None  # 来源单位名称
    undertake: str
    undertake_display: str  # 承担方式显示值
    remark: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    


class ProjectFilter(Schema):
    title: Optional[str] = None
    number: Optional[str] = None
    status: Optional[str] = None
    category_id: Optional[int] = None
    type: Optional[str] = None
    leader_id: Optional[int] = None
    undertake: Optional[str] = None
    source: Optional[str] = None
    # 添加缺失的日期字段
    start_date: Optional[date] = None
    end_date: Optional[date] = None



#预算
class ProjectBudgetIn(Schema):
    project_id: int
    name: str
    amount: Optional[float] = None
    year: Optional[int] = None
    type: str
    remark: Optional[str] = None


class ProjectBudgetOut(Schema):
    id: int
    project_id: int
    project_title: Optional[str] = None  # 项目标题
    name: str
    amount: Optional[float] = None
    year: Optional[int] = None
    type: str
    type_display: Optional[str] = None  # 类型显示值
    remark: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ProjectBudgetFilter(Schema):
    project_id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    year: Optional[int] = None
    # 日期范围筛选
    start_date: Optional[date] = None
    end_date: Optional[date] = None


# 在文件末尾添加

# 项目参与人员
class ProjectStaffIn(Schema):
    """项目参与人员创建/更新输入结构"""
    project_id: int
    staff_id: int
    role: str
    order: Optional[int] = None
    join_date: Optional[date] = None
    leave_date: Optional[date] = None

    remark: Optional[str] = None


class ProjectStaffOut(Schema):
    """项目参与人员输出结构"""
    id: int
    project_id: int
    project_title: Optional[str] = None
    staff_id: int
    staff_name: Optional[str] = None
    staff_department: Optional[str] = None
    role: str
    role_display: Optional[str] = None
    order: Optional[int] = None
    join_date: Optional[date] = None
    leave_date: Optional[date] = None
    
    remark: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ProjectStaffFilter(Schema):
    """项目参与人员筛选结构"""
    project_id: Optional[int] = None
    staff_id: Optional[int] = None
    staff_name: Optional[str] = None
    role: Optional[str] = None
  


# Import necessary modules
from ninja import Schema, UploadedFile
from typing import Optional


class ProjectDocumentIn(Schema):
    project_id: int
    name: str
    file: UploadedFile  # Change from str to UploadedFile
    remark: Optional[str] = None


class ProjectDocumentOut(Schema):
    id: int
    project_id: int
    project_title: Optional[str] = None
    name: str
    file: str
    remark: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ProjectDocumentFilter(Schema):
    project_id: Optional[int] = None
    name: Optional[str] = None
