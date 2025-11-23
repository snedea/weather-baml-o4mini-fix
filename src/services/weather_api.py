"""
OpenWeatherMap API client with caching and error handling
"""
import httpx
from typing import Dict, Any
from src.config import Settings
from src.services.cache_service import CacheService


class WeatherAPIClient:
    """Client for fetching weather data from OpenWeatherMap API"""

    def __init__(self, settings: Settings, cache_service: CacheService):
        self.settings = settings
        self.cache = cache_service
        self.base_url = settings.openweather_base_url
        self.api_key = settings.openweather_api_key

    async def get_current_weather(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Fetch current weather for a city with cache check

        Args:
            city: City name (e.g., "London", "New York")
            units: Temperature units (metric, imperial, standard)

        Returns:
            Weather data dictionary from OpenWeatherMap API

        Raises:
            httpx.HTTPStatusError: If API request fails (404, 429, etc.)
            httpx.TimeoutException: If request times out
        """
        # Check cache first
        cache_key = f"weather:{city}:{units}"
        cached = self.cache.get(cache_key)

        if cached:
            return cached

        # Fetch from API
        url = f"{self.base_url}/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        # Cache for configured TTL (default 10 minutes)
        self.cache.set(cache_key, data, ttl=self.settings.weather_cache_ttl)

        return data

    async def get_forecast(self, city: str, units: str = "metric") -> Dict[str, Any]:
        """
        Fetch 5-day forecast for a city (optional enhancement)

        Args:
            city: City name
            units: Temperature units

        Returns:
            Forecast data dictionary
        """
        # Check cache first
        cache_key = f"forecast:{city}:{units}"
        cached = self.cache.get(cache_key)

        if cached:
            return cached

        # Fetch from API
        url = f"{self.base_url}/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

        # Cache for configured TTL
        self.cache.set(cache_key, data, ttl=self.settings.weather_cache_ttl)

        return data
