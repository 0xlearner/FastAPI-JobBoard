from fastapi import APIRouter

from routes import route_user, route_jobs

api = APIRouter()

api.include_router(route_user.router, prefix="/registration", tags=["users"])
api.include_router(route_jobs.router, prefix="/job", tags=["Jobs"])