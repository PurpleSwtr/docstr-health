import time
from functools import wraps
from typing import Callable

all_timed: list[float] = []


def check_all_functions_time_avg(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        average = sum(all_timed) / len(all_timed)
        print(f"avg = {round(average, 6)}")
        return res

    return wrapper


def check_seconds(func: Callable):
    """Measuring the execution time of a function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        timed = end - start
        # print(f"{func.__name__}: {timed:.12f}")
        all_timed.append(timed)
        return res

    return wrapper
