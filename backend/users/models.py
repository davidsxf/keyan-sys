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
        verbose_name = "部门"
        verbose_name_plural = "部门"


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey('Department',null=True, blank=True, related_name='teams', on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users_teams'
        verbose_name = "团队"
        verbose_name_plural = "团队"


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
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users_staffs'
        verbose_name = "职工"
        verbose_name_plural = "职工"



# from django.db import models
# from django.utils.translation import gettext_lazy as _


# class StaffStatus(models.TextChoices):
#     """员工状态枚举类"""
#     ON_DUTY = "ON_DUTY", _("在职")
#     OFF_DUTY = "OFF_DUTY", _("离职")
#     RETIRE = "RETIRE", _("退休")
#     # 可以在此处添加其他状态


# class Staff(models.Model):
#     """员工信息模型"""
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255, unique=True, verbose_name=_("姓名"))
#     gender = models.CharField(
#         max_length=10, 
#         null=True, 
#         default="男", 
#         verbose_name=_("性别")
#     )
#     birthday = models.DateField(
#         null=True, 
#         default="1990-01-01", 
#         verbose_name=_("出生日期")
#     )
#     email = models.EmailField(
#         max_length=255, 
#         null=True, 
#         verbose_name=_("邮箱")
#     )
#     entry_date = models.DateField(
#         null=True, 
#         verbose_name=_("入职日期")
#     )
#     department = models.ForeignKey(
#         "Department", 
#         related_name='staffs', 
#         null=True, 
#         on_delete=models.SET_NULL,
#         verbose_name=_("部门")
#     )
#     team = models.ForeignKey(
#         "Team", 
#         related_name='members', 
#         null=True, 
#         on_delete=models.SET_NULL,
#         verbose_name=_("团队")
#     )
#     position = models.CharField(
#         max_length=255, 
#         null=True, 
#         verbose_name=_("职位")
#     )
#     is_team_leader = models.BooleanField(
#         default=False, 
#         verbose_name=_("是否团队负责人")
#     )
#     status = models.CharField(
#         max_length=20, 
#         choices=StaffStatus.choices,
#         default=StaffStatus.ON_DUTY,
#         verbose_name=_("员工状态")
#     )
#     phone = models.CharField(
#         max_length=20, 
#         null=True, 
#         verbose_name=_("电话")
#     )
#     remark = models.TextField(
#         null=True, 
#         verbose_name=_("备注")
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True, 
#         verbose_name=_("创建时间")
#     )
#     updated_at = models.DateTimeField(
#         auto_now=True, 
#         verbose_name=_("更新时间")
#     )

#     class Meta:
#         verbose_name = _("员工")
#         verbose_name_plural = _("员工")
#         ordering = ['-created_at']

#     def __str__(self):
#         return self.name