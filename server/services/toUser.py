from server.db.database import database
from server.schemas.user import UserCreate
from server.models.user import User as UserModel


async def create(user: UserCreate):
    query = UserModel.__table__.insert().values(username=user.username)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}
