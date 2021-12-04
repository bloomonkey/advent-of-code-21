# -*- coding: utf-8 -*-
from pathlib import Path


def get_input_path(filename: str) -> Path:
    return Path(__file__).parent.parent.parent / "data" / filename
