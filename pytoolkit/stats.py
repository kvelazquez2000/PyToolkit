import sys
from collections import Counter, defaultdict
from functools import lru_cache, partial, wraps

@lru_cache(maxsize=32)
def cached_world_count(text):
    return len(text.split())

def log_call(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"Calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper


def word_stats(words):
    counter = Counter(w.lower().strip(".,!?") for w in words if w)
    by_prefix = defaultdict(list)
    for w in counter:
        by_prefix[w[0]].append(w)
    return counter, by_prefix
 