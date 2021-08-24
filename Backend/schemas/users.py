from typing import Optional
from pydantic import BaseModel, EmailStr
from fastapi import Form

def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls

@form_body
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    username: str
    email: EmailStr
    is_active: bool

    class Config():
        orm_mode = True