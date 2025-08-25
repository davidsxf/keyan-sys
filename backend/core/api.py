# from django.db import router
from ninja import Router
from ninja import ModelSchema
from .models import Org, Category


router = Router(tags=['core'])

#加一个测试的api
@router.get("/test")
def test(request):
    return {"message": "Hello, world!"}

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
    data_dict = data.dict()

    print(data_dict)
    # Convert parent ID to Category instance if provided and not null
    if data_dict.get('parent') is not None:
        try:
            data_dict['parent'] = Category.objects.get(id=data_dict['parent'])
        except Category.DoesNotExist:
            data_dict['parent'] = None
    
    return Category.objects.create(**data_dict)

@router.put("/categories/{category_id}", response=CategoryOut)
def update_category(request, category_id: int, data: CategoryIn):
    category = Category.objects.get(id=category_id)
    data_dict = data.dict()
    # Convert parent ID to Category instance if provided and not null
    if data_dict.get('parent') is not None:
        try:
            data_dict['parent'] = Category.objects.get(id=data_dict['parent'])
        except Category.DoesNotExist:
            data_dict['parent'] = None
    for attr, value in data_dict.items():
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


