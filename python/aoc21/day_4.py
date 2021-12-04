# -*- coding: utf-8 -*-
"""Document day_4 here.

Created 04. Dec 2021 14:13

"""
import asyncio
from pathlib import Path
from typing import AsyncIterable, List, Optional

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

        @property
        def is_complete(self) -> bool:
            return self.WIN in self.rows or self.WIN in self.columns

        def play(self, call) -> bool:
            for row in self.rows:
                try:
                    row[row.index(call)] = None
                except ValueError:
                    # Not in row
                    pass

            if self.is_complete:
                self._score = int(call) * self._calculate_board_score()
                return True
            return False

        def _calculate_board_score(self):
            return sum(
                [
                    sum([int(cell) for cell in row if cell is not None])
                    for row in self.rows
                ]
            )

    def __init__(self, boards: List[Board], calls: List[str]):
        self.boards = boards
        self.calls = calls

    @classmethod
    async def parse(cls, lines: AsyncIterable[str]):
        calls_line = await lines.__anext__()
        calls = calls_line.strip().split(",")
        rows = [line.strip().split() async for line in lines if line.strip()]
        boards = []
        while len(rows):
            b = []
            for _ in range(5):
                b.append(rows.pop(0))
            boards.append(cls.Board(b))
        return Bingo(boards, calls)

    async def play(self) -> List[Board]:
        boards = self.boards.copy()
        results = []
        for call in self.calls:
            completed = await self._play_round(boards, call)
            results.extend(completed)
            for board in completed:
                boards.remove(board)

            asyncio.sleep(0)
            if not boards:
                break
        else:
            raise NoWinner()

        return results

    async def _play_round(self, boards, call):
        completed = []
        for board in boards:
            if board.play(call):
                completed.append(board)
        return completed


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
