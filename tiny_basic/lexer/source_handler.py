class SourceHandler:
    """
    SourceHandler class provides common interface for reading source code
    """

    def __init__(self):
        """
        Constructor sets line and column to default
        """
        self.line = 1
        self.pos = 0

    def _read(self) -> str:
        """
        Read the next character from the input.
        Should be overridden by subclasses
        :return: The next character on input
        """
        return ""

    def get_char(self) -> str:
        """
        Public interface to read the next character from the input.
        Uses _read() for reading, but also handles end of file and updates the position for proper error reporting
        :return: The next character on input
        """
        if self.eof():
            return ""
        result = self._read()
        self.pos += 1
        if result == '\n':
            self.line += 1
            self.pos = 0
        return result

    def eof(self) -> bool:
        """
        :return: True when we reached EOF (end of input/file)
        """
        return True


class StringSourceHandler(SourceHandler):
    """
    A source handler that operates on a string
    """
    def __init__(self, source: str):
        """
        Constructor
        :param source: Source code as string
        """
        super().__init__()
        self.source = source
        self.at_end = 0 == len(source)

    def _read(self) -> str:
        if 0 < len(self.source):
            result = self.source[0]
            self.source = self.source[1:]
            return result
        self.at_end = True
        return ""

    def eof(self) -> bool:
        return self.at_end


def source_from_string(source: str) -> SourceHandler:
    """
    Factory method to construct source handler from string
    :param source: source code as string
    :return: SourceHandler interface
    """
    return StringSourceHandler(source)