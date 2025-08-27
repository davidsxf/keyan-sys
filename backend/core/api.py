from ninja import Router
from typing import List
from .models import Category
from .schemas import CategoryIn, CategoryOut


router = Router(tags=['core'])

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