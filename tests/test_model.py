from unittest.mock import MagicMock, patch

from chatbotcli.core import Model
from chatbotcli.core.providers import Message, ProviderResponse


def test_model_init_creates_provider_via_registry():
    with patch("chatbotcli.core.model.get_provider") as mock_get_provider:
        Model(provider_name="openai", model_name="gpt-4o-mini")

    mock_get_provider.assert_called_once_with("openai", "gpt-4o-mini")


def test_model_generate_returns_response_and_turn_cost():
    fake_provider = MagicMock()
    fake_provider.complete.return_value = ProviderResponse(
        response="Hi!", input_token=10, output_token=4
    )
    fake_provider.calculate_cost.return_value = 0.001

    with patch("chatbotcli.core.model.get_provider", return_value=fake_provider):
        model = Model(provider_name="openai", model_name="gpt-4o-mini")
        messages = [Message(role="user", content="Hello")]
        response, turn_cost = model.generate(messages)

    fake_provider.complete.assert_called_once_with(messages)
    fake_provider.calculate_cost.assert_called_once_with(10, 4)
    assert response.response == "Hi!"
    assert turn_cost == 0.001
