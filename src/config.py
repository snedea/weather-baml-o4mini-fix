"""
Application configuration with environment variable loading
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Keys
    openai_api_key: str
    openweather_api_key: str

    # API Configuration
    openweather_base_url: str = "https://api.openweathermap.org/data/2.5"

    # Cache Configuration
    weather_cache_ttl: int = 600  # 10 minutes
    llm_cache_ttl: int = 1800  # 30 minutes

    # Rate Limiting
    max_requests_per_minute: int = 50

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance (singleton pattern)

    Returns:
        Settings instance
    """
    return Settings()
