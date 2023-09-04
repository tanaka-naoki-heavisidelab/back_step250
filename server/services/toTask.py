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
    last_record_id = await database.execute(query)
    return {**task.model_dump(), "id": last_record_id}
