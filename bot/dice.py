from __future__ import annotations

import random
from collections.abc import Callable

RandomFunc = Callable[[], float]
RandIntFunc = Callable[[int, int], int]


def biased_high_roll(
    random_func: RandomFunc | None = None,
    randint_func: RandIntFunc | None = None,
) -> int:
    """65以上が約20%になる 1d100 を返す。"""

    random_func = random_func or random.random
    randint_func = randint_func or random.randint

    if random_func() < 0.20:
        return randint_func(65, 100)
    return randint_func(1, 64)


def biased_low_roll(
    random_func: RandomFunc | None = None,
    randint_func: RandIntFunc | None = None,
) -> int:
    """30%で 1〜5 を返し、それ以外は 6〜100 を返す。"""

    random_func = random_func or random.random
    randint_func = randint_func or random.randint

    if random_func() < 0.30:
        return randint_func(1, 5)
    return randint_func(6, 100)


def roll_many(roller: Callable[[], int], count: int = 10) -> list[int]:
    return [roller() for _ in range(count)]


def format_rolls(label: str, rolls: list[int]) -> str:
    joined = ", ".join(str(value) for value in rolls)
    return f"**{label}**\n[{joined}]"