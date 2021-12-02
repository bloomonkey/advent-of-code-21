# -*- coding: utf-8 -*-
"""Document test_day_2 here.

Copyright (C) 2021, Auto Trader UK
Created 02. Dec 2021 10:54

"""
from typing import AsyncIterator

import pytest

from day_2 import Submarine


@pytest.fixture()
def instructions():
    data = [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2",
    ]

    async def _inner():
        for row in data:
            yield row

    return _inner()


@pytest.mark.asyncio
async def test_part_1(instructions: AsyncIterator[str]):
    sub = Submarine()

    async for instruction in instructions:
        sub.move(instruction)

    assert sub.horizontal == 15
    assert sub.vertical == 10