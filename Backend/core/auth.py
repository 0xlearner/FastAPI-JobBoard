from jose import jwt
from datetime import datetime, timedelta
from core.config import Settings
from pydantic import UUID4, EmailStr
import uuid
from passlib.context import CryptContext

settings = Settings()


class Auth():
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.password_context.hash(password)

    @classmethod
    def verify_password(cls, plain_passwd, hashed_passwd):
        return cls.password_context.verify(plain_passwd, hashed_passwd)

    @staticmethod
    def get_token(data: dict, expires_delta: int):
        to_encode = data.copy()
        to_encode.update({
            "exp": datetime.utcnow() + timedelta(seconds=expires_delta),
            "iss": settings.PROJECT_NAME
        })
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.TOKEN_ALGORITHM
        )

    @staticmethod
    def get_confirmation_token(user_email: str, jti: UUID4):
        claims = {
            "sub": str(user_email),
            "scope": "registration",
            "jti": str(jti)
        }
        return {
            "jti": str(jti),
            "token": Auth.get_token(
                claims,
                settings.REGISTRATION_TOKEN_LIFETIME
            )
        }