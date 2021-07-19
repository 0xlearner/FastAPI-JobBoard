from db.session import async_session
from db.repository.jobs_data_access_layer import JobBoard
from db.repository.users_data_access_layer import Users

async def get_job_db():
    async with async_session() as session:
        async with session.begin():
            yield JobBoard(session)

async def get_user_db():
    async with async_session() as session:
        async with session.begin():
            yield Users(session)