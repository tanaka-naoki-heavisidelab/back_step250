from fastapi import APIRouter
from server.schemas.user import User, UserCreate
from server.services.toUser import create

router = APIRouter()


@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    return await create(user)
