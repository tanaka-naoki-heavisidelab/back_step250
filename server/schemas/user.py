from server.schemas.common import UserBase

class UserPost(UserBase):
    password1:str
    password2:str

class UserCreate(UserBase):
    password:str

class User(UserCreate):
    id:int