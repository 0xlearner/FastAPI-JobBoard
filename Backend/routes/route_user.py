from fastapi import APIRouter
from fastapi import Depends

from schemas.users import UserCreate, ShowUser
from db.repository.job_board_dal import User
from depends import get_db

router = APIRouter()


@router.post("/",response_model=ShowUser)
async def create_user(user: UserCreate, users: User = Depends(get_db)):
    return await users.register_user(user)