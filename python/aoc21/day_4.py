# -*- coding: utf-8 -*-
"""Document day_4 here.

Created 04. Dec 2021 14:13

"""
import asyncio
from pathlib import Path
from typing import AsyncIterable, List

import aiofiles
import typer


class NoWinner(Exception):
    pass


class Bingo:
    class Board:

        WIN = [None] * 5

        def __init__(self, rows: List[str]):
            self.rows = rows
            self._score = None

        @property
        def columns(self):
            return [list(r) for r in zip(*self.rows)]

        @property
        def score(self) -> int:
            return self._score

        def play(self, call) -> bool:
            for row in self.rows:
                try:
                    row[row.index(call)] = None
                except ValueError:
                    # Not in row
                    pass

            if self.WIN in self.rows or self.WIN in self.columns:
                self._assign_score(call)
                return True
            return False

        def _assign_score(self, call: str):
            self._score = int(call) * sum(
                [
                    sum([int(cell) for cell in row if cell is not None])
                    for row in self.rows
                ]
            )

    def __init__(self, boards: List[Board], calls: List[str]):
        self.boards = boards
        self.calls = calls

    async def play(self) -> Board:
        winner = None
        for call in self.calls:
            for board in self.boards:
                if board.play(call) and not winner:
                    winner = board
            asyncio.sleep(0)
            if winner:
                break
        else:
            raise NoWinner()

        return winner

    @classmethod
    async def parse(cls, lines: AsyncIterable[str]):
        calls_line = await lines.__anext__()
        calls = calls_line.strip().split(",")
        # await lines.__anext__()  # blank line
        rows = [line.strip().split() async for line in lines if line]
        boards = []
        while len(rows):
            b = []
            for _ in range(5):
                b.append(rows.pop(0))
            boards.append(cls.Board(b))
        return Bingo(boards, calls)


async def _main():
    input_path = Path(__file__).parent.parent.parent / "data" / "input-4.txt"
    async with aiofiles.open(input_path, mode="r") as f:
        bingo = await Bingo.parse(f)

    winner = await bingo.play()
    print(f"Winning score: {winner.score}")


def main():
    asyncio.run(_main())


if __name__ == "__main__":
    typer.run(main)
