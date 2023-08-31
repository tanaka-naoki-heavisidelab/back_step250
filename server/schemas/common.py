from pydantic import BaseModel

class UserBase(BaseModel):
    email:str
    username:str

class UserRead(BaseModel):
    id: int
    username:str