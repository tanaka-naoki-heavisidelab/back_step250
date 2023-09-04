from pydantic import BaseModel
from server.schemas.task import TaskRead
from server.schemas.common import UserRead

from typing import List

class UserTasksResponse(BaseModel):
    user: UserRead
    tasks: List[TaskRead]