from tiny_basic.errors import TinyBasicException
from . import Variable


class VariableStorage:
    def __init__(self):
        self.variables: dict[str, Variable] = {}

    def reset(self):
        self.variables.clear()

    def access_var(self, variable_name: str) -> Variable:
        variable_name = variable_name.upper()
        if variable_name not in self.variables:
            raise TinyBasicException(f'Undefined variable: {variable_name}')
        return self.variables[variable_name]

    def write_var(self, variable_name: str, base_type: str, must_exist: bool = False) -> Variable:
        variable_name = variable_name.upper()
        if variable_name not in self.variables:
            if must_exist:
                raise TinyBasicException(f'Undefined variable: {variable_name}')
            self.dim(variable_name, 1, base_type)
        var = self.variables[variable_name]
        if base_type != var.base_type:
            raise TinyBasicException(f'TYPE MISMATCH, EXPECTED: {base_type}, GOT: {var.base_type} OF {variable_name}')
        return var

    def dim(self, variable_name: str, dim: int, base_type: str or None = None):
        variable_name = variable_name.upper()
        if base_type is None:
            if variable_name.endswith('$'):
                base_type = Variable.TYPE_STR
            else:
                base_type = Variable.TYPE_NUM
        var = Variable(variable_name, base_type, dim)
        self.variables[variable_name] = var

    def get_dim(self, variable_name) -> int:
        var = self.access_var(variable_name)
        return var.dim

    def read_var(self, variable_name: str, index: int = 0) -> str or int or float:
        return self.access_var(variable_name).read(index)

    def read_num_var(self, variable_name: str, index: int = 0) -> int or float:
        return self.access_var(variable_name).read_num(index)

    def read_str_var(self, variable_name: str, index: int = 0) -> str:
        return self.access_var(variable_name).read_str(index)

    def write_num_var(self, variable_name: str, value: int or float, index: int = 0):
        self.write_var(variable_name, Variable.TYPE_NUM, index != 0).write_num(value, index)

    def write_str_var(self, variable_name: str, value: str, index: int = 0):
        self.write_var(variable_name, Variable.TYPE_STR, index != 0).write_str(value, index)

    def write_str_array(self, variable_name: str, value: list[str]):
        self.write_var(variable_name, Variable.TYPE_STR, False).write_str_array(value)
