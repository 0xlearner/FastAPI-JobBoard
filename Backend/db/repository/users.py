
from sqlalchemy.orm import Session

from schemas.users import UserCreate
from db.models.users import User
from core.hashing import Hasher



class UserReg():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def register_user(self, user: UserCreate):
        new_user = User(username=user.username,
        email=user.email,
        hashed_password=Hasher.get_password_hash(user.password),
        is_active = True,
        is_superuser=False
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user


# def user_registration(user: UserCreate, db: Session):
#     user = User(username=user.username,
#     email=user.email,
#     hashed_password=Hasher.get_password_hash(user.password),
#     is_active = True,
#     is_superuser=False
#     )

#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user
