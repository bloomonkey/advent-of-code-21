# -*- coding: utf-8 -*-
"""Day 1."""
import asyncio
from collections import deque
from pathlib import Path
from typing import AsyncIterable, Optional

import aiofiles
import typer


async def count_increasing_depths(depths: AsyncIterable[int]) -> int:
    """Calculate and return number of depths that increase."""
    increasing_count = 0
    previous_depth = None
    async for d in depths:
        if previous_depth and previous_depth < d:
            increasing_count += 1
        previous_depth = d

    return increasing_count


async def sum_window_depths(
    depths: AsyncIterable[int], window_size: int
) -> int:
    window = deque([], maxlen=window_size)
    for x in range(window_size - 1):
        window.append(await depths.__anext__())
    async for d in depths:
        window.append(d)
        yield sum(window)


async def _main(window_size: int) -> None:

    async with aiofiles.open(
        Path(__file__).parent / ".." / ".." / "data" / "input-1.txt"
    ) as f:
        depths = (int(line) async for line in f)
        sum_depths = sum_window_depths(depths, window_size)
        print(await count_increasing_depths(sum_depths))


def main(window_size: Optional[int] = typer.Option(1)):
    asyncio.run(_main(window_size))


if __name__ == "__main__":
    typer.run(main)
