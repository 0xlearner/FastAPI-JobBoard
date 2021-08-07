from fastapi import APIRouter

from web_apps.jobs import route_jobs
from web_apps.users import route_users

webapp_router = APIRouter()

webapp_router.include_router(route_jobs.router, prefix="", tags=["homepage"])
webapp_router.include_router(route_users.router, prefix="", tags=["users"])