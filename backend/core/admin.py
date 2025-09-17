from django.contrib import admin
from .models import Org, Category
from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

# 导入通用的编码处理类
from common.admin import EncodingAwareImportExportModelAdmin

# 定义资源类
class OrgResource(resources.ModelResource):
    class Meta:
        model = Org
        fields = ('id', 'name', 'description', 'phone', 'email', 'org_type', 'created_at', 'updated_at')

class CategoryResource(resources.ModelResource):
    # 添加 ForeignKeyWidget 处理自引用字段
    parent = Field(attribute='parent', widget=ForeignKeyWidget(Category, 'name'))
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'weight', 'sort_order', 'created_at', 'updated_at')

@admin.register(Org)
class OrgAdmin(EncodingAwareImportExportModelAdmin):
    resource_class = OrgResource
    list_display = ('id', 'name', 'description', 'phone', 'email', 'org_type', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'phone', 'email', 'org_type')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(EncodingAwareImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('id', 'name', 'parent', 'weight', 'sort_order', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('parent', 'created_at', 'updated_at')
    ordering = ('parent', 'sort_order')
    prepopulated_fields = {}