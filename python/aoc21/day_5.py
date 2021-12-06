# -*- coding: utf-8 -*-
"""Document day_5 here.

Created 06. Dec 2021 13:11

"""
import asyncio
from collections import namedtuple
from itertools import chain, filterfalse
from typing import AsyncIterable, List

import aiofiles
import typer

from aoc21 import get_input_path

Point = namedtuple("Point", ["x", "y"])
Line = namedtuple("Line", ["start", "end"])


class Grid(list):
    def __repr__(self):
        return "\n".join([repr(row) for row in self])


class HydrothermalMap:
    def __init__(self, lines: List[Line]):
        self.lines = lines

    @classmethod
    async def parse(cls, lines: AsyncIterable[str]):
        lines_ = []
        async for line in lines:
            start, end = [
                cls._parse_point(p) for p in line.strip().split(" -> ", 1)
            ]
            lines_.append(Line(start, end))

        return HydrothermalMap(lines_)

    async def count_danger_spots(self) -> int:
        grid = await self.plot_grid()
        return len(
            list(filterfalse(lambda x: x < 2, chain.from_iterable(grid)))
        )

    async def plot_grid(self) -> Grid:
        grid = await self._blank_grid()
        for line in self.lines:
            if line.start.x == line.end.x:
                # Horizontal
                grid = await self._plot_horizontal(line, grid)
            elif line.start.y == line.end.y:
                # Vertical
                grid = await self._plot_vertical(line, grid)
            else:
                # Diagonal
                grid = await self._plot_diagonal(line, grid)

        return grid

    async def plot_map(self) -> str:
        grid = await self.plot_grid()
        return "\n".join(["".join(map(str, row)) for row in grid]).replace(
            "0", "."
        )

    async def _blank_grid(self) -> Grid:
        n_x = (
            max(
                [line.start.x for line in self.lines]
                + [line.end.x for line in self.lines]
            )
            + 1
        )
        n_y = (
            max(
                [line.start.y for line in self.lines]
                + [line.end.y for line in self.lines]
            )
            + 1
        )
        rows = [[0] * n_x for _ in range(n_y)]
        return Grid(rows)

    @classmethod
    def _parse_point(cls, p: str):
        x, y = [int(coord) for coord in p.split(",", 1)]
        return Point(x, y)

    async def _plot_horizontal(self, line: Line, grid: Grid) -> Grid:
        start, end = sorted(line)
        for y in range(start.y, end.y + 1):
            # Horizontal line will not enter this loop, can used fixed y
            grid[y][start.x] += 1

        return grid

    async def _plot_vertical(self, line, grid: Grid) -> Grid:
        start, end = sorted(line)
        for x in range(start.x, end.x + 1):
            # Horizontal line will not enter this loop, can used fixed y
            grid[start.y][x] += 1

        return grid

    async def _plot_diagonal(self, line, grid: Grid) -> Grid:
        n_x = abs(line.end.x - line.start.x)
        n_y = abs(line.end.y - line.start.y)
        n = max(n_x, n_y)
        x_increment = 1 if line.start.x < line.end.x else -1
        y_increment = 1 if line.start.y < line.end.y else -1
        for i in range(n + 1):
            grid[line.start.y + (i * y_increment)][
                line.start.x + (i * x_increment)
            ] += 1

        return grid


async def _main():
    async with aiofiles.open(get_input_path("input-5.txt"), mode="r") as f:
        map = await HydrothermalMap.parse(f)

    n_danger_spots = await map.count_danger_spots()
    print(f"Danger spots: {n_danger_spots}")


def main():
    asyncio.run(_main())


if __name__ == "__main__":
    typer.run(main)
