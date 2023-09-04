from fastapi import APIRouter, Depends
from sqlalchemy import select
from server.schemas.common import TaskBase,UserRead
from server.schemas.task import Task, TaskCreate, TaskRead
from server.schemas.token import TokenData
from server.schemas.usertasks import UserTasksResponse
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


@router.get("/usertasks", response_model=UserTasksResponse)
async def get_usertasks(current_user: TokenData = Depends(get_current_user)):
    # タスクを取得
    query = select([TaskModel]).where(TaskModel.user_id == current_user.id)
    results = await database.fetch_all(query)
    tasks = [TaskRead(**dict(result)) for result in results]
    
    # ユーザー情報を取得
    user_info = UserRead(id=current_user.id, username=current_user.username)
    
    # レスポンスを返す
    return {
        "user": user_info,
        "tasks": tasks
    }