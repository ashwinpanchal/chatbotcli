# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-09-13

### Added
- Initial release of CLI Chatbot
- Interactive command-line chat interface
- OpenAI API integration with support for configurable models
- Environment-based configuration using Pydantic
- Custom error handling with `CustomError` class
- Support for multiple OpenAI models (default: `gpt-4o-mini`)
- Environment variable management with `.env` support
- Graceful keyboard interrupt handling (Ctrl+C to exit)

### Features
- Real-time chat interaction in terminal
- Configurable OpenAI API settings
- Development and production environment support
- Error logging and custom error messages
- Secure API key handling using Pydantic's `SecretStr`

### Documentation
- Comprehensive README with setup instructions
- `.env.example` template for environment configuration
- Project structure documentation

## [Unreleased]

### Planned for Future Releases
- Conversation history management
- Multiple LLM provider support
- Prompt templates and customization
- Rate limiting and usage tracking
- Response caching
- Configuration file support
- Chat export functionality
