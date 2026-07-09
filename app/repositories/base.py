from abc import ABC, abstractmethod
from typing import Optional

from app.domain.enums import Status
from app.domain.models import Item


class ItemRepository(ABC):
    @abstractmethod
    def create(self, item: Item) -> Item:
        ...

    @abstractmethod
    def get_by_id(self, item_id: str) -> Optional[Item]:
        ...

    @abstractmethod
    def list(self, page: int, limit: int) -> tuple[list[Item], int]:
        ...

    @abstractmethod
    def update_status(self, item_id: str, status: Status) -> Optional[Item]:
        ...
