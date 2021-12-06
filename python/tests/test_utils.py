# -*- coding: utf-8 -*-
"""Document test_utils here.

Copyright (C) 2021, Auto Trader UK
Created 06. Dec 2021 13:05

"""
from typing import AsyncIterable


def async_iter_lines(data: str) -> AsyncIterable[str]:
    async def _inner():
        for row in data.split("\n"):
            yield row

    return _inner()