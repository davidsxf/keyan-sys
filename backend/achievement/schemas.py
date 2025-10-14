from pydantic import BaseModel

from datetime import datetime
from typing import Optional, List
from ninja import Schema
from django.utils.translation import gettext_lazy as _


class AuthorIn(Schema):
    """作者信息输入模型"""
    name: str
    email: Optional[str] = None
    staff_id: Optional[int] = None  # 关联员工ID
    external_organization: Optional[str] = None


class AuthorOut(Schema):
    """作者信息输出模型"""
    id: int
    name: str
    email: Optional[str] = None
    staff_id: Optional[int] = None  # 关联员工ID
    staff_name: Optional[str] = None  # 关联员工姓名
    external_organization: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class JournalIn(Schema):
    """期刊信息输入模型"""
    name: str
    issn: str
    jcr_quartile: Optional[str] = None
    impact_factor: Optional[float] = None


class JournalMetricIn(Schema):
    """期刊年度指标输入模型"""
    year: int
    jcr_quartile: Optional[str] = None
    impact_factor: Optional[float] = None


class JournalMetricOut(Schema):
    """期刊年度指标输出模型"""
    id: int
    journal_id: int
    year: int
    jcr_quartile: Optional[str] = None
    impact_factor: Optional[float] = None
    created_at: datetime
    updated_at: datetime


class JournalOut(Schema):
    """期刊信息输出模型"""
    id: int
    name: str
    issn: str
    jcr_quartile: Optional[str] = None
    impact_factor: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    metrics: Optional[List[JournalMetricOut]] = None  # 期刊所有年度指标


class PaperIn(Schema):
    """论文信息输入模型"""
    title: str
    first_author_ids: List[int]  # 第一作者ID列表
    corresponding_author_ids: List[int]  # 通讯作者ID列表
    journal_id: Optional[int] = None
    publication_year: int
    unit_ranking: int
    page_numbers: Optional[str] = None
    keywords: Optional[str] = None
    abstract: Optional[str] = None


class PaperOut(Schema):
    """论文信息输出模型"""
    id: int
    title: str
    first_authors: List[AuthorOut]  # 第一作者列表
    corresponding_authors: List[AuthorOut]  # 通讯作者列表
    journal: Optional[JournalOut] = None
    publication_year: int
    unit_ranking: int
    page_numbers: Optional[str] = None
    keywords: Optional[str] = None
    abstract: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class AuthorFilter(Schema):
    """作者过滤条件模型"""
    name: Optional[str] = None
    email: Optional[str] = None
    has_staff: Optional[bool] = None
    external_organization: Optional[str] = None


class JournalFilter(Schema):
    """期刊过滤条件模型"""
    name: Optional[str] = None
    issn: Optional[str] = None
    jcr_quartile: Optional[str] = None
    min_impact_factor: Optional[float] = None


class PaperFilter(Schema):
    """论文过滤条件模型"""
    title: Optional[str] = None
    author_id: Optional[int] = None
    journal_id: Optional[int] = None
    publication_year: Optional[int] = None
    min_publication_year: Optional[int] = None
    max_publication_year: Optional[int] = None



