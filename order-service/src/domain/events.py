from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict

@dataclass(frozen=True)
class OrderCreated:
    order_id: str
    customer_id: str
    items: List[Dict]
    total_amount: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
