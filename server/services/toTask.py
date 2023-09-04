from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from server.db.database import database
from server.schemas.task import TaskCreate
from server.models.task import Task as TaskModel


async def create(task: TaskCreate):
    query = TaskModel.__table__.insert().values(
        title=task.title,
        detail=task.detail,
        end_time=task.end_time,
        user_id=task.user_id,
    )
    try:
        last_record_id = await database.execute(query)
        return {**task.model_dump(), "id": last_record_id}
    except SQLAlchemyError as e:
        # エラーメッセージのログを残す（例：printやログライブラリを使用）
        print(f"Database error: {e}")
        # 500のHTTPステータスコードでエラーメッセージをクライアントに返す
        raise HTTPException(status_code=500, detail="Database error")
