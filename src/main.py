"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_settings
from src.services.cache_service import CacheService
from src.services.weather_api import WeatherAPIClient
from src.services.baml_service import BAMLService
from src.api import routes

# Initialize settings
settings = get_settings()

# Initialize services
cache_service = CacheService()
weather_service = WeatherAPIClient(settings, cache_service)
baml_service = BAMLService(settings, cache_service)

# Set services in routes module
routes.set_services(weather_service, baml_service, cache_service)

# Create FastAPI app
app = FastAPI(
    title="Weather Insights API",
    description="Type-safe weather insights powered by BAML and OpenAI o4-mini",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Include routes
app.include_router(routes.router, tags=["weather"])


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    print("=" * 60)
    print("Weather BAML API Starting...")
    print(f"OpenAI API Key: {'✓ Configured' if settings.openai_api_key else '✗ Missing'}")
    print(f"OpenWeather API Key: {'✓ Configured' if settings.openweather_api_key else '✗ Missing'}")
    print(f"Cache TTL - Weather: {settings.weather_cache_ttl}s, LLM: {settings.llm_cache_ttl}s")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    print("Weather BAML API Shutting down...")
    cache_service.clear()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
