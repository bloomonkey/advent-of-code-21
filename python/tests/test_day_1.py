# -*- coding: utf-8 -*-
"""Document test_day_1 here.

Created 02. Dec 2021 09:10

"""
from pathlib import Path

import aiofiles
import pytest

from aoc21.day_1 import count_increasing_depths, sum_window_depths


@pytest.mark.asyncio
async def test_part_1():
    async with aiofiles.open(
        Path(__file__).parent / ".." / ".." / "data" / "test-1.txt"
    ) as f:
        window_size = 1
        depths = (int(line) async for line in f)
        sum_depths = sum_window_depths(depths, window_size)
        assert await count_increasing_depths(sum_depths) == 7


@pytest.mark.asyncio
async def test_part_2():
    async with aiofiles.open(
        Path(__file__).parent / ".." / ".." / "data" / "test-1.txt"
    ) as f:
        window_size = 3
        depths = (int(line) async for line in f)
        sum_depths = sum_window_depths(depths, window_size)
        assert await count_increasing_depths(sum_depths) == 5
