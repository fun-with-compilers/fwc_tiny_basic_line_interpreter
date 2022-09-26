class AbstractIo:
    def input_int(self, message: str) -> int:
        return int(self.input_str(message))

    def input_str(self, message: str) -> str:
        return ""

    def print_msg(self, message: str, new_line: bool = True):
        pass

    def clear_screen(self):
        pass