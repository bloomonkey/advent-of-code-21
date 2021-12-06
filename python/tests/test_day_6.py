# -*- coding: utf-8 -*-
"""Document test_day_6 here.

Created 06. Dec 2021 18:00

"""

import pytest

from day_6 import LanternfishSimulator


@pytest.mark.asyncio
async def test_lanternfish_model():
    start_state = "3,4,3,1,2"
    sim = await LanternfishSimulator.parse(start_state)
    async for population in sim.run_days(18):
        print(",".join(map(str, population)))

    assert sim.population_count == 26

    async for _ in sim.run_days(80 - 18):
        pass

    assert sim.population_count == 5934
