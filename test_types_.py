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
    given = ['a', 'b', 'ccc', 'dd', 'ee', 'fff', 'ggggg', 'h']
    len1 = WordList(['a', 'b', 'h'])
    len2 = WordList(['dd', 'ee'])
    len3 = WordList(['ccc', 'fff'])
    len5 = WordList(['ggggg'])

    def test_group_by_len(self):
        expected = [self.len1, self.len2, self.len3, self.len5]

        wd_list = WordList(self.given)
        actual = wd_list.group_by_len()

        assert expected == actual

    def test_wds_of_len_m_and_n(self):
        expected = [
            # longer words come first
            (self.len1, self.len1),
            (self.len2, self.len1),
            (self.len3, self.len1),
            (self.len5, self.len1),

            (self.len2, self.len2),
            (self.len3, self.len2),
            (self.len5, self.len2),

            (self.len3, self.len3),
            (self.len5, self.len3),

            (self.len5, self.len5),
        ]
        wd_list = WordList(self.given)
        actual = wd_list.wds_of_len_m_and_n()

        assert expected == actual
