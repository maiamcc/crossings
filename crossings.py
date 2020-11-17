from typing import Dict, Generator, List, Set, Tuple

Wordlist = List[str]
Pair = Set[str]
Crossing = Set[Pair]
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


def find_pairs_and_group_by_xpoint(len_m: Wordlist, len_n: Wordlist) -> Dict[CrossingPoint, Set[Pair]]:
    """
    Find all possible pairs of one word of length m & one of length n.

    Group all pairs by their valid crossing points. (Note that a single pair may have
    multiple valid crossing points.)
    """

    pairs = find_pairs(len_m, len_n)
    return group_by_xpoint(pairs)


def find_pairs(len_m: Wordlist, len_n: Wordlist) -> Set[Pair]:
    """
    Find all possible pairs of one word of length m and one of length n
    (order does not matter).
    """
    pass


def group_by_xpoint(pairs: Set[Pair]) -> Dict[CrossingPoint, Set[Pair]]:
    """
    Group all pairs by their valid crossing points. (Note that a single pair may have
    multiple valid crossing points.)

    :param pairs: pairs of words to group
    :return: a dict of crossing points (int tuples indicating indices) -> all the pairs for which this is a valid crossing point
    """
    pass


def xpoints_for_pair(pair: Pair) -> List[CrossingPoint]:
    """
    Find all possible crossing points for the given pair of words.

    A pair of words has a crossing point at (i, j) if wd1[i] == wd2[j]
    (meaning the two words could be placed on a grid such that they
    intersected at this letter).
    """
    return []


def crossings_from_xpoint_groups(xpoint_groups: Dict[CrossingPoint, Set[Pair]]) -> Set[Crossing]:
    """

    :param xpoint_groups: a dict of crossing points (int tuples indicating indices) -> all the pairs for which this is a valid crossing point
    :return: all possible distinct combinations of pairs (i.e. no word appears more than once over the two pairs) with at least one shared crossing point
    """