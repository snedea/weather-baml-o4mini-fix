"""
Unit tests for cache service
"""
import pytest
import time
from src.services.cache_service import CacheService


def test_cache_set_and_get(cache_service):
    """Test basic cache set and get operations"""
    cache_service.set("test_key", "test_value", ttl=60)
    assert cache_service.get("test_key") == "test_value"


def test_cache_expiry(cache_service):
    """Test that cache entries expire after TTL"""
    cache_service.set("temp_key", "temp_value", ttl=1)
    assert cache_service.get("temp_key") == "temp_value"

    # Wait for expiry
    time.sleep(2)
    assert cache_service.get("temp_key") is None


def test_cache_miss(cache_service):
    """Test cache miss returns None"""
    assert cache_service.get("nonexistent_key") is None


def test_cache_clear(cache_service):
    """Test cache clear removes all entries"""
    cache_service.set("key1", "value1", ttl=60)
    cache_service.set("key2", "value2", ttl=60)

    assert len(cache_service.get_stats()["keys"]) == 2

    cache_service.clear()
    assert len(cache_service.get_stats()["keys"]) == 0


def test_cache_stats(cache_service):
    """Test cache statistics"""
    cache_service.set("key1", "value1", ttl=60)
    cache_service.set("key2", "value2", ttl=60)

    stats = cache_service.get_stats()
    assert stats["size"] == 2
    assert "key1" in stats["keys"]
    assert "key2" in stats["keys"]


def test_cache_overwrites(cache_service):
    """Test that setting same key overwrites previous value"""
    cache_service.set("key", "value1", ttl=60)
    assert cache_service.get("key") == "value1"

    cache_service.set("key", "value2", ttl=60)
    assert cache_service.get("key") == "value2"
