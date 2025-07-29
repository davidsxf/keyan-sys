from ninja import Router
from ninja.orm import ModelSchema
from .models import Team, Staff

router = Router(tags=["users"])


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
        from_attributes = True

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
    return Staff.objects.create(**data.dict())

@router.put("/staff/{staff_id}", response=StaffOut)
def update_staff(request, staff_id: int, data: StaffIn):
    staff = Staff.objects.get(id=staff_id)
    for attr, value in data.dict().items():
        setattr(staff, attr, value)
    staff.save()
    return staff

@router.delete("/staff/{staff_id}")
def delete_staff(request, staff_id: int):
    Staff.objects.get(id=staff_id).delete()
    return {"success": True}