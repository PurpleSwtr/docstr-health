import time
from functools import wraps
from typing import Callable


def display_module(func):
    """
    Не особо пригодился этот декоратор, решил перейти глобально на rich.Panels, но пока что оставлю
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        instance = args[0]
        print(str(f"| {instance.module} |").center(32, "-"))
        # instance.output.display_panel(text, str(instance.module))
        return func(*args, **kwargs)

    return wrapper


def check_seconds(func: Callable):
    """Measuring the execution time of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        timed = end - start
        print(f"{func.__name__}: {timed:.12f}")
        return res

    return wrapper
