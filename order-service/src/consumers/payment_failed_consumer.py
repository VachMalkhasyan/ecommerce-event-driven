import asyncio
import logging
import os
from src.domain.order import Order
from libs.event_bus.subscriber import Subscriber
from libs.event_bus.publisher import Publisher

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AMQP_URL = os.getenv("AMQP_URL", "amqp://guest:guest@rabbitmq:5672/")

async def handle_payment_failed(data: dict):
    order_id = data.get("order_id")
    reason = data.get("reason", "Payment failed")
    
    logger.info(f"Received PaymentFailed for order {order_id}. Reason: {reason}")
    
    # Mock loading the order and cancelling it
    # items and total_amount would normally come from a DB
    order = Order(
        order_id=order_id,
        customer_id="mock_user",
        items=[],
        total_amount=0.0
    )
    # Clear initial OrderCreated event for this mock instance
    order.events = []
    
    order.cancel(reason=f"Compensating action: {reason}")
    logger.info(f"Order {order_id} has been CANCELLED due to payment failure.")
    
    # Emit OrderCancelled compensating event
    publisher = Publisher(AMQP_URL)
    await publisher.connect()
    
    for event in order.events:
        await publisher.publish(
            exchange_name="ecommerce_events",
            routing_key="order.ordercancelled",
            message=event
        )
        logger.info(f"Emitted OrderCancelled event for order {order_id}")
    
    await publisher.close()

async def main():
    subscriber = Subscriber(AMQP_URL)
    await subscriber.connect()
    
    logger.info("Order Service Saga Consumer started, listening for PaymentFailed...")
    await subscriber.subscribe(
        exchange_name="ecommerce_events",
        queue_name="order_saga_payment_failed",
        routing_key="payment.failed",
        handler=handle_payment_failed
    )

if __name__ == "__main__":
    asyncio.run(main())
