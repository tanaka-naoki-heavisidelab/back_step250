from pydantic import BaseModel

class UserBase(BaseModel):
    username:str

class UserRead(BaseModel):
    id: int
    username:str