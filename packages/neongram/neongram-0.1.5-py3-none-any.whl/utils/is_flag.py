from functools import wraps
from typing import Dict, Any, Callable

def is_flag(func: Callable) -> Callable:
    """Decorator to mark a TL parameter as a flag and handle its conditional presence.

    Args:
        func: The function or method to decorate (e.g., serialize or deserialize).

    Returns:
        Callable: Wrapped function with flag handling.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        params = kwargs.get('params', [])
        values = kwargs.get('values', {})
        for param in params:
            if 'flag' in param and param.get('flag') is not None:
                flag_value = values.get(param['flag'], 0)
                if not (flag_value & (1 << param.get('bit', 0))):
                    # If the flag bit is not set, exclude this parameter
                    values.pop(param['name'], None)
        return func(self, *args, **kwargs)
    return wrapper