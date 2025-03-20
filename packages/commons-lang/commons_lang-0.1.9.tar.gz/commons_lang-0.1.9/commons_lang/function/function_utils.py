import time
from loguru import logger


def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} elapsed time: {end_time - start_time:.4f} s")
        return result

    return wrapper

