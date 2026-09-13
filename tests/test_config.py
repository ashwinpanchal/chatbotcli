from chatbotcli.config import settings


def test_settings_load():
    assert settings.ENVIRONMENT == "test"
    assert settings.OPEN_API_MODEL == "gpt-4o-mini"
    assert settings.OPEN_API_SECRET_KEY.get_secret_value() == "sk-test-key-12345"
