# from django.db import router
from ninja import Router
from ninja import ModelSchema
from .models import Org, Category


router = Router(tags=['core'])

# Category schemas
class CategoryIn(ModelSchema):
    class Meta:
        model = Category
        exclude = ["id", "created_at", "updated_at"]
        from_attributes = True

class CategoryOut(ModelSchema):
    class Meta:
        model = Category
        fields = "__all__"
        from_attributes = True

# Category endpoints
@router.get("/categories", response=list[CategoryOut])
def list_categories(request):
    return Category.objects.all()

@router.get("/categories/{category_id}", response=CategoryOut)
def get_category(request, category_id: int):
    return Category.objects.get(id=category_id)

@router.post("/categories", response=CategoryOut)
def create_category(request, data: CategoryIn):
    return Category.objects.create(**data.dict())

@router.put("/categories/{category_id}", response=CategoryOut)
def update_category(request, category_id: int, data: CategoryIn):
    category = Category.objects.get(id=category_id)
    for attr, value in data.dict().items():
        setattr(category, attr, value)
    category.save()
    return category

@router.delete("/categories/{category_id}")
def delete_category(request, category_id: int):
    Category.objects.get(id=category_id).delete()



 
# 组织架构相关Schema

class OrgIn(ModelSchema):
    class Meta:
        model = Org
        exclude = ['created_at', 'updated_at']

class OrgOut(ModelSchema):
    class Meta:
        model = Org
        exclude = ['created_at', 'updated_at']
        from_attributes = True  # 允许从 ORM 对象加载数据
        


def get_org_children(org_id):
    departments = Department.objects.filter(org_id=org_id)
    return [{
        'id': dept.id,
        'name': dept.name,
        'children': get_dept_children(dept.id)
    } for dept in departments]


