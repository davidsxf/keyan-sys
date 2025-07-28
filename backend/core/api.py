from ninja import NinjaAPI, Router, Schema
from .models import Org, Department, Category

api = NinjaAPI()
core_router = Router(tags=['core'])

# 组织架构相关Schema
def get_org_children(org_id):
    departments = Department.objects.filter(org_id=org_id)
    return [{
        'id': dept.id,
        'name': dept.name,
        'description': dept.description,
    } for dept in departments]

class OrgSchema(Schema):
    id: int
    name: str
    description: str = None
    phone: str = None
    email: str = None
    org_type: str = None
    departments: list = None

    @classmethod
    def from_orm(cls, obj):
        schema = super().from_orm(obj)
        schema.departments = get_org_children(obj.id)
        return schema

class OrgCreateSchema(Schema):
    name: str
    description: str = None
    phone: str = None
    email: str = None
    org_type: str = None

class OrgUpdateSchema(Schema):
    name: str = None
    description: str = None
    phone: str = None
    email: str = None
    org_type: str = None

# 部门相关Schema
class DepartmentSchema(Schema):
    id: int
    org_id: int
    name: str
    description: str = None

class DepartmentCreateSchema(Schema):
    org_id: int
    name: str
    description: str = None

class DepartmentUpdateSchema(Schema):
    name: str = None
    description: str = None

# 类别相关Schema
class CategorySchema(Schema):
    id: int
    name: str
    parent_id: int = None
    weight: int
    sort_order: int

class CategoryCreateSchema(Schema):
    name: str
    parent_id: int = None
    weight: int = 0
    sort_order: int = 0

class CategoryUpdateSchema(Schema):
    name: str = None
    parent_id: int = None
    weight: int = None
    sort_order: int = None

# 组织相关接口
@core_router.get('/orgs', response=list[OrgSchema])
def list_orgs(request):
    return Org.objects.all()

@core_router.get('/orgs/{org_id}', response=OrgSchema)
def get_org(request, org_id: int):
    return Org.objects.get(id=org_id)

@core_router.post('/orgs', response=OrgSchema)
def create_org(request, data: OrgCreateSchema):
    org = Org.objects.create(**data.dict())
    return org

@core_router.put('/orgs/{org_id}', response=OrgSchema)
def update_org(request, org_id: int, data: OrgUpdateSchema):
    org = Org.objects.get(id=org_id)
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(org, attr, value)
    org.save()
    return org

@core_router.delete('/orgs/{org_id}', response={204: None})
def delete_org(request, org_id: int):
    Org.objects.get(id=org_id).delete()
    return 204

# 部门相关接口
@core_router.get('/departments', response=list[DepartmentSchema])
def list_departments(request, org_id: int = None):
    query = Department.objects.all()
    if org_id:
        query = query.filter(org_id=org_id)
    return query

@core_router.post('/departments', response=DepartmentSchema)
def create_department(request, data: DepartmentCreateSchema):
    department = Department.objects.create(**data.dict())
    return department

@core_router.put('/departments/{dept_id}', response=DepartmentSchema)
def update_department(request, dept_id: int, data: DepartmentUpdateSchema):
    dept = Department.objects.get(id=dept_id)
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(dept, attr, value)
    dept.save()
    return dept

@core_router.delete('/departments/{dept_id}', response={204: None})
def delete_department(request, dept_id: int):
    Department.objects.get(id=dept_id).delete()
    return 204

# 类别相关接口
@core_router.get('/categories', response=list[CategorySchema])
def list_categories(request, parent_id: int = None):
    query = Category.objects.all()
    if parent_id is not None:
        query = query.filter(parent_id=parent_id)
    return query

@core_router.post('/categories', response=CategorySchema)
def create_category(request, data: CategoryCreateSchema):
    category = Category.objects.create(**data.dict())
    return category

@core_router.put('/categories/{category_id}', response=CategorySchema)
def update_category(request, category_id: int, data: CategoryUpdateSchema):
    category = Category.objects.get(id=category_id)
    for attr, value in data.dict(exclude_unset=True).items():
        setattr(category, attr, value)
    category.save()
    return category

@core_router.delete('/categories/{category_id}', response={204: None})
def delete_category(request, category_id: int):
    Category.objects.get(id=category_id).delete()
    return 204

api.add_router('/v1/', core_router)