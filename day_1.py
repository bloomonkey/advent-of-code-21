# -*- coding: utf-8 -*-
"""Day 1."""
import asyncio
from collections import deque
from typing import AsyncIterable

import aiofiles


async def count_increasing_depths(depths: AsyncIterable[int]) -> int:
    """Calculate and return number of depths that increase."""
    increasing_count = 0
    previous_depth = None
    async for d in depths:
        if previous_depth and previous_depth < d:
            increasing_count += 1
        previous_depth = d

    return increasing_count


async def sum_window_depths(depths: AsyncIterable[int], window_size: int) -> int:
    window = deque([], maxlen=window_size)
    for x in range(window_size - 1):
        window.append(await depths.__anext__())
    async for d in depths:
        window.append(d)
        yield sum(window)


async def main() -> None:
    window_size = 3

    # Test
    async with aiofiles.open('data/test-1.txt') as f:
        depths = (int(line) async for line in f)
        sum_depths = sum_window_depths(depths, window_size)
        assert await count_increasing_depths(sum_depths) == 5

    async with aiofiles.open('data/input-1.txt') as f:
        depths = (int(line) async for line in f)
        sum_depths = sum_window_depths(depths, window_size)
        print(await count_increasing_depths(sum_depths))


if __name__ == "__main__":
    asyncio.run(main())
