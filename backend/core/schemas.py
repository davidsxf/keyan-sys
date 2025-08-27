from ninja import Schema
from typing import List, Optional

class CategoryIn(Schema):
    name: str
    parent_id: Optional[int] = None
    weight: int = 0
    sort_order: int = 0

class CategoryOut(Schema):
    id: int
    name: str
    parent_id: Optional[int]
    weight: int
    sort_order: int
    children: List['CategoryOut'] = []
    
# 解决自引用问题
CategoryOut.update_forward_refs()