from django.contrib import admin
from .models import Org, Category

@admin.register(Org)
class OrgAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'phone', 'email', 'org_type', 'created_at', 'updated_at')
    search_fields = ('name', 'description', 'phone', 'email', 'org_type')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'weight', 'sort_order', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('parent', 'created_at', 'updated_at')
    ordering = ('parent', 'sort_order')
    prepopulated_fields = {}