# from django.db import router
from ninja import Router, Query, Body, Path
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from .models import Org, Category
from .schemas import CategoryIn, CategoryOut, CategoryListOut


router = Router(tags=['core'])

#加一个测试的api
@router.get("/test")
def test(request):
    return {"message": "Hello, world!"}


# Category endpoints
@router.get("/categories", response=list[CategoryListOut])
def list_categories(request, parent_id: int = Query(None, description="父类别ID，为空则获取所有顶级类别")):
    """获取类别列表，支持按父类别筛选"""
    if parent_id is not None:
        return Category.objects.filter(parent_id=parent_id).order_by('sort_order').all()
    return Category.objects.filter(parent__isnull=True).order_by('sort_order').all()

@router.get("/categories/{category_id}", response=CategoryOut)
def get_category(request, category_id: int = Path(..., description="类别ID")):
    """获取单个类别详情"""
    return get_object_or_404(Category, id=category_id)

@router.post("/categories", response=CategoryOut)
def create_category(request, data: CategoryIn = Body(...)):
    """创建新类别"""
    # 准备创建数据
    create_data = data.dict()
    
    # 检查并处理父类别
    if 'parent' in create_data and create_data['parent'] is not None:
        # 获取父类别ID（可能是整数或对象）
        parent_id = create_data['parent'].id if hasattr(create_data['parent'], 'id') else create_data['parent']
        
        # 验证父类别是否存在
        if not Category.objects.filter(id=parent_id).exists():
            raise HttpError(400, "父类别不存在")
        
        # 将父类别ID转换为Category实例
        create_data['parent'] = Category.objects.get(id=parent_id)
    else:
        # 没有父类别，设置为None
        create_data['parent'] = None
    
    # 创建类别
    category = Category.objects.create(**create_data)
    return category

@router.put("/categories/{category_id}", response=CategoryOut)
def update_category(
    request, 
    category_id: int = Path(..., description="类别ID"),
    data: CategoryIn = Body(...)
):
    """更新类别信息"""
    category = get_object_or_404(Category, id=category_id)
    
    # 准备更新数据
    update_data = data.dict()
    
    # 检查并处理父类别
    if 'parent' in update_data:
        if update_data['parent'] is not None:
            # 获取父类别ID（可能是整数或对象）
            parent_id = update_data['parent'].id if hasattr(update_data['parent'], 'id') else update_data['parent']
            
            # 验证不能将类别设置为自身的父类别
            if parent_id == category_id:
                raise HttpError(400, "类别不能设置为自身的父类别")
            
            # 验证父类别是否存在
            if not Category.objects.filter(id=parent_id).exists():
                raise HttpError(400, "父类别不存在")
            
            # 将父类别ID转换为Category实例
            update_data['parent'] = Category.objects.get(id=parent_id)
        else:
            # 设置为无父类别
            update_data['parent'] = None
    
    # 更新类别字段
    for field, value in update_data.items():
        setattr(category, field, value)
    
    # 保存更新后的类别
    category.save()
    return category


@router.delete("/categories/{category_id}")
def delete_category(request, category_id: int = Path(..., description="类别ID")):
    """删除类别"""
    category = get_object_or_404(Category, id=category_id)
    
    # 检查是否有子类别
    if category.children.exists():
        raise HttpError(400, "该类别存在子类别，不能删除")
    
    category.delete()
    return None



 
# 组织架构相关Schema

# class OrgIn(ModelSchema):
#     class Meta:
#         model = Org
#         exclude = ['created_at', 'updated_at']

# class OrgOut(ModelSchema):
#     class Meta:
#         model = Org
#         exclude = ['created_at', 'updated_at']
#         from_attributes = True  # 允许从 ORM 对象加载数据
        


# def get_org_children(org_id):
#     departments = Department.objects.filter(org_id=org_id)
#     return [{
#         'id': dept.id,
#         'name': dept.name,
#         'children': get_dept_children(dept.id)
#     } for dept in departments]


