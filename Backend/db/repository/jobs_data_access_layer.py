
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy import delete


from schemas.jobs import JobCreate
from db.models.jobs import Job




class JobBoard():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    
    async def create_new_job(self, job: JobCreate, owner_id: int):
        new_job = Job(**job.dict(), owner_id = owner_id)
        self.db_session.add(new_job)
        await self.db_session.flush()
        return new_job

    async def retrieve_job(self, id:int):
        item = await self.db_session.get(Job, id)
        return item

    async def get_all_jobs(self) -> List[Job]:
        query = await self.db_session.execute(select(Job).order_by(Job.is_active == True))
        return query.scalars().all()

    async def update_job_by_id(self, id: int, job: JobCreate, owner_id):
        exist_job = await self.db_session.get(Job, id)
        if not exist_job:
            return 0
        job.__dict__.update(owner_id=owner_id)
        await self.db_session.execute(update(Job)
        .values(job.__dict__)
        .where(Job.id == id)
        .execution_options(synchronize_session="fetch"))
        return 1

    async def delete_job_by_id(self, id: int, owner_id):
        exist_job = await self.db_session.get(Job, id)
        if not exist_job:
            return 0
        await self.db_session.execute(delete(Job)
        .where(Job.id==id)
        .execution_options(synchronize_session=False))
        return 1

    
