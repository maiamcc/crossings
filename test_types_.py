import pytest

from types_ import WordPair, WordList


class TestWordPair:
    def test_first_longer(self):
        p = WordPair('bbbbb', 'aaa')
        assert p == ('bbbbb', 'aaa')

    def test_first_shorter(self):
        p = WordPair('aaa', 'bbbbb')
        assert p == ('bbbbb', 'aaa')

    def test_equal_length_first_earlier(self):
        p = WordPair('aaa', 'bbb')
        assert p == ('aaa', 'bbb')

    def test_equal_length_first_later(self):
        p = WordPair('bbb', 'aaa')
        assert p == ('aaa', 'bbb')


class TestWordList:
    def test_group_by_len(self):
        given = ['a', 'b', 'ccc', 'dd', 'ee', 'fff', 'ggggg', 'h']
        expected = [
            WordList(['a', 'b', 'h']),
            WordList(['dd', 'ee']),
            WordList(['ccc', 'fff']),
            WordList(['ggggg']),
        ]

        wd_list = WordList(given)
        actual = wd_list.group_by_len()

        assert expected == actual

    def wds_of_len_m_and_n(self):
        pass
