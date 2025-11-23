"""
Pytest configuration and fixtures
"""
import pytest
from src.services.cache_service import CacheService
from src.config import Settings


@pytest.fixture
def cache_service():
    """Fixture for cache service"""
    service = CacheService()
    yield service
    service.clear()


@pytest.fixture
def mock_settings():
    """Fixture for mock settings"""
    return Settings(
        openai_api_key="test_openai_key",
        openweather_api_key="test_weather_key",
        openweather_base_url="https://api.openweathermap.org/data/2.5",
        weather_cache_ttl=600,
        llm_cache_ttl=1800
    )


@pytest.fixture
def mock_weather_data():
    """Fixture for mock weather data"""
    return {
        "name": "London",
        "sys": {"country": "GB"},
        "main": {
            "temp": 15.2,
            "feels_like": 13.8,
            "humidity": 75
        },
        "weather": [
            {"description": "light rain"}
        ],
        "wind": {"speed": 5.5},
        "dt": 1234567890
    }
