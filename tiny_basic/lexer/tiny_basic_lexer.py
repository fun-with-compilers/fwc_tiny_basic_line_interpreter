from .tiny_basic_tokens import TinyBasicTokenizer, TinyBasicToken
from .token_type import TinyBasicTokenType
from .syntax_error import TinyBasicSyntaxError


class TinyBasicLexerError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class TinyBasicLexer:
    def __init__(self, line: str):
        self.tokenizer = TinyBasicTokenizer(line)
        self.pos = self.tokenizer.pos
        self.look = self.read()
        self.has_line_number, self.line_number = self.read_on_match(TinyBasicTokenType.LINE_NUMBER)

    def read(self):
        return self.tokenizer.next()

    def next(self) -> TinyBasicToken:
        prev = self.look
        self.pos = self.tokenizer.pos
        self.look = self.read()
        return prev

    def match(self, token_type: TinyBasicTokenType, value=None) -> bool:
        is_match, value = self.read_on_match(token_type, value)
        return is_match

    def read_on_match(self, token_type: TinyBasicTokenType, value=None) -> tuple[bool, any]:
        if self.looks_like(token_type, value):
            return True, self.next().value
        return False, None

    def looks_like(self, token_type: TinyBasicTokenType, value=None) -> bool:
        if self.look.type == token_type:
            if value is None or self.look.value == value:
                return True
        return False

    def fail_unexpected_token(self, expected_token: str, expected_value=None):
        if expected_value is None:
            raise TinyBasicSyntaxError(self.tokenizer.src, f'{expected_token} expected, but {self.look.type} found')
        else:
            raise TinyBasicSyntaxError(
                f'{expected_token} "{expected_token}" expected, but {self.look.type} "{self.look.value}" found')

    def expect(self, token_type: TinyBasicTokenType, value=None):
        found, token_value = self.read_on_match(token_type, value)
        if found:
            return token_value
        self.fail_unexpected_token(str(token_type), value)

    def eof(self) -> bool:
        return self.look.type == TinyBasicTokenType.THE_END
