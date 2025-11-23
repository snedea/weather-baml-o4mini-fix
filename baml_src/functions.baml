// Generate weather insight from weather data
function GenerateWeatherInsight(weather: WeatherData) -> WeatherInsight {
  client OpenAIO4Mini
  prompt #"
    You are a helpful weather assistant. Analyze this weather data and provide insights:

    City: {{weather.city}}
    Temperature: {{weather.temperature}}°C (feels like {{weather.feels_like}}°C)
    Humidity: {{weather.humidity}}%
    Conditions: {{weather.description}}
    Wind Speed: {{weather.wind_speed}} m/s

    Provide:
    1. A brief summary (1-2 sentences) about the current weather
    2. Practical recommendations (what to wear, activities to consider)
    3. Comfort level assessment (choose one: "comfortable", "moderate", or "uncomfortable")
    4. Whether to bring an umbrella (true/false)

    Respond in JSON format matching the WeatherInsight structure.
  "#
}
