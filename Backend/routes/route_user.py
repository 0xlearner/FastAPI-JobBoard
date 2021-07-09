from fastapi import APIRouter
from fastapi import Depends

from schemas.users import UserCreate, ShowUser
from db.repository.users import User
from depends import get_userdb

router = APIRouter()


@router.post("/",response_model=ShowUser)
async def create_user(user: UserCreate, users: User = Depends(get_userdb)):
    return await users.register_user(user)