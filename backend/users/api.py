from ninja import Router
from typing import List, Optional
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.errors import HttpError
from .schemas import DepartmentIn, DepartmentOut, TeamIn, TeamOut,StaffIn, StaffOut, DepartmentOption, TeamOption
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


@router.get("/departments/options/", response=List[DepartmentOption])
def get_department_options(request):
    """获取部门选项列表"""
    departments = Department.objects.all()
    return [{"id": dept.id, "name": dept.name} for dept in departments]

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

@router.get("/teams/options/", response=List[TeamOption])
def get_team_options(request):
    """获取团队选项列表"""
    teams = Team.objects.all()
    return [{"id": team.id, "name": team.name} for team in teams]

    
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



# 员工相关接口 staffs

@router.post("/staffs/", response={201: StaffOut})
def create_staff(request, data: StaffIn):
    """创建员工"""
    # 检查名称是否已存在
    if Staff.objects.filter(name=data.name).exists():
        raise HttpError(400, "员工姓名已存在")
    
    department = None
    if data.department_id:
        department = get_object_or_404(Department, id=data.department_id)
    
    team = None
    if data.team_id:
        team = get_object_or_404(Team, id=data.team_id)
    
    staff = Staff.objects.create(
        name=data.name,
        gender=data.gender,
        birthday=data.birthday,
        email=data.email,
        entry_date=data.entry_date,
        department=department,
        team=team,
        position=data.position,
        is_team_leader=data.is_team_leader,
        status=data.status.value,
        phone=data.phone,
        remark=data.remark
    )
    
    return prepare_staff_response(staff)


@router.get("/staffs/choices/")
def get_staff_choices(request):
    """获取员工选项列表（用于下拉选择）"""
    staffs = Staff.objects.all().order_by('name')
    return [{"value": staff.id, "label": staff.name} for staff in staffs]

@router.get("/staffs/", response=List[StaffOut])
def list_staffs(request, 
                search: Optional[str] = None,
                department_id: Optional[int] = None,
                team_id: Optional[int] = None,
                status: Optional[str] = None,
                skip: int = 0, 
                limit: int = 100):
    """获取员工列表（支持搜索、筛选和分页）"""
    staffs = Staff.objects.all().select_related('department', 'team').order_by("-created_at")
    
    # 搜索功能
    if search:
        staffs = staffs.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(position__icontains=search)
        )
    
    # 按部门筛选
    if department_id:
        staffs = staffs.filter(department_id=department_id)
    
    # 按团队筛选
    if team_id:
        staffs = staffs.filter(team_id=team_id)
    
    # 按状态筛选
    if status:
        staffs = staffs.filter(status=status)
    
    # 分页
    staffs = staffs[skip:skip + limit]
    
    # 准备响应数据
    return [prepare_staff_response(staff) for staff in staffs]



@router.get("/staffs/{staff_id}/", response=StaffOut)
def get_staff(request, staff_id: int):
    """根据ID获取员工详情"""
    staff = get_object_or_404(Staff, id=staff_id)
    return prepare_staff_response(staff)



@router.put("/staffs/{staff_id}/", response=StaffOut)
def update_staff(request, staff_id: int, data: StaffIn):
    """更新员工信息"""
    staff = get_object_or_404(Staff, id=staff_id)
    
    # 检查名称重复（排除自身）
    if Staff.objects.filter(name=data.name).exclude(id=staff_id).exists():
        raise HttpError(400, "员工姓名已存在")
    
    department = None
    if data.department_id:
        department = get_object_or_404(Department, id=data.department_id)
    
    team = None
    if data.team_id:
        team = get_object_or_404(Team, id=data.team_id)
    
    staff.name = data.name
    staff.gender = data.gender
    staff.birthday = data.birthday
    staff.email = data.email
    staff.entry_date = data.entry_date
    staff.department = department
    staff.team = team
    staff.position = data.position
    staff.is_team_leader = data.is_team_leader
    staff.status = data.status.value
    staff.phone = data.phone
    staff.remark = data.remark
    staff.save()
    
    return prepare_staff_response(staff)

@router.delete("/staffs/{staff_id}/", response={204: None})
def delete_staff(request, staff_id: int):
    """删除员工"""
    staff = get_object_or_404(Staff, id=staff_id)
    staff.delete()
    return 204, None

def prepare_staff_response(staff):
    """准备员工响应数据"""
    return {
        "id": staff.id,
        "name": staff.name,
        "gender": staff.gender,
        "birthday": staff.birthday,
        "email": staff.email,
        "entry_date": staff.entry_date,
        "department_id": staff.department.id if staff.department else None,
        "department_name": staff.department.name if staff.department else None,
        "team_id": staff.team.id if staff.team else None,
        "team_name": staff.team.name if staff.team else None,
        "position": staff.position,
        "is_team_leader": staff.is_team_leader,
        "status": staff.status,
        "phone": staff.phone,
        "remark": staff.remark,
        "created_at": staff.created_at,
        "updated_at": staff.updated_at
    }