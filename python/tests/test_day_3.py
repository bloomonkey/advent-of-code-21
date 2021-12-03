# -*- coding: utf-8 -*-
"""Document test_day_3 here.

Created 03. Dec 2021 09:04

"""

import pytest

from aoc21.day_3 import Diagnostics


@pytest.fixture()
def readings():
    data = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".split()

    async def _inner():
        for row in data:
            yield row

    return _inner()


@pytest.mark.asyncio
async def test_power_consumption(readings):
    diagnostics = Diagnostics()
    async for reading in readings:
        await diagnostics.update(reading)

    assert diagnostics.power_consumption == 198


@pytest.mark.asyncio
async def test_power_output_update_deals_with_longer_input(readings):
    diagnostics = Diagnostics()
    await diagnostics.update("01" * 10)
    assert isinstance(diagnostics.power_consumption, int)


@pytest.mark.asyncio
async def test_oxygen_generator_rating(readings):
    diagnostics = Diagnostics()
    async for reading in readings:
        await diagnostics.update(reading)

    assert diagnostics.oxygen_generator_rating == 23


@pytest.mark.asyncio
async def test_c02_scrubber_rating(readings):
    diagnostics = Diagnostics()
    async for reading in readings:
        await diagnostics.update(reading)

    assert diagnostics.co2_scrubber_rating == 10

async def test_life_support_rating(readings):
    diagnostics = Diagnostics()
    async for reading in readings:
        await diagnostics.update(reading)

    assert diagnostics.life_support_rating == 230
