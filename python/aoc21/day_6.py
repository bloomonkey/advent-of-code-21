# -*- coding: utf-8 -*-
"""Document day_6 here.

Created 06. Dec 2021 19:34

"""
import asyncio
from typing import AsyncGenerator, List

import aiofiles
import typer
from aoc21 import get_input_path


class LanternfishSimulator:

    def __init__(self, population: List[int]):
        self.population = population

    @classmethod
    async def parse(cls, pop: str) -> "LanternfishSimulator":
        return LanternfishSimulator(list(map(int, pop.strip().split(","))))

    @property
    def population_count(self):
        return len(self.population)

    async def run_days(self, n: int) -> AsyncGenerator[List[int], None]:
        for n in range(n):
            await self._run_day()
            yield self.population
            await asyncio.sleep(0)

    async def _run_day(self):
        newborns = [8] * self.population.count(0)
        for i, fish in enumerate(self.population):
            if fish == 0:
                self.population[i] = 6
            else:
                self.population[i] -= 1

        self.population.extend(newborns)


async def _main(days: int):
    async with aiofiles.open(get_input_path("input-6.txt"), mode="r") as f:
        sim = await LanternfishSimulator.parse(await f.read())

    async for _ in sim.run_days(days):
        pass

    print(f"Lanternfish population: {sim.population_count}")


def main(days: int):
    asyncio.run(_main(days))


if __name__ == "__main__":
    typer.run(main)
