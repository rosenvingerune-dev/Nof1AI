
import time
import logging
from typing import Any, Dict, Optional, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class CacheEntry:
    value: Any
    timestamp: float
    ttl: float

class CacheManager:
    """
    Simple in-memory cache manager with TTL support.
    Singleton pattern ensures shared cache across components.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CacheManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._cache: Dict[str, CacheEntry] = {}
        self._stats = {'hits': 0, 'misses': 0, 'sets': 0, 'invalidations': 0}
        self._initialized = True
        logger.info("CacheManager initialized")
        
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache. Returns None if key missing or expired.
        """
        entry = self._cache.get(key)
        if not entry:
            self._stats['misses'] += 1
            return None
            
        if time.time() - entry.timestamp > entry.ttl:
            del self._cache[key]
            self._stats['misses'] += 1
            return None
            
        self._stats['hits'] += 1
        return entry.value
        
    def set(self, key: str, value: Any, ttl: float = 60.0):
        """
        Set value in cache with TTL in seconds.
        """
        self._cache[key] = CacheEntry(value, time.time(), ttl)
        self._stats['sets'] += 1
        
    def invalidate(self, key_pattern: str = None):
        """
        Invalidate keys matching pattern (startswith) or all if None.
        """
        if key_pattern:
             keys_to_remove = [k for k in self._cache.keys() if k.startswith(key_pattern)]
             for k in keys_to_remove:
                 del self._cache[k]
             self._stats['invalidations'] += len(keys_to_remove)
             if keys_to_remove:
                 logger.debug(f"Invalidated {len(keys_to_remove)} keys matching '{key_pattern}'")
        else:
            count = len(self._cache)
            self._cache.clear()
            self._stats['invalidations'] += count
            logger.info("Cache cleared completely")

    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics"""
        return self._stats.copy()

def get_cache_manager() -> CacheManager:
    """Get the singleton CacheManager instance"""
    return CacheManager()
