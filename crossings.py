from collections import defaultdict
from typing import Any, Generator, Iterable, List, Set, Tuple


def sorted_tuple(*args, **kwargs):
    return tuple(sorted(args, **kwargs))


class Pair(tuple):
    def __new__(cls, wd1: str, wd2: str):
        # Sort first by length (longer first), then if same length, alphabetically
        return sorted_tuple(wd1, wd2, key=lambda x: (-len(x), x))


# Dict[CrossingPoint, List[Pair]
class XpointGroups(dict):
    # Just assume that all the pairs in here have the same word lengths. And are
    # like, the right types and stuff. I'm not doing input verification because
    # untyped languages are PERFECTLY SAFE what could go wrong 😬
    def m(self):
        for v in self.values():
            return len(v[0][0])

    def n(self):
        for v in self.values():
            return len(v[0][1])


class Crossing:
    def __init__(self, pairs: Tuple[Pair, Pair], xpoints: Tuple[Tuple[int, int], Tuple[int, int]]):
        if len(pairs) != 2:
            raise TypeError('Need exactly two pairs (got {}: {})'.
                            format(len(pairs), pairs))
        if len(xpoints) != 2:
            raise TypeError('Need exactly two xpoints (got {}: {})'.
                            format(len(xpoints), xpoints))

        self.pairs = pairs
        self.xpoints = xpoints

    def __hash__(self): return self.pairs.__hash__() + self.xpoints.__hash__()

    def __eq__(self, other): return self.__hash__() == other.__hash__()

    def __repr__(self):
        return '{} @ {} & {} @ {}'.format(self.pairs[0], self.xpoints[0],
                                          self.pairs[1], self.xpoints[1])




Wordlist = List[str]
CrossingPoint = Tuple[int, int]


def find_all_crossings(wds: Wordlist) -> Set[Crossing]:
    result = set()
    for len_m, len_n in wds_of_len_m_and_n(wds):
        result.update(find_crossings(len_m, len_n))
    return result


def group_by_len(wds: Wordlist) -> List[Wordlist]:
    """Given a list of words, return a list of lists of words,
       where each list contains all the words of a given length."""
    pass


def wds_of_len_m_and_n(wds: Wordlist) -> Generator[Tuple[Wordlist, Wordlist], None, None]:
    """
        Given a list of words, group by length and yield all possible pairwise
        combinations of groups.
    """
    wds_by_len = group_by_len(wds)

    # all possible pairwise combinations
    pass


def find_crossings(len_m: Wordlist, len_n: Wordlist) -> Set[Crossing]:
    """
    Find crossings between words of length m and length n.

    A crossing is a set of pairs of words (each pair of words containing one word
    of length m and one of length n) such that the two pairs may intersect symmetrically.
    E.g. if the first pair intersects at (2, 4), the second pair intersects at (n-3, n-5)
    or, in English: in pair #1, if the 3rd character of the first word is the same as the
    5th character of the second word (i.e. the crossing point), then the second pair must
    have the inverse crossing point; i.e. in pair #2, the 3rd character from the END of
    the first word must be the same as the 5th character from the END of the second word.

    :param len_m: words of length m
    :param len_n: words of length n
    :return: all possible crossings where two words of length m can intersect two words of length n symmetrically
    """
    pairs_by_xpoint = find_pairs_and_group_by_xpoint(len_m, len_n)
    return crossings_from_xpoint_groups(pairs_by_xpoint)


def find_pairs_and_group_by_xpoint(len_m: Wordlist, len_n: Wordlist) -> XpointGroups:
    """
    Find all possible pairs of one word of length m & one of length n.

    Group all pairs by their valid crossing points. (Note that a single pair may have
    multiple valid crossing points.)
    """

    pairs = find_pairs(len_m, len_n)
    return group_by_xpoint(pairs)


def find_pairs(len_m: Wordlist, len_n: Wordlist) -> List[Pair]:
    """
    Find all possible pairs of one word of length m and one of length n.
    """
    res = []
    combs = pairwise_combinations(len_m, len_n)
    for wd1, wd2 in combs:
        res.append(Pair(wd1, wd2))

    return res


def pairwise_combinations(a: Iterable, b: Iterable) -> List[Tuple[Any]]:
    res = []
    for elemA in a:
        for elemB in b:
            if elemA != elemB:
                res.append(sorted_tuple(elemA, elemB))
    return res


def group_by_xpoint(pairs: List[Pair]) -> XpointGroups:
    """
    Group all pairs by their valid crossing points. (Note that a single pair may have
    multiple valid crossing points.)

    :param pairs: pairs of words to group
    :return: a dict of crossing points (int tuples indicating indices) -> all the pairs for which this is a valid crossing point
    """
    grps = defaultdict(list)
    for p in pairs:
        xpoints = xpoints_for_pair(p)
        for xpt in xpoints:
            grps[xpt].append(p)

    return XpointGroups(grps)


def xpoints_for_pair(pair: Pair) -> List[CrossingPoint]:
    """
    Find all possible crossing points for the given pair of words.

    A pair of words has a crossing point at (i, j) if wd1[i] == wd2[j]
    (meaning the two words could be placed on a grid such that they
    intersected at this letter).
    """
    res = []

    # this is inefficient but words are short so I don't care
    for i, ch1 in enumerate(pair[0]):
        for j, ch2 in enumerate(pair[1]):
            if ch1 == ch2:
                res.append((i, j))
    return res


def get_reciprocal_xpoints(xpoints: List[CrossingPoint], m: int, n: int) -> Set[Tuple[CrossingPoint]]:
    res = set()
    xpoints = set(xpoints)
    for xp in xpoints:
        reciprocal = (m-1-xp[0], n-1-xp[1])
        if reciprocal in xpoints:
            res.add(sorted_tuple(xp, reciprocal))  # make sure it goes into the set in consistent order
    return res


def crossings_from_xpoint_groups(xpoint_groups: XpointGroups) -> List[Crossing]:
    """
        :param xpoint_groups: a dict of crossing points (int tuples indicating indices) -> all the pairs for which this is a valid crossing point
        :return: all possible distinct combinations of pairs (i.e. no word appears more than once over the two pairs) with at least one shared crossing point
    """

    res = []

    reciprocal_xpoint_pairs = get_reciprocal_xpoints(list(xpoint_groups.keys()), xpoint_groups.m(), xpoint_groups.n())
    print('recip. pairs:', reciprocal_xpoint_pairs)
    for rxps in reciprocal_xpoint_pairs:
        for pairs in pairwise_combinations(xpoint_groups[rxps[0]], xpoint_groups[rxps[1]]):
            print('pairs:', pairs)
            print('rxps:', rxps)
            res.append(Crossing(pairs, rxps))
    return res


