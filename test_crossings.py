import string
from typing import List, Tuple

from crossings import Crossing, crossings_from_xpoint_groups, get_reciprocal_xpoints, group_by_xpoint, xpoints_for_pair, Pair, CrossingPoint, XpointGroups

import pytest


class TestPair:
    def test_first_longer(self):
        p = Pair('bbbbb', 'aaa')
        assert p == ('bbbbb', 'aaa')

    def test_first_shorter(self):
        p = Pair('aaa', 'bbbbb')
        assert p == ('bbbbb', 'aaa')

    def test_equal_length_first_earlier(self):
        p = Pair('aaa', 'bbb')
        assert p == ('aaa', 'bbb')

    def test_equal_length_first_later(self):
        p = Pair('bbb', 'aaa')
        assert p == ('aaa', 'bbb')


class TestXpointsForPair:
    @staticmethod
    def assert_xpoints(pair: Pair, expected: List[CrossingPoint]):
        actual = xpoints_for_pair(pair)
        assert set(expected) == set(actual)  # order doesn't matter

    def test_no_common_letters(self):
        self.assert_xpoints(Pair('abcde', 'fghij'), [])

    def test_one_possible_crossing(self):
        self.assert_xpoints(Pair('abcxde', 'fgxhij'), [(3, 2)])

    def test_common_letter_twice_one_word(self):
        self.assert_xpoints(Pair('abcxdex', 'fgxhij'), [(3, 2), (6, 2)])

    def test_common_letter_twice_each_word(self):
        self.assert_xpoints(Pair('abcxdex', 'xfgxhij'), [(3, 0), (6, 0), (3, 3), (6, 3)])

    def test_many_crossing_points(self):
        self.assert_xpoints(Pair('stackoverflow', 'storkovenmitt'),
                            [(0, 0), (1, 1), (1, 11), (1, 12), (4, 4), (5, 2),
                             (5, 5), (6, 6), (7, 7), (8, 3), (11, 2), (11, 5)]
                            )


def test_group_by_xpoint():
    p0 = Pair('abcdefgh', 'ijklmnop')  # no xpoints
    p1 = Pair('abcxdefg', 'hixjklmn')  # (3,2)
    p2 = Pair('abcxdexf', 'ghxijklm')  # (3,2), (6,2)
    p3 = Pair('abxdefgh', 'ijklmnxo')  # (2,6)

    expected = XpointGroups({
        (3, 2): [p1, p2],
        (6, 2): [p2],
        (2, 6): [p3]
    })

    # (a more robust test might check that each key contains the right values, ignoring order)
    assert group_by_xpoint([p0, p1, p2, p3]) == expected


class TestGetReciprocalXpoints:
    def test_no_reciprocal(self):
        expected = set()
        actual = get_reciprocal_xpoints([(0, 0), (0, 1), (0, 2)], 4, 7)
        assert actual == expected

    def test_reciprocal(self):
        expected = {((0, 0), (7, 10)), ((3, 8), (4, 2))}
        actual = get_reciprocal_xpoints([(0, 0), (7, 10), (3, 8), (4, 2), (5, 6)], 8, 11)
        assert actual == expected

    def test_reciprocal_symmetrical(self):
        expected = {((0, 1), (6, 5)), ((3, 3), (3, 3))}
        actual = get_reciprocal_xpoints([(0, 1), (6, 5), (3, 3), (4, 2), (5, 6)], 7, 7)
        assert actual == expected


# def test_crossings_from_xpoint_groups():
#     pairs = random_pairs(5, 7, 13)
#
#     xpoint_groups = XpointGroups({
#         (0, 0): [pairs[0]],
#         (0, 4): [pairs[1]],
#         (1, 3): [pairs[2], pairs[3]],
#         (2, 3): [pairs[4], pairs[5]],
#         (3, 1): [pairs[6], pairs[7]],
#         (3, 5): [pairs[8], pairs[9]],
#         (4, 2): [pairs[10], pairs[11]],
#         (4, 6): [pairs[12]]
#
#     })
#
#     expected = [
#         Crossing([pairs[0], pairs[12]], [(0, 0), (4, 6)]),
#         Crossing([pairs[1], pairs[10]], [(0, 4), (4, 2)]),
#         Crossing([pairs[1], pairs[11]], [(0, 4), (4, 2)]),
#         Crossing([pairs[4], pairs[5]], [(2, 3), (2, 3)]),
#         Crossing([pairs[6], pairs[8]], [(3, 1), (3, 5)]),
#         Crossing([pairs[6], pairs[9]], [(3, 1), (3, 5)]),
#         Crossing([pairs[7], pairs[8]], [(3, 1), (3, 5)]),
#         Crossing([pairs[7], pairs[9]], [(3, 1), (3, 5)]),
#     ]
#
#     actual = crossings_from_xpoint_groups(xpoint_groups)
#     assert set(actual) == set(expected)  # order doesn't matter


def random_pairs(m: int, n: int, num_pairs: int) -> List[Pair]:
    """Test util to generate unique word-pairs."""
    if num_pairs > 13:
        raise Exception('why are you generating that many pairs?? There\'s only so much alphabet.')

    res = []
    letters = [l for l in string.ascii_lowercase]
    for i in range(num_pairs):
        res.append(Pair(letters.pop() * m, letters.pop() * n))
    return res
