from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update, delete
from server.schemas.common import TaskBase, UserRead
from server.schemas.task import Task, TaskCreate, TaskRead
from server.schemas.token import TokenData
from server.schemas.usertasks import UserTasksResponse, UserTaskResponse
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
        is_deleted=False,
    )
    return await create(taskcreate)


@router.get("/usertasks", response_model=UserTasksResponse)
async def get_usertasks(current_user: TokenData = Depends(get_current_user)):
    # タスクを取得
    query = select([TaskModel]).where(
        (TaskModel.user_id == current_user.id) & (TaskModel.is_deleted == False)
    )
    results = await database.fetch_all(query)
    tasks = [TaskRead(**dict(result)) for result in results]

    # ユーザー情報を取得
    user_info = UserRead(id=current_user.id, username=current_user.username)

    # レスポンスを返す
    return {"user": user_info, "tasks": tasks}


@router.get("/usertask/{task_id}", response_model=UserTaskResponse)
async def get_usertask(
    task_id: int, current_user: TokenData = Depends(get_current_user)
):
    query = select([TaskModel]).where(
        (TaskModel.user_id == current_user.id)
        & (TaskModel.id == task_id)
        & (TaskModel.is_deleted == False)
    )
    result = await database.fetch_one(query)

    # タスクが見つからない場合のエラーハンドリング
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")

    task = TaskRead(**dict(result))
    user_info = UserRead(id=current_user.id, username=current_user.username)
    return {"user": user_info, "task": task}


@router.get("/usertask/delete/{task_id}", response_model=TaskRead)
async def delete_usertask(
    task_id: int, current_user: TokenData = Depends(get_current_user)
):
    # 現在のユーザーと関連するタスクがあるかを確認
    query = select([TaskModel]).where(
        (TaskModel.user_id == current_user.id) & (TaskModel.id == task_id)
    )
    result = await database.fetch_one(query)

    # タスクが見つからない、またはユーザーと関連がない場合はエラーを発生させる
    if not result:
        raise HTTPException(status_code=404, detail="タスクが見つかりません")

    # タスクを論理削除
    update_query = (
        update(TaskModel.__table__)
        .where(TaskModel.id == task_id)
        .values(is_deleted=True)
    )
    await database.execute(update_query)

    # タスクの最新情報を再取得
    latest_task = await database.fetch_one(query)

    # SQLAlchemyのRowオブジェクトを辞書に変換してから、TaskReadモデルに渡す
    return TaskRead(**dict(latest_task))


@router.delete("/usertask/harddelete/{task_id}", status_code=204)
async def harddelete_usertask(
    task_id: int, current_user: TokenData = Depends(get_current_user)
):
    # 現在のユーザーと関連するタスクがあるかを確認
    query = select([TaskModel]).where(
        (TaskModel.user_id == current_user.id) & (TaskModel.id == task_id)
    )
    result = await database.fetch_one(query)

    # タスクが見つからない、またはユーザーと関連がない場合はエラーを発生させる
    if not result:
        raise HTTPException(status_code=404, detail="タスクが見つかりません")

    # タスクを削除
    delete_query = delete(TaskModel).where(TaskModel.id == task_id)
    await database.execute(delete_query)

    # 削除が成功した場合はコンテンツなしで応答
    return
