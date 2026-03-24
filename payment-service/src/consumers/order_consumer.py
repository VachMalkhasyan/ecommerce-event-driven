import asyncio
import logging
import random
import os
import uuid
from src.domain.events import PaymentProcessed, PaymentFailed
from libs.event_bus.subscriber import Subscriber
from libs.event_bus.publisher import Publisher

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AMQP_URL = os.getenv("AMQP_URL", "amqp://guest:guest@rabbitmq:5672/")

async def handle_order_created(data: dict):
    order_id = data.get("order_id")
    customer_id = data.get("customer_id")
    total_amount = data.get("total_amount")
    
    logger.info(f"Received OrderCreated for order {order_id}")
    
    # Mock payment logic (70% success)
    success = random.random() < 0.7
    
    publisher = Publisher(AMQP_URL)
    await publisher.connect()
    
    if success:
        payment_id = str(uuid.uuid4())
        event = PaymentProcessed(
            order_id=order_id,
            payment_id=payment_id,
            amount=total_amount
        )
        logger.info(f"Payment processed successfully for order {order_id}. Payment ID: {payment_id}")
        await publisher.publish("ecommerce_events", "payment.processed", event)
    else:
        event = PaymentFailed(
            order_id=order_id,
            reason="Insufficient funds (Mock)"
        )
        logger.warning(f"Payment failed for order {order_id}")
        await publisher.publish("ecommerce_events", "payment.failed", event)
    
    await publisher.close()

async def main():
    subscriber = Subscriber(AMQP_URL)
    await subscriber.connect()
    
    logger.info("Payment Service Consumer started, listening for OrderCreated...")
    await subscriber.subscribe(
        exchange_name="ecommerce_events",
        queue_name="payment_order_created",
        routing_key="order.ordercreated", # Matches order-service routing key mapping
        handler=handle_order_created
    )

if __name__ == "__main__":
    asyncio.run(main())
