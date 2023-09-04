from fastapi import APIRouter, Depends
from sqlalchemy import select
from pydantic import parse_obj_as
from typing import List
from server.schemas.common import TaskBase
from server.schemas.task import Task, TaskCreate, TaskRead
from server.schemas.token import TokenData
from server.services.toAuth import get_current_user
from server.services.toTask import create
from server.models.task import Task as TaskModel
from server.db.database import database


router = APIRouter()


@router.post("/task", response_model=Task)
async def create_task(
    task: TaskBase, current_user: TokenData = Depends(get_current_user)
):
    taskcreate = TaskCreate(
        title=task.title,
        detail=task.detail,
        end_time=task.end_time,
        user_id=current_user.id,
    )
    return await create(taskcreate)


@router.get("/task", response_model=List[TaskRead])
async def get_task(current_user: TokenData = Depends(get_current_user)):
    query = select([TaskModel]).where(TaskModel.user_id == current_user.id)
    results = await database.fetch_all(query)
    return [parse_obj_as(TaskRead, dict(result)) for result in results]
