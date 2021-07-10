
from sqlalchemy.orm import Session, query

from schemas.users import UserCreate
from schemas.jobs import JobCreate
from db.models.users import User
from db.models.jobs import Job
from core.hashing import Hasher



class job_board():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def register_user(self, user: UserCreate):
        new_user = User(username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active = False,
        is_superuser=False
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    
    async def create_new_job(self, job: JobCreate, owner_id: int):
        new_job = Job(**job.dict(), owner_id = owner_id)
        self.db_session.add(new_job)
        await self.db_session.flush()
        return new_job

    async def retrieve_job(self, id:int):
        item = await self.db_session.get(Job, id)
        return item
