from ninja import Router
from ninja.orm import ModelSchema
from .models import Team, Staff, Department

router = Router(tags=["users"])

# Department schemas
class DepartmentIn(ModelSchema):
    class Meta:
        model = Department
        exclude = ["id", "created_at", "updated_at"]
        from_attributes = True

class DepartmentOut(ModelSchema):
    class Meta:
        model = Department
        fields = "__all__"
        from_attributes = True

# Department endpoints
@router.get("/departments", response=list[DepartmentOut])
def list_departments(request):
    return Department.objects.all()

@router.get("/departments/{department_id}", response=DepartmentOut)
def get_department(request, department_id: int):
    return Department.objects.get(id=department_id)

@router.post("/departments", response=DepartmentOut)
def create_department(request, data: DepartmentIn):
    return Department.objects.create(**data.dict())

@router.put("/departments/{department_id}", response=DepartmentOut)
def update_department(request, department_id: int, data: DepartmentIn):
    department = Department.objects.get(id=department_id)
    for attr, value in data.dict().items():
        setattr(department, attr, value)
    department.save()
    return department

@router.delete("/departments/{department_id}")
def delete_department(request, department_id: int):
    Department.objects.get(id=department_id).delete()
    return {"success": True}      

# Team schemas and endpoints
class TeamIn(ModelSchema):
    class Meta:
        model = Team
        exclude = ["id", "created_at", "updated_at"]
        from_attributes = True

class TeamOut(ModelSchema):
    class Meta:
        model = Team
        fields = "__all__"
        from_attributes = True

@router.get("/teams", response=list[TeamOut])
def list_teams(request):
    return Team.objects.all()

@router.get("/teams/{team_id}", response=TeamOut)
def get_team(request, team_id: int):
    return Team.objects.get(id=team_id)

@router.post("/teams", response=TeamOut)
def create_team(request, data: TeamIn):
    return Team.objects.create(**data.dict())

@router.put("/teams/{team_id}", response=TeamOut)
def update_team(request, team_id: int, data: TeamIn):
    team = Team.objects.get(id=team_id)
    for attr, value in data.dict().items():
        setattr(team, attr, value)
    team.save()
    return team

@router.delete("/teams/{team_id}")
def delete_team(request, team_id: int):
    Team.objects.get(id=team_id).delete()
    return {"success": True}

# Staff schemas and endpoints
class StaffIn(ModelSchema):
    class Meta:
        model = Staff
        exclude = ["id", "created_at", "updated_at"]
        from_attributes = False

class StaffOut(ModelSchema):
    class Meta:
        model = Staff
        fields = "__all__"
        from_attributes = True

@router.get("/staff", response=list[StaffOut])
def list_staff(request):
    return Staff.objects.all()

@router.get("/staff/{staff_id}", response=StaffOut)
def get_staff(request, staff_id: int):
    return Staff.objects.get(id=staff_id)

@router.post("/staff", response=StaffOut)
def create_staff(request, data: StaffIn):
    data_dict = data.dict()
    # Convert department ID to instance
    if 'department' in data_dict and data_dict['department']:
        department_id = data_dict.pop('department')
        data_dict['department'] = Department.objects.get(id=department_id)
    # Convert team ID to instance
    if 'team' in data_dict and data_dict['team']:
        team_id = data_dict.pop('team')
        data_dict['team'] = Team.objects.get(id=team_id)
    return Staff.objects.create(** data_dict)

@router.put("/staff/{staff_id}", response=StaffOut)
def update_staff(request, staff_id: int, data: StaffIn):
    staff = Staff.objects.get(id=staff_id)
    data_dict = data.dict()
    # Convert department ID to instance if provided
    if 'department' in data_dict:
        dept_id = data_dict.pop('department')
        if dept_id:
            staff.department = Department.objects.get(id=dept_id)
        else:
            staff.department = None
    # Convert team ID to instance if provided
    if 'team' in data_dict:
        team_id = data_dict.pop('team')
        if team_id:
            staff.team = Team.objects.get(id=team_id)
        else:
            staff.team = None
    # Update remaining fields
    for attr, value in data_dict.items():
        setattr(staff, attr, value)
    staff.save()
    return staff

@router.delete("/staff/{staff_id}")
def delete_staff(request, staff_id: int):
    Staff.objects.get(id=staff_id).delete()
    return {"success": True}