from typing import Any, Iterable, List, Tuple


def sorted_tuple(*args, **kwargs):
    return tuple(sorted(args, **kwargs))


def pairwise_combinations(a: Iterable, b: Iterable) -> List[Tuple[Any]]:
    res = []
    for elemA in a:
        for elemB in b:
            if elemA != elemB:
                res.append(sorted_tuple(elemA, elemB))
    return res