import asyncio
from typing import Callable, Dict, List, Any

class EventBus:
    def __init__(self):
        self._subscribers: Dict[type, List[Callable]] = {}

    def subscribe(self, event_type: type, handler: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def publish(self, event: Any):
        event_type = type(event)
        if event_type in self._subscribers:
            handlers = self._subscribers[event_type]
            await asyncio.gather(*(handler(event) for handler in handlers))
