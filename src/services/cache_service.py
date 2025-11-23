"""
Cache service with TTL support for weather data and LLM outputs
"""
from datetime import datetime, timedelta
from typing import Any, Optional, Dict


class CacheService:
    """Simple in-memory cache with time-to-live (TTL) support"""

    def __init__(self):
        self._cache: Dict[str, tuple[Any, datetime]] = {}

    def get(self, key: str) -> Optional[Any]:
        """
        Get cached value if not expired

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        if key not in self._cache:
            return None

        value, expiry = self._cache[key]

        # Check if expired
        if datetime.now() > expiry:
            del self._cache[key]
            return None

        return value

    def set(self, key: str, value: Any, ttl: int):
        """
        Set value with TTL in seconds

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
        """
        expiry = datetime.now() + timedelta(seconds=ttl)
        self._cache[key] = (value, expiry)

    def clear(self):
        """Clear all cache entries (useful for testing)"""
        self._cache.clear()

    def get_stats(self) -> Dict[str, Any]:
        """
        Return cache statistics for monitoring

        Returns:
            Dictionary with cache size and active keys
        """
        # Clean up expired entries before returning stats
        now = datetime.now()
        expired_keys = [k for k, (_, expiry) in self._cache.items() if expiry < now]
        for key in expired_keys:
            del self._cache[key]

        return {
            "size": len(self._cache),
            "keys": list(self._cache.keys())
        }
