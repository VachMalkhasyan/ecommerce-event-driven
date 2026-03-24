import aio_pika
import json
from datetime import datetime
from dataclasses import asdict
from typing import Any

class Publisher:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()

    async def publish(self, exchange_name: str, routing_key: str, message: Any):
        if not self.channel:
            await self.connect()

        exchange = await self.channel.declare_exchange(
            exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
        )

        # Custom JSON serializer for datetime
        def json_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return obj

        message_body = json.dumps(asdict(message) if hasattr(message, "asdict") else asdict(message) if hasattr(message, "__dataclass_fields__") else message, default=json_serializer).encode()

        await exchange.publish(
            aio_pika.Message(
                body=message_body,
                content_type="application/json",
            ),
            routing_key=routing_key,
        )

    async def close(self):
        if self.connection:
            await self.connection.close()
