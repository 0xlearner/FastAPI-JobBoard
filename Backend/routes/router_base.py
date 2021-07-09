from fastapi import APIRouter

from routes import route_user

api = APIRouter()

api.include_router(route_user.router, prefix="/registration", tags=["users"])