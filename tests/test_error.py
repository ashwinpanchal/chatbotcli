from chatbotcli.error import CustomError
from pathlib import Path


def test_custom_error_format():
    try:
        raise ValueError("test error")
    except ValueError as e:
        # Use a file path that's guaranteed to be in the src directory
        test_file = Path(__file__).parent.parent / "src" / "chatbotcli" / "config" / "main.py"
        error = CustomError(str(test_file), e)
        error_str = str(error)

    assert "ERROR" in error_str
    assert "ValueError" in error_str
    assert "config/main.py" in error_str or "main.py" in error_str
