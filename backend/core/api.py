from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Q

from typing import List,Optional
from .models import Category,Org

from .schemas import CategoryIn, CategoryOut,OrgIn, OrgOut, Message


router = Router(tags=['core'])

#类别
@router.post("/categories/")
def create_category(request, data: CategoryIn):
    category = Category.objects.create(**data.dict())
    return {"id": category.id}

@router.get("/categories/", response=List[CategoryOut])
def list_categories(request):
   
   # 获取所有根节点（无父节点的分类）
    root_categories = Category.objects.filter(parent__isnull=True)
    return build_category_tree(root_categories)


def build_category_tree(queryset):
    """递归构建分类树"""
    result = []
    for category in queryset:
        category_data = CategoryOut.from_orm(category)
        children = category.children.all()
        if children.exists():
            category_data.children = build_category_tree(children)
        result.append(category_data)
    return result

@router.put("/categories/{category_id}/")
def update_category(request, category_id: int, data: CategoryIn):
    category = Category.objects.get(id=category_id)
    for attr, value in data.dict().items():
        setattr(category, attr, value)
    category.save()
    return {"success": True}

@router.delete("/categories/{category_id}/")
def delete_category(request, category_id: int):
    Category.objects.filter(id=category_id).delete()
    return {"success": True}


 

 #机构

@router.post("/orgs/", response={201: OrgOut, 400: Message})
def create_org(request, data: OrgIn):
    """创建组织"""
    try:
        # 检查名称是否已存在
        if Org.objects.filter(name=data.name).exists():
            return 400, {"message": "组织名称已存在", "success": False}
        
        org = Org.objects.create(**data.dict())
        return 201, org
    except Exception as e:
        return 400, {"message": f"创建失败: {str(e)}", "success": False}


@router.get("/orgs/", response=List[OrgOut])
def list_orgs(request, search: Optional[str] = None, 
              skip: int = 0, limit: int = 100):
    """获取组织列表（支持搜索和分页）"""
    orgs = Org.objects.all().order_by("-created_at")
    
    # 搜索功能
    if search:
        orgs = orgs.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(org_type__icontains=search)
        )
    
    # 分页
    return orgs[skip:skip + limit]


@router.get("/orgs/{org_id}/", response={200: OrgOut, 404: Message})
def get_org(request, org_id: int):
    """根据ID获取组织详情"""
    org = get_object_or_404(Org, id=org_id)
    return 200, org


@router.put("/orgs/{org_id}/", response={200: OrgOut, 400: Message, 404: Message})
def update_org(request, org_id: int, data: OrgIn):
    """更新组织信息"""
    org = get_object_or_404(Org, id=org_id)
    
    # 检查名称重复（排除自身）
    if Org.objects.filter(name=data.name).exclude(id=org_id).exists():
        return 400, {"message": "组织名称已存在", "success": False}
    
    for attr, value in data.dict().items():
        setattr(org, attr, value)
    org.save()
    
    return 200, org


@router.delete("/orgs/{org_id}/", response={200: Message, 404: Message})
def delete_org(request, org_id: int):
    """删除组织"""
    org = get_object_or_404(Org, id=org_id)
    org.delete()
    return 200, {"message": "组织删除成功", "success": True}
