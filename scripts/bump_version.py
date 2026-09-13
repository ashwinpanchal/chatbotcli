#!/usr/bin/env python3
import sys
import tomllib
from pathlib import Path


def parse_version(version_str: str) -> tuple[int, int, int]:
    """Parse a semver version string into (major, minor, patch)."""
    try:
        parts = version_str.split(".")
        if len(parts) != 3:
            raise ValueError
        return tuple(int(p) for p in parts)
    except (ValueError, AttributeError):
        raise ValueError(f"Invalid version format: {version_str}. Expected MAJOR.MINOR.PATCH")


def compute_next_version(current_version: str, bump_type: str) -> str:
    """Compute the next version based on the bump type."""
    major, minor, patch = parse_version(current_version)

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}. Expected major, minor, or patch")

    return f"{major}.{minor}.{patch}"


def update_pyproject(pyproject_path: Path, new_version: str) -> None:
    """Update the version in pyproject.toml."""
    content = pyproject_path.read_text()
    # Find and replace the version line
    import re
    new_content = re.sub(
        r'version = "[^"]*"',
        f'version = "{new_version}"',
        content,
        count=1
    )
    if new_content == content:
        raise RuntimeError("Failed to update version in pyproject.toml")
    pyproject_path.write_text(new_content)


def update_init(init_path: Path, new_version: str) -> None:
    """Update __version__ in __init__.py."""
    content = init_path.read_text()
    import re
    new_content = re.sub(
        r'__version__ = "[^"]*"',
        f'__version__ = "{new_version}"',
        content,
        count=1
    )
    if new_content == content:
        raise RuntimeError("Failed to update __version__ in __init__.py")
    init_path.write_text(new_content)


def main():
    if len(sys.argv) != 2:
        print("Usage: bump_version.py <major|minor|patch>", file=sys.stderr)
        sys.exit(1)

    bump_type = sys.argv[1]

    root = Path(__file__).parent.parent
    pyproject_path = root / "pyproject.toml"
    init_path = root / "src" / "chatbotcli" / "__init__.py"

    # Read current version from pyproject.toml
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)
    current_version = pyproject["project"]["version"]

    # Compute next version
    try:
        next_version = compute_next_version(current_version, bump_type)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Update files
    try:
        update_pyproject(pyproject_path, next_version)
        update_init(init_path, next_version)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Print the new version to stdout (for workflow to capture)
    print(next_version)


if __name__ == "__main__":
    main()
