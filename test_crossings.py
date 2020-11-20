import pytest

from crossings import crossings_from_xpoint_groups, group_by_xpoint, new_pair, xpoints_for_pair, Pair, CrossingPoint

from typing import List


class TestNewPair:
    def test_first_longer(self):
        p = new_pair('bbbbb', 'aaa')
        assert p == ('bbbbb', 'aaa')

    def test_first_shorter(self):
        p = new_pair('aaa', 'bbbbb')
        assert p == ('bbbbb', 'aaa')

    def test_equal_length_first_earlier(self):
        p = new_pair('aaa', 'bbb')
        assert p == ('aaa', 'bbb')

    def test_equal_length_first_later(self):
        p = new_pair('bbb', 'aaa')
        assert p == ('aaa', 'bbb')


class TestXpointsForPair:
    @staticmethod
    def assert_xpoints(pair: Pair, expected: List[CrossingPoint]):
        actual = xpoints_for_pair(pair)
        assert set(expected) == set(actual)  # order doesn't matter

    def test_no_common_letters(self):
        self.assert_xpoints(new_pair('abcde', 'fghij'), [])

    def test_one_possible_crossing(self):
        self.assert_xpoints(new_pair('abcxde', 'fgxhij'), [(3, 2)])

    def test_common_letter_twice_one_word(self):
        self.assert_xpoints(new_pair('abcxdex', 'fgxhij'), [(3, 2), (6, 2)])

    def test_common_letter_twice_each_word(self):
        self.assert_xpoints(new_pair('abcxdex', 'xfgxhij'), [(3, 0), (6, 0), (3, 3), (6, 3)])

    def test_many_crossing_points(self):
        self.assert_xpoints(new_pair('stackoverflow', 'storkovenmitt'),
                            [(0, 0), (1, 1), (1, 11), (1, 12), (4, 4), (5, 2),
                             (5, 5), (6, 6), (7, 7), (8, 3), (11, 2), (11, 5)]
                            )


def test_group_by_xpoint():
    p0 = new_pair('abcde', 'fghij')     # no xpoints
    p1 = new_pair('abcxde', 'fgxhij')   # (3,2)
    p2 = new_pair('abcxdex', 'fgxhij')  # (3,2), (6,2)
    p3 = new_pair('abxdefg', 'hijklmx')  # (2,6)

    expected = {
        (3, 2): [p1, p2],
        (6, 2): [p2],
        (2, 6): [p3]
    }

    # (a more robust test might check that each key contains the right values, ignoring order)
    assert group_by_xpoint([p0, p1, p2, p3]) == expected


def test_crossings_from_xpoint_groups():
    pass
