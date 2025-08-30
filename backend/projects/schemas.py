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
    type_id: Optional[int] = None
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
    type_id: Optional[int] = None
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
    type_id: Optional[int] = None
    leader_id: Optional[int] = None
    undertake: Optional[str] = None
