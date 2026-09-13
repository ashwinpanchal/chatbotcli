from unittest.mock import MagicMock, patch

import pytest

from chatbotcli.core.providers import BaseProvider, Message, OpenAIProvider, ProviderResponse, get_provider
from chatbotcli.core.providers.resgistry import PROVIDERS


def test_get_provider_returns_openai_provider():
    provider = get_provider("openai", "gpt-4o-mini")

    assert isinstance(provider, OpenAIProvider)
    assert provider.model == "gpt-4o-mini"


def test_get_provider_unknown_raises_value_error():
    with pytest.raises(ValueError, match="Unknown provider"):
        get_provider("does-not-exist", "some-model")


def test_registry_contains_openai():
    assert PROVIDERS["openai"] is OpenAIProvider


def test_calculate_cost_known_model():
    provider = get_provider("openai", "gpt-4o-mini")

    cost = provider.calculate_cost(1_000_000, 1_000_000)

    assert cost == pytest.approx(0.15 + 0.60)


def test_calculate_cost_unknown_model_defaults_zero():
    provider = get_provider("openai", "unknown-model")

    cost = provider.calculate_cost(1_000_000, 1_000_000)

    assert cost == 0.0


def test_base_provider_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseProvider("some-model")


def test_openai_provider_complete_returns_provider_response():
    fake_response = MagicMock()
    fake_response.choices[0].message.content = "Hello there!"
    fake_response.usage.prompt_tokens = 12
    fake_response.usage.completion_tokens = 5

    with patch("chatbotcli.core.providers.openai_provider.OpenAI") as mock_openai_cls:
        mock_client = mock_openai_cls.return_value
        mock_client.chat.completions.create.return_value = fake_response

        provider = OpenAIProvider("gpt-4o-mini")
        messages = [Message(role="user", content="Hi")]
        response = provider.complete(messages)

    assert isinstance(response, ProviderResponse)
    assert response.response == "Hello there!"
    assert response.input_token == 12
    assert response.output_token == 5

    mock_client.chat.completions.create.assert_called_once_with(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hi"}],
    )
