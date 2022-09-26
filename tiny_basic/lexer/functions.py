from enum import unique, Enum


@unique
class TinyBasicFunction(Enum):
    STR = "STR$"
    INT = "INT"
    NUM = "NUM"
    LEN = "LEN"
    ALEN = "ALEN"
    MID = "MID$"
    RND = "RND"
