from typing import Optional, Tuple, Any

from ..errors import TinyBasicException
from . import Context, AbstractIo, SourceText, VariableStorage

class AbstractVM:
    def __init__(self, io: AbstractIo):
        self.text = SourceText()
        self.variables = VariableStorage()
        self.context = Context(self.text)
        self.io = io

    def reset(self):
        self.variables.reset()
        labels = self.text.get_labels()
        for label in labels:
            self.variables.write_num_var(label, labels[label])
        self.context.reset(self.text.get_line_table())

    def execute(self, line: str) -> int or None:
        raise TinyBasicException("Abstract VM has no function to execute instructions")

    def step(self):
        if not self.context.step(self.execute):
            self.io.print_msg(f'PROGRAM TERMINATED')

    def run(self):
        self.context.run(self.execute)
        self.io.print_msg("DONE.")

    def get_line_for_ip(self, ip: int) -> tuple[int or None, str or None]:
        if 0 <= ip < self.context.get_max_ip():
            line_number = self.context.line_tab[ip]
            return line_number, str(self.text.text[line_number])
        return None, None

    def dump_line_info(self, ip: int or None = None, prefix: str = ""):
        if ip is None:
            ip = self.context.ip
        line_number, line = self.get_line_for_ip(ip)
        if line_number is not None:
            self.io.print_msg(f'{prefix}IP={ip}@{line_number}')
        if line is not None:
            self.io.print_msg(f'{prefix}LINE: {line}')

    def get_current_line(self):
        return self.get_line_for_ip(self.context.ip)

    def debug(self):
        self.dump_line_info(self.context.ip)
        self.dump_line_info(self.context.ip_next, "NEXT ")
        self.io.print_msg(f'STACK ({len(self.context.stack)} entries): ')
        for entry in self.context.stack:
            self.io.print_msg(f'   {entry}')
