# api.py
# 在文件顶部添加HttpError的导入
from ninja import Router
from ninja import NinjaAPI, Query
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.errors import HttpError  # 添加这行导入
from .models import Project, ProjectStatus, UndertakeType, ProjectType, Category, Staff,ProjectStaff,ProjectDocument
from .schemas import ProjectIn, ProjectOut, ProjectFilter,ProjectStaffIn, ProjectStaffOut, ProjectStaffFilter,ProjectDocumentIn,ProjectDocumentOut,ProjectDocumentFilter


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

    # 打印查询结果
    # for project in queryset:
    #     print(project.__dict__)
    
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
        if filters.start_date:
            queryset = queryset.filter(start_date__gte=filters.start_date)
        if filters.end_date:
            queryset = queryset.filter(end_date__lte=filters.end_date)
    
    # 直接返回queryset，让Ninja的序列化器处理ProjectOut中的自定义字段
    return queryset

# 恢复get_project接口中的预加载代码，以便获取关联对象数据
@router.get("/{project_id}", response=ProjectOut)  # 移除重复的 '/projects'
def get_project(request, project_id: int):
    """获取单个项目详情"""
    project = get_object_or_404(Project.objects.select_related('leader', 'category', 'source'), id=project_id)
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


#项目预算

from .schemas import ProjectBudgetIn, ProjectBudgetOut, ProjectBudgetFilter
from .models import ProjectBudget,ProjectBudgetType

# 项目预算相关API
@router.get("/budget/budgets", response=List[ProjectBudgetOut])
@paginate(CustomPagination)
def list_project_budgets(request, filters: ProjectBudgetFilter = Query(None)):
    """获取项目预算列表"""
    # 使用select_related预加载项目信息
    queryset = ProjectBudget.objects.all().select_related('project')
    
    # 如果提供了筛选条件，则应用它们
    if filters:
        if filters.project_id:
            queryset = queryset.filter(project_id=filters.project_id)
        if filters.name:
            queryset = queryset.filter(name__icontains=filters.name)
        if filters.type:
            queryset = queryset.filter(type=filters.type)
        if filters.year:
            queryset = queryset.filter(year=filters.year)
        if filters.start_date:
            queryset = queryset.filter(created_at__gte=filters.start_date)
        if filters.end_date:
            queryset = queryset.filter(created_at__lte=filters.end_date)
    
    return queryset


@router.get("/budget/budgets/{budget_id}", response=ProjectBudgetOut)
def get_project_budget(request, budget_id: int):
    """获取单个项目预算详情"""
    budget = get_object_or_404(ProjectBudget.objects.select_related('project'), id=budget_id)
    return budget


@router.post("/budget/budgets", response=ProjectBudgetOut)
def create_project_budget(request, data: ProjectBudgetIn):
    """创建新项目预算"""
    budget_data = data.dict()
    
    # 从数据中提取project_id，用于查找Project对象
    project_id = budget_data.pop('project_id')
    project = get_object_or_404(Project, id=project_id)
    
    # 创建预算记录
    budget = ProjectBudget.objects.create(project=project, **budget_data)
    return budget


@router.put("/budget/budgets/{budget_id}", response=ProjectBudgetOut)
def update_project_budget(request, budget_id: int, data: ProjectBudgetIn):
    """更新项目预算信息"""
    budget = get_object_or_404(ProjectBudget, id=budget_id)
    update_data = data.dict(exclude_unset=True)
    
    # 处理project_id字段
    if 'project_id' in update_data:
        project_id = update_data.pop('project_id')
        project = get_object_or_404(Project, id=project_id)
        budget.project = project
    
    # 更新其他字段
    for attr, value in update_data.items():
        setattr(budget, attr, value)
    
    budget.save()
    return budget


@router.delete("/budget/budgets/{budget_id}")
def delete_project_budget(request, budget_id: int):
    """删除项目预算"""
    budget = get_object_or_404(ProjectBudget, id=budget_id)
    budget.delete()
    return {"success": True, "message": "预算删除成功"}


@router.get("/budget/types")
def get_budget_type_choices(request):
    """获取预算类型选项"""
    return [{"value": choice[0], "label": choice[1]} for choice in ProjectBudgetType.choices]


# 将router添加到api
# api.add_router("/projects", router)



# 在文件末尾添加项目参与人员相关API

@router.get("/participants/list", response=List[ProjectStaffOut])
@paginate(CustomPagination)
def list_project_participants(request, filters: ProjectStaffFilter = Query(...)):  # 使用...作为默认值
    """获取项目参与人员列表"""
    queryset = ProjectStaff.objects.all().select_related('project', 'staff')
    
    # 应用筛选条件
    if filters:
        if filters.project_id:
            queryset = queryset.filter(project_id=filters.project_id)
        if filters.staff_id:
            queryset = queryset.filter(staff_id=filters.staff_id)
        if filters.staff_name:
            queryset = queryset.filter(staff__name__icontains=filters.staff_name)
        if filters.role:
            queryset = queryset.filter(role=filters.role)
        # if filters.join_date:
        #     queryset = queryset.filter(join_date__gte=filters.join_date)
        # if filters.leave_date:
        #     queryset = queryset.filter(leave_date__lte=filters.leave_date)
    
    return queryset


@router.get("/participants/roles")
def get_participant_role_choices(request):
    """获取项目参与人员角色选项"""
    return [{"value": choice[0], "label": choice[1]} for choice in ProjectStaff.ROLE_CHOICES]


@router.post("/participants/create", response=ProjectStaffOut)
def create_project_participant(request, data: ProjectStaffIn):
    """创建项目参与人员"""
    # 检查项目和员工是否存在
    print('create_project_participant data:', data)
    project = get_object_or_404(Project, id=data.project_id)
    staff = get_object_or_404(Staff, id=data.staff_id)
    
    # 检查是否已存在参与关系
    if ProjectStaff.objects.filter(project=project, staff=staff).exists():
        # 替换为HttpError，这样前端就能接收到错误信息
        raise HttpError(400, "该员工已参与此项目")
    
    # 创建参与关系
    participant = ProjectStaff.objects.create(
        project=project,
        staff=staff,
        role=data.role,
        order=data.order,
        join_date=data.join_date,
        leave_date=data.leave_date,
        remark=data.remark
    )
    
    return participant





@router.get("/participants/{participant_id}", response=ProjectStaffOut)
def get_project_participant(request, participant_id: int):
    """获取参与人员的参与项目详情"""
    participant = get_object_or_404(ProjectStaff.objects.select_related('project', 'staff'), id=participant_id)
    return participant


@router.get("/participants/{participant_id}/projects", response=List[ProjectOut])
def get_participant_projects(request, participant_id: int):
    """获取参与人员参与的项目列表"""
    projects = ProjectStaff.objects.filter(staff_id=participant_id).select_related('project')
    return [ps.project for ps in projects]


@router.put("/participants/{participant_id}", response=ProjectStaffOut)
def update_project_participant(request, participant_id: int, data: ProjectStaffIn):
    """更新项目参与人员信息"""
    participant = get_object_or_404(ProjectStaff, id=participant_id)
    
    # 检查项目和员工是否存在
    project = get_object_or_404(Project, id=data.project_id)
    staff = get_object_or_404(Staff, id=data.staff_id)
    # 检查是否已存在参与关系（排除当前记录）
    if ProjectStaff.objects.filter(project=project, staff=staff).exclude(id=participant_id).exists():
        raise Exception("该员工已参与此项目")
    # 更新参与关系
    participant.project = project
    participant.staff = staff
    participant.role = data.role
    participant.order = data.order
    participant.join_date = data.join_date
    participant.leave_date = data.leave_date
    participant.remark = data.remark
    participant.save()
    
    return participant



@router.delete("/participants/{participant_id}")
def delete_project_participant(request, participant_id: int):
    """删除项目参与人员"""
    participant = get_object_or_404(ProjectStaff, id=participant_id)
    participant.delete()
    return {"success": True, "message": "项目参与人员删除成功"}





@router.get("/{project_id}/participants", response=List[ProjectStaffOut])
@paginate(CustomPagination)
def list_project_participants_by_project(request, project_id: int):
    """获取指定项目的所有参与人员"""
    project = get_object_or_404(Project, id=project_id)
    participants = ProjectStaff.objects.filter(project=project).select_related('staff')
    return participants


# 项目文档相关API


from projects.schemas import ProjectDocumentIn, ProjectDocumentOut, ProjectDocumentFilter
from django.db.models import Case, When, Value, CharField
from django.db.models.functions import Coalesce
from django.db.models import F, Q

@router.get("/{project_id}/documents", response=List[ProjectDocumentOut])
@paginate(CustomPagination)
def list_project_documents(request, project_id: int, filters: ProjectDocumentFilter = Query(...)):
    """获取指定项目的所有文档"""
    queryset = ProjectDocument.objects.filter(project_id=project_id)
    
    # 应用筛选条件
    if filters:
        if filters.name:
            queryset = queryset.filter(name__icontains=filters.name)
    
    return queryset.annotate(
        project_title=Case(
            When(project__title__isnull=False, then=Value(F('project__title'))),
            default=Value(''),
            output_field=CharField()
        )
    )


@router.post("/{project_id}/documents", response=ProjectDocumentOut)
def create_project_document(request, project_id: int, data: ProjectDocumentIn):
    """创建项目文档"""
    project = get_object_or_404(Project, id=project_id)
    document = ProjectDocument.objects.create(
        project=project,
        name=data.name,
        file=data.file,
        remark=data.remark
    )
    return document

@router.get("/documents/{document_id}", response=ProjectDocumentOut)
def get_project_document(request, document_id: int):
    """获取项目文档详情"""
    document = get_object_or_404(ProjectDocument, id=document_id)
    return document


@router.put("/documents/{document_id}", response=ProjectDocumentOut)
def update_project_document(request, document_id: int, data: ProjectDocumentIn):
    """更新项目文档"""
    document = get_object_or_404(ProjectDocument, id=document_id)
    document.name = data.name
    document.file = data.file
    document.remark = data.remark
    document.save()
    return document
    

@router.delete("/documents/{document_id}")
def delete_project_document(request, document_id: int):
    """删除项目文档"""
    document = get_object_or_404(ProjectDocument, id=document_id)
    document.delete()
    return {"success": True, "message": "项目文档删除成功"}
