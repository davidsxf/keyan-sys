from django.contrib import admin
from .models import Department, Team, Staff
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# 定义资源类
class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department
        fields = ('id', 'name', 'description', 'parent', 'created_at', 'updated_at')

class TeamResource(resources.ModelResource):
    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'department', 'created_at', 'updated_at')

class StaffResource(resources.ModelResource):
    class Meta:
        model = Staff
        fields = (
            'id', 'name', 'gender', 'birthday', 'email', 'entry_date',
            'department', 'team', 'position', 'is_team_leader', 'status',
            'phone', 'remark', 'created_at', 'updated_at'
        )

# 更新 Admin 类
@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource
    list_display = ('id', 'name', 'description', 'parent', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    resource_class = TeamResource
    list_display = ('id', 'name', 'description', 'department', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('department', 'created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Staff)
class StaffAdmin(ImportExportModelAdmin):
    resource_class = StaffResource
    list_display = (
        'id', 'name', 'gender', 'birthday', 'email', 'entry_date',
        'department', 'team', 'position', 'is_team_leader', 'status',
        'phone', 'remark', 'created_at', 'updated_at'
    )
    search_fields = ('name', 'email', 'phone', 'position', 'remark')
    list_filter = ('gender', 'department', 'team', 'status', 'is_team_leader', 'created_at', 'updated_at')
    ordering = ('-created_at',)
