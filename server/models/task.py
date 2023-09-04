from sqlalchemy import Column, Integer, String, DateTime as SQLDateTime, ForeignKey, func
from server.models.base import Base

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(64), index=True, nullable=False)
    detail = Column(String(128), index=True)
    end_time = Column(SQLDateTime, nullable=False)
    created_at = Column(SQLDateTime, server_default=func.now(), nullable=False)
    update_at = Column(SQLDateTime, onupdate=func.utc_timestamp(), nullable=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )