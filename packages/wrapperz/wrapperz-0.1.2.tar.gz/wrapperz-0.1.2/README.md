# Wrapperz (WIP - agent generated)

Simple wrappers for various AI APIs including LLMs, ASR, and TTS.

## Installation

```bash
pip install wrapperz
uv add wrapperz
```

## Features

- **LLM API Wrappers**: Unified interface for OpenAI, Anthropic, Google, and other LLM providers
- **ASR (Automatic Speech Recognition)**: Convert speech to text
- **TTS (Text-to-Speech)**: Convert text to speech
- **Async Support**: Asynchronous API calls for improved performance

## Quick Start

```python
import os
from wrapperz import call_ai, MessageBuilder

os.environ["OPENAI_API_KEY"] = "your_openai_key" # or load from .env using dotenv etc...
messages = MessageBuilder().add_system("You are a helpful assistant.").add_user("What's 1+1?")

# Call an LLM with a simple interface
response = call_ai(
    model="openai/gpt-4o",
    messages=messages
)

print(response)
```

## Environment Variables

Set up your API keys in environment variables to enable providers.

```bash
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
