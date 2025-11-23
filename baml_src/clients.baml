// OpenAI o4-mini client configuration
client<llm> OpenAIO4Mini {
  provider openai
  options {
    model "o4-mini"
    api_key env.OPENAI_API_KEY
    temperature 0
    max_tokens 500
  }
}
