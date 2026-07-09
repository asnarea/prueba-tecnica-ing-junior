from sqlalchemy import Column, DateTime, String

from app.db.database import Base


class ItemORM(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    description = Column(String, nullable=True)
