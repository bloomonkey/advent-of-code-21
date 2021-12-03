# -*- coding: utf-8 -*-
"""Document day_3 here.

Created 03. Dec 2021 09:11

"""
import asyncio
from collections import Counter
from pathlib import Path
from typing import List

import aiofiles
import typer


class Diagnostics:
    def __init__(self):
        self._bit_counters = []
        self._raw_readings = []

    async def update(self, reading) -> None:
        self._raw_readings.append(reading)
        for i, bit in enumerate(reading):
            try:
                self._bit_counters[i].update(bit)
            except IndexError:
                self._bit_counters.append(Counter(bit))

        return

    @property
    def power_consumption(self) -> int:
        return self.gamma * self.epsilon

    @property
    def life_support_rating(self) -> int:
        return self.oxygen_generator_rating * self.co2_scrubber_rating

    @property
    def gamma(self) -> int:
        return int(
            "".join([c.most_common()[0][0] for c in self._bit_counters]),
            base=2,
        )

    @property
    def epsilon(self) -> int:
        return int(
            "".join([c.most_common()[-1][0] for c in self._bit_counters]),
            base=2,
        )

    @property
    def oxygen_generator_rating(self) -> int:
        return self._calculate_life_support_rating(
            self._raw_readings.copy(), True
        )

    @property
    def co2_scrubber_rating(self) -> int:
        return self._calculate_life_support_rating(
            self._raw_readings.copy(), False
        )

    def _calculate_life_support_rating(
        self, readings: List[str], supportive: bool
    ) -> int:
        # supportive: is the gas supportive of life...
        for i, _ in enumerate(self._bit_counters):
            counter = Counter([r[i] for r in readings])
            selector = sorted(
                counter.items(),
                key=lambda r: (r[1], r[0]),
                reverse=supportive,
            )[0][0]
            readings = [r for r in readings if r[i] == selector]
            if len(readings) == 1:
                break
        return int(readings[0], base=2)


async def _main():
    diagnostics = Diagnostics()
    input_path = Path(__file__).parent.parent.parent / "data" / "input-3.txt"
    async with aiofiles.open(input_path, mode="r") as f:
        async for reading in f:
            await diagnostics.update(reading)

    print(f"Power consumption: {diagnostics.power_consumption}")
    print(f"Life Support Rating: {diagnostics.life_support_rating}")


def main():
    asyncio.run(_main())


if __name__ == "__main__":
    typer.run(main)
