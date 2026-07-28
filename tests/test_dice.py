from __future__ import annotations

import unittest

from bot.dice import biased_high_roll, biased_low_roll, roll_many


class DiceLogicTests(unittest.TestCase):
    def test_biased_high_roll_uses_high_bucket(self) -> None:
        result = biased_high_roll(random_func=lambda: 0.19, randint_func=lambda a, b: a)
        self.assertGreaterEqual(result, 65)
        self.assertLessEqual(result, 100)

    def test_biased_high_roll_uses_low_bucket(self) -> None:
        result = biased_high_roll(random_func=lambda: 0.20, randint_func=lambda a, b: b)
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 64)

    def test_biased_low_roll_uses_low_special_bucket(self) -> None:
        result = biased_low_roll(random_func=lambda: 0.29, randint_func=lambda a, b: a)
        self.assertGreaterEqual(result, 1)
        self.assertLessEqual(result, 5)

    def test_biased_low_roll_uses_normal_bucket(self) -> None:
        result = biased_low_roll(random_func=lambda: 0.30, randint_func=lambda a, b: a)
        self.assertGreaterEqual(result, 6)
        self.assertLessEqual(result, 100)

    def test_roll_many_returns_10_results(self) -> None:
        rolls = roll_many(lambda: 42, count=10)
        self.assertEqual(len(rolls), 10)
        self.assertTrue(all(value == 42 for value in rolls))


if __name__ == "__main__":
    unittest.main()