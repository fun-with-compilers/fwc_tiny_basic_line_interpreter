from .tiny_basic import TinyBasicInterpreter
from .vm import AbstractVM, AbstractIo


class TinyInterpreterVM(AbstractVM):
    def __init__(self, io: AbstractIo):
        super().__init__(io)

    def execute(self, line: str):
        interpreter = TinyBasicInterpreter(self, line)
        interpreter.interpret()
