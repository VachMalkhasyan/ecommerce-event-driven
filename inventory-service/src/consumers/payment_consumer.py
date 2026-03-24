import asyncio
import logging
import os
from src.domain.events import InventoryReserved, InventoryFailed
from libs.event_bus.subscriber import Subscriber
from libs.event_bus.publisher import Publisher

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AMQP_URL = os.getenv("AMQP_URL", "amqp://guest:guest@rabbitmq:5672/")

async def handle_payment_processed(data: dict):
    order_id = data.get("order_id")
    
    logger.info(f"Received PaymentProcessed for order {order_id}")
    
    # Mock stock check logic
    # In a real system, you'd check a DB here
    success = True # Mocking success for now
    
    publisher = Publisher(AMQP_URL)
    await publisher.connect()
    
    if success:
        event = InventoryReserved(
            order_id=order_id,
            items=[] # Mock items
        )
        logger.info(f"Inventory reserved for order {order_id}")
        await publisher.publish("ecommerce_events", "inventory.reserved", event)
    else:
        event = InventoryFailed(
            order_id=order_id,
            reason="Out of stock (Mock)"
        )
        logger.warning(f"Inventory reservation failed for order {order_id}")
        await publisher.publish("ecommerce_events", "inventory.failed", event)
    
    await publisher.close()

async def main():
    subscriber = Subscriber(AMQP_URL)
    await subscriber.connect()
    
    logger.info("Inventory Service Consumer started, listening for PaymentProcessed...")
    await subscriber.subscribe(
        exchange_name="ecommerce_events",
        queue_name="inventory_payment_processed",
        routing_key="payment.processed",
        handler=handle_payment_processed
    )

if __name__ == "__main__":
    asyncio.run(main())
