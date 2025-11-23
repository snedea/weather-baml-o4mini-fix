"""
API request and response models
"""
from pydantic import BaseModel, Field
from baml_client.types import WeatherInsight


class WeatherInsightResponse(BaseModel):
    """Response model for weather endpoint"""

    city: str = Field(description="City name")
    country: str = Field(description="Country code (e.g., GB, US)")
    temperature: float = Field(description="Temperature in specified units")
    feels_like: float = Field(description="Feels like temperature")
    humidity: int = Field(description="Humidity percentage")
    conditions: str = Field(description="Weather conditions description")
    wind_speed: float = Field(description="Wind speed")
    insight: WeatherInsight = Field(description="AI-generated weather insight")

    class Config:
        json_schema_extra = {
            "example": {
                "city": "London",
                "country": "GB",
                "temperature": 15.2,
                "feels_like": 13.8,
                "humidity": 75,
                "conditions": "light rain",
                "wind_speed": 5.5,
                "insight": {
                    "summary": "Cool and rainy day in London with temperatures around 15°C.",
                    "recommendation": "Wear a light jacket and bring an umbrella. Indoor activities recommended.",
                    "comfort_level": "moderate",
                    "should_bring_umbrella": True
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""

    detail: str = Field(description="Error message")
    status_code: int = Field(description="HTTP status code")


class HealthResponse(BaseModel):
    """Health check response model"""

    status: str = Field(description="Service status")
    service: str = Field(description="Service name")


class CacheStatsResponse(BaseModel):
    """Cache statistics response model"""

    size: int = Field(description="Number of cached items")
    keys: list[str] = Field(description="List of cache keys")
