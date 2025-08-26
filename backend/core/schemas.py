from ninja import ModelSchema
from .models import Category
from typing import Optional

class CategoryIn(ModelSchema):
    """用于创建和更新类别的输入模型"""
    class Meta:
        model = Category
        exclude = ["id", "created_at", "updated_at"]
        from_attributes = True

class CategoryListOut(ModelSchema):
    """用于列表展示的输出模型"""
    has_children: bool = False
    
    class Meta:
        model = Category
        fields = ["id", "name", "parent", "weight", "sort_order"]
        from_attributes = True
    
    @staticmethod
    def resolve_has_children(obj):
        return obj.children.exists()

class CategoryOut(ModelSchema):
    """用于详情展示的输出模型"""
    children: list["CategoryListOut"] = []
    
    class Meta:
        model = Category
        fields = ["id", "name", "parent", "weight", "sort_order", "created_at", "updated_at"]
        from_attributes = True
    
    @staticmethod
    def resolve_children(obj):
        return obj.children.order_by('sort_order').all()
    