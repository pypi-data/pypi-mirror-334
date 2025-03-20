import time
from typing import Any, Callable, TypeVar, Optional, List
from neongram.client.client import NeonClient
from neongram.parser.tl_object import TLObject
from neongram.errors.exceptions import TimeoutError

T = TypeVar("T")


def retry_sync(func: Callable[..., T], retries: int = 3, delay: float = 1.0, exceptions: tuple[type[Exception], ...] = (Exception,)) -> T:
    for attempt in range(retries):
        try:
            return func()
        except exceptions as e:
            if attempt == retries - 1:
                raise
            time.sleep(delay)


def batch_process(items: List[Any], batch_size: int, process_func: Callable[[Any], None]) -> None:
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        for item in batch:
            process_func(item)


def wait_for_response_sync(client: NeonClient, request_id: int, timeout: float = 10.0) -> Optional[TLObject]:
    start_time = time.time()
    while True:
        if response := client.responses.get(request_id):
            client.responses.pop(request_id, None)
            return response
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Timeout waiting for response with request_id={request_id}")
        time.sleep(0.1)


def throttle(func: Callable[..., T], rate_limit: float) -> Callable[..., T]:
    last_call = 0

    def wrapper(*args: Any, **kwargs: Any) -> T:
        nonlocal last_call
        current_time = time.time()
        elapsed = current_time - last_call
        if elapsed < rate_limit:
            time.sleep(rate_limit - elapsed)
        last_call = time.time()
        return func(*args, **kwargs)

    return wrapper


def memoize(func: Callable[..., T]) -> Callable[..., T]:
    cache: dict[tuple, T] = {}

    def wrapper(*args: Any, **kwargs: Any) -> T:
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper