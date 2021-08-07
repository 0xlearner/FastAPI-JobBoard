from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from sqlalchemy.sql import exists


from db.models.users import User
from schemas.users import UserCreate
from core.hashing import Hasher
from core.auth import Auth


db_session = Session

class Users():
    
    def __init__(self, db_session: Session):
        self.db_session = db_session

    
        #print(self.db_session)

    #@classmethod
    async def save(self, user_instance):
        try:
            self.db_session.add(user_instance)
            await self.db_session.flush()
        except Exception as error:
            await self.db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    #@classmethod
    async def get_user_by_id(self, id):
        user = await self.db_session.execute(select(User).filter(User.id==id))
        return user.scalar_one_or_none()

    #@classmethod
    async def get_user_by_username(self, username):
        user = await self.db_session.execute(select(User).filter(User.username==username))
        return user.scalar_one_or_none()

    #@classmethod
    async def get_user_by_email(self, email):
        user = await self.db_session.execute(select(User).filter(User.email==email))
        return user.scalar_one_or_none()

    #@classmethod
    async def get_user_by_confirmation(self, confirmation):
        user = await self.db_session.execute(select(User).filter(User.confirmation==confirmation))
        return user.scalar_one_or_none()

    #@classmethod
    async def create_user(self, user: UserCreate):
        new_user = User(username=user.username,
                        email=user.email,
                        hashed_password=Auth.get_password_hash(user.password),
                        is_active=False
                        )
        await self.save(new_user)
        return new_user

    async def authenticate_user(self, username, password):
        user = await self.get_user_by_username(username=username)
        
        if not user:
            return False
        if not Auth.verify_password(password, user.hashed_password):
            return False

        return user