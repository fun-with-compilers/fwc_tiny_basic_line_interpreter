from .errors import TinyBasicException, TinyBasicQuitException
from .interpreter_vm import TinyInterpreterVM
from .tiny_basic import TinyBasicInterpreter
from .lexer.syntax_error import TinyBasicSyntaxError
from .tiny_basic_io import TinyConsoleIo


def exec_line(vm: TinyInterpreterVM, line: str):
    if 0 == len(line):
        return
    interpreter = TinyBasicInterpreter(vm, line)
    if interpreter.line_number is not None:
        vm.text.edit_text(interpreter, line_number=interpreter.line_number)
    else:
        interpreter.interpret()


def run_tiny_basic_program(filename: str, io = TinyConsoleIo()):
    vm = TinyInterpreterVM(io)
    vm.execute(f'LOAD "{filename}"')
    vm.execute('RUN')


def run_tiny_basic(io = TinyConsoleIo()):
    io.print_msg('TinyBasic Interpreter v1.00')
    io.print_msg('Copyright (c) 1985-2022. Ákos Nagy')

    vm = TinyInterpreterVM(io)

    io.print_msg("READY")
    while True:
        io.print_msg("")
        command = io.input_str()
        try:
            exec_line(vm, command)
        except TinyBasicQuitException:
            io.print_msg('GOOD BYE!')
            break
        except TinyBasicSyntaxError as e:
            io.print_msg(f'SYNTAX ERROR: {e.msg}@{e.pos}')
        except TinyBasicException as e:
            io.print_msg(f'BASIC ERROR: {e.msg}@{vm.context.ip}')
            vm.dump_line_info()
        except Exception as e:
            io.print_msg(f'FATAL ERROR: {e}')
            vm.dump_line_info()
