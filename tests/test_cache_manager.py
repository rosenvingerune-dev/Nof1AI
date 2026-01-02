
import time
import pytest
from src.gui.services.cache_manager import CacheManager, get_cache_manager

class TestCacheManager:
    
    def setup_method(self):
        self.cache = CacheManager()
        self.cache.invalidate() # Clear cache before each test
        
    def test_singleton(self):
        c1 = get_cache_manager()
        c2 = get_cache_manager()
        assert c1 is c2
        assert c1 is self.cache

    def test_set_get(self):
        self.cache.set("foo", "bar", ttl=1.0)
        assert self.cache.get("foo") == "bar"
        
    def test_ttl_expiration(self):
        self.cache.set("quick", "gone", ttl=0.1)
        assert self.cache.get("quick") == "gone"
        time.sleep(0.15)
        assert self.cache.get("quick") is None

    def test_invalidation(self):
        self.cache.set("test_1", "v1")
        self.cache.set("test_2", "v2")
        self.cache.set("other", "v3")
        
        # Invalidate pattern
        self.cache.invalidate("test")
        assert self.cache.get("test_1") is None
        assert self.cache.get("test_2") is None
        assert self.cache.get("other") == "v3" # Should survive

    def test_stats(self):
        self.cache.invalidate() # Reset stats implicitly? No, stats persist in singleton usually.
        # Ideally we should define a method to reset stats for testing, but let's just check increments
        
        initial_stats = self.cache.get_stats()
        self.cache.set("stat_key", "val")
        self.cache.get("stat_key") # hit
        self.cache.get("missing") # miss
        
        new_stats = self.cache.get_stats()
        assert new_stats['sets'] == initial_stats['sets'] + 1
        assert new_stats['hits'] == initial_stats['hits'] + 1
        assert new_stats['misses'] == initial_stats['misses'] + 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
