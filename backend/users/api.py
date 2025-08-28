from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from .schemas import DepartmentIn, DepartmentOut
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