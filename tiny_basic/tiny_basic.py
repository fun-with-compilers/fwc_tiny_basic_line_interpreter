from .builtin_functions import fn_mid, fn_rnd
from .errors import TinyBasicException, TinyBasicQuitException, TinyBasicRunStopException
from .lexer import TinyBasicLexer, TinyBasicStatement, TinyBasicTokenType, TinyBasicBoolOperator, TinyBasicKeyword
from .lexer.functions import TinyBasicFunction
from .vm import AbstractVM, Variable


class TinyBasicInterpreter(TinyBasicLexer):
    def __init__(self, vm: AbstractVM, line: str):
        super().__init__(line)
        self.line = line
        self.vm = vm
        self.statements = {
            TinyBasicStatement.DEBUG: self.stmt_debug,
            TinyBasicStatement.TRACE: self.stmt_trace,
            TinyBasicStatement.REM: self.stmt_rem,
            TinyBasicStatement.LET: self.stmt_let,
            TinyBasicStatement.DIM: self.stmt_dim,
            TinyBasicStatement.GOTO: self.stmt_goto,
            TinyBasicStatement.GOSUB: self.stmt_gosub,
            TinyBasicStatement.RET: self.stmt_ret,
            TinyBasicStatement.CLS: self.stmt_cls,
            TinyBasicStatement.PRINT: self.stmt_print,
            TinyBasicStatement.INPUT: self.stmt_input,
            TinyBasicStatement.NEW: self.stmt_new,
            TinyBasicStatement.LIST: self.stmt_list,
            TinyBasicStatement.READ: self.stmt_read,
            TinyBasicStatement.WRITE: self.stmt_write,
            TinyBasicStatement.LOAD: self.stmt_load,
            TinyBasicStatement.SAVE: self.stmt_save,
            TinyBasicStatement.END: self.stmt_end,
            TinyBasicStatement.QUIT: self.stmt_quit,
            TinyBasicStatement.RUN: self.stmt_run,
            TinyBasicStatement.RESET: self.stmt_reset,
            TinyBasicStatement.CONT: self.stmt_cont,
            TinyBasicStatement.IF: self.stmt_if,
            TinyBasicStatement.ON: self.stmt_on,
            TinyBasicStatement.FOR: self.stmt_for,
            TinyBasicStatement.NEXT: self.stmt_next
        }
        self.functions = {
            TinyBasicFunction.STR: (Variable.TYPE_STR, lambda x: str(x[0]), 1, 1, [Variable.TYPE_ANY]),
            TinyBasicFunction.INT: (Variable.TYPE_INT, lambda x: int(x[0]), 1, 1, [Variable.TYPE_ANY]),
            TinyBasicFunction.NUM: (Variable.TYPE_NUM, lambda x: float(x[0]), 1, 1, [Variable.TYPE_ANY]),
            TinyBasicFunction.LEN: (Variable.TYPE_INT, lambda x: len(x[0]), 1, 1, [Variable.TYPE_STR]),
            TinyBasicFunction.ALEN: (Variable.TYPE_INT, lambda x: x[0].dim, 1, 1, [None]),
            TinyBasicFunction.MID: (Variable.TYPE_STR, fn_mid, 2, 3, [Variable.TYPE_STR, Variable.TYPE_INT, Variable.TYPE_INT]),
            TinyBasicFunction.RND: (Variable.TYPE_INT, fn_rnd, 1, 2, [Variable.TYPE_INT, Variable.TYPE_INT])
        }

    def interpret(self):
        self.statement()
        self.expect(TinyBasicTokenType.THE_END)

    def statement(self):
        is_statement, statement = self.read_on_match(TinyBasicTokenType.STATEMENT)
        if is_statement:
            if statement not in self.statements:
                raise TinyBasicException(f'Illegal statement')
            func = self.statements[statement]
            func()
        elif self.looks_like(TinyBasicTokenType.IDENTIFIER):
            name = self.expect(TinyBasicTokenType.IDENTIFIER)
            if self.looks_like(TinyBasicTokenType.COLON):
                self.label(name)
            else:
                variable_name, index = self.variable(name)
                self.assignment(variable_name, index)
        else:
            self.fail_unexpected_token('STATEMENT')
        if self.match(TinyBasicTokenType.COLON):
            self.statement()

    def label(self, label_name: str):
        self.match(TinyBasicTokenType.COLON)
        if self.has_line_number:
            self.vm.variables.write_num_var(label_name, self.line_number)

    def stmt_debug(self):
        self.vm.debug()

    def stmt_trace(self):
        if self.match(TinyBasicTokenType.THE_END):
            trace_state = self.vm.context.trace
        else:
            trace_state = self.bool_expression()
            self.vm.context.trace = trace_state
        trace_state_text = 'ON' if trace_state else 'OFF'
        self.vm.io.print_msg(f'TRACE IS: {trace_state_text}')

    def stmt_run(self):
        self.vm.reset()
        self.vm.run()

    def stmt_cont(self):
        self.vm.run()

    def stmt_reset(self):
        self.vm.reset()

    def stmt_rem(self):
        comment = self.expect(TinyBasicTokenType.COMMENT)
        if self.vm.context.trace:
            self.vm.io.print_msg(f'COMMENT: "{comment}"')

    def stmt_quit(self):
        raise TinyBasicQuitException()

    def stmt_end(self):
        raise TinyBasicRunStopException()

    def stmt_new(self):
        self.vm.text.reset()

    def stmt_list(self):
        start = None
        end = None
        if self.looks_like(TinyBasicTokenType.LITERAL):
            has_start, start = self.read_on_match(TinyBasicTokenType.LITERAL)
        elif self.looks_like(TinyBasicTokenType.IDENTIFIER):
            has_start = True
            start = self.int_expression()
        else:
            has_start = False
        if has_start:
            if self.looks_like(TinyBasicTokenType.COMMA):
                self.expect(TinyBasicTokenType.COMMA)
                end = self.int_expression()
        for line in self.vm.text.get_program_text(start, end):
            self.vm.io.print_msg(line)
        self.vm.io.print_msg("DONE")

    def stmt_load(self):
        file_name = self.str_expression()
        with open(file_name) as f:
            lines = f.readlines()
        self.vm.text.set_text(lines)
        self.vm.io.print_msg(f'PROGRAM LOADED: {file_name}, {len(lines)} LINES')

    def stmt_save(self):
        file_name = self.str_expression()
        with open(file_name, 'wt') as f:
            for line in self.vm.text.get_program_text():
                f.write(line)
                f.write('\n')
        self.vm.io.print_msg(f'PROGRAM STORED INTO {file_name}')

    def stmt_read(self):
        variable_name = self.expect(TinyBasicTokenType.IDENTIFIER)
        self.expect(TinyBasicTokenType.COMMA)
        file_name = self.str_expression()
        with open(file_name) as f:
            lines = f.readlines()
        lines = [line.rstrip() for line in lines]
        self.vm.variables.write_str_array(variable_name, lines)

    def stmt_write(self):
        variable_name = self.expect(TinyBasicTokenType.IDENTIFIER)
        dim = self.vm.variables.get_dim(variable_name)
        self.expect(TinyBasicTokenType.COMMA)
        file_name = self.str_expression()
        with open(file_name, 'w') as f:
            for i in range(0, dim):
                value = self.vm.variables.read_str_var(variable_name, i)
                f.write(value)

    def stmt_goto(self):
        line_number = self.int_expression()
        self.jump_to(line_number)

    # noinspection SpellCheckingInspection
    def stmt_gosub(self):
        line_number = self.int_expression()
        self.vm.context.stack.append(self.vm.context.ip_next)
        self.jump_to(line_number)

    def stmt_ret(self):
        if 0 == len(self.vm.context.stack):
            raise TinyBasicException('STACK IS EMPTY')
        line_number = self.vm.context.stack.pop()
        if (not isinstance(line_number, int)) or (line_number < 0) or (len(self.vm.context.line_tab) <= line_number):
            raise TinyBasicException('STACK TOP IS NOT A VALID IP')
        self.vm.context.ip_next = line_number

    def stmt_cls(self):
        self.vm.io.clear_screen()

    def stmt_print(self):
        message = ""
        sep = True
        new_line = False
        while sep:
            new_line = True
            sep = False
            part = self.expression()
            message += str(part)
            if self.match(TinyBasicTokenType.COMMA):
                new_line = False
                sep = not (self.looks_like(TinyBasicTokenType.COLON) or self.looks_like(TinyBasicTokenType.THE_END))
            elif self.match(TinyBasicTokenType.SEMICOLON):
                new_line = False
                sep = not (self.looks_like(TinyBasicTokenType.COLON) or self.looks_like(TinyBasicTokenType.THE_END))
                message += ' '
        self.vm.io.print_msg(message, new_line)

    def stmt_input(self):
        message = self.str_expression()
        if self.match(TinyBasicTokenType.SEMICOLON):
            message += '?'
        else:
            self.expect(TinyBasicTokenType.COMMA)
        variable_name, index = self.variable()
        if variable_name.endswith('$'):
            result = self.vm.io.input_str(message)
            self.vm.variables.write_str_var(variable_name, result, index)
        else:
            result = self.vm.io.input_int(message)
            self.vm.variables.write_num_var(variable_name, result, index)

    def stmt_let(self):
        variable_name, index = self.variable()
        self.assignment(variable_name, index)

    def stmt_dim(self):
        while True:
            variable_name = self.expect(TinyBasicTokenType.IDENTIFIER)
            self.expect(TinyBasicTokenType.PARENS_OPEN)
            dim = self.expression()
            self.expect(TinyBasicTokenType.PARENS_CLOSE)
            self.vm.variables.dim(variable_name, dim)
            if not self.match(TinyBasicTokenType.COMMA):
                break

    def assignment(self, variable_name: str, index: int = 0):
        self.expect(TinyBasicTokenType.EQ_OPERATOR)
        if self.is_str_variable_name(variable_name):
            self.vm.variables.write_str_var(variable_name, self.str_expression(), index)
        else:
            self.vm.variables.write_num_var(variable_name, self.num_expression(), index)

    def stmt_for(self):
        variable_name, index = self.int_variable_name()
        self.expect(TinyBasicTokenType.EQ_OPERATOR)
        init_value = self.int_expression()
        self.expect(TinyBasicTokenType.KEYWORD, TinyBasicKeyword.TO)
        max_value = self.int_expression()
        if self.match(TinyBasicTokenType.KEYWORD, TinyBasicKeyword.STEP):
            step = self.int_expression()
        else:
            step = 1
        if self.match(TinyBasicTokenType.COLON):
            self.do_loop(variable_name, index, init_value, max_value, step)
        else:
            loop = (variable_name, self.vm.context.ip_next, max_value, step, index)
            self.vm.context.stack.append(loop)
            self.vm.variables.write_num_var(variable_name, init_value, index)

    def do_loop(self, variable_name, index, init, max_value, step):
        value = init
        while value <= max_value:
            self.vm.variables.write_num_var(variable_name, value, index)
            sub_interpreter = TinyBasicInterpreter(self.vm, self.line[self.pos:])
            sub_interpreter.interpret()
            value += step

    def stmt_next(self):
        if 0 == len(self.vm.context.stack):
            raise TinyBasicException('Stack is empty, can\'t next')
        has_variable, loop_variable = self.read_on_match(TinyBasicTokenType.IDENTIFIER)
        while True:
            if 0 == len(self.vm.context.stack):
                if loop_variable is not None:
                    raise TinyBasicException(f'Stack underflow while looking for {loop_variable}')
                raise TinyBasicException(f'Stack underflow')
            loop = self.vm.context.stack.pop()
            if 5 != len(loop):
                raise TinyBasicException('Stack error')
            variable_name = loop[0]
            if not self.is_int_variable_name(variable_name):
                self.fail_unexpected_token('INTEGER VARIABLE')
            if loop_variable is None or variable_name == loop_variable:
                break
        loop_start = loop[1]
        limit = loop[2]
        step = loop[3]
        index = loop[4]
        value = self.vm.variables.read_num_var(variable_name, index) + step
        if value <= limit:
            self.vm.variables.write_num_var(variable_name, value, index)
            self.vm.context.ip_next = loop_start
            self.vm.context.stack.append(loop)

    def stmt_if(self):
        if self.bool_expression():
            if self.match(TinyBasicTokenType.STATEMENT, TinyBasicStatement.GOTO) or \
                    self.looks_like(TinyBasicTokenType.LITERAL):
                self.stmt_goto()
            else:
                self.expect(TinyBasicTokenType.KEYWORD, TinyBasicKeyword.THEN)
                self.statement()
        else:
            while not self.looks_like(TinyBasicTokenType.THE_END):
                self.next()

    def stmt_on(self):
        condition = self.expression()
        self.expect(TinyBasicTokenType.GOTO)
        if self.expr_to_bool(condition):
            line_number = self.int_expression()
            self.jump_to(line_number)
        pass

    def jump_to(self, line_number: int):
        ip = self.vm.context.line_tab.index(line_number)
        if 0 <= ip:
            self.vm.context.ip_next = ip
        else:
            raise TinyBasicException(f'Line number not found: {line_number}')

    def variable(self, variable_name: str or None = None) -> tuple[str, int]:
        if variable_name is None:
            variable_name = self.expect(TinyBasicTokenType.IDENTIFIER)
        index = self.indexer()
        return variable_name, index

    def int_variable_name(self) -> tuple[str, int]:
        name, index = self.variable()
        if not self.is_int_variable_name(name):
            self.fail_unexpected_token('INTEGER VARIABLE')
        return name, index

    def is_str_variable_name(self, variable_name: str) -> bool:
        return variable_name.endswith('$')

    def is_int_variable_name(self, variable_name: str) -> bool:
        return not self.is_str_variable_name(variable_name)

    def indexer(self) -> int:
        if not self.match(TinyBasicTokenType.PARENS_OPEN):
            return 0
        index = self.int_expression()
        self.expect(TinyBasicTokenType.PARENS_CLOSE)
        return index

    def expect_int(self, value) -> int:
        if not isinstance(value, int):
            self.fail_unexpected_token('INTEGER EXPRESSION')
        return value

    def bool_expression(self) -> bool:
        return self.expr_to_bool(self.expression())

    def int_expression(self) -> int:
        return self.expect_int(self.expression())

    def num_expression(self) -> int or float:
        result = self.expression()
        if not (isinstance(result, int) or isinstance(result, float)):
            self.fail_unexpected_token('NUMERIC EXPRESSION')
        return result

    def str_expression(self) -> str:
        result = self.expression()
        if not isinstance(result, str):
            self.fail_unexpected_token('STRING EXPRESSION')
        return result

    def expression(self):
        return self.or_expression()

    def or_expression(self):
        left = self.and_expression()
        while self.match(TinyBasicTokenType.BOOL_OPERATOR, TinyBasicBoolOperator.OR):
            right = self.and_expression()
            left = self.expr_to_bool(left) or right
        return left

    def and_expression(self):
        left = self.xor_expression()
        while self.match(TinyBasicTokenType.BOOL_OPERATOR, TinyBasicBoolOperator.AND):
            right = self.xor_expression()
            left = self.expr_to_bool(left) and right
        return left

    def xor_expression(self):
        left = self.bool_term()
        while self.match(TinyBasicTokenType.BOOL_OPERATOR, TinyBasicBoolOperator.XOR):
            right = self.bool_term()
            left = self.expr_to_bool(left) ^ right
        return left

    def bool_term(self):
        if self.match(TinyBasicTokenType.BOOL_OPERATOR, TinyBasicBoolOperator.NOT):
            return not self.bool_expression()
        return self.comparison()

    def expr_to_bool(self, value) -> bool:
        return self.expect_int(value) != 0

    def comparison(self):
        left = self.arithmetic_expression()
        is_eq, eq_op = self.read_on_match(TinyBasicTokenType.EQ_OPERATOR)
        if is_eq:
            right = self.arithmetic_expression()
            if eq_op == '=':
                return left == right
            self.fail_unexpected_token('EQUALITY OPERATOR')
        is_cmp, cmp_op = self.read_on_match(TinyBasicTokenType.COMPARISON_OPERATOR)
        if is_cmp:
            right = self.arithmetic_expression()
            if cmp_op == '<>':
                return left != right
            if cmp_op == '<':
                return left < right
            if cmp_op == '<=':
                return left <= right
            if cmp_op == '>':
                return left > right
            if cmp_op == '>=':
                return left >= right
            self.fail_unexpected_token('COMPARATOR')
        return left

    def arithmetic_expression(self):
        left = self.term()
        while self.looks_like(TinyBasicTokenType.ADD_OP):
            if self.match(TinyBasicTokenType.ADD_OP, '+'):
                right = self.term()
                left += right
            if self.match(TinyBasicTokenType.ADD_OP, '-'):
                right = self.term()
                left -= right
        return left

    def term(self):
        left = self.factor()
        while self.looks_like(TinyBasicTokenType.MUL_OP):
            if self.match(TinyBasicTokenType.MUL_OP, '*'):
                right = self.factor()
                left *= right
            if self.match(TinyBasicTokenType.MUL_OP, '/'):
                right = self.factor()
                if isinstance(left, int) and isinstance(right, int):
                    left //= right
                else:
                    left /= right
            if self.match(TinyBasicTokenType.MUL_OP, 'DIV'):
                right = self.factor()
                left //= right
            if self.match(TinyBasicTokenType.MUL_OP, 'MOD'):
                right = self.factor()
                left %= right
        return left

    def factor(self):
        result = None
        negate = False
        if self.match(TinyBasicTokenType.ADD_OP):
            negate = True
        elif self.match(TinyBasicTokenType.ADD_OP, '+'):
            negate = False
        elif self.match(TinyBasicTokenType.PARENS_OPEN):
            result = self.expression()
            self.expect(TinyBasicTokenType.PARENS_CLOSE)
        elif self.looks_like(TinyBasicTokenType.LITERAL) or self.looks_like(TinyBasicTokenType.STRING_LITERAL):
            result = self.next().value
        elif self.looks_like(TinyBasicTokenType.IDENTIFIER):
            variable_name, index = self.variable()
            result = self.vm.variables.read_var(variable_name, index)
        elif self.looks_like(TinyBasicTokenType.FUNCTION):
            result = self.function()
        else:
            self.expect(TinyBasicTokenType.LITERAL)
        if negate:
            result = -result
        return result

    def function(self):
        function_name = self.expect(TinyBasicTokenType.FUNCTION)
        if function_name not in self.functions:
            raise TinyBasicException(f'UNKNOWN FUNCTION: {function_name}')
        function_def = self.functions[function_name]
        ret, fn, min_args, max_args, arg_types = function_def
        self.expect(TinyBasicTokenType.PARENS_OPEN)
        args = []
        while not self.looks_like(TinyBasicTokenType.PARENS_CLOSE):
            index = len(args)
            if arg_types[index] == Variable.TYPE_STR:
                args.append(self.str_expression())
            elif arg_types[index] == Variable.TYPE_INT:
                args.append(self.int_expression())
            elif arg_types[index] == Variable.TYPE_NUM:
                args.append(self.num_expression())
            elif arg_types[index] == Variable.TYPE_ANY:
                args.append(self.expression())
            elif arg_types[index] is None:
                variable_name = self.expect(TinyBasicTokenType.IDENTIFIER)
                var = self.vm.variables.access_var(variable_name)
                args.append(var)
            else:
                raise TinyBasicException(f'UNKNOWN ARGUMENT')
            if not self.looks_like(TinyBasicTokenType.PARENS_CLOSE):
                self.expect(TinyBasicTokenType.COMMA)
        if max_args is not None and max_args < len(args):
            raise TinyBasicException(f'TOO MUCH ARGUMENTS FOR {function_name}')
        if len(args) < min_args:
            raise TinyBasicException(f'TOO FEW ARGUMENTS FOR {function_name}')
        result = fn(args)
        self.expect(TinyBasicTokenType.PARENS_CLOSE)
        return result
