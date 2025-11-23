"""
API routes for weather insights
"""
from fastapi import APIRouter, HTTPException, Query
import httpx
from src.models.api_models import (
    WeatherInsightResponse,
    HealthResponse,
    CacheStatsResponse
)
from src.services.weather_api import WeatherAPIClient
from src.services.baml_service import BAMLService
from src.services.cache_service import CacheService

router = APIRouter()

# These will be initialized in main.py
weather_service: WeatherAPIClient = None
baml_service: BAMLService = None
cache_service: CacheService = None


def set_services(weather: WeatherAPIClient, baml: BAMLService, cache: CacheService):
    """Set service instances (called from main.py)"""
    global weather_service, baml_service, cache_service
    weather_service = weather
    baml_service = baml
    cache_service = cache


@router.get("/weather", response_model=WeatherInsightResponse)
async def get_weather_insight(
    city: str = Query(..., description="City name (e.g., 'London', 'New York')"),
    units: str = Query("metric", description="Temperature units (metric/imperial/standard)")
) -> WeatherInsightResponse:
    """
    Get current weather with AI-generated insights

    - **city**: City name (required)
    - **units**: metric (°C), imperial (°F), or standard (K) - default: metric

    Returns weather data with AI-generated recommendations, comfort assessment,
    and whether to bring an umbrella.
    """
    try:
        # Fetch weather data
        weather_data = await weather_service.get_current_weather(city, units)

        # Generate insight with BAML
        insight = await baml_service.generate_insight(weather_data)

        # Build response
        return WeatherInsightResponse(
            city=weather_data["name"],
            country=weather_data["sys"]["country"],
            temperature=weather_data["main"]["temp"],
            feels_like=weather_data["main"]["feels_like"],
            humidity=weather_data["main"]["humidity"],
            conditions=weather_data["weather"][0]["description"],
            wind_speed=weather_data["wind"]["speed"],
            insight=insight
        )

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"City '{city}' not found. Please check the spelling and try again."
            )
        elif e.response.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="API rate limit exceeded. Please try again later."
            )
        elif e.response.status_code == 401:
            raise HTTPException(
                status_code=500,
                detail="Weather API authentication failed. Please check API key configuration."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Weather API error: {e.response.status_code}"
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Weather API request timed out. Please try again."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint

    Returns service status. Use this to verify the API is running.
    """
    return HealthResponse(
        status="healthy",
        service="weather-baml-api"
    )


@router.get("/cache/stats", response_model=CacheStatsResponse)
async def cache_stats() -> CacheStatsResponse:
    """
    Cache statistics endpoint

    Returns current cache size and active keys. Useful for monitoring
    cache hit rates and debugging.
    """
    stats = cache_service.get_stats()
    return CacheStatsResponse(
        size=stats["size"],
        keys=stats["keys"]
    )
