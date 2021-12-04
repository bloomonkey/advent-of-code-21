# -*- coding: utf-8 -*-
"""Document test_day_4 here.

Copyright (C) 2021, Auto Trader UK

"""
import pytest

from day_4 import Bingo, Board


@pytest.fixture()
def lines():
    data = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

    async def _inner():
        for row in data.split("\n"):
            yield row

    return _inner()


@pytest.mark.asyncio
async def test_parse_call_and_boards(lines):
    bingo = await Bingo.parse(lines)

    assert isinstance(bingo.calls, list)

    assert len(bingo.boards) == 3
    assert len(bingo.boards[0].rows) == 5
    assert len(bingo.boards[0].columns) == 5


@pytest.mark.asyncio
async def test_columns():
    bingo = Bingo(
        [
            Board(
                [["1"] * 5, ["2"] * 5, ["3"] * 5, ["4"] * 5, ["5"] * 5]
            )
        ],
        ["1"],
    )

    assert bingo.boards[0].columns[0] == ["1", "2", "3", "4", "5"]


@pytest.mark.asyncio
async def test_parse_call_and_boards(lines):
    bingo = await Bingo.parse(lines)

    results = await bingo.play()
    assert results[0].score == 4512


@pytest.mark.asyncio
async def test_parse_call_and_boards(lines):
    bingo = await Bingo.parse(lines)

    results = await bingo.play()
    assert results[-1].score == 1924
