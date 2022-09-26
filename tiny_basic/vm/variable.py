from tiny_basic.errors import TinyBasicException


class Variable:
    TYPE_STR = 'STRING'
    TYPE_NUM = 'NUM'
    TYPE_INT = 'INT'
    TYPE_ANY = ''

    def __init__(self, name: str, base_type: str, dim: int = 1, value = None):
        self.base_type = base_type
        self.dim = dim
        self.name = name
        if self.base_type == Variable.TYPE_STR and not name.endswith('$'):
            raise TinyBasicException(f'STRING VAR MUST END WITH $ {name}')
        if self.base_type == Variable.TYPE_NUM and name.endswith('$'):
            raise TinyBasicException(f'NUMERIC VAR MUST NOT END WITH $ {name}')
        if dim < 0:
            raise TinyBasicException(f'DIM should be a positive number, not {dim} for {name}')
        if value is None:
            self.value = []
            for i in range(0, dim):
                self.value.append(None)
        else:
            if len(value) != dim:
                raise TinyBasicException(f'Wrong init value for {name}')
            self.value = value

    def get_type(self):
        if self.dim == 1:
            return self.base_type
        else:
            return f'{self.base_type}[{self.dim}]'

    def verify_index(self, index: int):
        if (not 0 <= index < self.dim) or self.value is None:
            raise TinyBasicException(f'{index} IS OUT OF BOUNDS FOR {self.name}: 0..{self.dim}')

    def read(self, index: int, type: str or None = None):
        if type is not None and self.base_type != type:
            raise TinyBasicException(f'{self.name} IS NOT {type}')
        self.verify_index(index)
        result = self.value[index]
        if result is None:
            raise TinyBasicException(f'{self.name}[{index}] IS NOT YET ASSIGNED')
        return result

    def write(self, index: int, value):
        self.verify_index(index)
        self.value[index] = value

    def read_num(self, index: int = 0) -> int or float:
        result = self.read(index, Variable.TYPE_NUM)
        if not (isinstance(result, int) or isinstance(result, float)):
            raise TinyBasicException(f'{self.name}[{self.dim}] IS NOT A NUMBER')
        return result

    def read_str(self, index: int = 0) -> str:
        result = self.read(index, Variable.TYPE_STR)
        if not (isinstance(result, str)):
            raise TinyBasicException(f'{self.name}[{self.dim}] IS NOT A STRING')
        return result

    def write_num(self, value: int or float, index: int = 0):
        if not (isinstance(value, int) or isinstance(value, float)):
            raise TinyBasicException(f'{value} IS NOT A NUMBER')
        self.write(index, value)

    def write_str(self, value: str, index: int = 0):
        if not isinstance(value, str):
            raise TinyBasicException(f'{value} IS NOT A STRING')
        self.write(index, value)

    def write_num_array(self, value: list[int or float]):
        self.dim = len(value)
        self.value = value

    def write_str_array(self, value: list[str]):
        self.dim = len(value)
        self.value = value
