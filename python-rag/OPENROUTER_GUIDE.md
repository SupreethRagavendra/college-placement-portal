# OpenRouter API Usage Guide

This guide provides detailed information about using the OpenRouter API in the College Placement Portal RAG system.

## Overview

OpenRouter is a unified interface for Large Language Models (LLMs) that provides access to multiple AI models through a single API. Our system uses OpenRouter to power the chatbot functionality with automatic fallback between models.

## Models Used

### Primary Model
- **Model**: `qwen/qwen-2.5-72b-instruct:free`
- **Provider**: Qwen (Alibaba)
- **Capabilities**: Advanced reasoning, complex queries, detailed explanations
- **Use Case**: Primary choice for all student queries

### Fallback Model
- **Model**: `deepseek/deepseek-v3.1:free`
- **Provider**: DeepSeek
- **Capabilities**: Reliable general-purpose responses
- **Use Case**: Fallback when primary model fails or is unavailable

## API Configuration

### Environment Variables

The following environment variables control OpenRouter API behavior:

```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_API_URL=https://openrouter.ai/api/v1/chat/completions
OPENROUTER_PRIMARY_MODEL=qwen/qwen-2.5-72b-instruct:free
OPENROUTER_FALLBACK_MODEL=deepseek/deepseek-v3.1:free
```

### API Client Configuration

The OpenRouter client is configured in `openrouter_client.py` with the following parameters:

- **API Key**: Authentication token for OpenRouter
- **Primary Model**: Main model for processing queries
- **Fallback Model**: Backup model for reliability
- **API URL**: Endpoint for OpenRouter API

## API Usage Patterns

### Basic Chat Request

```python
from openrouter_client import OpenRouterClient

client = OpenRouterClient(
    api_key="your_key",
    primary_model="qwen/qwen-2.5-72b-instruct:free",
    fallback_model="deepseek/deepseek-v3.1:free"
)

messages = [
    {"role": "user", "content": "What assessments are available?"}
]

response = client.call_with_fallback(messages)
```

### Direct Model Calls

```python
# Call primary model directly
response = client.call_api(messages, model=client.primary_model)

# Call fallback model directly
response = client.call_api(messages, model=client.fallback_model)
```

## Best Practices

### Prompt Engineering

1. **Context Provision**: Always provide relevant context in the system prompt
2. **Clear Instructions**: Be explicit about desired response format
3. **Role Definition**: Clearly define the AI's role and purpose
4. **Constraint Setting**: Specify limitations and boundaries

### Error Handling

1. **Timeout Management**: Set appropriate timeouts (default: 30 seconds)
2. **Fallback Mechanism**: Always use `call_with_fallback` for reliability
3. **Error Logging**: Log all API errors for debugging
4. **Graceful Degradation**: Provide meaningful fallback responses

### Rate Limiting

1. **Request Spacing**: Avoid burst requests
2. **Retry Logic**: Implement exponential backoff for rate limits
3. **Monitoring**: Track API usage and performance

## Headers and Metadata

### Required Headers

The API client automatically includes these headers:

- `Authorization: Bearer {api_key}`
- `Content-Type: application/json`
- `HTTP-Referer: http://localhost:8000`
- `X-Title: College Placement Portal`

### Response Metadata

Responses include metadata for monitoring:

```json
{
  "model_used": "qwen/qwen-2.5-72b-instruct:free",
  "response_time": "1.25s",
  "tokens_used": 150
}
```

## Model Selection Strategy

### When to Use Primary Model

- Complex reasoning tasks
- Detailed explanations required
- When maximum accuracy is needed
- For student-specific data analysis

### When to Use Fallback Model

- Primary model timeout or failure
- High traffic situations
- When primary model is rate-limited
- For simple, straightforward queries

### Automatic Fallback

The system automatically falls back when:
- Primary model returns an error
- API call times out
- Rate limit is exceeded
- Model is unavailable

## Cost Management

### Free Tier Usage

Both models used are free-tier:
- `qwen/qwen-2.5-72b-instruct:free`
- `deepseek/deepseek-v3.1:free`

### Usage Tracking

Even though models are free, the system tracks:
- Number of API calls
- Tokens consumed
- Response times
- Model performance metrics

## Response Formatting

### Expected Response Structure

```json
{
  "id": "response_id",
  "choices": [
    {
      "message": {
        "content": "Response content here",
        "role": "assistant"
      }
    }
  ],
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 100,
    "total_tokens": 150
  }
}
```

### Error Response Structure

```json
{
  "error": {
    "message": "Error description",
    "code": 429
  }
}
```

## Troubleshooting Common Issues

### Timeout Errors

- Increase timeout value in API calls
- Check network connectivity
- Verify OpenRouter service status

### Authentication Errors

- Verify API key is correct
- Check API key permissions
- Ensure key is not expired

### Rate Limit Errors

- Implement retry with exponential backoff
- Reduce request frequency
- Monitor usage quotas

### Model Unavailable

- System automatically falls back to alternative model
- Log the error for investigation
- Check OpenRouter status page

## Performance Optimization

### Caching Strategies

- Cache frequently asked questions
- Store successful responses temporarily
- Implement cache invalidation for updated data

### Connection Management

- Reuse HTTP connections
- Implement connection pooling
- Set appropriate timeout values

### Batch Processing

- Group related requests when possible
- Minimize API round trips
- Optimize data retrieval patterns

## Security Considerations

### API Key Security

- Store keys in environment variables
- Never commit keys to version control
- Rotate keys periodically
- Restrict key permissions

### Data Privacy

- Only send necessary data to API
- Avoid sending sensitive student information
- Comply with data protection regulations
- Implement data minimization principles

## Monitoring and Logging

### Key Metrics to Track

- API response times
- Success/failure rates
- Model performance comparison
- Token usage statistics

### Logging Best Practices

- Log all API requests and responses
- Include timing information
- Record error details
- Monitor for unusual patterns

## Integration Testing

### Test Scenarios

1. **Normal Operation**: Primary model responds successfully
2. **Fallback Trigger**: Primary model fails, fallback works
3. **Rate Limiting**: Handle rate limit responses
4. **Timeout Handling**: Manage timeout scenarios
5. **Error Recovery**: Recover from various error conditions

### Test Data

Use representative student queries:
- Assessment inquiries
- Result requests
- Help and navigation questions
- Technical support requests

## Future Considerations

### Model Updates

- Monitor for new model releases
- Test new models before deployment
- Plan for model deprecations
- Evaluate performance improvements

### Feature Enhancements

- Advanced prompt engineering techniques
- Conversation history management
- Multi-turn dialogue optimization
- Personalization improvements