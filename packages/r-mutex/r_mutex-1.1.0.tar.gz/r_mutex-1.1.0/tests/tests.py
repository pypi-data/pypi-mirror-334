import asyncio
from faker import Faker
from typing import Coroutine
from r_mutex import LockClient
from .config import REDIS_CLIENT

fkr = Faker()


async def stress_test(
    num_coroutines: int = 3, key: str = "test", sleep: int = 3
) -> None:
    async def func(name: str) -> None:
        _lock = LockClient(REDIS_CLIENT, key, is_manager=False)
        await _lock.run()

        while True:
            async with _lock:
                print(f"{name} has the lock")
                await asyncio.sleep(0.05)
                print(f"{name} releasing the lock")

    lock = LockClient(REDIS_CLIENT, key, timeout=0.75)
    asyncio.create_task(lock.run())

    i = 1
    while not lock.manager.is_running and i < 10:
        print("Lock not running...")
        i += 1
        await asyncio.sleep(i)

    print("Lock running")
    await asyncio.gather(*[func(fkr.first_name()) for _ in range(num_coroutines)])
