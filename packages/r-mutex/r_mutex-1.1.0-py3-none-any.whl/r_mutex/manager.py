import json
import logging

from collections import deque
from typing import Callable
from redis.asyncio import Redis
from .base import LockBase

logger = logging.getLogger(__name__)


class LockManager(LockBase):
    def __init__(self, client: Redis, key) -> None:
        super().__init__(client, key)
        self._queue = deque()
        self._current: str = None
        self._is_running: bool = False

    async def run(self) -> None:
        handlers: dict[str, Callable] = {
            "acquire": self._handle_acquire,
            "release": self._handle_release,
        }
        
        async with self._client.pubsub() as ps:
            await ps.subscribe(self._broadcast_key)
            self._is_running = True
            async for message in ps.listen():
                if message["type"] == "subscribe":
                    continue

                payload: dict = json.loads(message["data"])
                await handlers[payload["action"]](payload)

    async def _handle_acquire(self, payload: dict) -> None:
        if self._current is not None:
            self._queue.append(payload)
        else:
            self._current = payload['name']
            await self._client.publish(
                self._receiver_key, json.dumps({"name": payload["name"]})
            )

    async def _handle_release(self, payload: dict) -> None:
        if payload["name"] == self._current or '-':
            try:
                self._current = self._queue.popleft()['name']
            except IndexError:
                self._current = None

            await self._client.publish(
                self._receiver_key, json.dumps({"name": self._current or "-"})
            )
    
    @property
    def is_running(self):
        return self._is_running
