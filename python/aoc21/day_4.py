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


class Board:
    WIN = [None] * 5

    def __init__(self, rows: List[List[str]]):
        self.rows = rows
        self._score = None

    @property
    def columns(self) -> List[List[str]]:
        return [list(r) for r in zip(*self.rows)]

    @property
    def score(self) -> int:
        return self._score

    @property
    def is_complete(self) -> bool:
        return self.WIN in self.rows or self.WIN in self.columns

    def play(self, call):
        """Play the round."""
        for row in self.rows:
            try:
                row[row.index(call)] = None
            except ValueError:
                pass  # Not in row

        if self.is_complete:
            self._score = int(call) * self._calculate_board_score()

    def _calculate_board_score(self):
        return sum(
            [
                sum([int(cell) for cell in row if cell is not None])
                for row in self.rows
            ]
        )


class Bingo:
    def __init__(self, boards: List[Board], calls: List[str]):
        self.boards = boards
        self.calls = calls

    @classmethod
    async def parse(cls, lines: AsyncIterable[str]) -> "Bingo":
        calls_line = await lines.__anext__()
        calls = calls_line.strip().split(",")
        rows = [line.strip().split() async for line in lines if line.strip()]
        boards = []
        while len(rows):
            b = []
            for _ in range(5):
                b.append(rows.pop(0))
            boards.append(Board(b))
        return Bingo(boards, calls)

    async def play(self) -> List[Board]:
        """Play the game, return boards in order of finish."""
        results = []
        for call in self.calls:
            incomplete_boards = [b for b in self.boards if not b.is_complete]
            if not incomplete_boards:
                break

            results.extend(await self._play_round(incomplete_boards, call))
            asyncio.sleep(0)
        else:
            raise NoWinner()

        return results

    async def _play_round(self, boards, call):
        """Play a single round"""
        for board in boards:
            board.play(call)

        return [board for board in boards if board.is_complete]


async def _main():
    input_path = Path(__file__).parent.parent.parent / "data" / "input-4.txt"
    async with aiofiles.open(input_path, mode="r") as f:
        bingo = await Bingo.parse(f)

    results = await bingo.play()
    print(f"Winning score: {results[0].score}")
    print(f"Last place score: {results[-1].score}")


def main():
    asyncio.run(_main())


if __name__ == "__main__":
    typer.run(main)
