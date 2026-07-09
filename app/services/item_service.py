from typing import Optional

from app.domain.enums import Priority, Status
from app.domain.models import Item
from app.repositories.base import ItemRepository


class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def create_item(
        self, title: str, priority: Priority, description: Optional[str] = None
    ) -> Item:
        item = Item(title=title, priority=priority, description=description)
        return self.repository.create(item)

    def get_item(self, item_id: str) -> Optional[Item]:
        return self.repository.get_by_id(item_id)

    def list_items(self, page: int = 1, limit: int = 10) -> tuple[list[Item], int]:
        return self.repository.list(page=page, limit=limit)

    def update_status(self, item_id: str, status: Status) -> Optional[Item]:
        return self.repository.update_status(item_id, status)
