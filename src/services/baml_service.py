"""
BAML service wrapper for type-safe LLM integration
"""
import hashlib
import json
from typing import Dict, Any
from baml_client import b
from baml_client.types import WeatherData, WeatherInsight
from src.services.cache_service import CacheService
from src.config import Settings


class BAMLService:
    """Wrapper for BAML client with caching and error handling"""

    def __init__(self, settings: Settings, cache_service: CacheService):
        self.settings = settings
        self.cache = cache_service

    def _hash_weather_data(self, weather: WeatherData) -> str:
        """
        Create a hash of weather data for cache key

        Args:
            weather: WeatherData object

        Returns:
            SHA256 hash of weather data
        """
        # Create a stable string representation
        data_str = f"{weather.city}:{weather.temperature}:{weather.humidity}:{weather.description}"
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]

    async def generate_insight(self, weather_data: Dict[str, Any]) -> WeatherInsight:
        """
        Generate weather insight using BAML with LLM output caching

        Args:
            weather_data: Raw weather data from OpenWeatherMap API

        Returns:
            WeatherInsight object with AI-generated recommendations

        Raises:
            Exception: If BAML function call fails after retries
        """
        # Create BAML WeatherData object from API response
        weather = WeatherData(
            city=weather_data["name"],
            temperature=float(weather_data["main"]["temp"]),
            feels_like=float(weather_data["main"]["feels_like"]),
            humidity=int(weather_data["main"]["humidity"]),
            description=weather_data["weather"][0]["description"],
            wind_speed=float(weather_data["wind"]["speed"]),
            timestamp=int(weather_data["dt"])
        )

        # Check LLM output cache
        cache_key = f"insight:{weather.city}:{self._hash_weather_data(weather)}"
        cached_insight = self.cache.get(cache_key)

        if cached_insight:
            # Reconstruct WeatherInsight from cached dict
            return WeatherInsight(**cached_insight)

        # Call BAML function (auto-retries on failure via OpenAI client)
        insight = await b.GenerateWeatherInsight(weather)

        # Cache the insight for configured TTL (default 30 minutes)
        # Convert Pydantic model to dict for caching
        self.cache.set(
            cache_key,
            insight.model_dump(),
            ttl=self.settings.llm_cache_ttl
        )

        return insight
