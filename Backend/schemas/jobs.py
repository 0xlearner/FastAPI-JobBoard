from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


class JobBase(BaseModel):
    title: Optional[str] = None
    company_name: Optional[str] = None
    company_url: Optional[str] = None
    location: Optional[str] = "remote"
    description: Optional[str] = None
    date_posted: Optional[date] = datetime.now().date()

class JobCreate(JobBase):
    title: str
    company_name: str
    location: str
    description: str

class ShowJob(JobBase):
    title: str
    company_name: str
    company_url: Optional[str]
    location: str
    date_posted: date
    description: str

    class Config():
        orm_mode = True