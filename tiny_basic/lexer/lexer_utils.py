def is_alpha(look: str) -> bool:
    """
    Check if input is a letter
    :param look: input character
    :return: True when input is a letter (a..z, A..Z, underscore)
    """
    assert len(look) <= 1
    return 'a' <= look <= 'z' or 'A' <= look <= 'Z' or look == '_'


def is_digit(look: str) -> bool:
    """
    Check if input is a numeric digit character
    :param look: input character
    :return: True when input is a numeric digit character (0..9)
    """
    assert len(look) <= 1
    return '0' <= look <= '9'


def is_whitespace(look: str) -> bool:
    """
    Check if input is a white space character
    :param look: input character
    :return: True when input is a white space character (new line, space, tabulator)
    """
    assert len(look) <= 1
    return look == ' ' or look == '\t' or look == '\n' or look == '\r'


