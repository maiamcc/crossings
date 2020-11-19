import pytest

from crossings import xpoints_for_pair, Pair, CrossingPoint

from typing import List


class TestXpointsForPair:
    @staticmethod
    def assert_xpoints(pair: Pair, expected: List[CrossingPoint]):
        actual = xpoints_for_pair(pair)
        assert set(expected) == set(actual)  # order doesn't matter

    def test_no_common_letters(self):
        self.assert_xpoints(('abcde', 'fghij'), [])

    def test_one_possible_crossing(self):
        self.assert_xpoints(('abcxde', 'fgxhij'), [(3, 2)])

    def test_common_letter_twice_one_word(self):
        self.assert_xpoints(('abcxdex', 'fgxhij'), [(3, 2), (6, 2)])

    def test_common_letter_twice_each_word(self):
        self.assert_xpoints(('abcxdex', 'xfgxhij'), [(3, 0), (6, 0), (3, 3), (6, 3)])

    def test_many_crossing_points(self):
        self.assert_xpoints(('stackoverflow', 'storkovenmitt'),
                            [(0, 0), (1, 1), (1, 11), (1, 12), (4, 4), (5, 2),
                             (5, 5), (6, 6), (7, 7), (8, 3), (11, 2), (11, 5)]
                            )
