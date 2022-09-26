from enum import unique, Enum, auto


@unique
class TinyBasicTokenType(Enum):
    LINE_NUMBER = auto(),
    STATEMENT = auto(),
    KEYWORD = auto(),
    FUNCTION = auto(),
    COMMENT = auto(),
    IDENTIFIER = auto(),
    LITERAL = auto(),
    STRING_LITERAL = auto(),
    EQ_OPERATOR = auto(),
    MUL_OP = auto(),
    ADD_OP = auto(),
    BOOL_OPERATOR = auto(),
    COMPARISON_OPERATOR = auto(),
    COMMA = auto(),
    COLON = auto(),
    SEMICOLON = auto(),
    PARENS_OPEN = auto(),
    PARENS_CLOSE = auto(),
    SQUARE_BRACKETS_OPEN = auto(),
    SQUARE_BRACKETS_CLOSE = auto(),
    THE_END = auto()
