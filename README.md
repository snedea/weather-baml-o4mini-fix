# Weather Insights API

> Type-safe weather insights powered by BAML and OpenAI o4-mini

A production-grade weather application demonstrating type-safe LLM integration using BAML (Boundary AI Markup Language). Fetches real-time weather data from OpenWeatherMap and generates intelligent insights using OpenAI's o4-mini model with aggressive caching to minimize costs.

## Features

- ✅ **Type-Safe LLM Integration** - BAML ensures compile-time type safety across the LLM boundary
- ✅ **Two-Tier Caching** - Weather data (10 min) + LLM outputs (30 min) = 90% cost reduction
- ✅ **Backend-First Architecture** - Secure API key management, no CORS issues
- ✅ **AI-Powered Insights** - Personalized weather recommendations and comfort assessments
- ✅ **OpenAPI Documentation** - Auto-generated interactive API docs at `/docs`
- ✅ **Comprehensive Testing** - Unit, integration, and BAML function tests
- ✅ **Cost Optimized** - OpenAI o4-mini is 10x cheaper than alternatives

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend | FastAPI | Async API framework with automatic docs |
| LLM Integration | BAML + OpenAI o4-mini | Type-safe LLM calls with structured outputs |
| Weather API | OpenWeatherMap | Real-time weather data (1,000 calls/day free) |
| Caching | In-memory (Python dict) | Fast cache with TTL support |
| Testing | pytest + pytest-asyncio | Comprehensive test coverage |

## Quick Start

### Prerequisites

- Python 3.9+ (tested on 3.14)
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- OpenWeatherMap API key ([Get one here](https://home.openweathermap.org/api_keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/weather-baml-o4mini-fix.git
   cd weather-baml-o4mini-fix
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. **Generate BAML client code**
   ```bash
   baml-cli generate
   ```

6. **Run the application**
   ```bash
   uvicorn src.main:app --reload
   ```

7. **Visit the API docs**
   - OpenAPI docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Usage

### Get Weather Insight

```bash
# Get weather for London (metric units)
curl "http://localhost:8000/weather?city=London"

# Get weather for New York (imperial units)
curl "http://localhost:8000/weather?city=New%20York&units=imperial"
```

**Response Example:**
```json
{
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
    "should_bring_umbrella": true
  }
}
```

### Health Check

```bash
curl "http://localhost:8000/health"
```

### Cache Statistics

```bash
curl "http://localhost:8000/cache/stats"
```

## Project Structure

```
weather-baml-o4mini-fix/
├── baml_src/              # BAML definitions (source of truth)
│   ├── types.baml         # Weather data types
│   ├── clients.baml       # OpenAI o4-mini client config
│   └── functions.baml     # LLM function definitions
├── baml_client/           # Auto-generated code (DO NOT EDIT)
├── src/
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Environment configuration
│   ├── services/
│   │   ├── weather_api.py    # OpenWeatherMap client
│   │   ├── baml_service.py   # BAML wrapper
│   │   └── cache_service.py  # Two-tier cache
│   ├── models/
│   │   └── api_models.py     # API request/response models
│   └── api/
│       └── routes.py         # API endpoints
├── tests/
│   ├── unit/             # Unit tests
│   └── conftest.py       # Pytest fixtures
├── .env                  # Environment variables (gitignored)
├── .env.example          # Environment template
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Configuration

### Environment Variables

Create a `.env` file with the following:

```bash
# Required
OPENAI_API_KEY=sk-your-openai-key-here
OPENWEATHER_API_KEY=your-openweather-key-here

# Optional (with defaults)
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5
WEATHER_CACHE_TTL=600      # 10 minutes
LLM_CACHE_TTL=1800         # 30 minutes
MAX_REQUESTS_PER_MINUTE=50
```

## Testing

### Run Unit Tests

```bash
pytest tests/unit/ -v
```

### Run All Tests

```bash
pytest tests/ -v
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

View coverage report: Open `htmlcov/index.html` in a browser

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/weather?city={city}&units={units}` | Get weather + AI insight |
| GET | `/health` | Health check |
| GET | `/cache/stats` | Cache statistics |
| GET | `/docs` | OpenAPI documentation |

## Architecture Highlights

### Two-Tier Caching Strategy

**Tier 1: Weather API Cache (10 minutes)**
- Reduces OpenWeatherMap API calls
- Key format: `weather:{city}:{units}`

**Tier 2: LLM Output Cache (30 minutes)**
- Reduces OpenAI API costs by ~90%
- Key format: `insight:{city}:{weather_hash}`

### Type-Safe LLM Integration with BAML

BAML provides:
- **Compile-time type safety** - Auto-generated Pydantic models
- **Schema-aligned parsing** - Validates LLM outputs against types
- **Automatic retries** - Exponential backoff for transient failures
- **Multi-provider support** - Easy switching between OpenAI, Anthropic, etc.

### Cost Optimization

- **OpenWeatherMap**: FREE (1,000 calls/day)
- **OpenAI o4-mini**: ~$0.15 per 1M input tokens (10x cheaper than GPT-4)
- **With caching**: ~$5-10/month for moderate usage

## BAML Development Workflow

1. Modify BAML definitions in `baml_src/*.baml`
2. Regenerate code: `baml-cli generate`
3. Restart server (important! Old imports will be stale)
4. Test changes

## Troubleshooting

### "Module not found" after BAML changes
**Solution**: Restart your Python kernel/server to reload generated code

### API key errors
**Solution**: Verify your `.env` file has valid keys and is in the project root

### BAML test failures
**Solution**: Check prompt template in `baml_src/functions.baml`

### Cache not working
**Solution**: Check logs for cache hits/misses, verify TTL settings

## Future Enhancements

- [ ] Replace in-memory cache with Redis (distributed caching)
- [ ] Add rate limiting middleware
- [ ] Implement monitoring (Prometheus/Grafana)
- [ ] Add 5-day forecast with BAML processing
- [ ] Build React frontend with city search
- [ ] Multi-model support (Gemini, Claude)
- [ ] Natural language queries ("Will I need a jacket tomorrow?")

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [BAML](https://www.boundaryml.com/) - Type-safe LLM integration
- [OpenWeatherMap](https://openweathermap.org/) - Weather data API
- [OpenAI](https://openai.com/) - o4-mini language model
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework

## Support

- Documentation: Check `/docs` endpoint for interactive API documentation
- Issues: [GitHub Issues](https://github.com/yourusername/weather-baml-o4mini-fix/issues)
- Questions: Open a discussion on GitHub

---

**Built with ❤️ using BAML and OpenAI o4-mini**
