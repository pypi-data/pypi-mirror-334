# Suada Python SDK

The official Python SDK for Suada's Business Analyst API. This SDK allows you to easily integrate Suada's powerful business analysis capabilities into your applications and LangChain agents.

## Installation

```bash
pip install suada
```

## Usage

### Basic Usage

```python
from suada import Suada, SuadaConfig, ChatPayload

# Initialize the client
suada = Suada(
    config=SuadaConfig(
        api_key="your-api-key"
    )
)

# Send a chat message
response = suada.chat(
    payload=ChatPayload(
        message="What's our revenue trend?",
        external_user_identifier="user-123"  # Optional when passthrough_mode is False
    )
)

print(response)
```

### Integration with LangChain

```python
from suada import Suada, SuadaConfig
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# Initialize Suada
suada = Suada(
    config=SuadaConfig(
        api_key="your-api-key"
    )
)

# Create Suada tool
suada_tool = suada.create_tool(
    name="business_analyst",
    description="Use this tool to get business insights and analysis",
    external_user_identifier="user-123",  # Required when passthrough_mode is True
    passthrough_mode=True  # Optional, defaults to False
)

# Create OpenAI agent with Suada tool
model = ChatOpenAI(temperature=0)
tools = [suada_tool]

prompt = PromptTemplate.from_template(
    """You are a helpful assistant that uses Suada's business analyst capabilities.
    
    Current conversation:
    {chat_history}
    
    Human: {input}
    Assistant: Let me help you with that."""
)

agent = create_openai_functions_agent(
    llm=model,
    tools=tools,
    prompt=prompt
)

executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True
)

# Use the agent
result = executor.invoke({
    "input": "What's our revenue trend for the last quarter?",
    "chat_history": []
})

print(result["output"])
```

### Passthrough Mode and User Identification

The SDK supports two modes of operation:

1. **Standard Mode** (`passthrough_mode=False`, default): In this mode, Suada's AI analyzes the query and provides structured business insights. The `external_user_identifier` is optional.

2. **Passthrough Mode** (`passthrough_mode=True`): In this mode, messages are passed directly to the LLM. When using passthrough mode, `external_user_identifier` is required for proper user tracking.

```python
# Standard mode - external_user_identifier is optional
response_standard = suada.chat(
    payload=ChatPayload(
        message="What's our revenue trend?",
        passthrough_mode=False  # This is the default
    )
)

# Passthrough mode - external_user_identifier is required
response_passthrough = suada.chat(
    payload=ChatPayload(
        message="What's our revenue trend?",
        external_user_identifier="user-123",
        passthrough_mode=True
    )
)
```

## Response Format

The SDK formats responses from Suada's API into a structured string format that can be easily parsed by LangChain agents. The response includes the following sections:

- `<metrics>`: Key performance metrics
- `<insights>`: Business insights
- `<recommendations>`: Action recommendations
- `<risks>`: Potential risks
- `<reasoning>`: Analysis reasoning
- `<response>`: Main response text

Example response:
```
<metrics>
revenue: $1.2M
growth_rate: 15%
</metrics>

<insights>
Strong growth in enterprise segment
New product adoption exceeding expectations
</insights>

<recommendations>
Increase focus on enterprise sales
Expand product feature set
</recommendations>

<risks>
Market competition intensifying
Supply chain constraints
</risks>

<reasoning>
Analysis shows positive growth trajectory with some areas requiring attention
</reasoning>

<response>
Your revenue has shown strong growth, particularly in the enterprise segment...
</response>
```

## Configuration

The SDK accepts the following configuration options:

```python
from suada import SuadaConfig

config = SuadaConfig(
    api_key="your-api-key",
    base_url="https://suada.ai/api/public/"  # Optional, defaults to https://suada.ai/api/public/
)
```

## Type Safety

The SDK uses Pydantic models for type safety and validation:

```python
from suada import ChatPayload, ChatMessage

# All fields are properly typed and validated
payload = ChatPayload(
    message="What's our revenue?",
    external_user_identifier="user-123",  # Required only when passthrough_mode is True
    passthrough_mode=True,
    chat_history=[
        ChatMessage(
            role="user",
            content="Previous message"
        )
    ]
)
```

## Error Handling

The SDK throws descriptive exceptions when API calls fail:

```python
from suada import Suada, SuadaConfig, ChatPayload

suada = Suada(config=SuadaConfig(api_key="your-api-key"))

try:
    response = suada.chat(
        payload=ChatPayload(
            message="What's our revenue?",
            external_user_identifier="user-123"
        )
    )
except Exception as e:
    print(f"Error: {str(e)}")
```

## Development

To set up the development environment:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run type checking
mypy suada

# Run code formatting
black suada
isort suada
```

## License

MIT 