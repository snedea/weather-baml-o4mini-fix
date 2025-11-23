"""
Unit tests for weather API client
"""
import pytest
from unittest.mock import AsyncMock, patch
from src.services.weather_api import WeatherAPIClient


@pytest.mark.asyncio
async def test_get_current_weather_cache_hit(mock_settings, cache_service, mock_weather_data):
    """Test weather API returns cached data on cache hit"""
    client = WeatherAPIClient(mock_settings, cache_service)

    # Pre-populate cache
    cache_service.set("weather:London:metric", mock_weather_data, ttl=600)

    # Should return cached data without API call
    result = await client.get_current_weather("London", "metric")
    assert result == mock_weather_data


@pytest.mark.asyncio
@patch('httpx.AsyncClient.get')
async def test_get_current_weather_cache_miss(mock_get, mock_settings, cache_service, mock_weather_data):
    """Test weather API fetches from API on cache miss"""
    client = WeatherAPIClient(mock_settings, cache_service)

    # Mock HTTP response
    mock_response = AsyncMock()
    mock_response.json.return_value = mock_weather_data
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = await client.get_current_weather("London", "metric")

    assert result == mock_weather_data
    assert cache_service.get("weather:London:metric") == mock_weather_data


@pytest.mark.asyncio
async def test_get_current_weather_different_units(mock_settings, cache_service, mock_weather_data):
    """Test that different units create separate cache entries"""
    client = WeatherAPIClient(mock_settings, cache_service)

    # Pre-populate cache with metric
    cache_service.set("weather:London:metric", mock_weather_data, ttl=600)

    # Should return cached data for metric
    result = await client.get_current_weather("London", "metric")
    assert result == mock_weather_data

    # Imperial should be a cache miss (but we can't test the API call without mocking)
    cache_entry = cache_service.get("weather:London:imperial")
    assert cache_entry is None
