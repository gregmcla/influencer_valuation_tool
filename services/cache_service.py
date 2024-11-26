
from functools import wraps
from datetime import datetime, timedelta
import json
from pathlib import Path

class CacheService:
    def __init__(self, cache_dir='cache', ttl_hours=24):
        self.cache_dir = Path(__file__).parent.parent / cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        self.cache_dir.mkdir(exist_ok=True)

    def cache_key(self, *args, **kwargs):
        key = f"{'-'.join(str(arg) for arg in args)}"
        return key.replace('/', '_').lower()

    def get_cached(self, key):
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            data = json.loads(cache_file.read_text())
            if datetime.fromisoformat(data['timestamp']) + self.ttl > datetime.now():
                return data['content']
        return None

    def set_cached(self, key, content):
        cache_file = self.cache_dir / f"{key}.json"
        data = {
            'timestamp': datetime.now().isoformat(),
            'content': content
        }
        cache_file.write_text(json.dumps(data))

def cached(ttl_hours=24):
    def decorator(func):
        cache_service = CacheService(ttl_hours=ttl_hours)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = cache_service.cache_key(func.__name__, *args, **kwargs)
            cached_result = cache_service.get_cached(cache_key)
            
            if cached_result is not None:
                return cached_result
                
            result = func(*args, **kwargs)
            cache_service.set_cached(cache_key, result)
            return result
        return wrapper
    return decorator