from enum import Enum, unique, auto

from .abstract_lexer import AbstractLexer
from .functions import TinyBasicFunction
from .source_handler import source_from_string
from .token_type import TinyBasicTokenType
from .statements import TinyBasicStatement
from .keywords import TinyBasicKeyword
from .operators import TinyBasicBoolOperator
from ..errors import TinyBasicException


@unique
class TinyBasicLineState(Enum):
    START = auto(),
    STATEMENT_BEGIN = auto()
    STATEMENT = auto(),
    COMMENT = auto(),
    END = auto()


class TinyBasicToken:
    def __init__(self, type: TinyBasicTokenType, val=None, pos=None):
        self.type = type
        self.value = val
        self.pos = pos

    def to_src(self) -> str:
        if self.value is None:
            return str(self.type.value)
        if self.type == TinyBasicTokenType.STATEMENT:
            statement: TinyBasicStatement = self.value
            return str(statement.value)
        if self.type == TinyBasicTokenType.COMMA:
            return ','
        if self.type == TinyBasicTokenType.COLON:
            return ':'
        if self.type == TinyBasicTokenType.SEMICOLON:
            return ';'
        if self.type == TinyBasicTokenType.PARENS_OPEN:
            return '('
        if self.type == TinyBasicTokenType.PARENS_CLOSE:
            return ')'
        if self.type == TinyBasicTokenType.KEYWORD:
            keyword: TinyBasicKeyword = self.value
            return str(keyword.value)
        if self.type == TinyBasicTokenType.FUNCTION:
            keyword: TinyBasicFunction = self.value
            return str(keyword.value)
        if self.type == TinyBasicTokenType.IDENTIFIER:
            return self.value
        if self.type == TinyBasicTokenType.COMMENT:
            return self.value
        if self.type == TinyBasicTokenType.STRING_LITERAL:
            return f'"{self.value}"'
        if self.type == TinyBasicTokenType.LITERAL:
            return str(self.value)
        if self.type == TinyBasicTokenType.ADD_OP \
                or self.type == TinyBasicTokenType.MUL_OP \
                or self.type == TinyBasicTokenType.EQ_OPERATOR \
                or self.type == TinyBasicTokenType.COMPARISON_OPERATOR:
            return self.value
        if self.type == TinyBasicTokenType.BOOL_OPERATOR:
            bool_op: TinyBasicBoolOperator = self.value
            return str(bool_op.value)
        if self.type == TinyBasicTokenType.SQUARE_BRACKETS_OPEN:
            return '['
        if self.type == TinyBasicTokenType.SQUARE_BRACKETS_CLOSE:
            return ']'
        if self.type == TinyBasicTokenType.LINE_NUMBER:
            return str(self.value)

        return str(self.value)

    def __str__(self):
        if self.value is not None:
            return f'{str(self.type)}::"{self.value}"'
        else:
            return f'{str(self.type)}'


def is_in_enum(value, enum):
    attr_name = 'value_list'
    values = getattr(enum, attr_name) if hasattr(enum, attr_name) else None
    if values is None:
        values = [member.value for member in enum]
        setattr(enum, attr_name, values)
    return value in values


class TinyBasicTokenizer(AbstractLexer):
    def __init__(self, line: str):
        self.is_comment = False
        src = source_from_string(line)
        super(TinyBasicTokenizer, self).__init__(src)
        self.skip_whitespace()
        self.pos = 0
        self.state = TinyBasicLineState.START
        self.states = {
            TinyBasicLineState.START: self.next_start,
            TinyBasicLineState.COMMENT: self.next_comment,
            TinyBasicLineState.STATEMENT: self.next_statement,
            TinyBasicLineState.END: self.next_end
        }

    def next(self) -> TinyBasicToken:
        if self.src.eof():
            return TinyBasicToken(TinyBasicTokenType.THE_END)
        if self.state not in self.states:
            raise TinyBasicException(f'Invalid parser state: {self.state}')
        self.pos = self.src.pos
        next_state, result = self.states[self.state]()
        self.state = next_state
        if result is None:
            return self.next()
        return result

    def next_start(self) -> tuple[TinyBasicLineState, TinyBasicToken or None]:
        if self.is_digit():
            line_number = self.read_number()
            return TinyBasicLineState.STATEMENT, TinyBasicToken(TinyBasicTokenType.LINE_NUMBER, line_number)
        return TinyBasicLineState.STATEMENT, None

    def next_end(self) -> tuple[TinyBasicLineState, TinyBasicToken or None]:
        if not self.src.eof():
            self._raise_error_expected('END OF LINE')
        return TinyBasicLineState.END, TinyBasicToken(TinyBasicTokenType.THE_END)

    def next_statement_token(self) -> TinyBasicToken or None:
        if self.match_ch(':'):
            return TinyBasicToken(TinyBasicTokenType.COLON, ':')
        if self.match_ch(','):
            return TinyBasicToken(TinyBasicTokenType.COMMA, ',')
        if self.match_ch(';'):
            return TinyBasicToken(TinyBasicTokenType.SEMICOLON, ';')
        if self.match_ch('+'):
            return TinyBasicToken(TinyBasicTokenType.ADD_OP, '+')
        if self.match_ch('-'):
            return TinyBasicToken(TinyBasicTokenType.ADD_OP, '-')
        if self.match_ch('*'):
            return TinyBasicToken(TinyBasicTokenType.MUL_OP, '*')
        if self.match_ch('/'):
            return TinyBasicToken(TinyBasicTokenType.MUL_OP, '/')
        if self.match_ch('='):
            return TinyBasicToken(TinyBasicTokenType.EQ_OPERATOR, '=')
        if self.match_ch('('):
            return TinyBasicToken(TinyBasicTokenType.PARENS_OPEN, '(')
        if self.match_ch(')'):
            return TinyBasicToken(TinyBasicTokenType.PARENS_CLOSE, ')')
        if self.match_ch('['):
            return TinyBasicToken(TinyBasicTokenType.SQUARE_BRACKETS_OPEN, '[')
        if self.match_ch(']'):
            return TinyBasicToken(TinyBasicTokenType.SQUARE_BRACKETS_CLOSE, ']')
        if self.match_ch('<'):
            if self.match_ch('='):
                return TinyBasicToken(TinyBasicTokenType.COMPARISON_OPERATOR, '<=')
            if self.match_ch('>'):
                return TinyBasicToken(TinyBasicTokenType.COMPARISON_OPERATOR, '<>')
            return TinyBasicToken(TinyBasicTokenType.COMPARISON_OPERATOR, '<')
        if self.match_ch('>'):
            if self.match_ch('='):
                return TinyBasicToken(TinyBasicTokenType.COMPARISON_OPERATOR, '>=')
            return TinyBasicToken(TinyBasicTokenType.COMPARISON_OPERATOR, '>')
        if self.is_digit():
            return TinyBasicToken(TinyBasicTokenType.LITERAL, self.read_number())
        if self.match_ch('"', skip_whitespace=False):
            result = TinyBasicToken(TinyBasicTokenType.STRING_LITERAL, self.read_until(lambda ch: ch != '"'))
            self.expect_ch('"')
            return result
        if self.is_alpha():
            return self.identifier()
        return None

    def next_statement(self) -> tuple[TinyBasicLineState, TinyBasicToken or None]:
        result = self.next_statement_token()
        if result is None:
            self._raise_error_expected('STATEMENT')
        elif result.type == TinyBasicTokenType.STATEMENT and result.value == TinyBasicStatement.REM:
            return TinyBasicLineState.COMMENT, result
        if self.src.eof():
            return TinyBasicLineState.END, result
        return TinyBasicLineState.STATEMENT, result

    def next_comment(self) -> tuple[TinyBasicLineState, TinyBasicToken or None]:
        comment = self.read_until(lambda x: not self.src.eof())
        self.state = TinyBasicLineState.END
        return TinyBasicLineState.END, TinyBasicToken(TinyBasicTokenType.COMMENT, comment)

    def identifier(self) -> TinyBasicToken:
        if not self.is_alpha():
            self._raise_error_expected('Identifier')
        name = self.read_identifier()
        if self.match_ch('$'):
            name = name + '$'
        upper_name = name.upper()
        if is_in_enum(upper_name, TinyBasicStatement):
            return TinyBasicToken(TinyBasicTokenType.STATEMENT, TinyBasicStatement(upper_name))
        if is_in_enum(upper_name,TinyBasicBoolOperator):
            return TinyBasicToken(TinyBasicTokenType.BOOL_OPERATOR, TinyBasicBoolOperator(upper_name))
        if is_in_enum(upper_name, TinyBasicKeyword):
            return TinyBasicToken(TinyBasicTokenType.KEYWORD, TinyBasicKeyword(upper_name))
        if is_in_enum(upper_name, TinyBasicFunction):
            return TinyBasicToken(TinyBasicTokenType.FUNCTION, TinyBasicFunction(upper_name))
        if upper_name == "DIV":
            return TinyBasicToken(TinyBasicTokenType.MUL_OP, "DIV")
        if upper_name == "MOD":
            return TinyBasicToken(TinyBasicTokenType.MUL_OP, "MOD")
        return TinyBasicToken(TinyBasicTokenType.IDENTIFIER, name)
