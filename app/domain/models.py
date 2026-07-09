import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.enums import Priority, Status

@dataclass
class Item:
    title: str
    priority: Priority
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: Status = Status.PENDING
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    description: str | None = None
