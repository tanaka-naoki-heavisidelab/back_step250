from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from fastapi import HTTPException
from server.db.database import database
from server.schemas.user import UserCreate
from server.models.user import User as UserModel


async def create(user: UserCreate):
    query = UserModel.__table__.insert().values(
        email=user.email, username=user.username, password=user.password
    )

    try:
        last_record_id = await database.execute(query)
        return {**user.model_dump(), "id": last_record_id}
    except SQLAlchemyError as e:
        # エラーメッセージのログを残す（例：printやログライブラリを使用）
        print(f"Database error: {e}")
        # 500のHTTPステータスコードでエラーメッセージをクライアントに返す
        raise HTTPException(status_code=500, detail="Database error")


async def select_by_email(email: str):
    query = select([UserModel]).where(UserModel.email == email)
    result = await database.fetch_one(query)
    return result
