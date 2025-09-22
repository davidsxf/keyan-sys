from django.contrib import admin
from .models import Department, Team, Staff
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, DateWidget, DateTimeWidget

# 导入通用的编码处理类
# from common.admin import EncodingAwareImportExportModelAdmin

# 定义资源类
class DepartmentResource(resources.ModelResource):
    # 自定义parent字段处理，支持通过name查找parent
    parent = Field(attribute='parent', widget=ForeignKeyWidget(Department, 'name'))
    
    class Meta:
        model = Department
        fields = ('id', 'name', 'description', 'parent', 'created_at', 'updated_at')

# 使用通用的编码处理类
@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource
    list_display = ('id', 'name', 'description', 'parent', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

class TeamResource(resources.ModelResource):
    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'department', 'created_at', 'updated_at')

class StaffResource(resources.ModelResource):
    # 使用 ForeignKeyWidget 通过名称关联部门和团队
    # department = Field(attribute='department', widget=ForeignKeyWidget(Department, 'name'), save_as_m2m=False)
    # team = Field(attribute='team', widget=ForeignKeyWidget(Team, 'name'), save_as_m2m=False)
    
    class Meta:
        model = Staff
        # 只包含用户要求的字段
        fields = ('id', 'name', 'department', 'team')
        # 设置导入时使用的 ID 字段
        import_id_fields = ('id',)
        # 配置字段的默认值策略
        skip_unchanged = True
        report_skipped = False

@admin.register(Staff)
# 修改为使用 ImportExportModelAdmin 类
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

@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    resource_class = TeamResource
    list_display = ('id', 'name', 'description', 'department', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('department', 'created_at', 'updated_at')
    ordering = ('-created_at',)
