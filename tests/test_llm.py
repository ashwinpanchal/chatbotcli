from chatbotcli.core import LLM


def test_llm_init():
    llm = LLM()
    assert llm.model == "gpt-4o-mini"
    assert llm.messages is not None
    assert len(llm.messages) > 0
    assert llm.total_cost == 0.0
