// BAML function tests
// These tests verify that the GenerateWeatherInsight function works correctly

test GenerateWeatherInsightSunny {
  functions [GenerateWeatherInsight]
  args {
    weather {
      city "London"
      temperature 22.5
      feels_like 21.0
      humidity 45
      description "clear sky"
      wind_speed 3.2
      timestamp 1234567890
    }
  }
}

test GenerateWeatherInsightRainy {
  functions [GenerateWeatherInsight]
  args {
    weather {
      city "Seattle"
      temperature 12.0
      feels_like 10.5
      humidity 85
      description "light rain"
      wind_speed 5.5
      timestamp 1234567890
    }
  }
}

test GenerateWeatherInsightCold {
  functions [GenerateWeatherInsight]
  args {
    weather {
      city "Oslo"
      temperature -5.0
      feels_like -8.0
      humidity 70
      description "snow"
      wind_speed 8.0
      timestamp 1234567890
    }
  }
}
