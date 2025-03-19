"""
.. include:: ../README.md
"""

__docformat__ = "restructuredtext"
from efinance.api import bond, fund, futures, stock

from efinance import utils

import tomli
from pathlib import Path


def get_version():
    pyproject_path = Path(__file__).parent / "data" / "pyproject.toml"
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomli.load(f)
    return pyproject_data["project"]["version"]


__version__ = get_version()

__all__ = ["stock", "fund", "bond", "futures", "utils"]
