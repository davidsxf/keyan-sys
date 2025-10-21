from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.errors import HttpError
from ninja import Router
from .models import Author, Journal, Paper
from .schemas import (
    AuthorIn, AuthorOut, JournalIn, JournalOut, PaperIn, PaperOut,
    AuthorFilter, JournalFilter, PaperFilter, JournalMetricIn, JournalMetricOut
)
from users.models import Staff

router = Router(tags=["achievement"])

# 作者相关接口
def _author_to_out(author: Author) -> AuthorOut:
    """将Author模型转换为AuthorOut输出模型"""
    author_data = AuthorOut.from_orm(author)
    if author.staff:
        author_data.staff_name = author.staff.name
    return author_data

@router.post("/authors/", response=AuthorOut)
def create_author(request, data: AuthorIn):
    """创建作者信息"""
    author_dict = data.dict()
    staff_id = author_dict.pop("staff_id", None)
    staff = None
    
    if staff_id:
        staff = get_object_or_404(Staff, id=staff_id)
        # 检查该员工是否已经有作者档案
        if Author.objects.filter(staff=staff).exists():
            raise HttpError(400, "该员工已有作者档案")
    
    author = Author.objects.create(staff=staff, **author_dict)
    return _author_to_out(author)

@router.get("/authors/", response=List[AuthorOut])
def list_authors(request, filters: AuthorFilter = None, skip: int = 0, limit: int = 100):
    """获取作者列表"""
    authors = Author.objects.all().order_by("name")
    
    # 应用过滤条件
    if filters:
        if filters.name:
            authors = authors.filter(name__icontains=filters.name)
        if filters.email:
            authors = authors.filter(email__icontains=filters.email)
        if filters.has_staff is not None:
            if filters.has_staff:
                authors = authors.filter(staff__isnull=False)
            else:
                authors = authors.filter(staff__isnull=True)
        if filters.external_organization:
            authors = authors.filter(external_organization__icontains=filters.external_organization)
    
    # 分页
    authors = authors[skip:skip + limit]
    
    # 转换为输出模型
    return [_author_to_out(author) for author in authors]

@router.get("/authors/{author_id}/", response=AuthorOut)
def get_author(request, author_id: int):
    """获取单个作者详情"""
    author = get_object_or_404(Author, id=author_id)
    return _author_to_out(author)

@router.put("/authors/{author_id}/", response=AuthorOut)
def update_author(request, author_id: int, data: AuthorIn):
    """更新作者信息"""
    author = get_object_or_404(Author, id=author_id)
    author_dict = data.dict()
    staff_id = author_dict.pop("staff_id", None)
    staff = None
    
    if staff_id:
        staff = get_object_or_404(Staff, id=staff_id)
        # 检查该员工是否已经有其他作者档案
        if Author.objects.filter(staff=staff).exclude(id=author_id).exists():
            raise HttpError(400, "该员工已有其他作者档案")
    
    # 更新作者信息
    for attr, value in author_dict.items():
        setattr(author, attr, value)
    author.staff = staff
    author.save()
    
    return _author_to_out(author)

@router.delete("/authors/{author_id}/", response={204: None})
def delete_author(request, author_id: int):
    """删除作者信息"""
    print(f"author_id: {author_id}")
    author = get_object_or_404(Author, id=author_id)
    # 检查是否有关联的论文
    if author.first_author_papers.exists() or author.corresponding_author_papers.exists():
        raise HttpError(400, "该作者关联了论文，无法删除")
    author.delete()
    return 204, None

def _journal_to_out(journal: Journal) -> JournalOut:
    """将Journal模型转换为JournalOut输出模型，包含年度指标"""
    journal_data = JournalOut.from_orm(journal)
    # 添加期刊的所有年度指标
    journal_data.metrics = [
        JournalMetricOut.from_orm(metric) for metric in journal.metrics.all()
    ]
    return journal_data

# 期刊相关接口
@router.post("/journals/", response=JournalOut)
def create_journal(request, data: JournalIn):
    """创建期刊信息"""
    # 检查ISSN是否已存在
    if Journal.objects.filter(issn=data.issn).exists():
        raise HttpError(400, "该ISSN已存在")
    
    journal = Journal.objects.create(**data.dict())
    return _journal_to_out(journal)

@router.get("/journals/", response=List[JournalOut])
def list_journals(request, filters: Optional[JournalFilter] = None, skip: int = 0, limit: int = 100):
    """获取期刊列表"""
    journals = Journal.objects.all().order_by("name")
    
    # 应用过滤条件
    if filters:
        if filters.name:
            journals = journals.filter(name__icontains=filters.name)
        if filters.issn:
            journals = journals.filter(issn__icontains=filters.issn)    
    # 分页
    journals = journals[skip:skip + limit]
    
    # 转换为输出模型，包含年度指标
    return [_journal_to_out(journal) for journal in journals]

@router.get("/journals/{journal_id}/", response=JournalOut)
def get_journal(request, journal_id: int):
    """获取单个期刊详情"""
    journal = get_object_or_404(Journal, id=journal_id)
    return _journal_to_out(journal)

@router.put("/journals/{journal_id}/", response=JournalOut)
def update_journal(request, journal_id: int, data: JournalIn):
    """更新期刊信息"""
    journal = get_object_or_404(Journal, id=journal_id)
    
    # 检查ISSN是否已被其他期刊使用
    if Journal.objects.filter(issn=data.issn).exclude(id=journal_id).exists():
        raise HttpError(400, "该ISSN已被其他期刊使用")
    
    for attr, value in data.dict().items():
        setattr(journal, attr, value)
    journal.save()
    return _journal_to_out(journal)

@router.delete("/journals/{journal_id}/", response={204: None})
def delete_journal(request, journal_id: int):
    """删除期刊信息"""
    journal = get_object_or_404(Journal, id=journal_id)
    # 检查是否有关联的论文
    if journal.papers.exists():
        raise HttpError(400, "该期刊关联了论文，无法删除")
    journal.delete()
    return 204, None

# 期刊年度指标相关接口
@router.post("/journals/{journal_id}/metrics/", response=JournalMetricOut)
def create_journal_metric(request, journal_id: int, data: JournalMetricIn):
    """创建期刊年度指标"""
    journal = get_object_or_404(Journal, id=journal_id)
    
    # 检查该年份的指标是否已存在
    if journal.metrics.filter(year=data.year).exists():
        raise HttpError(400, f"该期刊的{data.year}年指标已存在")
    
    metric = journal.metrics.create(**data.dict())
    return JournalMetricOut.from_orm(metric)

@router.get("/journals/{journal_id}/metrics/", response=List[JournalMetricOut])
def list_journal_metrics(request, journal_id: int):
    """获取期刊的所有年度指标"""
    journal = get_object_or_404(Journal, id=journal_id)
    metrics = journal.metrics.all().order_by('-year')
    return [JournalMetricOut.from_orm(metric) for metric in metrics]

@router.get("/journals/{journal_id}/metrics/{year}/", response=JournalMetricOut)
def get_journal_metric_by_year(request, journal_id: int, year: int):
    """获取特定年份的期刊指标"""
    journal = get_object_or_404(Journal, id=journal_id)
    metric = get_object_or_404(journal.metrics, year=year)
    return JournalMetricOut.from_orm(metric)

@router.put("/journals/{journal_id}/metrics/{year}/", response=JournalMetricOut)
def update_journal_metric(request, journal_id: int, year: int, data: JournalMetricIn):
    """更新期刊年度指标"""
    # 确保传入的年份与URL中的年份一致
    if data.year != year:
        raise HttpError(400, "请求数据中的年份与URL中的年份不一致")
    
    journal = get_object_or_404(Journal, id=journal_id)
    metric = get_object_or_404(journal.metrics, year=year)
    
    # 更新指标信息
    for attr, value in data.dict().items():
        setattr(metric, attr, value)
    metric.save()
    return JournalMetricOut.from_orm(metric)

@router.delete("/journals/{journal_id}/metrics/{year}/", response={204: None})
def delete_journal_metric(request, journal_id: int, year: int):
    """删除期刊年度指标"""
    journal = get_object_or_404(Journal, id=journal_id)
    metric = get_object_or_404(journal.metrics, year=year)
    metric.delete()
    return 204, None

# 论文相关接口
def _paper_to_out(paper: Paper) -> PaperOut:
    """将Paper模型转换为PaperOut输出模型"""
    paper_data = PaperOut.from_orm(paper)
    # 处理第一作者
    paper_data.first_authors = [_author_to_out(author) for author in paper.first_authors.all()]
    # 处理通讯作者
    paper_data.corresponding_authors = [_author_to_out(author) for author in paper.corresponding_authors.all()]
    return paper_data

@router.post("/papers/", response=PaperOut)
def create_paper(request, data: PaperIn):
    """创建论文信息"""
    paper_dict = data.dict()
    
    # 提取并验证作者ID
    first_author_ids = paper_dict.pop("first_author_ids")
    corresponding_author_ids = paper_dict.pop("corresponding_author_ids")
    journal_id = paper_dict.pop("journal_id", None)
    
    # 验证作者存在
    first_authors = []
    for author_id in first_author_ids:
        author = get_object_or_404(Author, id=author_id)
        first_authors.append(author)
    
    corresponding_authors = []
    for author_id in corresponding_author_ids:
        author = get_object_or_404(Author, id=author_id)
        corresponding_authors.append(author)
    
    # 验证期刊存在
    journal = None
    if journal_id:
        journal = get_object_or_404(Journal, id=journal_id)
    
    # 创建论文
    paper = Paper.objects.create(journal=journal, **paper_dict)
    
    # 设置多对多关系
    paper.first_authors.set(first_authors)
    paper.corresponding_authors.set(corresponding_authors)
    
    return _paper_to_out(paper)

@router.get("/papers/", response=List[PaperOut])
def list_papers(request, filters: PaperFilter = None, skip: int = 0, limit: int = 100):
    """获取论文列表"""
    papers = Paper.objects.all().order_by("-publication_year", "title")
    
    # 应用过滤条件
    if filters:
        if filters.title:
            papers = papers.filter(title__icontains=filters.title)
        if filters.author_id:
            papers = papers.filter(
                Q(first_authors__id=filters.author_id) | 
                Q(corresponding_authors__id=filters.author_id)
            ).distinct()
        if filters.journal_id:
            papers = papers.filter(journal_id=filters.journal_id)
        if filters.publication_year:
            papers = papers.filter(publication_year=filters.publication_year)
        if filters.min_publication_year is not None:
            papers = papers.filter(publication_year__gte=filters.min_publication_year)
        if filters.max_publication_year is not None:
            papers = papers.filter(publication_year__lte=filters.max_publication_year)
    
    # 分页
    papers = papers[skip:skip + limit]
    
    # 转换为输出模型
    return [_paper_to_out(paper) for paper in papers]

@router.get("/papers/{paper_id}/", response=PaperOut)
def get_paper(request, paper_id: int):
    """获取单个论文详情"""
    paper = get_object_or_404(Paper, id=paper_id)
    return _paper_to_out(paper)

@router.put("/papers/{paper_id}/", response=PaperOut)
def update_paper(request, paper_id: int, data: PaperIn):
    """更新论文信息"""
    paper = get_object_or_404(Paper, id=paper_id)
    paper_dict = data.dict()
    
    # 提取并验证作者ID
    first_author_ids = paper_dict.pop("first_author_ids")
    corresponding_author_ids = paper_dict.pop("corresponding_author_ids")
    journal_id = paper_dict.pop("journal_id", None)
    
    # 验证作者存在
    first_authors = []
    for author_id in first_author_ids:
        author = get_object_or_404(Author, id=author_id)
        first_authors.append(author)
    
    corresponding_authors = []
    for author_id in corresponding_author_ids:
        author = get_object_or_404(Author, id=author_id)
        corresponding_authors.append(author)
    
    # 验证期刊存在
    journal = None
    if journal_id:
        journal = get_object_or_404(Journal, id=journal_id)
    
    # 更新论文信息
    for attr, value in paper_dict.items():
        setattr(paper, attr, value)
    paper.journal = journal
    paper.save()
    
    # 更新多对多关系
    paper.first_authors.set(first_authors)
    paper.corresponding_authors.set(corresponding_authors)
    
    return _paper_to_out(paper)

@router.delete("/papers/{paper_id}/", response={204: None})
def delete_paper(request, paper_id: int):
    """删除论文信息"""
    paper = get_object_or_404(Paper, id=paper_id)
    paper.delete()
    return 204, None