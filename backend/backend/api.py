from ninja import NinjaAPI
from core.api import router as core_router
from users.api import router as users_router
from projects.api import router as projects_router


api_v1 = NinjaAPI(version="1.0.0", title="项目 API")
api_v1.add_router("core", core_router)
api_v1.add_router("users", users_router)
api_v1.add_router("projects", projects_router)
