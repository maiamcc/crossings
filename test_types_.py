import pytest

from types_ import WordPair


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