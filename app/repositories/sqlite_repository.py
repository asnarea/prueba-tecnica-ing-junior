from typing import Optional

from sqlalchemy.orm import Session

from app.db.models_orm import ItemORM
from app.domain.enums import Priority, Status
from app.domain.models import Item
from app.repositories.base import ItemRepository


class SQLiteItemRepository(ItemRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, item: Item) -> Item:
        orm_item = ItemORM(
            id=item.id,
            title=item.title,
            priority=item.priority.value,
            status=item.status.value,
            created_at=item.created_at,
            description=item.description,
        )
        self.db.add(orm_item)
        self.db.commit()
        self.db.refresh(orm_item)
        return self._to_domain(orm_item)

    def get_by_id(self, item_id: str) -> Optional[Item]:
        orm_item = self.db.query(ItemORM).filter(ItemORM.id == item_id).first()
        return self._to_domain(orm_item) if orm_item else None

    def list(self, page: int, limit: int) -> tuple[list[Item], int]:
        query = self.db.query(ItemORM)
        total = query.count()
        offset = (page - 1) * limit
        orm_items = query.offset(offset).limit(limit).all()
        return [self._to_domain(o) for o in orm_items], total

    def update_status(self, item_id: str, status: Status) -> Optional[Item]:
        orm_item = self.db.query(ItemORM).filter(ItemORM.id == item_id).first()
        if not orm_item:
            return None
        orm_item.status = status.value
        self.db.commit()
        self.db.refresh(orm_item)
        return self._to_domain(orm_item)

    @staticmethod
    def _to_domain(orm_item: ItemORM) -> Item:
        return Item(
            id=orm_item.id,
            title=orm_item.title,
            priority=Priority(orm_item.priority),
            status=Status(orm_item.status),
            created_at=orm_item.created_at,
            description=orm_item.description,
        )
