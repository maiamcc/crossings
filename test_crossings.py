import string
from typing import List, Set

from crossings import find_all_multicrossings, find_pairs, get_reciprocal_xpoints, group_by_xpoint, multicrossings_from_xpoint_groups, xpoints_for_word_pair
from types_ import Multicrossing, WordPair, CrossingPoint, XpointGroups

import pytest


class TestXpointsForPair:
    @staticmethod
    def assert_xpoints(pair: WordPair, expected: List[CrossingPoint]):
        actual = xpoints_for_word_pair(pair)
        assert set(expected) == set(actual)  # order doesn't matter

    def test_no_common_letters(self):
        self.assert_xpoints(WordPair('abcde', 'fghij'), [])

    def test_one_possible_crossing(self):
        self.assert_xpoints(WordPair('abcxde', 'fgxhij'), [(3, 2)])

    def test_common_letter_twice_one_word(self):
        self.assert_xpoints(WordPair('abcxdex', 'fgxhij'), [(3, 2), (6, 2)])

    def test_common_letter_twice_each_word(self):
        self.assert_xpoints(WordPair('abcxdex', 'xfgxhij'), [(3, 0), (6, 0), (3, 3), (6, 3)])

    def test_many_crossing_points(self):
        self.assert_xpoints(WordPair('stackoverflow', 'storkovenmitt'),
                            [(0, 0), (1, 1), (1, 11), (1, 12), (4, 4), (5, 2),
                             (5, 5), (6, 6), (7, 7), (8, 3), (11, 2), (11, 5)]
                            )


def test_group_by_xpoint():
    p0 = WordPair('abcdefgh', 'ijklmnop')  # no xpoints
    p1 = WordPair('abcxdefg', 'hixjklmn')  # (3,2)
    p2 = WordPair('abcxdexf', 'ghxijklm')  # (3,2), (6,2)
    p3 = WordPair('abxdefgh', 'ijklmnxo')  # (2,6)

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
        actual = get_reciprocal_xpoints({(0, 0), (0, 1), (0, 2)}, 4, 7)
        assert actual == expected

    def test_reciprocal(self):
        expected = {((0, 0), (7, 10)), ((3, 8), (4, 2))}
        actual = get_reciprocal_xpoints({(0, 0), (7, 10), (3, 8), (4, 2), (5, 6)}, 8, 11)
        assert actual == expected

    def test_reciprocal_symmetrical(self):
        expected = {((0, 1), (6, 5)), ((3, 3), (3, 3))}
        actual = get_reciprocal_xpoints({(0, 1), (6, 5), (3, 3), (4, 2), (5, 6)}, 7, 7)
        assert actual == expected


def test_find_pairs():
    expected = {WordPair('a', 'b'), WordPair('a', 'c'), WordPair('a', 'c'), WordPair('b', 'c')}
    actual = find_pairs(['a', 'b', 'c'], ['a', 'b'])
    assert expected == set(actual)


class TestCrossingsFromXpointGroups:
    @staticmethod
    def assert_crossings(grps: XpointGroups, expected: Set[Multicrossing]):
        actual = multicrossings_from_xpoint_groups(grps)
        assert expected == set(actual)  # order doesn't matter

    @staticmethod
    def random_pairs(m: int, n: int, num_pairs: int) -> List[WordPair]:
        """Test util to generate unique word-pairs."""
        if num_pairs > 13:
            raise Exception('why are you generating that many pairs?? There\'s only so much alphabet.')

        res = []
        letters = [l for l in string.ascii_lowercase]
        for i in range(num_pairs):
            res.append(WordPair(letters.pop(0) * m, letters.pop(0) * n))
        return res

    def test_no_crossings(self):
        pairs = self.random_pairs(7, 5, 3)

        xpoint_groups = XpointGroups({
            (0, 0): [pairs[0]],  # recip. (6, 4) (DNE)
            (1, 1): [pairs[1]],  # recip. (5, 3) (DNE)
            (2, 2): [pairs[2]],  # recip. (4, 2) (DNE)
        })

        expected = set()

        self.assert_crossings(xpoint_groups, expected)

    def test_one_crossing(self):
        pairs = self.random_pairs(7, 5, 2)

        xpoint_groups = XpointGroups({
            (0, 0): [pairs[0]],
            (6, 4): [pairs[1]]

        })

        expected = {
            Multicrossing((pairs[0], pairs[1]), ((0, 0), (6, 4))),
        }

        self.assert_crossings(xpoint_groups, expected)

    def test_symmetrical_crossing_but_no_dupes(self):
        pairs = self.random_pairs(7, 5, 2)

        xpoint_groups = XpointGroups({
            (3, 2): [pairs[0], pairs[1]],
        })

        expected = {
            Multicrossing((pairs[0], pairs[1]), ((3, 2), (3, 2))),
        }

        self.assert_crossings(xpoint_groups, expected)

    def test_combinatorics_two_by_one(self):
        pairs = self.random_pairs(5, 4, 3)

        xpoint_groups = XpointGroups({
            (0, 1): [pairs[0]],
            (4, 2): [pairs[1], pairs[2]]

        })

        expected = {
            Multicrossing((pairs[0], pairs[1]), ((0, 1), (4, 2))),
            Multicrossing((pairs[0], pairs[2]), ((0, 1), (4, 2))),
        }

        self.assert_crossings(xpoint_groups, expected)

    def test_combinatorics_two_by_two(self):
        pairs = self.random_pairs(5, 4, 4)

        xpoint_groups = XpointGroups({
            (0, 1): [pairs[0], pairs[1]],
            (4, 2): [pairs[2], pairs[3]]

        })

        expected = {
            Multicrossing((pairs[0], pairs[2]), ((0, 1), (4, 2))),
            Multicrossing((pairs[1], pairs[2]), ((0, 1), (4, 2))),
            Multicrossing((pairs[0], pairs[3]), ((0, 1), (4, 2))),
            Multicrossing((pairs[1], pairs[3]), ((0, 1), (4, 2))),
        }

        self.assert_crossings(xpoint_groups, expected)


class TestFindAllMulticrossings:
    def test_simple(self):
        given = ['ABCDE', 'FGHIJ', 'ZDZZZZ', 'ZZZZGZ']
        expected = {
            Multicrossing(
                (WordPair('ZDZZZZ', 'ABCDE'), WordPair('ZZZZGZ', 'FGHIJ')),
                ((1, 3), (4, 1))
            )
        }
        actual = find_all_multicrossings(given)

        assert expected == actual

    def test_no_valid_multicrossings(self):
        given = ['ABCDE', 'fghij', 'klmn', 'opqr']
        expected = set()
        actual = find_all_multicrossings(given)

        assert expected == actual

    def test_normalized(self):
        given = ['some CLUE', 'clue-again', 'other clue!', '"next clue"']
        expected = {
            Multicrossing(
                (WordPair('CLUEAGAIN', 'SOMECLUE'), WordPair('OTHERCLUE', 'NEXTCLUE')),
                ((3, 3), (5, 4))
            )
        }
        actual = find_all_multicrossings(given)

        assert expected == actual
