from importlib import metadata
from pathlib import Path

import yaml


def test_version():
    assert metadata.version("reno-structured-output")
