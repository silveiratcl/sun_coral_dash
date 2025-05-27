from datetime import timedelta
import pandas as pd
from functools import wraps
import time

class DataCache:
    def __init__(self):
        self._cache = {}
        self._timestamps = {}

    def cached(self, timeout=300):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
                
                # Check if cached and not expired
                if cache_key in self._cache:
                    if time.time() - self._timestamps[cache_key] < timeout:
                        return self._cache[cache_key]
                
                # Execute and cache
                result = func(*args, **kwargs)
                self._cache[cache_key] = result
                self._timestamps[cache_key] = time.time()
                return result
            return wrapper
        return decorator

cache = DataCache()