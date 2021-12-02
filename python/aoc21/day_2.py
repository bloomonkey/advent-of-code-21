# -*- coding: utf-8 -*-
"""Document day_2 here.

Created 02. Dec 2021 11:30

"""
import asyncio
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

import aiofiles
import typer as typer


class Direction(Enum):
    up = auto()
    down = auto()
    forward = auto()


@dataclass
class Movement:
    direction: Direction
    distance: int


class Submarine:
    def __init__(self, horizontal: int = 0, depth: int = 0, aim: int = 0):
        self.horizontal = horizontal
        self.depth = depth
        self.aim = aim

    def move(self, instruction: str):
        movement = self._parse(instruction)
        if movement.direction is Direction.up:
            self._tilt(0 - movement.distance)
        if movement.direction is Direction.down:
            self._tilt(movement.distance)
        if movement.direction is Direction.forward:
            self._advance(movement.distance)

    @staticmethod
    def _parse(instruction: str) -> Movement:
        bits = str.split(instruction)
        direction = Direction[bits[0]]
        distance = int(bits[1])
        return Movement(direction, distance)

    def _advance(self, distance: int):
        self.horizontal += distance
        self.depth += self.aim * distance

    def _tilt(self, distance):
        self.aim += distance


async def _main():
    sub = Submarine()
    async with aiofiles.open(Path(__file__).parent.parent.parent / "data" / "input-2.txt", mode="r") as f:
        async for instruction in f:
            sub.move(instruction)

    print(f"Sub position: horizontal: {sub.horizontal}, depth: {sub.depth}")
    print(f"AOC answer: {sub.horizontal * sub.depth}")


def main():
    asyncio.run(_main())


if __name__ == '__main__':
    typer.run(main)
