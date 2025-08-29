from ninja import Router
from typing import List, Optional
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from .schemas import DepartmentIn, DepartmentOut, TeamIn, TeamOut
from .models import Team, Staff, Department

router = Router(tags=["users"])

@router.post("/departments/", response=DepartmentOut)
def create_department(request, data: DepartmentIn):
    """创建部门"""
    parent_id = data.parent_id
    parent = None
    if parent_id:
        parent = get_object_or_404(Department, id=parent_id)
    
    department = Department.objects.create(
        name=data.name,
        description=data.description,
        parent=parent
    )
    return department

@router.get("/departments/", response=List[DepartmentOut])
def list_departments(request):
    """获取部门列表（以树形结构返回）"""
    # 获取所有根部门（没有父部门的部门）
    root_departments = Department.objects.filter(parent__isnull=True)
    return _build_department_tree(root_departments)

def _build_department_tree(departments):
    """递归构建部门树"""
    result = []
    for dept in departments:
        dept_data = DepartmentOut.from_orm(dept)
        # 获取当前部门的所有直接子部门
        children = Department.objects.filter(parent=dept)
        if children.exists():
            dept_data.children = _build_department_tree(children)
        result.append(dept_data)
    return result

@router.get("/departments/{dept_id}/", response=DepartmentOut)
def get_department(request, dept_id: int):
    """根据ID获取部门详情"""
    department = get_object_or_404(Department, id=dept_id)
    return department

@router.put("/departments/{dept_id}/", response=DepartmentOut)
def update_department(request, dept_id: int, data: DepartmentIn):
    """更新部门信息"""
    department = get_object_or_404(Department, id=dept_id)
    
    # 检查是否试图将部门设置为自己的父部门
    if data.parent_id == dept_id:
        from ninja.errors import HttpError
        raise HttpError(400, "部门不能成为自己的父部门")
    
    parent = None
    if data.parent_id:
        parent = get_object_or_404(Department, id=data.parent_id)
    
    department.name = data.name
    department.description = data.description
    department.parent = parent
    department.save()
    
    return department

@router.delete("/departments/{dept_id}/", response={204: None})
def delete_department(request, dept_id: int):
    """删除部门"""
    department = get_object_or_404(Department, id=dept_id)
    department.delete()
    return 204, None


# 团队相关接口 teams
@router.post("/teams/", response={201: TeamOut})
def create_team(request, data: TeamIn):
    """创建团队"""
    # 检查名称是否已存在
    if Team.objects.filter(name=data.name).exists():
        raise HttpError(400, "团队名称已存在")
    
    department = None
    if data.department_id:
        department = get_object_or_404(Department, id=data.department_id)
    
    team = Team.objects.create(
        name=data.name,
        description=data.description,
        department=department
    )
    
    # 返回包含部门名称的响应
    return prepare_team_response(team)


@router.get("/teams/", response=List[TeamOut])
def list_teams(request, search: Optional[str] = None, 
               department_id: Optional[int] = None,
               skip: int = 0, limit: int = 100):
    """获取团队列表（支持搜索、按部门筛选和分页）"""
    teams = Team.objects.all().select_related('department').order_by("-created_at")
    
    # 搜索功能
    if search:
        teams = teams.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    # 按部门筛选
    if department_id:
        teams = teams.filter(department_id=department_id)
    
    # 分页
    teams = teams[skip:skip + limit]
    
    # 准备响应数据
    return [prepare_team_response(team) for team in teams]


@router.get("/teams/{team_id}/", response=TeamOut)
def get_team(request, team_id: int):
    """根据ID获取团队详情"""
    team = get_object_or_404(Team, id=team_id)
    return prepare_team_response(team)


@router.put("/teams/{team_id}/", response=TeamOut)
def update_team(request, team_id: int, data: TeamIn):
    """更新团队信息"""
    team = get_object_or_404(Team, id=team_id)
    
    # 检查名称重复（排除自身）
    if Team.objects.filter(name=data.name).exclude(id=team_id).exists():
        raise HttpError(400, "团队名称已存在")
    
    department = None
    if data.department_id:
        department = get_object_or_404(Department, id=data.department_id)
    
    team.name = data.name
    team.description = data.description
    team.department = department
    team.save()
    
    return prepare_team_response(team)


@router.delete("/teams/{team_id}/", response={204: None})
def delete_team(request, team_id: int):
    """删除团队"""
    team = get_object_or_404(Team, id=team_id)
    team.delete()
    return 204, None


def prepare_team_response(team):
    """准备团队响应数据"""
    return {
        "id": team.id,
        "name": team.name,
        "description": team.description,
        "department_id": team.department.id if team.department else None,
        "department_name": team.department.name if team.department else None,
        "created_at": team.created_at,
        "updated_at": team.updated_at
    }
