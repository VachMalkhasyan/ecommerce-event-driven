from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class PaymentProcessed:
    order_id: str
    payment_id: str
    amount: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
@dataclass(frozen=True)
class PaymentFailed:
    order_id: str
    reason: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
