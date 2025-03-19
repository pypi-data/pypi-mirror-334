import tomli  # TOML parser for Python <3.11
from pathlib import Path

from funcshauns.utils import get_repo_root


# Dynamically extract version from pyproject.toml
def get_version():
    """
    Reads the version of the package from pyproject.toml.

    Returns:
        str: The version specified in the pyproject.toml file.
    """
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        pyproject_data = tomli.load(f)
    return pyproject_data["tool"]["poetry"]["version"]


__version__ = get_version()

# Exports
__all__ = ["get_repo_root"]
