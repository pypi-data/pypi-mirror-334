import asyncio
from typing import Any, Callable, TypeVar, Coroutine, Optional, List
from neongram.client.client import NeonClient
from neongram.parser.tl_object import TLObject
from neongram.errors.exceptions import TimeoutError

T = TypeVar("T")


async def retry_async(func: Callable[..., Coroutine[Any, Any, T]], retries: int = 3, delay: float = 1.0, exceptions: tuple[type[Exception], ...] = (Exception,)) -> T:
    for attempt in range(retries):
        try:
            return await func()
        except exceptions as e:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(delay)


async def run_in_executor(client: NeonClient, func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


async def gather_with_concurrency(limit: int, tasks: List[Coroutine[Any, Any, T]]) -> List[T]:
    semaphore = asyncio.Semaphore(limit)

    async def sem_task(task: Coroutine[Any, Any, T]) -> T:
        async with semaphore:
            return await task

    return await asyncio.gather(*[sem_task(task) for task in tasks])


async def wait_for_response(client: NeonClient, request_id: int, timeout: float = 10.0) -> Optional[TLObject]:
    start_time = asyncio.get_event_loop().time()
    while True:
        if response := client.responses.get(request_id):
            client.responses.pop(request_id, None)
            return response
        if asyncio.get_event_loop().time() - start_time > timeout:
            raise TimeoutError(f"Timeout waiting for response with request_id={request_id}")
        await asyncio.sleep(0.1)


async def debounce(func: Callable[..., Coroutine[Any, Any, T]], wait: float) -> Callable[..., Coroutine[Any, Any, T]]:
    last_call = 0
    last_task: Optional[asyncio.Task] = None

    async def wrapper(*args: Any, **kwargs: Any) -> T:
        nonlocal last_call, last_task
        current_time = asyncio.get_event_loop().time()
        if current_time - last_call < wait and last_task:
            last_task.cancel()

        last_call = current_time
        last_task = asyncio.create_task(func(*args, **kwargs))
        return await last_task

    return wrapper