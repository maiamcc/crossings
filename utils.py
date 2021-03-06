from typing import Any, Iterable, List, Tuple


def sorted_tuple(*args, **kwargs):
    return tuple(sorted(args, **kwargs))


def pairwise_combinations(a: Iterable, b: Iterable, sort=True, allow_self_pair=False, sortkey=lambda x: x) -> List[Tuple[Any]]:
    res = []
    seen = set()
    for elemA in a:
        for elemB in b:
            if elemA != elemB or allow_self_pair:
                tup = sorted_tuple(elemA, elemB)
                if tup not in seen:
                    seen.add(tup)
                    if not sort:
                        res.append((elemA, elemB))
                    else:
                        res.append(sorted_tuple(elemA, elemB, key=sortkey))
    return res


def normalize(wd: str):
    return ''.join([ch for ch in wd if ch.isalnum()]).upper()
