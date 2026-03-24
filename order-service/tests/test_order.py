import pytest
import asyncio
from src.domain.order import Order, OrderStatus
from src.domain.events import OrderCreated
from src.infrastructure.event_bus import EventBus

@pytest.mark.asyncio
async def test_order_creation_emits_event():
    # Arrange
    event_bus = EventBus()
    received_events = []
    
    async def handle_order_created(event: OrderCreated):
        received_events.append(event)
    
    event_bus.subscribe(OrderCreated, handle_order_created)
    
    # Act
    order = Order(
        order_id="123",
        customer_id="cust_456",
        items=[{"id": "item_1", "quantity": 2}],
        total_amount=100.0
    )
    
    # Publish events from the aggregate
    for event in order.events:
        await event_bus.publish(event)
        
    # Assert
    assert len(received_events) == 1
    assert isinstance(received_events[0], OrderCreated)
    assert received_events[0].order_id == "123"
    assert order.status == OrderStatus.PENDING

def test_order_status_transitions():
    order = Order("123", "cust_456", [], 0.0)
    
    order.confirm()
    assert order.status == OrderStatus.CONFIRMED
    
    with pytest.raises(ValueError):
        order.confirm()
        
    order.cancel()
    assert order.status == OrderStatus.CANCELLED
