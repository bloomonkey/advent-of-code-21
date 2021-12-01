# -*- coding: utf-8 -*-
"""Day 1."""
import asyncio
from typing import AsyncIterable

import aiofiles


async def increasing_depths(depths: AsyncIterable[int]) -> int:
    """Calculate and return number of depths that increase."""
    increasing_count = 0
    previous_depth = None
    async for d in depths:
        if previous_depth and previous_depth < d:
            increasing_count += 1
        previous_depth = d

    return increasing_count


async def main() -> None:
    async with aiofiles.open('data/test-1.txt') as f:
        depths = (int(line) async for line in f)
        assert await increasing_depths(depths) == 7

    async with aiofiles.open('data/input-1.txt') as f:
        depths = (int(line) async for line in f)
        print(await increasing_depths(depths))


if __name__ == "__main__":
    asyncio.run(main())
