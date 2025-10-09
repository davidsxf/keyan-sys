# api.py
# 在文件顶部添加HttpError的导入
from ninja import Router, File, Form
from ninja.files import UploadedFile

from ninja import NinjaAPI, Query
from ninja.pagination import paginate, PageNumberPagination
from typing import List
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ninja.errors import HttpError  # 添加这行导入
from django.http import JsonResponse  # 添加JsonResponse导入
from .models import Project,Org, ProjectStatus, UndertakeType, ProjectType, ProjectLevel, Category, Staff,ProjectStaff,ProjectDocument,ProjectLeaderChange
from .schemas import ProjectIn, ProjectOut, ProjectFilter,ProjectStaffIn, ProjectStaffOut, ProjectStaffFilter,ProjectLeaderChangeIn,ProjectLeaderChangeOut
# 在文件顶部添加事务模块的导入
from django.db import transaction


api = NinjaAPI(title="项目管理API", version="1.0.0")
router = Router(tags=['projects'])

# 项目负责人变更
@router.post("/leader-change", response=ProjectLeaderChangeOut)
@transaction.atomic  # 添加事务装饰器确保原子性
def create_project_leader_change(request, data: ProjectLeaderChangeIn):
    """创建项目负责人变更并同时更新项目leader"""
    # 1. 验证项目是否存在
    project = get_object_or_404(Project, id=data.project_id)
    
    # 2. 验证新负责人是否存在
    new_leader = get_object_or_404(Staff, id=data.leader_id)
    print(new_leader)
    

    # 6. 记录变更历史 查询是否第一次变更 ，如果是则记录项目创建时的负责人
    first_change = ProjectLeaderChange.objects.filter(project=project).first()
    
    if first_change is None:
        # 3. 记录旧负责人信息，用于记录变更历史
        old_leader_id = project.leader.id if project.leader else None
        # 项目创建时的负责人变更
        ProjectLeaderChange.objects.create(
            project=project,
            leader_id=old_leader_id,
            change_date=project.start_date,
            remark='项目创建时的负责人',
        )
    
    # 普通的负责人变更
        ProjectLeaderChange.objects.create(
            project=project,
            leader_id=new_leader.id,
            change_date=data.change_date,
            remark=data.remark,
        )

    # 4. 更新项目的负责人
    project.leader = new_leader
    project.save()
  
    
    # 5. 创建项目负责人变更记录
    project_leader_change = ProjectLeaderChange.objects.create(**data.dict())
    
    return project_leader_change



# 自定义分页类，确保与前端参数名匹配
class CustomPagination(PageNumberPagination):
    page_size_query_param = "size"


# @router.get("", response=List[ProjectOut])  # 移除重复的 '/projects'
# @paginate(CustomPagination)
# 移除分页装饰器，手动实现分页
@router.get("")
def list_projects(request, filters: ProjectFilter = Query(None), page: int = 1, size: int = 10):
    """获取项目列表"""
    queryset = Project.objects.all().select_related('leader', 'category', 'source')

    # 如果提供了筛选条件，则应用它们
    if filters:
        if filters.title:
            queryset = queryset.filter(title__icontains=filters.title)
        if filters.number:
            queryset = queryset.filter(number__icontains=filters.number)
        if filters.status:
            queryset = queryset.filter(status=filters.status)
        if filters.level:
            queryset = queryset.filter(level=filters.level)
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
    
    # 计算总条数
    total = queryset.count()
    
    # 手动实现分页
    skip = (page - 1) * size
    paged_projects = queryset[skip:skip + size]
    
    # 返回包含items和total的字典
    return {
        'items': [ProjectOut.from_orm(project) for project in paged_projects],
        'total': total
    }
    
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



@router.get("/level/choices")  # 移除重复的 '/projects'
def get_level_choices(request):
    """获取项目级别选项"""
    # 由于未定义 ProjectLevel，推测此处应使用 Project 模型中的级别字段相关选项
    # 请根据实际模型确认是否有正确的 choices 定义
    # 以下假设模型中有对应 choices 定义为 level_choices
    return [{"value": choice[0], "label": choice[1]} for choice in ProjectLevel.choices]


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



# 项目来源选项
@router.get("/source/choices")  # 移除重复的 '/projects'
def get_source_choices(request):
    """获取项目来源选项"""

    sources = Org.objects.all()
    return [{"value": source.id, "label": source.name} for source in sources]


#项目负责人变更

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


@router.get("/budget/project/{project_id}", response=List[ProjectBudgetOut])
def get_project_budget(request, project_id: int):
    # 直接返回 QuerySet 对象，FastAPI 会自动将其转换为 List[ProjectBudgetOut]
    return ProjectBudget.objects.filter(project_id=project_id).select_related('project')


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


@router.put("/budget/{budget_id}", response=ProjectBudgetOut)
def update_project_budget(request, budget_id: int, data: ProjectBudgetIn):
    """更新项目预算信息"""
    print(budget_id)
    budget = get_object_or_404(ProjectBudget, id=budget_id)
    update_data = data.dict(exclude_unset=True)
    # print(update_data)
    
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
    print('list_project_participants_by_project project_id:', project_id)
    project = get_object_or_404(Project, id=project_id)
    participants = ProjectStaff.objects.filter(project=project).select_related('staff')
    return participants


# 项目文档相关API


from .schemas import ProjectDocumentIn, ProjectDocumentOut, ProjectDocumentFilter
from django.db.models import Case, When, Value, CharField
from django.db.models import F



@router.get("/documents/{project_id}/documents", response=List[ProjectDocumentOut])
@paginate(CustomPagination)
def list_project_documents(request, project_id: int, filters: ProjectDocumentFilter = Query(...)):
    """获取指定项目的所有文档"""
    queryset = ProjectDocument.objects.filter(project_id=project_id)
    
    # 应用筛选条件
    if filters:
        if filters.name:
            queryset = queryset.filter(name__icontains=filters.name)
    
    # 修复annotate方法中的错误，直接使用F表达式而不是嵌套在Value中
    return queryset.annotate(
        project_title=Case(
            When(project__title__isnull=False, then=F('project__title')),
            default=Value(''),
            output_field=CharField()
        )
    )


@router.post("/documents/{project_id}/documents", response=ProjectDocumentOut)
def create_project_document(request, project_id: int):
    """创建项目文档"""
    
    # 添加详细的调试信息
    print('create_project_document project_id:', project_id)
    print('Request POST data:', request.POST)
    print('Request FILES data:', request.FILES)
    
    # 1. 验证项目是否存在
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        raise HttpError(404, "项目不存在")
    
    # 2. 从request中直接获取FormData数据
    name = request.POST.get("name")
    file = request.FILES.get("file")
    remark = request.POST.get("remark")
    
    # 3. 验证必填字段
    if not name:
        raise HttpError(400, "文档名称不能为空")
    
    if not file:
        raise HttpError(400, "请选择上传文件")
    
    # 4. 验证文件类型
    valid_extensions = ['.pdf', '.docx', '.xlsx', '.txt', '.jpg', '.jpeg', '.png', '.gif']
    if not any(file.name.endswith(ext.lower()) for ext in valid_extensions):
        raise HttpError(400, "仅支持PDF、DOCX、XLSX、TXT、JPG、JPEG、PNG和GIF文件")
    
    # 5. 处理文件存储
    document = ProjectDocument.objects.create(
        project=project,
        name=name,
        file=file,  # 直接将UploadedFile对象赋值给FileField
        remark=remark
    )
    
    return document


    
@router.get("/documents/{document_id}", response=ProjectDocumentOut)
def get_project_document(request, document_id: int):
    """获取项目文档详情"""
    document = get_object_or_404(ProjectDocument, id=document_id)
    return document


@router.put("/documents/{document_id}", response=ProjectDocumentOut)
def update_project_document(request, document_id: int):
    """更新项目文档"""
    document = get_object_or_404(ProjectDocument, id=document_id)
    
    # 直接从request中获取FormData数据
    name = request.POST.get("name")
    file = request.FILES.get("file")
    remark = request.POST.get("remark")
    
    # 验证必填字段
    if not name:
        raise HttpError(400, "文档名称不能为空")
    
    # 如果没有提供新文件，则不更新文件字段
    document.name = name
    if file:
        document.file = file
    document.remark = remark
    document.save()
    return document
    

@router.delete("/documents/{document_id}")
def delete_project_document(request, document_id: int):
    """删除项目文档"""
    document = get_object_or_404(ProjectDocument, id=document_id)
    document.delete()
    return {"success": True, "message": "项目文档删除成功"}

# 在项目负责人变更相关代码部分添加以下内容

@router.get("/{project_id}/leader-changes", response=List[ProjectLeaderChangeOut])
# 使用自定义分页装饰器
@paginate(CustomPagination)

def get_project_leader_changes(request, project_id: int):
    """获取项目负责人变更记录"""
    project = get_object_or_404(Project, id=project_id)
    # 使用select_related预加载负责人信息和项目信息
    queryset = ProjectLeaderChange.objects.filter(project=project).select_related('project','leader')
    
    # 转换QuerySet对象为符合ProjectLeaderChangeOut schema的字典列表
    results = []
    for change in queryset:
        # 构建符合schema要求的字典
        result_item = {
            'id': change.id,
            'project_id': change.project.id,
            'project_title': change.project.title if change.project else None,
            'leader_id': change.leader.id if change.leader else None,
            'leader_name': change.leader.name if change.leader else None,
            'change_date': change.change_date,
            'remark': change.remark,
            'created_at': change.created_at,
            'updated_at': change.updated_at
        }
        results.append(result_item)
    
    return results
       

