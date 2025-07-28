from django.contrib import admin

from .models import Org, Department, Category

@admin.register(Org)
class OrgAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'org', 'name', 'created_at')
    search_fields = ('name',)
    list_filter = ('org',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'sort_order', 'created_at')
    search_fields = ('name',)
    list_filter = ('parent',)
