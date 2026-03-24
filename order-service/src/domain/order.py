from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime
from .events import OrderCreated

class OrderStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class Order:
    def __init__(self, order_id: str, customer_id: str, items: List[Dict], total_amount: float):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.total_amount = total_amount
        self.status = OrderStatus.PENDING
        self.events = []
        
        # Emit OrderCreated event on initialization
        self.events.append(OrderCreated(
            order_id=self.order_id,
            customer_id=self.customer_id,
            items=self.items,
            total_amount=self.total_amount
        ))

    def confirm(self):
        if self.status != OrderStatus.PENDING:
            raise ValueError(f"Cannot confirm order in status {self.status}")
        self.status = OrderStatus.CONFIRMED

    def cancel(self):
        if self.status == OrderStatus.CANCELLED:
            raise ValueError("Order is already cancelled")
        self.status = OrderStatus.CANCELLED
