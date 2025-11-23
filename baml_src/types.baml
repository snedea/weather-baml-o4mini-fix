// Weather data structure from OpenWeatherMap API
class WeatherData {
  city string
  temperature float
  feels_like float
  humidity int
  description string
  wind_speed float
  timestamp int
}

// AI-generated weather insight
class WeatherInsight {
  summary string
  recommendation string
  comfort_level string @description("One of: comfortable, moderate, uncomfortable")
  should_bring_umbrella bool
}
