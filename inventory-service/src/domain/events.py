from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class InventoryReserved:
    order_id: str
    items: list
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass(frozen=True)
class InventoryFailed:
    order_id: str
    reason: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
