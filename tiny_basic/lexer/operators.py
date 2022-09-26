from enum import unique, Enum


@unique
class TinyBasicBoolOperator(Enum):
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    XOR = "XOR"
