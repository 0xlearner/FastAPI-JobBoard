from passlib.context import CryptContext

pwt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher():
    @staticmethod
    def verify_password(plain_passwd, hashed_passwd):
        return pwt_context.verify(plain_passwd, hashed_passwd)

    @staticmethod
    def get_password_hash(plain_passwd):
        return pwt_context.hash(plain_passwd)