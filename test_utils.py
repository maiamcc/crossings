import pytest

from utils import pairwise_combinations


def test_pairwise_combinations():
    expected = {('a', 'b'), ('a', 'c'), ('a', 'c'), ('b', 'c')}
    actual = pairwise_combinations(['a', 'b', 'c'], ['a', 'b'])
    assert expected == set(actual)
