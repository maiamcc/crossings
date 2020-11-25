from typing import List, Tuple

from utils import sorted_tuple


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


Wordlist = List[str]
CrossingPoint = Tuple[int, int]
