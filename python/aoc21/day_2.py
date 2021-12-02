# -*- coding: utf-8 -*-
"""Document day_2 here.

Copyright (C) 2021, Auto Trader UK
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
    def __init__(self, start_horizontal: int = 0, start_vertical: int = 0):
        self.horizontal = start_horizontal
        self.vertical = start_vertical

    def move(self, instruction: str):
        movement = self._parse(instruction)
        self._move(movement)

    @staticmethod
    def _parse(instruction: str) -> Movement:
        bits = str.split(instruction)
        direction = Direction[bits[0]]
        distance = int(bits[1])
        return Movement(direction, distance)

    def _move(self, movement: Movement):
        if movement.direction is Direction.up:
            self.vertical -= movement.distance
        if movement.direction is Direction.down:
            self.vertical += movement.distance
        if movement.direction is Direction.forward:
            self.horizontal += movement.distance


async def _main():
    sub = Submarine()
    async with aiofiles.open(Path(__file__).parent.parent.parent / "data" / "input-2.txt", mode="r") as f:
        async for instruction in f:
            sub.move(instruction)

    print(f"Sub position: horizontal: {sub.horizontal}, depth: {sub.vertical}")

def main():
    asyncio.run(_main())


if __name__ == '__main__':
    typer.run(main)
