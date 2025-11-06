from django.contrib import admin
from django.http import HttpResponse
from .models import Project, ProjectStaff, ProjectDocument, ProjectBudget, ProjectLeaderChange
import csv
from datetime import datetime
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# 定义资源类
class ProjectResource(resources.ModelResource):
    class Meta:
        model = Project
        fields = ('id', 'title', 'number', 'funding_number', 'leader', 'start_date', 'end_date', 'status', 'category', 'type', 'created_at', 'updated_at')

class ProjectStaffResource(resources.ModelResource):
    class Meta:
        model = ProjectStaff
        fields = ('id', 'project', 'staff', 'role', 'order', 'join_date', 'leave_date', 'remark')

class ProjectDocumentResource(resources.ModelResource):
    class Meta:
        model = ProjectDocument
        fields = ('id', 'project', 'name', 'file', 'remark', 'created_at', 'updated_at')

class ProjectBudgetResource(resources.ModelResource):
    class Meta:
        model = ProjectBudget
        fields = ('id', 'project', 'name', 'amount', 'year', 'type', 'remark', 'created_at', 'updated_at')

class ProjectLeaderChangeResource(resources.ModelResource):
    class Meta:
        model = ProjectLeaderChange
        fields = ('id', 'project', 'leader', 'change_date', 'remark', 'created_at', 'updated_at')

# 修改现有的 Admin 类
@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    resource_class = ProjectResource
    list_display = (
        'id', 'title', 'number', 'funding_number', 'leader',
        'start_date', 'end_date', 'status', 'category', 'type',
        'created_at', 'updated_at'
    )
    search_fields = ('title', 'number', 'funding_number')
    list_filter = ('status', 'type', 'category', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    filter_horizontal = ()
    actions = ['export_as_csv']

@admin.register(ProjectStaff)
class ProjectStaffAdmin(ImportExportModelAdmin):
    resource_class = ProjectStaffResource
    list_display = ('id', 'project', 'staff', 'role', 'order', 'join_date', 'leave_date', 'remark')
    search_fields = ('project__title', 'staff__name', 'role', 'remark')
    list_filter = ('role', 'join_date', 'leave_date')
    ordering = ('order',)
    actions = ['export_as_csv']

@admin.register(ProjectDocument)
class ProjectDocumentAdmin(ImportExportModelAdmin):
    resource_class = ProjectDocumentResource
    list_display = ('id', 'project', 'name', 'file', 'remark', 'created_at', 'updated_at')
    search_fields = ('project__title', 'name', 'remark')

@admin.register(ProjectBudget)
class ProjectBudgetAdmin(ImportExportModelAdmin):
    resource_class = ProjectBudgetResource
    list_display = ('id', 'project', 'name', 'amount', 'year', 'type', 'remark', 'created_at', 'updated_at')
    search_fields = ('project__title', 'name', 'remark')
    list_filter = ('year', 'type', 'created_at', 'updated_at')

@admin.register(ProjectLeaderChange)
class ProjectLeaderChangeAdmin(ImportExportModelAdmin):
    resource_class = ProjectLeaderChangeResource
    list_display = ('id', 'project', 'leader', 'change_date', 'remark', 'created_at', 'updated_at')
    search_fields = ('project__title', 'remark')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

# 已通过ImportExportModelAdmin实现数据导入导出功能，不需要额外的ExportCsvMixin
