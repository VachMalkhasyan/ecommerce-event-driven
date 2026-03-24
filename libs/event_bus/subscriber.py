import aio_pika
import json
from typing import Callable, Any

class Subscriber:
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()

    async def subscribe(self, exchange_name: str, queue_name: str, routing_key: str, handler: Callable[[Any], Any]):
        if not self.channel:
            await self.connect()

        exchange = await self.channel.declare_exchange(
            exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
        )

        queue = await self.channel.declare_queue(queue_name, durable=True)
        await queue.bind(exchange, routing_key=routing_key)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body.decode())
                    await handler(data)

    async def close(self):
        if self.connection:
            await self.connection.close()
