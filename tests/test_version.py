import tomllib
from pathlib import Path
import chatbotcli


def test_version_consistency():
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    pyproject_version = pyproject["project"]["version"]
    package_version = chatbotcli.__version__

    assert pyproject_version == package_version, (
        f"Version mismatch: pyproject.toml has {pyproject_version}, "
        f"but __version__ in __init__.py is {package_version}"
    )
