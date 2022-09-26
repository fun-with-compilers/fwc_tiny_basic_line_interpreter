from tiny_basic.lexer import TinyBasicLexer, TinyBasicTokenType
from tiny_basic.errors import TinyBasicException


class SourceText:
    def __init__(self):
        self.text = {}

    def reset(self):
        self.text = {}

    def delete_text(self, line_number: int):
        if line_number in self.text:
            self.text.pop(line_number)
        else:
            raise TinyBasicException(f'Line number not defined: {line_number}')

    def edit_text(self, lexer: TinyBasicLexer, line_number: int or None = None):
        if line_number is None:
            line_number = lexer.line_number
        if lexer.looks_like(TinyBasicTokenType.THE_END):
            self.delete_text(line_number)
        else:
            line = []
            while not lexer.looks_like(TinyBasicTokenType.THE_END):
                token = lexer.next().to_src()
                line.append(token)
            text = " ".join(line)
            self.text[line_number] = text

    def set_text(self, lines: list[str]):
        line_number = 0
        self.text = {}
        for line in lines:
            if len(line.strip()) == 0:
                continue
            lexer = TinyBasicLexer(line)
            if not lexer.has_line_number:
                line_number = line_number + 10
            else:
                line_number = lexer.line_number
            self.edit_text(lexer, line_number)

    def get_line_table(self) -> list[int]:
        return sorted(self.text.keys())

    def get_labels(self) -> dict[str, int]:
        result = {}
        for line_number in self.text:
            line = self.text[line_number]
            lexer = TinyBasicLexer(line)
            if lexer.looks_like(TinyBasicTokenType.COLON):
                lexer.match(TinyBasicTokenType.COLON)
                label = lexer.expect(TinyBasicTokenType.IDENTIFIER)
                result[label] = line_number
        return result

    def get_program_text(self, start: int or None = None, end: int or None = None) -> list[str]:
        line_tab = self.get_line_table()
        result = []
        for i in line_tab:
            if (start is None or start <= i) and (end is None or i <= end):
                result.append(f'{i} {self.text[i]}')
        return result
