from server.schemas.common import TaskBase
from datetime import datetime as PythonDateTime
from typing import Optional


class TaskCreate(TaskBase):
    user_id: int


class Task(TaskCreate):
    id: int


class TaskRead(TaskBase):
    created_at: PythonDateTime
    update_at: Optional[PythonDateTime]
    user_id: int
