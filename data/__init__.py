from .repositories import DataRepository
from .cache import DataCache

class DataService:
    def __init__(self):
        self.repo = DataRepository()
        self.cache = DataCache()
    
    def get_property_data(self, filters=None):
        cache_key = f"property_data_{str(filters)}"
        cached_data = self.cache.get(cache_key)
        
        if cached_data is not None:
            return cached_data
            
        data = self.repo.get_property_data(filters)
        self.cache.set(cache_key, data, timeout=3600)  # Cache for 1 hour
        return data