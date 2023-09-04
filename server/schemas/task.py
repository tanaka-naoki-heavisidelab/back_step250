from server.schemas.common import TaskBase


class TaskCreate(TaskBase):
    user_id:int

class Task(TaskCreate):
    id:int