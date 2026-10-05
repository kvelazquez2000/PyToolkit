from functools import cache, cached_property, lru_cache


@lru_cache(maxsize=3)
def add_5(num):
    print(f"Adding 5 to {num}")
    return num + 5
