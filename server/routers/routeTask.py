from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from server.schemas.common import TaskBase, UserRead
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
    if task.title == "" or task.detail == "" or task.end_time == "":
        raise HTTPException(status_code=400, detail="空のフォームがあります")
    else:        
        taskcreate = TaskCreate(
            title=task.title,
            detail=task.detail,
            end_time=task.end_time,
            user_id=current_user.id,
        )
        return await create(taskcreate)


@router.get("/usertasks", response_model=UserTasksResponse)
async def get_usertasks(current_user: TokenData = Depends(get_current_user)):

    try:
        # タスクを取得
        query = select([TaskModel]).where(TaskModel.user_id == current_user.id)
        results = await database.fetch_all(query)

        # タスクが見つからない場合のエラーハンドリング
        if not results:
            raise HTTPException(status_code=404, detail="Task not found")

        tasks = [TaskRead(**dict(result)) for result in results]

        # ユーザー情報を取得
        user_info = UserRead(id=current_user.id, username=current_user.username)

        # レスポンスを返す
        return {"user": user_info, "tasks": tasks}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@router.get("/usertask/{task_id}", response_model=TaskRead)
async def get_usertask(
    task_id: int,
    current_user: TokenData = Depends(get_current_user)
):
    try:
        query = select([TaskModel]).where(
            (TaskModel.user_id == current_user.id) &
            (TaskModel.id == task_id))
        result = await database.fetch_one(query)
        
        # タスクが見つからない場合のエラーハンドリング
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")

        task = TaskRead(**dict(result))
        user_info = UserRead(id=current_user.id, username=current_user.username)
        return {"user": user_info, "task": task}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
