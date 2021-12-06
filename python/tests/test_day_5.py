# -*- coding: utf-8 -*-
"""Document test_day_5 here.

Created 06. Dec 2021 13:01

"""
from typing import AsyncIterable

import pytest

from aoc21.day_5 import HydrothermalMap
from .test_utils import async_iter_lines


@pytest.fixture()
def lines() -> AsyncIterable[str]:
    data = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
    return async_iter_lines(data)


@pytest.mark.asyncio
async def test_parse_map(lines):
    map = await HydrothermalMap.parse(lines)

    start, end = map.lines[-1]
    assert start.x == 5
    assert start.y == 5
    assert end.x == 8
    assert end.y == 2


@pytest.mark.asyncio
async def test_plot_map(lines):
    map = await HydrothermalMap.parse(lines)

    expected_map = """\
1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111...."""

    assert await map.plot_map() == expected_map


@pytest.mark.asyncio
async def test_count_danger_spots(lines):
    map = await HydrothermalMap.parse(lines)
    assert await map.count_danger_spots() == 12
