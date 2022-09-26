import os

from .vm.io import AbstractIo


class TinyConsoleIo(AbstractIo):
    def input_str(self, message: str or None = None) -> str:
        if message is None:
            return input('? ')
        else:
            return input(message)

    def print_msg(self, message: str, new_line: bool = True):
        if new_line:
            print(message)
        else:
            print(message, end='')

    def clear_screen(self):
        command = 'cls' if os.name == 'nt' else 'clear'
        os.system(command)