from sqlalchemy import select
from server.db.database import database
from server.schemas.user import UserCreate
from server.models.user import User as UserModel


async def create(user: UserCreate):
    query = UserModel.__table__.insert().values(
        email=user.email, username=user.username, password=user.password
    )
    last_record_id = await database.execute(query)
    return {**user.model_dump(), "id": last_record_id}


async def select_by_email(email: str):
    query = select([UserModel]).where(UserModel.email == email)
    result = await database.fetch_one(query)
    return result
