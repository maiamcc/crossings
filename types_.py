from collections import defaultdict
from typing import List, Tuple

from utils import pairwise_combinations, sorted_tuple


class WordPair(tuple):
    def __new__(cls, wd1: str, wd2: str):
        # Sort first by length (longer first), then if same length, alphabetically
        return sorted_tuple(wd1, wd2, key=lambda x: (-len(x), x))


# Dict[CrossingPoint, List[WordPair]
class XpointGroups(dict):
    # Just assume that all the wdpairs in here have the same word lengths. And are
    # like, the right types and stuff. I'm not doing input verification because
    # untyped languages are PERFECTLY SAFE what could go wrong 😬
    def m(self):
        for v in self.values():
            return len(v[0][0])

    def n(self):
        for v in self.values():
            return len(v[0][1])


# This is a terrible name but #yolo
class Multicrossing:
    def __init__(self, wd_pairs: Tuple[WordPair, WordPair], xpoints: Tuple[Tuple[int, int], Tuple[int, int]]):
        if len(wd_pairs) != 2:
            raise TypeError('Need exactly two wd_pairs (got {}: {})'.
                            format(len(wd_pairs), wd_pairs))
        if len(xpoints) != 2:
            raise TypeError('Need exactly two xpoints (got {}: {})'.
                            format(len(xpoints), xpoints))

        self.wd_pairs = wd_pairs
        self.xpoints = xpoints

    def __hash__(self): return self.wd_pairs.__hash__() + self.xpoints.__hash__()

    def __eq__(self, other): return self.__hash__() == other.__hash__()

    def __repr__(self):
        return '{} @ {} & {} @ {}'.format(self.wd_pairs[0], self.xpoints[0],
                                          self.wd_pairs[1], self.xpoints[1])


class WordList(list):
    """A list of words (i.e. List[str])."""

    def __hash__(self): return str(self).__hash__()  # ugh I hate it.

    def __eq__(self, other): return self.__hash__() == other.__hash__()

    def group_by_len(self) -> List['WordList']:
        """Given a list of words, return a list of lists of words,
        where each list contains all the words of a given length."""
        d = defaultdict(list)
        for wd in self:
            d[len(wd)].append(wd)

        return [WordList(d[n]) for n in sorted(d.keys())]

    def wds_of_len_m_and_n(self) -> List[Tuple['WordList', 'WordList']]:
        """
            Given a list of words, group by length and yield all possible pairwise
            combinations of groups.
        """
        wds_by_len = self.group_by_len()

        return pairwise_combinations(wds_by_len, wds_by_len,
                                     allow_self_pair=True,  # can pair the same wordlist with itself
                                     sortkey=lambda x: -len(x[0]))  # order with longer words first


CrossingPoint = Tuple[int, int]
