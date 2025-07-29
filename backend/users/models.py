from django.db import models



class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "users_departments"


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey('Department', related_name='teams', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users_teams'


from enum import Enum

class StaffStatus(Enum):
    ON_DUTY = "在职"
    OFF_DUTY = "离职"
    RETIRE = "退休"

class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=10, null=True, default="男")
    birthday = models.DateField(null=True, default='1990-01-01')
    email = models.CharField(max_length=255, null=True)
    entry_date = models.DateField(null=True)
    department = models.ForeignKey('Department', related_name='staffs', null=True, on_delete=models.SET_NULL)
    team = models.ForeignKey('Team', related_name='members', null=True, on_delete=models.SET_NULL)
    position = models.CharField(max_length=255, null=True)
    is_team_leader = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default=StaffStatus.ON_DUTY.value)
    phone = models.CharField(max_length=20, null=True)
    remark = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users_staffs'

