from .source_handler import SourceHandler
from tiny_basic.errors import TinyBasicException


class TinyBasicSyntaxError(TinyBasicException):
    """
    Syntax error exception
    """
    def __init__(self, src: SourceHandler, msg: str):
        """
        Constructor to initialize exception with source handler, so we can provide location information
        :param src: Source handler
        :param msg: Error message
        """
        super().__init__(msg)
        self.line = src.line
        self.pos = src.pos

    def __str__(self):
        return f'ERROR at {self.line}:{self.pos}: {self.msg}'
