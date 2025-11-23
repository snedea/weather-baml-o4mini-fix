"""
Integration tests for the full weather insights pipeline
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.cache_service import CacheService
from src.services.weather_api import WeatherAPIClient
from src.services.baml_service import BAMLService
from src.config import Settings
from baml_client.types import WeatherInsight


@pytest.fixture
def settings():
    """Test settings fixture"""
    return Settings(
        openai_api_key="test_openai_key",
        openweather_api_key="test_weather_key",
        openweather_base_url="https://api.openweathermap.org/data/2.5",
        weather_cache_ttl=600,
        llm_cache_ttl=1800
    )


@pytest.fixture
def cache():
    """Cache service fixture"""
    service = CacheService()
    yield service
    service.clear()


@pytest.fixture
def weather_client(settings, cache):
    """Weather API client fixture"""
    return WeatherAPIClient(settings, cache)


@pytest.fixture
def baml_client(settings, cache):
    """BAML service fixture"""
    return BAMLService(settings, cache)


@pytest.fixture
def mock_weather_response():
    """Mock weather API response"""
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


@pytest.mark.asyncio
async def test_full_pipeline_with_mocks(weather_client, baml_client, cache, mock_weather_response):
    """Test full pipeline from weather fetch to insight generation with mocks"""
    
    # Mock the HTTP request
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_weather_response
        mock_response.raise_for_status = MagicMock()
        
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        
        # Fetch weather data
        weather_data = await weather_client.get_current_weather("London", "metric")
        
        assert weather_data["name"] == "London"
        assert weather_data["main"]["temp"] == 15.2
        
    # Mock the BAML function call
    mock_insight = WeatherInsight(
        summary="Cool and rainy day in London with temperatures around 15°C.",
        recommendation="Wear a light jacket and bring an umbrella.",
        comfort_level="moderate",
        should_bring_umbrella=True
    )
    
    with patch('baml_client.b.GenerateWeatherInsight', new_callable=AsyncMock) as mock_baml:
        mock_baml.return_value = mock_insight
        
        # Generate insight
        insight = await baml_client.generate_insight(weather_data)
        
        assert insight.summary == "Cool and rainy day in London with temperatures around 15°C."
        assert insight.should_bring_umbrella is True
        assert insight.comfort_level == "moderate"


@pytest.mark.asyncio
async def test_caching_reduces_api_calls(weather_client, cache, mock_weather_response):
    """Test that caching reduces redundant API calls"""
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.json.return_value = mock_weather_response
        mock_response.raise_for_status = MagicMock()
        
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        
        # First call - should hit API
        data1 = await weather_client.get_current_weather("London", "metric")
        assert data1["name"] == "London"
        
        # Second call - should use cache
        data2 = await weather_client.get_current_weather("London", "metric")
        assert data2["name"] == "London"
        
        # Verify API was only called once (cache hit on second call)
        assert mock_client.return_value.__aenter__.return_value.get.call_count == 1


@pytest.mark.asyncio
async def test_llm_cache_hit(baml_client, cache, mock_weather_response):
    """Test that LLM output is cached"""
    
    mock_insight = WeatherInsight(
        summary="Test summary",
        recommendation="Test recommendation",
        comfort_level="moderate",
        should_bring_umbrella=True
    )
    
    with patch('baml_client.b.GenerateWeatherInsight', new_callable=AsyncMock) as mock_baml:
        mock_baml.return_value = mock_insight
        
        # First call - should call BAML
        insight1 = await baml_client.generate_insight(mock_weather_response)
        assert insight1.summary == "Test summary"
        
        # Second call with same data - should use cache
        insight2 = await baml_client.generate_insight(mock_weather_response)
        assert insight2.summary == "Test summary"
        
        # Verify BAML was only called once (cache hit on second call)
        assert mock_baml.call_count == 1


@pytest.mark.asyncio
async def test_error_handling_city_not_found(weather_client):
    """Test error handling when city is not found"""
    
    with patch('httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
        
        # Should raise exception
        with pytest.raises(Exception):
            await weather_client.get_current_weather("InvalidCity123", "metric")
