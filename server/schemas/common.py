from pydantic import BaseModel
from datetime import datetime as PythonDateTime
from typing import Optional

class UserBase(BaseModel):
    email: str
    username: str


class UserRead(BaseModel):
    id: int
    username: str


class TaskBase(BaseModel):
    title: str
    detail: Optional[str]
    end_time: PythonDateTime
