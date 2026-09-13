from unittest.mock import MagicMock, patch

from chatbotcli.agents import Agent
from chatbotcli.core.providers import ProviderResponse


def _make_agent_with_fake_model(fake_model):
    with patch("chatbotcli.agents.agent1.Model", return_value=fake_model):
        return Agent()


def test_agent_init_sets_up_system_message_and_zero_cost():
    fake_model = MagicMock()
    agent = _make_agent_with_fake_model(fake_model)

    assert agent.total_cost == 0.0
    assert len(agent.messages) == 1
    assert agent.messages[0].role == "system"


def test_agent_chat_appends_messages_and_accumulates_cost():
    fake_model = MagicMock()
    fake_model.generate.return_value = (
        ProviderResponse(response="Hello!", input_token=5, output_token=3),
        0.002,
    )
    agent = _make_agent_with_fake_model(fake_model)

    reply = agent.chat("Hi there")

    assert reply == "Hello!"
    assert agent.total_cost == 0.002
    assert agent.messages[-2].role == "user"
    assert agent.messages[-2].content == "Hi there"
    assert agent.messages[-1].role == "assistant"
    assert agent.messages[-1].content == "Hello!"


def test_agent_chat_accumulates_cost_across_multiple_turns():
    fake_model = MagicMock()
    fake_model.generate.side_effect = [
        (ProviderResponse(response="First", input_token=1, output_token=1), 0.001),
        (ProviderResponse(response="Second", input_token=1, output_token=1), 0.004),
    ]
    agent = _make_agent_with_fake_model(fake_model)

    agent.chat("one")
    agent.chat("two")

    assert agent.total_cost == 0.005
