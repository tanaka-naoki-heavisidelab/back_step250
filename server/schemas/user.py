from server.schemas.common import UserBase

class UserCreate(UserBase):
    pass

class User(UserCreate):
    id:int