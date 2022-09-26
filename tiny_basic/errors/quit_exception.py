from tiny_basic.errors.tiny_basic_exception import TinyBasicException


class TinyBasicQuitException(TinyBasicException):
    def __init__(self):
        super().__init__("GOOD BYE")
