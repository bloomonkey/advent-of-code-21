# -*- coding: utf-8 -*-
"""Document day_6 here.

Created 06. Dec 2021 19:34

"""
import asyncio
from collections import Counter
from typing import AsyncGenerator, Counter as CounterType

import aiofiles
import typer
from aoc21 import get_input_path


class LanternfishSimulator:

    def __init__(self, population: CounterType[int]):
        self._population = Counter(population)

    @classmethod
    async def parse(cls, pop: str) -> "LanternfishSimulator":
        return LanternfishSimulator(Counter(map(int, pop.strip().split(","))))

    @property
    def population(self):
        return self._population.elements()

    @property
    def population_count(self):
        return sum(self._population.values())

    async def run_days(self, n: int) -> AsyncGenerator[CounterType[int], None]:
        for n in range(n):
            await self._run_day()
            yield self.population
            await asyncio.sleep(0)

    async def _run_day(self):
        n_birthers = self._population.pop(0, 0)
        self._population = Counter(
            {
                days_until_birth - 1: count
                for days_until_birth, count in self._population.items()
            }
        )
        self._population.update({6: n_birthers, 8: n_birthers})


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
