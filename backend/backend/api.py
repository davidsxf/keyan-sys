from ninja import NinjaAPI
from core.api import router as core_router
from users.api import router as users_router
from projects.api import router as projects_router
from achievement.api import router as achievement_router



# 创建api_v1实例
api_v1 = NinjaAPI(
    title="科研管理系统API",
    description="科研管理系统的接口文档",
    version="1.0.0",
    urls_namespace="api-v1",
    # 添加认证方案
    # auth=[]  # 暂时不需要全局认证，因为我们使用JWT token在请求头中
)
api_v1.add_router("core", core_router, tags=["基础"])
api_v1.add_router("users", users_router, tags=["用户"])
api_v1.add_router("projects", projects_router, tags=["项目"])
api_v1.add_router("achievement", achievement_router, tags=["成果"])
