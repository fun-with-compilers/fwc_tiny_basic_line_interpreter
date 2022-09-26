from .source_handler import SourceHandler
from .lexer_utils import is_alpha, is_digit, is_whitespace
from .syntax_error import TinyBasicSyntaxError


class AbstractLexer:
    """
    Base class for recursive descant parsing
    """
    def __init__(self, src: SourceHandler):
        """
        Initialize with SourceHandler
        :param src: source code
        """
        self.src = src
        self.look = src.get_char()
        self.skip_whitespace()

    def get_char(self) -> str:
        """
        Read the next character from the input and return the previous one
        :return: The previous character (self.look before get_char)
        """
        result = self.look
        self.look = self.src.get_char()
        return result

    def is_alpha(self) -> bool:
        """
        :return: True when self.look is a letter
        """
        return is_alpha(self.look)

    def is_digit(self) -> bool:
        """
        :return: True when self.look is a numeric digit
        """
        return is_digit(self.look)

    def is_whitespace(self) -> bool:
        """
        :return: True when self.look is a whitespace character
        """
        return is_whitespace(self.look)

    def read_until(self, fn) -> str:
        """
        Read the input while fn(self.look) is true
        :return: The input string
        """
        result = ""
        while fn(self.look):
            result += self.get_char()
        # Notice we call "skip_white" before reading, so white space is ignored between symbols, but not inside them
        self.skip_whitespace()
        return result

    def read_number(self) -> int:
        """
        :return: Read a signed integer from the source code
        """

        # Source code is a character string, so our result will be a string too. We have to convert it.
        # Since we are only reading digits, the conversion must succeed all times
        result = ""

        # Detect negative sign
        if self.look == '-':
            result += self.get_char()
            self.skip_whitespace()
        # If next input is not a digit then fail
        if not self.is_digit():
            self._raise_error_expected('number')
        # Read the input as long as the current character is a digit
        result += self.read_until(lambda ch: is_digit(ch))
        return int(result)

    def read_identifier(self) -> str:
        """
        Read an identifier from the source code. Works similarly to read_number, but expects alphanumeric characters
        :return: Symbol as string
        """
        if not self.is_alpha():
            self._raise_error_expected('identifier')
        return self.read_until(lambda ch: is_digit(ch) or is_alpha(ch))

    def match(self, fn, skip_white: bool = True) -> bool:
        """
        Detect if next character on input matches our expectation
        :param fn: expectation as a char->bool function
        :param skip_white: True if we must call skip_white
        :return: True if the input matches our expectation
        """
        if fn(self.look):
            self.get_char()
            if skip_white:
                self.skip_whitespace()
            return True
        return False

    def match_ch(self, ch: str, skip_whitespace: bool = True) -> bool:
        """
        Detect if next character on input matches an explicit character
        :param ch: expected character
        :param skip_whitespace: True if we must call skip_white
        :return: True if the input matches our expectation
        """
        return self.match(lambda look: look == ch, skip_whitespace)

    def expect_str(self, s: str, allow_whitespace: bool = False) -> None:
        """
        Expect a whole character sequence to be found on input
        :param allow_whitespace: set to True to allow white space between characters of the string
        :param s: Character sequence
        """
        for ch in s:
            if not self.match_ch(ch, skip_whitespace=allow_whitespace):
                self._raise_error_expected(s)
                return
        self.skip_whitespace()

    def expect_fn(self, fn, name: str) -> None:
        """
        Expect next input character to match our function.
        Raise an exception otherwise
        :param fn: Expectation as char->bool function
        :param name: Name of the expected token
        """
        if not self.match(fn):
            self._raise_error_expected(name)

    def expect_ch(self, ch: str) -> None:
        """
        Expect an exact character to be found on the input.
        Raise an exception otherwise
        :param ch: Expected character
        """
        self.expect_fn(lambda look: look == ch, ch)

    def skip_whitespace(self) -> None:
        """
        Skip whitespace characters on the input stream.
        Expected to be called after processing tokens.
        """
        while self.is_whitespace():
            self.get_char()

    def _raise_error_expected(self, name: str) -> None:
        """
        Raise an error that input didn't match our expectation
        :param name: Name of the expected token
        """
        raise TinyBasicSyntaxError(self.src, f'{name} expected, but {self.look} found')
