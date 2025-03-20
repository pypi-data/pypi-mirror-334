import asyncio
import json

from redis.asyncio import Redis
from uuid import uuid4
from .manager import LockManager
from .base import LockBase


class LockClient(LockBase):
    def __init__(
        self, client: Redis, key: str, is_manager: bool = True, timeout: float = 1.0
    ) -> None:
        super().__init__(client, key)
        self._is_manager = is_manager
        self._waiters: dict[str, asyncio.Future] = {}
        self._msg_queue = []
        self._msg_queue_index = 0
        self._timeout = timeout
        self._task: asyncio.Task = None

        if is_manager:
            self._manager = LockManager(client, key)

    async def run(self):
        if self.is_manager:
            asyncio.create_task(self._manager.run())
        asyncio.create_task(self._listen())

    async def _listen(self):
        async with self._client.pubsub() as ps:
            await ps.subscribe(self._receiver_key)

            async for message in ps.listen():
                if message["type"] == "subscribe":
                    continue

                name = json.loads(message["data"]).get("name")

                if name in self._waiters:
                    fut = self._waiters.pop(name)
                    fut.set_result(True)

    async def acquire(self):
        payload = {"name": str(uuid4()), "action": "acquire"}
        fut = self._waiters.setdefault(
            payload["name"], asyncio.get_running_loop().create_future()
        )
        await self.client.publish(
            self._broadcast_key,
            json.dumps(payload),
        )

        await fut
        return payload

    async def release(self):
        await self.client.publish(self._broadcast_key, json.dumps(self._payload))

    async def _release(self) -> None:
        await asyncio.sleep(self._timeout)
        await self.__aexit__()
        

    async def __aenter__(self):
        self._payload = await self.acquire()
        self._task = asyncio.create_task(self._release())
        return True

    async def __aexit__(self, exc_type=None, exc_value=None, tcb=None):
        self._task.cancel()
        self._payload["action"] = "release"
        await self.release()

    @property
    def client(self):
        return self._client

    @property
    def is_manager(self):
        return self._is_manager

    @property
    def manager(self):
        if self._is_manager:
            return self._manager

    @property
    def key(self):
        return self._key
