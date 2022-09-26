import unittest

from .abstract_lexer import AbstractLexer
from .source_handler import source_from_string
from .syntax_error import TinyBasicSyntaxError


def parser_from_string(src: str) -> AbstractLexer:
    src_handler = source_from_string(src)
    parser = AbstractLexer(src_handler)
    return parser


class AbstractParserReadSourceTest(unittest.TestCase):
    def test_get_char_empty(self):
        parser = parser_from_string('')
        self.assertEqual('', parser.get_char())

    def test_get_char_simple(self):
        parser = parser_from_string('a')
        self.assertEqual('a', parser.look)
        self.assertEqual('a', parser.get_char())
        self.assertEqual('', parser.get_char())

    def test_skip_whitespace_at_begin(self):
        parser = parser_from_string('   a')
        self.assertEqual('a', parser.get_char())
        self.assertEqual('', parser.get_char())

    def test_skip_whitespace(self):
        parser = parser_from_string('   ab c')
        self.assertEqual('a', parser.get_char())
        parser.skip_whitespace()
        self.assertEqual('b', parser.get_char())
        parser.skip_whitespace()
        self.assertEqual('c', parser.get_char())
        self.assertEqual('', parser.get_char())

    def test_is_alpha(self):
        parser = parser_from_string('a0')
        self.assertEqual('a', parser.look)
        self.assertTrue(parser.is_alpha())
        self.assertEqual('a', parser.get_char())
        self.assertEqual('0', parser.look)
        self.assertFalse(parser.is_alpha())
        self.assertEqual('0', parser.get_char())
        self.assertEqual('', parser.get_char())

    def test_is_digit(self):
        parser = parser_from_string('a0')
        self.assertEqual('a', parser.look)
        self.assertFalse(parser.is_digit())
        self.assertEqual('a', parser.get_char())
        self.assertEqual('0', parser.look)
        self.assertTrue(parser.is_digit())
        self.assertEqual('0', parser.get_char())
        self.assertEqual('', parser.get_char())


class AbstractParserReadTokensTest(unittest.TestCase):
    def test_read_until(self):
        # noinspection SpellCheckingInspection
        parser = parser_from_string('AAAAAABCD')
        self.assertEqual('AAAAAA', parser.read_until(lambda ch: ch == 'A'))
        self.assertEqual('', parser.read_until(lambda ch: ch == 'A'))

    def test_number(self):
        parser = parser_from_string('1985')
        self.assertEqual(1985, parser.read_number())

    def test_negative_number(self):
        parser = parser_from_string('-1985')
        self.assertEqual(-1985, parser.read_number())

    def test_non_number(self):
        parser = parser_from_string('apple tree')
        self.assertRaises(TinyBasicSyntaxError, parser.read_number)

    def test_identifier(self):
        parser = parser_from_string(' apple!')
        self.assertEqual('apple', parser.read_identifier())

    def test_non_identifier(self):
        parser = parser_from_string('1985')
        self.assertRaises(TinyBasicSyntaxError, parser.read_identifier)


class AbstractParserMatchFunctionTest(unittest.TestCase):
    def test_match_fn(self):
        parser = parser_from_string('a b')
        self.assertFalse(parser.match(lambda ch: ch == 'z', skip_white=True))
        self.assertTrue(parser.match(lambda ch: ch == 'a', skip_white=True))
        self.assertEqual('b', parser.look)

    def test_match_fn_with_whitespace(self):
        parser = parser_from_string('  a b')
        self.assertFalse(parser.match(lambda ch: ch == 'z', skip_white=True))
        self.assertTrue(parser.match(lambda ch: ch == 'a', skip_white=True))
        self.assertEqual('b', parser.look)

    def test_match_fn_no_skip(self):
        parser = parser_from_string('a b')
        self.assertFalse(parser.match(lambda ch: ch == 'z', skip_white=False))
        self.assertTrue(parser.match(lambda ch: ch == 'a', skip_white=False))
        self.assertEqual(' ', parser.look)


class AbstractParserMatchChTest(unittest.TestCase):
    def test_match_ch(self):
        parser = parser_from_string('a b')
        self.assertFalse(parser.match_ch('z', skip_whitespace=True))
        self.assertTrue(parser.match_ch('a', skip_whitespace=True))
        self.assertEqual('b', parser.look)

    def test_match_ch_no_skip(self):
        parser = parser_from_string('a b')
        self.assertFalse(parser.match_ch('z', skip_whitespace=False))
        self.assertTrue(parser.match_ch('a', skip_whitespace=False))
        self.assertEqual(' ', parser.look)


class AbstractParserExpectFunctionTest(unittest.TestCase):
    @staticmethod
    def _fn(ch: str) -> bool:
        return ch == 'a' or ch == '=' or ch == 'b'

    @staticmethod
    def _expect(expr: str, name: str = 'a=b') -> None:
        parser = parser_from_string(expr)
        parser.expect_fn(AbstractParserExpectFunctionTest._fn, name)
        parser.expect_fn(AbstractParserExpectFunctionTest._fn, name)
        parser.expect_fn(AbstractParserExpectFunctionTest._fn, name)

    def test_expect_fn(self):
        try:
            AbstractParserExpectFunctionTest._expect('a=b')
        except TinyBasicSyntaxError:
            self.fail("No syntax error shall be raised")

    def test_expect_fn_with_whitespace(self):
        try:
            AbstractParserExpectFunctionTest._expect(' a =  b  ')
        except TinyBasicSyntaxError:
            self.fail("No syntax error shall be raised")

    def test_unexpected_fn(self):
        self.assertRaises(TinyBasicSyntaxError, lambda: AbstractParserExpectFunctionTest._expect('a+b'))


class AbstractParserExpectChTest(unittest.TestCase):
    @staticmethod
    def _expect(expr: str):
        parser = parser_from_string(expr)
        parser.expect_ch('a')
        parser.expect_ch('=')
        parser.expect_ch('b')

    def test_expect_ch(self):
        try:
            AbstractParserExpectChTest._expect('a=b')
        except TinyBasicSyntaxError:
            self.fail("No syntax error shall be raised")

    def test_expect_ch_with_whitespace(self):
        try:
            AbstractParserExpectChTest._expect(' a =  b  ')
        except TinyBasicSyntaxError:
            self.fail("No syntax error shall be raised")

    def test_unexpected_ch(self):
        self.assertRaises(TinyBasicSyntaxError, lambda: AbstractParserExpectChTest._expect('a+b'))


class AbstractParserExpectStrTest(unittest.TestCase):
    def test_expect_str(self):
        parser = parser_from_string('apple tree')
        try:
            parser.expect_str('apple tree')
        except TinyBasicSyntaxError:
            self.fail("No syntax error shall be raised")

    def test_expect_str_with_whitespace(self):
        parser = parser_from_string('  apple tree')
        try:
            parser.expect_str('apple tree')
        except TinyBasicSyntaxError:
            self.fail("No syntax error shall be raised")

    def test_unexpected_prefix_str(self):
        parser = parser_from_string('apple tree')
        self.assertRaises(TinyBasicSyntaxError, lambda: parser.expect_str('xmas tree'))

    def test_unexpected_sub_str(self):
        parser = parser_from_string('apple tree')
        self.assertRaises(TinyBasicSyntaxError, lambda: parser.expect_str('apple juice'))


if __name__ == '__main__':
    unittest.main()
