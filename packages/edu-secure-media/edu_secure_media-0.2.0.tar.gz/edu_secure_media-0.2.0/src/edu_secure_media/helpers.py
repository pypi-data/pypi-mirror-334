from functools import (
    wraps,
)


def memoize(func, cache, num_args):
    """Декоратор, который возвращает результат выполнения функции из кеша.

    Если кэш пуст, возвращает результат выполнения функции.
    """

    @wraps(func)
    def wrapper(*args):
        mem_args = args[:num_args]
        if mem_args in cache:
            return cache[mem_args]
        result = func(*args)
        cache[mem_args] = result

        return result

    return wrapper
