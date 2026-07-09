from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.sqlite_repository import SQLiteItemRepository
from app.services.item_service import ItemService


def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    repository = SQLiteItemRepository(db)
    return ItemService(repository)
