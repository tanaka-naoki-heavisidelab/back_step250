from sqlalchemy import Column,Integer,String
from server.models.base import Base

class User(Base):
    __tablename__="users"
    __table_args__={"extend_existing":True}
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    username=Column(String(64),nullable=False)