from server.schemas.common import TaskBase
from server.schemas.task import Task,TaskCreate
from server.schemas.token import TokenData
from server.services.toAuth import get_current_user
from server.services.toTask import create
from fastapi import APIRouter,Depends

router = APIRouter()
@router.post("/create_task", response_model=Task)
async def create_user(
    task: TaskBase,
    current_user: TokenData = Depends(get_current_user)
):
    taskcreate = TaskCreate(
        title=task.title, 
        detail=task.detail, 
        end_time=task.end_time,
        user_id=current_user.id
    )
    return await create(taskcreate)