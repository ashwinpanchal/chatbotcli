# CLI Chatbot

A command-line chatbot application powered by OpenAI's API. Built with Python, Pydantic for configuration management, and UV for dependency management.

## Features

- Interactive CLI-based chat interface
- OpenAI API integration (supports configurable models)
- Environment-based configuration using Pydantic
- Custom error handling
- Easy to extend and customize

## Prerequisites

- Python 3.8+
- UV package manager
- OpenAI API key

## Setup

### 1. Clone or navigate to the project directory

```bash
cd chatBotCli
```

### 2. Install dependencies using UV

```bash
uv sync
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and update with your actual values:

```bash
cp .env.example .env
```

Then edit `.env` with your configuration:

```env
ENVIRONMENT=dev
OPEN_API_SECRET_KEY=sk-your-actual-api-key
OPEN_API_MODEL=gpt-4o-mini
```

**Environment Variables:**

- `ENVIRONMENT`: Application environment (`dev`, `prod`, etc.)
- `OPEN_API_SECRET_KEY`: Your OpenAI API key (required)
- `OPEN_API_MODEL`: OpenAI model to use (default: `gpt-4o-mini`)

## Running the Application

```bash
python -m chatbotcli.main
```

Start chatting! Type your messages and press Enter. Use `Ctrl+C` to exit.

```
You: Hello, how are you?
Assistant: I'm doing well, thank you for asking! How can I help you today?

You: 
```

## Project Structure

```
chatBotCli/
├── src/chatbotcli/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── core/
│   │   ├── __init__.py
│   │   └── llm.py           # LLM integration
│   ├── config/
│   │   ├── __init__.py
│   │   └── main.py          # Configuration management
│   └── error/
│       ├── __init__.py
│       └── main.py          # Custom error handling
├── .env                     # Environment variables (local)
├── .env.example             # Environment template
└── README.md
```

## Technologies Used

- **Python**: Core language
- **Pydantic**: Data validation and settings management
- **OpenAI API**: LLM integration
- **UV**: Dependency management

## Error Handling

The application includes custom error handling through the `CustomError` class. Errors are caught and displayed in a user-friendly format, ensuring graceful handling of API failures and configuration issues.

## Contributing

Feel free to extend the chatbot with additional features such as:
- Conversation history management
- Multiple LLM provider support
- Prompt templates
- Rate limiting
- Response caching

## License

This project is open source and available under the MIT License.
