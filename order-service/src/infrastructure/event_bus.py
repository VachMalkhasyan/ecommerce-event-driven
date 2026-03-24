import asyncio
import os
from typing import Callable, Dict, List, Any, Type
# RabbitMQ is chosen over Kafka here for its simplicity in smaller-scale microservices, 
# lower operational overhead, and built-in management UI, which are ideal for early-stage 
# event-driven systems.
from libs.event_bus.publisher import Publisher

class EventBus:
    def __init__(self):
        self._subscribers: Dict[type, List[Callable]] = {}
        # Simple bridge to RabbitMQ
        self.rabbit_publisher = Publisher(os.getenv("AMQP_URL", "amqp://guest:guest@rabbitmq:5672/"))

    def subscribe(self, event_type: type, handler: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def publish(self, event: Any):
        # Internal publish (in-process)
        event_type = type(event)
        if event_type in self._subscribers:
            handlers = self._subscribers[event_type]
            await asyncio.gather(*(handler(event) for handler in handlers))
        
        # External publish (RabbitMQ)
        # We can map domain events to exchanges/routing keys here
        await self.rabbit_publisher.publish(
            exchange_name="ecommerce_events",
            routing_key=f"order.{event_type.__name__.lower()}",
            message=event
        )
