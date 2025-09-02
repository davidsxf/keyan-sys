# api.py
from ninja import Router
from ninja import NinjaAPI, Query
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Project, ProjectStatus, UndertakeType, ProjectType, Category, Staff
from .schemas import ProjectIn, ProjectOut, ProjectFilter


api = NinjaAPI(title="项目管理API", version="1.0.0")
router = Router(tags=['projects'])


# 自定义分页类，确保与前端参数名匹配
class CustomPagination(PageNumberPagination):
    page_size_query_param = "size"


@router.get("", response=List[ProjectOut])  # 移除重复的 '/projects'
@paginate(CustomPagination)
def list_projects(request, filters: ProjectFilter = Query(None)):
    """获取项目列表"""
    # 修复select_related，将'type'改为'category'
    queryset = Project.objects.all().select_related('leader', 'category', 'source')

    
    # 如果提供了筛选条件，则应用它们
    if filters:
        if filters.title:
            queryset = queryset.filter(title__icontains=filters.title)
        if filters.number:
            queryset = queryset.filter(number__icontains=filters.number)
        if filters.status:
            queryset = queryset.filter(status=filters.status)
        if filters.category_id:
            queryset = queryset.filter(category_id=filters.category_id)
        if filters.type:
            queryset = queryset.filter(type=filters.type)
        if filters.leader_id:
            queryset = queryset.filter(leader_id=filters.leader_id)
        if filters.undertake:
            queryset = queryset.filter(undertake=filters.undertake)
        if filters.source:
            queryset = queryset.filter(source__name__icontains=filters.source)
    
    # 直接返回queryset，让Ninja的序列化器处理ProjectOut中的自定义字段
    return queryset

@router.get("/{project_id}", response=ProjectOut)  # 移除重复的 '/projects'
def get_project(request, project_id: int):
    """获取单个项目详情"""
    project = get_object_or_404(Project, id=project_id)
    return project


@router.post("", response=ProjectOut)  # 移除重复的 '/projects'
def create_project(request, data: ProjectIn):
    """创建新项目"""
    project_data = data.dict()
    # 处理外键字段
    if project_data.get('leader_id') is None:
        project_data.pop('leader_id', None)
    if project_data.get('category_id') is None:
        project_data.pop('category_id', None)
    if project_data.get('type') is None:
        project_data.pop('type', None)
    if project_data.get('source_id') is None:
        project_data.pop('source_id', None)
    
    project = Project.objects.create(**project_data)
    return project


@router.put("/{project_id}", response=ProjectOut)  # 移除重复的 '/projects'
def update_project(request, project_id: int, data: ProjectIn):
    """更新项目信息"""
    project = get_object_or_404(Project, id=project_id)
    update_data = data.dict(exclude_unset=True)
    
    for attr, value in update_data.items():
        setattr(project, attr, value)
    
    project.save()
    return project


@router.delete("/{project_id}")  # 移除重复的 '/projects'
def delete_project(request, project_id: int):
    """删除项目"""
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return {"success": True, "message": "项目删除成功"}


@router.get("/status/choices")  # 移除重复的 '/projects'
def get_status_choices(request):
    """获取项目状态选项"""
    return [{"value": choice[0], "label": choice[1]} for choice in ProjectStatus.choices]


@router.get("/undertake/choices")  # 移除重复的 '/projects'
def get_undertake_choices(request):
    """获取承担方式选项"""
    return [{"value": choice[0], "label": choice[1]} for choice in UndertakeType.choices]

@router.get("/type/choices")  # 移除重复的 '/projects'
def get_type_choices(request):
    """获取项目类型选项"""
    return [{"value": choice[0], "label": choice[1]} for choice in ProjectType.choices]


# category 类别
@router.get("/category/choices")  # 移除重复的 '/projects'
def get_category_choices(request):
    """获取项目类别选项"""
    # 从数据库查询所有类别
    categories = Category.objects.all().order_by('sort_order', 'name')
    # 返回格式化的选项列表
    return [{"value": category.id, "label": category.name} for category in categories]


