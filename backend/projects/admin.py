from django.contrib import admin
from django.http import HttpResponse
from .models import Project, ProjectStaff, ProjectDocument, ProjectBudget, ProjectLeaderChange
import csv
from datetime import datetime

# 添加这个函数到文件开头
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta}-{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "导出选中的记录为CSV"

# 修改现有的 Admin 类
@admin.register(Project)
class ProjectAdmin(ExportCsvMixin, admin.ModelAdmin):
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
class ProjectStaffAdmin(ExportCsvMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'staff', 'role', 'order', 'join_date', 'leave_date', 'remark')
    search_fields = ('project__title', 'staff__name', 'role', 'remark')
    list_filter = ('role', 'join_date', 'leave_date')
    ordering = ('order',)
    actions = ['export_as_csv']

@admin.register(ProjectDocument)
class ProjectDocumentAdmin(ExportCsvMixin, admin.ModelAdmin):
    list_display = ('id', 'project', 'name', 'file', 'remark', 'created_at', 'updated_at')
    search_fields = ('project__title', 'name', 'remark')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

# 添加项目预算管理
@admin.register(ProjectBudget)
class ProjectBudgetAdmin(ExportCsvMixin, admin.ModelAdmin):
    list_display = (
        'id', 'project', 'name', 'amount', 'year',
        'get_type_display', 'remark', 'created_at', 'updated_at'
    )
    search_fields = ('project__title', 'name', 'remark')
    list_filter = ('type', 'year', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    actions = ['export_as_csv']

# 添加项目负责人变更管理
@admin.register(ProjectLeaderChange)
class ProjectLeaderChangeAdmin(ExportCsvMixin, admin.ModelAdmin):
    list_display = (
        'id', 'project', 'leader', 'change_date', 'remark',
        'created_at', 'updated_at'
    )
    search_fields = ('project__title', 'leader__name', 'remark')
    list_filter = ('change_date', 'created_at', 'updated_at')
    ordering = ('-change_date', '-created_at')
    actions = ['export_as_csv']
