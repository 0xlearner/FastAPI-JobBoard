from db.session import async_session
from db.repository.users import UserReg

async def get_userdb():
    async with async_session() as session:
        async with session.begin():
            yield UserReg(session)