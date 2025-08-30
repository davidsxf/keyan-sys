# api.py
from ninja import Router
from ninja import NinjaAPI, Query

from ninja.pagination import paginate
from typing import List
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Project, ProjectStatus, UndertakeType
from .schemas import ProjectIn, ProjectOut, ProjectFilter


api = NinjaAPI(title="项目管理API", version="1.0.0")
router = Router(tags=['projects'])


@router.get("/projects", response=List[ProjectOut])
def list_projects(request, filters: ProjectFilter = Query(...)):
    """获取项目列表"""
    queryset = Project.objects.all().select_related('leader', 'type', 'source')
    
    # 应用过滤条件
    if filters.title:
        queryset = queryset.filter(title__icontains=filters.title)
    if filters.number:
        queryset = queryset.filter(number__icontains=filters.number)
    if filters.status:
        queryset = queryset.filter(status=filters.status)
    if filters.type_id:
        queryset = queryset.filter(type_id=filters.type_id)
    if filters.leader_id:
        queryset = queryset.filter(leader_id=filters.leader_id)
    if filters.undertake:
        queryset = queryset.filter(undertake=filters.undertake)
    
    return queryset

@router.get("/projects/{project_id}", response=ProjectOut)
def get_project(request, project_id: int):
    """获取单个项目详情"""
    project = get_object_or_404(Project, id=project_id)
    return project


@router.post("/projects", response=ProjectOut)
def create_project(request, data: ProjectIn):
    """创建新项目"""
    project_data = data.dict()
    # 处理外键字段
    if project_data.get('leader_id') is None:
        project_data.pop('leader_id', None)
    if project_data.get('type_id') is None:
        project_data.pop('type_id', None)
    if project_data.get('source_id') is None:
        project_data.pop('source_id', None)
    
    project = Project.objects.create(**project_data)
    return project


@router.put("/projects/{project_id}", response=ProjectOut)
def update_project(request, project_id: int, data: ProjectIn):
    """更新项目信息"""
    project = get_object_or_404(Project, id=project_id)
    update_data = data.dict(exclude_unset=True)
    
    for attr, value in update_data.items():
        setattr(project, attr, value)
    
    project.save()
    return project


@router.delete("/projects/{project_id}")
def delete_project(request, project_id: int):
    """删除项目"""
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return {"success": True, "message": "项目删除成功"}


@router.get("/projects/status/choices")
def get_status_choices(request):
    """获取项目状态选项"""
    return [{"value": choice[0], "label": choice[1]} for choice in ProjectStatus.choices]


@router.get("/projects/undertake/choices")
def get_undertake_choices(request):
    """获取承担方式选项"""
    return [{"value": choice[0], "label": choice[1]} for choice in UndertakeType.choices]
