from tiny_basic.errors import TinyBasicRunStopException
from . import SourceText


class Context:
    def __init__(self, text: SourceText):
        self.text = text
        self.ip = 0
        self.ip_next = 1
        self.stack = []
        self.line_tab = []
        self.trace = False

    def reset(self, line_tab: list):
        self.line_tab = line_tab
        self.ip = 0
        self.stack = []

    def get_max_ip(self):
        return len(self.line_tab)

    def step(self, fn_execute) -> bool:
        if 0 <= self.ip < len(self.line_tab):
            line_number = self.line_tab[self.ip]
            line = self.text.text[line_number]
            self.ip_next = self.ip + 1
            fn_execute(line)
            self.ip = self.ip_next
            return True
        else:
            return False

    def run(self, fn_execute):
        while self.ip < len(self.line_tab):
            try:
                self.step(fn_execute)
                if self.trace:
                    return
            except TinyBasicRunStopException:
                break
